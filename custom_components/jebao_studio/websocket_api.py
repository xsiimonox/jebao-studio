"""Read-only catalog. Controls use the normal authenticated HA services."""

import asyncio

import voluptuous as vol

from homeassistant.components import websocket_api
from homeassistant.core import callback
from homeassistant.helpers import device_registry as dr, entity_registry as er

from .const import DOMAIN, CONF_MODE, MODE_LOCAL


@callback
def async_register_websocket(hass):
    websocket_api.async_register_command(hass, async_catalog)
    websocket_api.async_register_command(hass, async_ble_inspect)


@websocket_api.websocket_command({vol.Required("type"): "jebao_studio/catalog"})
@websocket_api.async_response
async def async_catalog(hass, connection, msg):
    if not connection.user.is_admin:
        connection.send_error(msg["id"], "unauthorized", "Administratorrechte erforderlich.")
        return
    registry = er.async_get(hass)
    devices = dr.async_get(hass)
    result = []
    for entry in hass.config_entries.async_entries(DOMAIN):
        if entry.data.get("transport") == "ble_probe":
            result.append({
                "id": entry.entry_id, "name": entry.title, "kind": "bluetooth",
                "transport": "ble_probe", "address": entry.data["address"],
                "entities": [], "available": False,
            })
            continue
        for device in (getattr(entry, "runtime_data", None) or []):
            registered = devices.async_get_device_by_identifier((DOMAIN, device.uid), entry.entry_id)
            entities = [
                {"entity_id": entity.entity_id, "name": entity.name or entity.original_name or entity.entity_id}
                for entity in er.async_entries_for_config_entry(registry, entry.entry_id)
                if registered and entity.device_id == registered.id and not entity.disabled
            ]
            result.append({
                "id": device.uid, "name": (registered.name_by_user or registered.name) if registered else device.name or "Jebao",
                "kind": (device.device_config or {}).get("device_type", "unknown"),
                "transport": entry.data.get(CONF_MODE, MODE_LOCAL),
                "product_key": device.product_key, "available": device.available,
                "entities": entities,
            })
    connection.send_result(msg["id"], result)


@websocket_api.websocket_command({
    vol.Required("type"): "jebao_studio/ble_inspect", vol.Required("entry_id"): str,
})
@websocket_api.async_response
async def async_ble_inspect(hass, connection, msg):
    """Explicitly inspect GATT metadata of a configured device; send no pump commands."""
    if not connection.user.is_admin:
        connection.send_error(msg["id"], "unauthorized", "Administratorrechte erforderlich.")
        return
    entry = hass.config_entries.async_get_entry(msg["entry_id"])
    if not entry or entry.domain != DOMAIN or entry.data.get("transport") != "ble_probe":
        connection.send_error(msg["id"], "invalid_device", "Kein eingerichteter Bluetooth-Diagnosecontroller.")
        return
    state = hass.data.setdefault(DOMAIN, {})
    lock = state.setdefault("ble_lock", asyncio.Lock())
    if lock.locked():
        connection.send_error(msg["id"], "busy", "Eine Bluetooth-Diagnose läuft bereits.")
        return
    try:
        from homeassistant.components import bluetooth
        from bleak import BleakClient

        async with lock, asyncio.timeout(35):
            device = bluetooth.async_ble_device_from_address(hass, entry.data["address"], connectable=True)
            if device is None:
                connection.send_error(msg["id"], "not_found", "Controller nicht erreichbar. App schließen und Bluetooth-Empfang prüfen.")
                return
            # BLEDevice comes from HA's scanner, which also routes active ESPHome proxies.
            async with BleakClient(device, timeout=20) as client:
                services = [{
                    "uuid": service.uuid,
                    "characteristics": [{"uuid": char.uuid, "properties": list(char.properties)} for char in service.characteristics],
                } for service in client.services]
        connection.send_result(msg["id"], {"name": entry.title, "services": services, "control_supported": False})
    except Exception:
        connection.send_error(msg["id"], "inspect_failed", "GATT-Abfrage fehlgeschlagen. App schließen und Bluetooth-Empfang prüfen.")
