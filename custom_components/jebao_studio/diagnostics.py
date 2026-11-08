"""Credential-free model and connection diagnostics."""

from .const import CONF_MODE, MODE_LOCAL


def schedule_snapshot(device):
    """Export cached schedule bytes without identifiers, network I/O or writes."""
    fields = [f"AutoTime{index:02d}" for index in range(48)]
    fields += ["TimerON", "Mode", "Flow", "Frequency", "AutoMode", "AutoFlow", "AutoFreq"]
    result = {}
    for name in fields:
        value = device.get_attribute(name)
        if isinstance(value, (bytes, bytearray)):
            result[name] = {"hex": bytes(value).hex(), "length": len(value)}
        elif value is None or isinstance(value, (bool, int, float, str)):
            result[name] = value
    return {"source": "cached_controller_status", "fields": result}


async def async_get_config_entry_diagnostics(hass, entry):
    return {
        "version": "0.4.3",
        "transport": entry.data.get("transport", entry.data.get(CONF_MODE, MODE_LOCAL)),
        "devices": [{
            "product_key": device.product_key,
            "kind": (device.device_config or {}).get("device_type", "unknown"),
            "available": device.available,
            "schedule": schedule_snapshot(device),
        } for device in (getattr(entry, "runtime_data", None) or [])],
    }
