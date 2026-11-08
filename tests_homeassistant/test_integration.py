"""Native entity lifecycle, services, config flows and Studio on HA 2026.10.4."""
import inspect
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

import pytest
from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import entity_registry as er

import custom_components.jebao_studio as integration
from custom_components.jebao_studio import hub
from custom_components.jebao_studio.config_flow import ConfigFlow
from custom_components.jebao_studio.diagnostics import async_get_config_entry_diagnostics
from custom_components.jebao_studio.gizwits_lan.device_status import DeviceStatus
from custom_components.jebao_studio.websocket_api import async_catalog, async_ble_inspect

KEY = '54114ccdac1e41c0bb17e222887c07ba'
DOSER = '1aa33c38ba9d4b78a9e7796705b2fad7'


def entry(hass, key=KEY, **data):
    config = ConfigEntry(
        version=2, minor_version=1, domain='jebao_studio', title='Test controller',
        source='user', state=ConfigEntryState.LOADED, options={}, unique_id=None,
        discovery_keys={}, subentries_data=[],
        data={'devices':[{'uid':'test-controller','ip':'192.0.2.1','product_key':key}], **data},
    )
    hass.config_entries._entries[config.entry_id] = config
    return config


async def simulated_connect(device):
    manager = await hub.get_manager(device.hass)
    device.device_config = await hub.get_device_config_for_product_key(device.product_key)
    device.giz_device = await manager.create_device(device.ip, device.product_key)
    device.giz_device._connected = True
    device.giz_device.current_status = DeviceStatus({'SwitchON':True,'Flow':45,'Mode':1})
    device.giz_device.request_status_update = AsyncMock(return_value=True)

    async def write(name, value):
        status = DeviceStatus({**device.giz_device.current_status.data, name:value})
        device.giz_device.current_status = status
        device._handle_status_update(status)
        return b'\x00'
    device.giz_device.set_device_attribute = AsyncMock(side_effect=write)


@pytest.fixture
def transport():
    with (
        patch.object(integration,'async_register_studio_panel',AsyncMock()),
        patch.object(integration,'async_remove_studio_panel',Mock()),
        patch.object(integration,'async_discover_devices',AsyncMock(return_value=[])),
        patch.object(hub.JebaoDevice,'async_connect',simulated_connect),
    ):
        yield


def entity_id(hass, config, suffix):
    return next(e.entity_id for e in er.async_entries_for_config_entry(er.async_get(hass),config.entry_id) if e.unique_id.endswith(suffix))


async def test_native_entity_setup_services_push_and_unload(hass, transport):
    config = entry(hass)
    assert await integration.async_setup_entry(hass, config)
    await hass.async_block_till_done()
    power = entity_id(hass,config,'_SwitchON_switch')
    flow = entity_id(hass,config,'_Flow_number')
    mode = entity_id(hass,config,'_Mode_select')
    feed = entity_id(hass,config,'_FeedSwitch_switch')
    assert hass.states.get(power).state == 'on'
    assert float(hass.states.get(flow).state) == 45
    assert hass.states.get(mode).state == 'sine_wave'
    assert hass.states.get(feed).state == 'unknown'
    await hass.services.async_call('switch','turn_off',{'entity_id':power},blocking=True)
    await hass.services.async_call('number','set_value',{'entity_id':flow,'value':60},blocking=True)
    await hass.services.async_call('select','select_option',{'entity_id':mode,'option':'constant_flow'},blocking=True)
    await hass.async_block_till_done()
    assert hass.states.get(power).state == 'off'
    assert float(hass.states.get(flow).state) == 60
    assert hass.states.get(mode).state == 'constant_flow'
    assert await integration.async_unload_entry(hass, config)
    assert config.runtime_data is None
    assert all(hass.states.get(id_) is None or hass.states.get(id_).state == 'unavailable' for id_ in (power,flow,mode))


async def test_native_services_reject_invalid_values(hass, transport):
    config = entry(hass)
    await integration.async_setup_entry(hass, config)
    await hass.async_block_till_done()
    flow = entity_id(hass,config,'_Flow_number')
    write = config.runtime_data[0].giz_device.set_device_attribute
    for value in (-1,101,45.5):
        with pytest.raises(HomeAssistantError):
            await hass.services.async_call('number','set_value',{'entity_id':flow,'value':value},blocking=True)
    write.assert_not_awaited()
    await integration.async_unload_entry(hass,config)


