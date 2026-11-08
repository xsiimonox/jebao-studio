"""Behavioral tests for Studio's routing and authorization without a running HA."""
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, Mock

BASE = Path(__file__).parents[1] / 'custom_components/jebao_studio'


def load_function(file, name, globals_):
    tree = ast.parse((BASE / file).read_text())
    node = next(node for node in tree.body if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)) and node.name == name)
    node.decorator_list = []
    code = ast.Module(body=[ast.ImportFrom(module='__future__', names=[ast.alias(name='annotations')], level=0), node], type_ignores=[])
    ast.fix_missing_locations(code)
    exec(compile(code, str(BASE / file), 'exec'), globals_)
    return globals_[name]


class StudioTests(unittest.IsolatedAsyncioTestCase):
    async def test_ble_entry_registers_panel_without_starting_wifi_driver(self):
        panel, local, cloud = AsyncMock(), AsyncMock(), AsyncMock()
        setup = load_function('__init__.py', 'async_setup_entry', {
            'async_register_studio_panel':panel, '_async_setup_local':local,
            '_async_setup_cloud':cloud, 'CONF_MODE':'mode', 'MODE_LOCAL':'local', 'MODE_CLOUD':'cloud',
        })
        entry = SimpleNamespace(data={'transport':'ble_probe'})
        self.assertTrue(await setup(object(), entry))
        self.assertEqual(entry.runtime_data, [])
        panel.assert_awaited_once(); local.assert_not_awaited(); cloud.assert_not_awaited()

    async def test_websocket_handlers_reject_non_admin_before_accessing_devices(self):
        def require_admin(connection, msg):
            if connection.user.is_admin:
                return True
            connection.send_error(msg['id'], 'unauthorized', 'Administratorrechte erforderlich.')
            return False
        for name in ('async_catalog','async_ble_inspect'):
            handler = load_function(
                'websocket_api.py', name,
                {'_require_admin': require_admin},
            )
            connection = SimpleNamespace(user=SimpleNamespace(is_admin=False), send_error=Mock())
            await handler(None,connection,{'id':42})
            connection.send_error.assert_called_once_with(42,'unauthorized','Administratorrechte erforderlich.')

    async def test_local_discovery_does_not_append_to_cloud_entry(self):
        tree=ast.parse((BASE / 'config_flow.py').read_text())
        cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ConfigFlow')
        method=next(n for n in cls.body if isinstance(n,ast.AsyncFunctionDef) and n.name=='async_step_local')
        method.decorator_list=[]
        module=ast.Module(body=[ast.ImportFrom(module='__future__',names=[ast.alias(name='annotations')],level=0),method],type_ignores=[])
        ast.fix_missing_locations(module)
        cloud_entry=SimpleNamespace(data={'mode':'cloud','devices':[{'uid':'cloud-id'}]})
        entries=SimpleNamespace(async_entries=lambda domain:[cloud_entry],async_update_entry=Mock(),async_reload=AsyncMock())
        owner=SimpleNamespace(hass=SimpleNamespace(config_entries=entries),async_create_entry=Mock(return_value='created'))
        globals_={'hub':SimpleNamespace(async_discover_devices=AsyncMock(return_value=[{'uid':'local-id','product_key':'a'*32,'ip':'192.0.2.1'}])), 'DOMAIN':'jebao_studio','CONF_MODE':'mode','MODE_LOCAL':'local','format_mac':lambda value:value}
        exec(compile(module,'config_flow.py','exec'),globals_)
        self.assertEqual(await globals_['async_step_local'](owner),'created')
        entries.async_update_entry.assert_not_called()
        self.assertEqual(owner.async_create_entry.call_args.kwargs['data']['mode'],'local')

    async def test_local_discovery_reloads_existing_local_entry(self):
        tree=ast.parse((BASE/'config_flow.py').read_text())
        cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ConfigFlow')
        method=next(n for n in cls.body if isinstance(n,ast.AsyncFunctionDef) and n.name=='async_step_local')
        method.decorator_list=[]
        module=ast.Module(body=[ast.ImportFrom(module='__future__',names=[ast.alias(name='annotations')],level=0),method],type_ignores=[]);ast.fix_missing_locations(module)
        original=[{'uid':'old'}]
        entry=SimpleNamespace(data={'mode':'local','devices':original},entry_id='entry')
        entries=SimpleNamespace(async_entries=lambda domain:[entry],async_update_entry=Mock(),async_reload=AsyncMock())
        owner=SimpleNamespace(hass=SimpleNamespace(config_entries=entries),async_abort=Mock(return_value='added'))
        globals_={'hub':SimpleNamespace(async_discover_devices=AsyncMock(return_value=[{'uid':'new','ip':'192.0.2.2'}])), 'DOMAIN':'jebao_studio','CONF_MODE':'mode','MODE_LOCAL':'local','format_mac':lambda value:value}
        exec(compile(module,'config_flow.py','exec'),globals_)
        self.assertEqual(await globals_['async_step_local'](owner),'added')
        entries.async_reload.assert_awaited_once_with('entry')
        self.assertEqual(original,[{'uid':'old'}])
        self.assertEqual(len(entries.async_update_entry.call_args.kwargs['data']['devices']),2)

    async def test_doser_adapters_refuse_writes_before_transport_access(self):
        import sys
        from unittest.mock import patch
        class HomeAssistantError(Exception):
            pass
        errors = SimpleNamespace(HomeAssistantError=HomeAssistantError)
        for file, classname in (("hub.py", "JebaoDevice"), ("cloud.py", "JebaoCloudDevice")):
            tree = ast.parse((BASE / file).read_text())
            cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == classname)
            method = next(n for n in cls.body if isinstance(n, ast.AsyncFunctionDef) and n.name == "async_set_attribute")
            module = ast.Module(body=[ast.ImportFrom(module="__future__", names=[ast.alias(name="annotations")], level=0), method], type_ignores=[])
            ast.fix_missing_locations(module)
            globals_ = {}
            exec(compile(module, file, "exec"), globals_)
            device = SimpleNamespace(device_config={"device_type":"doser"})
            with patch.dict(sys.modules, {"homeassistant.exceptions": errors}):
                with self.assertRaisesRegex(HomeAssistantError, "Dosierpumpen"):
                    await globals_["async_set_attribute"](device, "channe1", True)
