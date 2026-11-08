"""Read-only catalog. Controls use the normal authenticated HA services."""

import asyncio
import re

import voluptuous as vol

from homeassistant.components import websocket_api
from homeassistant.core import callback
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers.storage import Store

from .const import DOMAIN, CONF_MODE, MODE_LOCAL

GROUPS_STORE_KEY = f"{DOMAIN}.groups"
GROUPS_STORE_VERSION = 1


def _require_admin(connection, msg) -> bool:
    """Reject non-admin panel commands before reading any integration state."""
    if connection.user.is_admin:
        return True
    connection.send_error(msg["id"], "unauthorized", "Administratorrechte erforderlich.")
    return False


async def async_setup_groups(hass) -> None:
    """Load persisted Studio groups once, separate from config entries."""
    state = hass.data.setdefault(DOMAIN, {})
    if "groups_store" in state:
        return
    store = Store(hass, GROUPS_STORE_VERSION, GROUPS_STORE_KEY)
    saved = await store.async_load() or {}
    state["groups_store"] = store
    state["groups"] = saved.get("groups", []) if isinstance(saved.get("groups", []), list) else []


async def _async_save_groups(hass, groups: list[dict]) -> None:
    state = hass.data[DOMAIN]
    state["groups"] = groups
    await state["groups_store"].async_save({"groups": groups})


@callback
def async_register_websocket(hass):
    websocket_api.async_register_command(hass, async_catalog)
    websocket_api.async_register_command(hass, async_ble_inspect)
    websocket_api.async_register_command(hass, async_groups)
    websocket_api.async_register_command(hass, async_save_group)
    websocket_api.async_register_command(hass, async_delete_group)


@websocket_api.websocket_command({vol.Required("type"): "jebao_studio/catalog"})
@websocket_api.async_response
async def async_catalog(hass, connection, msg):
    if not _require_admin(connection, msg):
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
        runtime_devices = getattr(entry, "runtime_data", None) or []
        runtime_uids = {device.uid for device in runtime_devices}
        for saved in entry.data.get("devices", []):
            if not saved.get("uid") or saved["uid"] in runtime_uids:
                continue
            registered = devices.async_get_device_by_identifier((DOMAIN, saved["uid"]), entry.entry_id)
            result.append({
                "id": saved["uid"],
                "name": ((registered.name_by_user or registered.name) if registered else None)
                    or saved.get("name") or "Gespeicherte Jebao-Pumpe",
                "kind": "unknown", "transport": entry.data.get(CONF_MODE, MODE_LOCAL),
                "product_key": saved.get("product_key", ""), "available": False,
                "entities": [], "configured_only": True,
            })
        for device in runtime_devices:
            registered = devices.async_get_device_by_identifier((DOMAIN, device.uid), entry.entry_id)
            entities = [
                {"entity_id": entity.entity_id, "name": entity.name or entity.original_name or entity.entity_id,
                 "attribute": entity.unique_id.removeprefix(f"{device.uid}_").rsplit("_", 1)[0]}
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
    if not _require_admin(connection, msg):
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


@websocket_api.websocket_command({vol.Required("type"): "jebao_studio/groups"})
@websocket_api.async_response
async def async_groups(hass, connection, msg):
    if not _require_admin(connection, msg):
        return
    connection.send_result(msg["id"], hass.data.get(DOMAIN, {}).get("groups", []))


@websocket_api.websocket_command({
    vol.Required("type"): "jebao_studio/group_save",
    vol.Optional("id"): str,
    vol.Required("name"): str,
    vol.Required("device_ids"): [str],
})
@websocket_api.async_response
async def async_save_group(hass, connection, msg):
    """Persist a named selection of eligible flow pumps."""
    if not _require_admin(connection, msg):
        return
    name = " ".join(msg["name"].split())
    device_ids = list(dict.fromkeys(msg["device_ids"]))
    if not 1 <= len(name) <= 48 or not device_ids:
        connection.send_error(msg["id"], "invalid_group", "Name und mindestens eine Pumpe sind erforderlich.")
        return
    available = {
        device.uid
        for entry in hass.config_entries.async_entries(DOMAIN)
        if entry.data.get("transport") != "ble_probe"
        for device in (getattr(entry, "runtime_data", None) or [])
        if (device.device_config or {}).get("device_type") != "doser"
    }
    if not set(device_ids).issubset(available):
        connection.send_error(msg["id"], "invalid_group", "Eine ausgewählte Pumpe ist nicht verfügbar.")
        return
    group_id = msg.get("id") or re.sub(r"[^a-z0-9_-]", "", name.casefold().replace(" ", "-"))[:48] or "gruppe"
    if msg.get("id") and not any(group.get("id") == group_id for group in hass.data[DOMAIN].get("groups", [])):
        connection.send_error(msg["id"], "invalid_group", "Die bearbeitete Gruppe existiert nicht mehr.")
        return
    groups = [group for group in hass.data[DOMAIN].get("groups", []) if not msg.get("id") or group.get("id") != group_id]
    base, suffix = group_id, 2
    used_ids = {group.get("id") for group in groups}
    while group_id in used_ids:
        group_id = f"{base}-{suffix}"
        suffix += 1
    group = {"id": group_id, "name": name, "device_ids": device_ids}
    groups.append(group)
    await _async_save_groups(hass, groups)
    connection.send_result(msg["id"], group)


@websocket_api.websocket_command({
    vol.Required("type"): "jebao_studio/group_delete", vol.Required("id"): str,
})
@websocket_api.async_response
async def async_delete_group(hass, connection, msg):
    if not _require_admin(connection, msg):
        return
    groups = [group for group in hass.data[DOMAIN].get("groups", []) if group.get("id") != msg["id"]]
    await _async_save_groups(hass, groups)
    connection.send_result(msg["id"], {"id": msg["id"]})