async def test_catalog_uses_registry_names_and_diagnostics_omit_credentials(hass, transport):
    config = entry(hass,password='secret-password',token='secret-token')
    await integration.async_setup_entry(hass,config)
    await hass.async_block_till_done()
    connection = SimpleNamespace(user=SimpleNamespace(is_admin=True),send_result=Mock())
    await inspect.unwrap(async_catalog)(hass,connection,{'id':1})
    catalog = connection.send_result.call_args.args[1]
    assert catalog[0]['kind'] == 'wavemaker'
    assert any(e['entity_id'].startswith('number.') for e in catalog[0]['entities'])
    diagnostic = await async_get_config_entry_diagnostics(hass,config)
    serialized = json.dumps([catalog,diagnostic])
    assert 'secret-password' not in serialized and 'secret-token' not in serialized
    assert '192.0.2.1' not in json.dumps(diagnostic)
    await integration.async_unload_entry(hass,config)


async def test_doser_creates_no_actuators(hass, transport):
    config = entry(hass,key=DOSER)
    await integration.async_setup_entry(hass,config)
    await hass.async_block_till_done()
    entities = er.async_entries_for_config_entry(er.async_get(hass),config.entry_id)
    assert entities
    assert not any(e.domain in ('switch','number','select','light') for e in entities)
    with pytest.raises(HomeAssistantError,match='Dosierpumpen'):
        await config.runtime_data[0].async_set_attribute('channe1',True)
    await integration.async_unload_entry(hass,config)


async def test_config_flow_menu_and_unreachable_manual_controller(hass):
    flow = ConfigFlow(); flow.hass = hass; flow.context = {'source':'user'}
    result = await flow.async_step_user()
    assert result['menu_options'] == ['local','manual','ble','cloud']
    with patch.object(hub,'async_directed_discovery',AsyncMock(return_value=None)):
        result = await flow.async_step_manual({'ip':'192.0.2.1'})
    assert result['errors'] == {'base':'cannot_connect'}


async def test_ble_setup_and_admin_guard(hass, transport):
    config = entry(hass,transport='ble_probe',address='AA:BB:CC:DD:EE:FF')
    assert await integration.async_setup_entry(hass,config)
    assert config.runtime_data == []
    connection = SimpleNamespace(user=SimpleNamespace(is_admin=False),send_error=Mock())
    await inspect.unwrap(async_ble_inspect)(hass,connection,{'id':2,'entry_id':config.entry_id})
    assert connection.send_error.call_args.args[1] == 'unauthorized'
    assert await integration.async_unload_entry(hass,config)


async def test_actual_panel_registration_is_admin_only_and_idempotent(hass):
    from homeassistant.components import frontend
    from custom_components.jebao_studio.panel import async_register_studio_panel, async_remove_studio_panel
    hass.http = SimpleNamespace(async_register_static_paths=AsyncMock())
    await async_register_studio_panel(hass)
    await async_register_studio_panel(hass)
    panel = hass.data[frontend.DATA_PANELS]['jebao-studio']
    assert panel.require_admin is True
    assert panel.sidebar_title == 'Jebao Studio'
    assert panel.config['_panel_custom']['module_url'].endswith('?v=0.2.4')
    hass.http.async_register_static_paths.assert_awaited_once()
    async_remove_studio_panel(hass)
    assert 'jebao-studio' not in hass.data[frontend.DATA_PANELS]


async def test_brand_icon_and_logo_are_served_by_home_assistant(hass):
    from homeassistant.components.brands import BrandsIntegrationView
    from homeassistant.loader import async_get_custom_components
    integrations = await async_get_custom_components(hass)
    assert integrations['jebao_studio'].has_branding
    view = BrandsIntegrationView(hass)
    for image in ('icon.png', 'logo.png', 'dark_icon.png', 'icon@2x.png'):
        response = await view._serve_from_custom_integration('jebao_studio', image)
        assert response is not None
        assert response.content_type == 'image/png'
        assert response.body.startswith(b'\x89PNG\r\n\x1a\n')
