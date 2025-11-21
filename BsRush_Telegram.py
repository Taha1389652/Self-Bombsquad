import babase
import bauiv1 as bui
from bauiv1lib import ingamemenu

_original_refresh = ingamemenu.InGameMenuWindow._refresh_in_game

def _new_refresh(self, *args, **kwargs):
    h, v, scale = _original_refresh(self, *args, **kwargs)
    
    button_h = -150  
    button_v = v + 80  

    btn_width = self._button_width * 0.8
    btn_height = self._button_height * 1.2  

    bui.textwidget(
        parent=self._root_widget,
        position=(button_h + 65, button_v + 90),
        size=(0, 0),
        scale=scale * 0.7,
        color=(0.9, 0.9, 0.1, 1),
        text="TELEGRAM CHANNELS",
        h_align='center',
        maxwidth=180,
        shadow=0.5
    )
    
    # Button 1: BsRush_Mod - Top
    def _open_telegram1():
        bui.open_url('https://t.me/BsRush_Mod')
        bui.getsound('gunCocking').play()
        self._resume()
    
    bui.buttonwidget(
        parent=self._root_widget,
        position=(button_h, button_v),
        size=(btn_width, btn_height),
        scale=scale * 0.8,
        label="BsRush Mod",
        on_activate_call=_open_telegram1,
        color=(0.1, 0.3, 0.8),
        textcolor=(1, 1, 1),
        text_scale=1.0
    )
    
    # Button 2: SinglMod - Middle
    def _open_telegram2():
        bui.open_url('https://t.me/SinglMod')
        bui.getsound('gunCocking').play()
        self._resume()
    
    bui.buttonwidget(
        parent=self._root_widget,
        position=(button_h, button_v - 70),
        size=(btn_width, btn_height),
        scale=scale * 0.8,
        label="Singl Mod",
        on_activate_call=_open_telegram2,
        color=(0.1, 0.6, 0.2),
        textcolor=(1, 1, 1),
        text_scale=1.0
    )
    
    # Button 3: BombSquad_PFBS - Bottom
    def _open_telegram3():
        bui.open_url('https://t.me/BombSquad_PFBS')
        bui.getsound('gunCocking').play()
        self._resume()
    
    bui.buttonwidget(
        parent=self._root_widget,
        position=(button_h, button_v - 140),
        size=(btn_width, btn_height),
        scale=scale * 0.8,
        label="PFBS Mod",
        on_activate_call=_open_telegram3,
        color=(0.7, 0.1, 0.1),
        textcolor=(1, 1, 1),
        text_scale=1.0
    )
    
    return h, v, scale

# Replace the method
ingamemenu.InGameMenuWindow._refresh_in_game = _new_refresh

# ba_meta require api 9
# ba_meta export plugin
class ByTaha(babase.Plugin):
    pass
