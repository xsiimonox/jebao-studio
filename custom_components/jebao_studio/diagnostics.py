"""Credential-free model and connection diagnostics."""

from .const import CONF_MODE, MODE_LOCAL


async def async_get_config_entry_diagnostics(hass, entry):
    return {
        "version": "0.1.0",
        "transport": entry.data.get("transport", entry.data.get(CONF_MODE, MODE_LOCAL)),
        "devices": [{
            "product_key": device.product_key,
            "kind": (device.device_config or {}).get("device_type", "unknown"),
            "available": device.available,
        } for device in (getattr(entry, "runtime_data", None) or [])],
    }
