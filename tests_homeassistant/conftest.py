"""Real HA core, registries and entity platforms; no network adapters or hardware."""
from pathlib import Path

import pytest_asyncio
from homeassistant import loader
from homeassistant.config_entries import ConfigEntries
from homeassistant.core import HomeAssistant
from homeassistant.helpers import (
    area_registry, device_registry, entity_registry, floor_registry, label_registry,
)


@pytest_asyncio.fixture
async def hass(tmp_path):
    (tmp_path / 'custom_components').symlink_to(
        Path(__file__).resolve().parents[1] / 'custom_components', target_is_directory=True,
    )
    instance = HomeAssistant(str(tmp_path))
    instance.config.skip_pip = True
    loader.async_setup(instance)
    instance.config_entries = ConfigEntries(instance, {})
    await loader.async_get_integration(instance, 'jebao_studio')
    # Transport/panel tests patch their hardware and HTTP boundary; do not start
    # Bluetooth scanning or a webserver just to exercise the native entities.
    instance.config.components.add('jebao_studio')
    device_registry.async_setup(instance)
    for registry in (floor_registry, area_registry, label_registry, device_registry, entity_registry):
        await registry.async_load(instance, load_empty=True)
    try:
        yield instance
    finally:
        await instance.async_stop(force=True)
