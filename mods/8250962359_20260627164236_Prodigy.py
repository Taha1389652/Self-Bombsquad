"""
    Plugin: Hold Chat Text in Party Window
    Keeps the typed message when chat closes, then restores it when reopened.
    Compatible with BombSquad 1.7.40+ (Mobile)
"""

import bauiv1 as bui
from bauiv1lib.party import PartyWindow
from typing import Callable, cast

# ba_meta require api 9
# ba_meta export plugin


class Plugin(bui.Plugin):
    _cached_text: str = ""

    @staticmethod
    def _wrap_init(original: Callable) -> Callable:
        def wrapped(self: PartyWindow, *args, **kwargs):
            original(self, *args, **kwargs)
            try:
                bui.textwidget(edit=self._text_field, text=Plugin._cached_text)
            except Exception as e:
                print("Chat Restore Error:", e)
        return wrapped

    @staticmethod
    def _wrap_close(original: Callable) -> Callable:
        def wrapped(self: PartyWindow, *args, **kwargs):
            try:
                Plugin._cached_text = cast(str, bui.textwidget(query=self._text_field)).strip()
            except Exception as e:
                print("Chat Save Error:", e)
            original(self, *args, **kwargs)
        return wrapped

# اعمال تغییرات به کلاس اصلی
PartyWindow.__init__ = Plugin._wrap_init(PartyWindow.__init__)
PartyWindow.close = Plugin._wrap_close(PartyWindow.close)