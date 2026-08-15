# Ballistica Safe Mod
# Safe UI mod for color and emoji selection.
# No cheating, autoclicking, or attack automation.

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

import babase
import bauiv1 as bui


MOD_NAME = "Safe Color & Emoji"
CONFIG_KEY = "safe_color_emoji_mod"


@dataclass
class ModConfig:
    player_color: tuple[float, float, float] = (0.2, 0.6, 1.0)
    emoji: str = "🙂"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ModConfig":
        color = data.get("player_color", (0.2, 0.6, 1.0))
        emoji = data.get("emoji", "🙂")
        if not isinstance(color, (list, tuple)) or len(color) != 3:
            color = (0.2, 0.6, 1.0)
        try:
            color = tuple(float(x) for x in color)
        except Exception:
            color = (0.2, 0.6, 1.0)
        if not isinstance(emoji, str) or not emoji:
            emoji = "🙂"
        return cls(player_color=color, emoji=emoji)

    def to_dict(self) -> dict[str, Any]:
        return {
            "player_color": list(self.player_color),
            "emoji": self.emoji,
        }


class SafeColorEmojiPlugin(babase.Plugin):
    def __init__(self) -> None:
        super().__init__()
        self._config = self._load_config()
        self._window: Optional[SafeColorEmojiWindow] = None

    def on_app_running(self) -> None:
        self._register_menu_button()

    def _register_menu_button(self) -> None:
        try:
            app = bui.app
            classic = getattr(app, "classic", None)
            if classic is not None and hasattr(classic, "main_menu_window"):
                pass
        except Exception:
            pass

    def show_window(self) -> None:
        if self._window is None:
            self._window = SafeColorEmojiWindow(plugin=self)
        else:
            self._window.refresh_from_config()
        self._window.on_activate()

    def get_config(self) -> ModConfig:
        return self._config

    def set_color(self, color: tuple[float, float, float]) -> None:
        self._config.player_color = color
        self._save_config()

    def set_emoji(self, emoji: str) -> None:
        self._config.emoji = emoji
        self._save_config()

    def _load_config(self) -> ModConfig:
        try:
            raw = babase.app.config.get(CONFIG_KEY, {})
            if isinstance(raw, dict):
                return ModConfig.from_dict(raw)
        except Exception:
            pass
        return ModConfig()

    def _save_config(self) -> None:
        try:
            babase.app.config[CONFIG_KEY] = self._config.to_dict()
            babase.app.config.commit()
        except Exception:
            pass


class SafeColorEmojiWindow(bui.MainWindow):
    def __init__(self, plugin: SafeColorEmojiPlugin):
        self._plugin = plugin
        self._width = 560.0
        self._height = 420.0
        self._bg_color = (0.12, 0.12, 0.14)
        self._title_color = (0.95, 0.95, 0.98)
        self._emoji_choices = ["🙂", "😎", "🔥", "✨", "❤️", "👑", "🎯", "⚡"]
        self._color_choices = [
            (0.2, 0.6, 1.0),
            (1.0, 0.35, 0.35),
            (0.35, 1.0, 0.5),
            (1.0, 0.8, 0.2),
            (0.8, 0.45, 1.0),
            (1.0, 1.0, 1.0),
        ]
        self._root_widget = bui.containerwidget(
            size=(self._width, self._height),
            transition="in_scale",
            scale=1.0,
            stack_offset=(0.0, 0.0),
            color=self._bg_color,
        )
        super().__init__(root_widget=self._root_widget)
        self._build_ui()
        self.refresh_from_config()

    def _build_ui(self) -> None:
        bui.textwidget(
            parent=self._root_widget,
            position=(32, self._height - 52),
            size=(self._width - 64, 40),
            text=MOD_NAME,
            color=self._title_color,
            scale=1.35,
            h_align="center",
            v_align="center",
        )

        bui.textwidget(
            parent=self._root_widget,
            position=(32, self._height - 88),
            size=(self._width - 64, 28),
            text="Choose a safe cosmetic color and emoji preset.",
            color=(0.75, 0.78, 0.82),
            scale=0.8,
            h_align="center",
            v_align="center",
        )

        bui.textwidget(
            parent=self._root_widget,
            position=(40, 286),
            size=(180, 24),
            text="Color Presets",
            color=(0.9, 0.9, 0.95),
            scale=0.95,
            h_align="left",
            v_align="center",
        )

        x0, y0 = 40, 232
        bw, bh = 76, 50
        pad = 10
        for i, color in enumerate(self._color_choices):
            x = x0 + (i % 3) * (bw + pad)
            y = y0 - (i // 3) * (bh + pad)
            bui.buttonwidget(
                parent=self._root_widget,
                position=(x, y),
                size=(bw, bh),
                label="",
                button_type="square",
                color=color,
                on_activate_call=babase.Call(self._set_color, color),
            )

        bui.textwidget(
            parent=self._root_widget,
            position=(300, 286),
            size=(220, 24),
            text="Emoji Presets",
            color=(0.9, 0.9, 0.95),
            scale=0.95,
            h_align="left",
            v_align="center",
        )

        ex, ey = 300, 232
        ew, eh = 80, 50
        for i, emoji in enumerate(self._emoji_choices):
            x = ex + (i % 3) * (ew + pad)
            y = ey - (i // 3) * (eh + pad)
            bui.buttonwidget(
                parent=self._root_widget,
                position=(x, y),
                size=(ew, eh),
                label=emoji,
                button_type="square",
                text_scale=1.2,
                on_activate_call=babase.Call(self._set_emoji, emoji),
            )

        bui.textwidget(
            parent=self._root_widget,
            position=(40, 90),
            size=(480, 24),
            text="Current selection",
            color=(0.9, 0.9, 0.95),
            scale=0.9,
            h_align="left",
            v_align="center",
        )

        self._preview = bui.textwidget(
            parent=self._root_widget,
            position=(40, 48),
            size=(480, 34),
            text="",
            color=(1, 1, 1),
            scale=1.05,
            h_align="left",
            v_align="center",
        )

        bui.buttonwidget(
            parent=self._root_widget,
            position=(self._width - 132, 18),
            size=(92, 42),
            label="Done",
            on_activate_call=self._root_widget.delete,
        )

    def refresh_from_config(self) -> None:
        cfg = self._plugin.get_config()
        bui.textwidget(
            edit=self._preview,
            text=f"Color: {tuple(round(v, 2) for v in cfg.player_color)}   Emoji: {cfg.emoji}",
        )

    def _set_color(self, color: tuple[float, float, float]) -> None:
        self._plugin.set_color(color)
        self.refresh_from_config()

    def _set_emoji(self, emoji: str) -> None:
        self._plugin.set_emoji(emoji)
        self.refresh_from_config()

    def on_activate(self) -> None:
        bui.containerwidget(edit=self._root_widget, transition="in_scale")


def get_safe_color_emoji_plugin() -> SafeColorEmojiPlugin:
    global _PLUGIN_INSTANCE
    try:
        return _PLUGIN_INSTANCE
    except NameError:
        _PLUGIN_INSTANCE = SafeColorEmojiPlugin()
        return _PLUGIN_INSTANCE


_PLUGIN_INSTANCE = SafeColorEmojiPlugin()
