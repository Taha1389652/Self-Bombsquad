from __future__ import annotations
from typing import TYPE_CHECKING
import babase
import bascenev1 as bs
import bauiv1 as bui
from bauiv1lib.party import PartyWindow as OriginalPartyWindow
from babase import app, Plugin

# تعریف دکمه‌ها با موقعیت و سایز جدید - فاصله متوسط
buttons = [
    {"label": "hug a", "x": -160, "y": 50, "width": 130, "height": 43},
    {"label": "e", "x": -160, "y": 83, "width": 130, "height": 43},
    {"label": "a chat", "x": -160, "y": 116, "width": 130, "height": 43},
    {"label": "sl a", "x": -160, "y": 149, "width": 130, "height": 43},
    {"label": "bm", "x": -160, "y": 182, "width": 130, "height": 43},
    {"label": "f i", "x": -160, "y": 215, "width": 130, "height": 43},
    {"label": "vip$", "x": -160, "y": 248, "width": 130, "height": 43},
    {"label": "k$", "x": -160, "y": 281, "width": 130, "height": 43},
    {"label": "i", "x": -160, "y": 314, "width": 130, "height": 43},
    {"label": "fish$", "x": -250, "y": 50, "width": 130, "height": 43},  # x از -210 به -250 تغییر کرد
    {"label": "spidy$", "x": -250, "y": 83, "width": 130, "height": 43},
    {"label": "cbb$", "x": -250, "y": 116, "width": 130, "height": 43},
    {"label": "g$", "x": -250, "y": 149, "width": 130, "height": 43},
    {"label": "z$", "x": -250, "y": 182, "width": 130, "height": 43},
    {"label": "fr a", "x": -250, "y": 215, "width": 130, "height": 43},
    {"label": "1", "x": -250, "y": 248, "width": 130, "height": 43},
    {"label": "2", "x": -250, "y": 281, "width": 130, "height": 43},
    {"label": "d a", "x": -250, "y": 314, "width": 130, "height": 43},
    {"label": "sol$", "x": -250, "y": 347, "width": 130, "height": 43},
]

class PartyWindow(bui.Window):
    _redefine_methods = ['__init__']
    def __init__(self, *args, **kwargs):
        getattr(self, '__init___old')(*args, **kwargs)
        self.bg_color = (-10,-10,-10)
        
        # ایجاد دکمه‌ها با موقعیت و سایز جدید
        for i, btn in enumerate(buttons):
            if btn["label"] is not None:
                bui.buttonwidget(
                    parent=self._root_widget,
                    scale=0.7,
                    position=(btn["x"], self._height - btn["y"]),
                    size=(btn["width"], btn["height"]),
                    label=btn["label"],
                    autoselect=True,
                    button_type='square',
                    on_activate_call=bui.Call(bs.chatmessage, btn["label"]),
                    color=self.bg_color,
                    iconscale=1.2
                )

def redefine(obj: object, name: str, new: callable, new_name: str = None) -> None:
    if not new_name:
        new_name = name + '_old'
    if hasattr(obj, name):
        setattr(obj, new_name, getattr(obj, name))
    setattr(obj, name, new)

def redefine_class(original_cls: object, cls: object) -> None:
    for method in cls._redefine_methods:
        redefine(original_cls, method, getattr(cls, method))

redefine_class(OriginalPartyWindow, PartyWindow)

# ba_meta require api 9
# ba_meta export babase.Plugin
class Practice(Plugin):
    def on_app_running(self) -> None:
        pass
