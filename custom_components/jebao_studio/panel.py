"""Authenticated Jebao Studio sidebar."""

from pathlib import Path

from homeassistant.components import frontend
from homeassistant.components.http import StaticPathConfig
from homeassistant.components.panel_custom import async_register_panel

from .const import DOMAIN

PANEL_PATH = "jebao-studio"


async def async_register_studio_panel(hass):
    state = hass.data.setdefault(DOMAIN, {})
    if not state.get("static_registered"):
        await hass.http.async_register_static_paths([
            StaticPathConfig("/jebao_studio_panel", str(Path(__file__).parent / "panel"), False)
        ])
        state["static_registered"] = True
    if PANEL_PATH not in hass.data.get(frontend.DATA_PANELS, {}):
        await async_register_panel(
            hass, frontend_url_path=PANEL_PATH,
            webcomponent_name="jebao-studio-panel", sidebar_title="Jebao Studio",
            sidebar_icon="mdi:waves", module_url="/jebao_studio_panel/jebao-studio.js?v=0.1.0",
            require_admin=True, embed_iframe=False,
        )


def async_remove_studio_panel(hass):
    frontend.async_remove_panel(hass, PANEL_PATH)
