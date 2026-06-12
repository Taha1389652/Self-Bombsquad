# ba_meta require api 9
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

from typing import TYPE_CHECKING

import babase as ba
import bascenev1 as bs
import bauiv1 as bui
from bauiv1lib import popup

if TYPE_CHECKING:
    pass


class CustomLang:
    lang = ba.app.lang.language
    if lang == 'Spanish':
        title = 'Escala de Juego'
        change = 'Tipo de Escala'
        large = 'Largo'
        medium = 'Mediano'
        small = 'Pequeño'
        channel = 'Canal'
    else:
        title = 'تغییر اندازه رابط کاربری'
        change = 'انتخاب حالت نمایش'
        large = 'دسکتاپ (بزرگ)'
        medium = 'تبلت (متوسط)'
        small = 'موبایل (کوچک)'
        channel = 'کانال'


class ChangeUIPopup(popup.PopupWindow):

    def __init__(self):
        uiscale = ba.app.ui_v1.uiscale
        self._transitioning_out = False
        self._width = 400
        self._height = 280
        bg_color = (0.4, 0.37, 0.49)

        super().__init__(
            position=(0.0, 0.0),
            size=(self._width, self._height),
            scale=2.4 if uiscale is ba.UIScale.SMALL else 1.2,
            bg_color=bg_color)

        self._cancel_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(25, self._height - 40),
            size=(50, 50),
            scale=0.58,
            label='',
            color=bg_color,
            on_activate_call=self._on_cancel_press,
            autoselect=True,
            icon=bui.gettexture('crossOut'),
            iconscale=1.2)
        bui.containerwidget(edit=self.root_widget,
                           cancel_button=self._cancel_button)

        bui.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.5, self._height - 27),
            size=(0, 0),
            h_align='center',
            v_align='center',
            scale=0.8,
            text=CustomLang.title,
            maxwidth=self._width * 0.7,
            color=bui.app.ui_v1.title_color)

        # متن انتخاب حالت نمایش - بالاتر برده شد
        bui.textwidget(
            parent=self.root_widget,
            position=(self._width * 0.265, self._height * 0.35 + 45),
            size=(0, 0),
            h_align='center',
            v_align='center',
            scale=1.0,
            text=CustomLang.change,
            maxwidth=150,
            color=(0.8, 0.8, 0.8, 1.0))

        # منوی انتخاب - بالاتر برده شد
        popup.PopupMenu(
            parent=self.root_widget,
            position=(self._width * 0.5, self._height * 0.25 + 45),
            width=150,
            scale=2.8 if uiscale is ba.UIScale.SMALL else 1.3,
            choices=[0, 1, 2],
            choices_display=[
                ba.Lstr(value=CustomLang.large),
                ba.Lstr(value=CustomLang.medium),
                ba.Lstr(value=CustomLang.small),
            ],
            current_choice=ba.app.config.get('UIScale', self._get_current_scale()),
            on_value_change_call=self._set_uiscale,
        )

        # دکمه کانال - سمت راست
        self._channel_button = bui.buttonwidget(
            parent=self.root_widget,
            position=(self._width - 250, self._height * 0.08),
            size=(120, 35),
            scale=0.8,
            label=f'⚡ {CustomLang.channel}',
            color=(0.2, 0.5, 0.7),
            textcolor=(1, 1, 1),
            on_activate_call=self._open_channel,
            autoselect=True)

    def _get_current_scale(self) -> int:

        current = ba.app.ui_v1.uiscale
        if current is ba.UIScale.LARGE:
            return 0
        elif current is ba.UIScale.MEDIUM:
            return 1
        else:
            return 2

    def _set_uiscale(self, val: int) -> None:
        cfg = ba.app.config
        cfg['UIScale'] = val
        cfg.apply_and_commit()
        
        if val == 0:
            new_scale = ba.UIScale.LARGE
        elif val == 1:
            new_scale = ba.UIScale.MEDIUM
        else:
            new_scale = ba.UIScale.SMALL
        
        ba.app.set_ui_scale(new_scale)
        self._transition_out()

    def _open_channel(self) -> None:

        try:

            ba.open_url("https://t.me/bsrush_mod")
            bui.getsound('swish').play()
            bui.screenmessage("Opening channel...", color=(0, 1, 0))
        except Exception as e:
            try:

                import webbrowser
                webbrowser.open("https://t.me/bsrush_mod")
                bui.getsound('swish').play()
            except:
                bui.screenmessage("Error opening channel!", color=(1, 0, 0))
                bui.getsound('error').play()

    def _on_cancel_press(self) -> None:
        self._transition_out()

    def _transition_out(self) -> None:
        if not self._transitioning_out:
            self._transitioning_out = True
            bui.containerwidget(edit=self.root_widget, transition='out_scale')

    def on_popup_cancel(self) -> None:
        bui.getsound('swish').play()
        self._transition_out()


# ba_meta export babase.Plugin
class BsRush(ba.Plugin):

    def __init__(self) -> None:
        if 'UIScale' not in ba.app.config:
            current = ba.app.ui_v1.uiscale
            if current is ba.UIScale.LARGE:
                scale = 0
            elif current is ba.UIScale.MEDIUM:
                scale = 1
            else:
                scale = 2
            ba.app.config['UIScale'] = scale
            ba.app.config.commit()

    def on_app_running(self) -> None:
        saved_scale = ba.app.config.get('UIScale', self._get_current_scale())
        
        if saved_scale == 0:
            target_scale = ba.UIScale.LARGE
        elif saved_scale == 1:
            target_scale = ba.UIScale.MEDIUM
        else:
            target_scale = ba.UIScale.SMALL
        
        if ba.app.ui_v1.uiscale is not target_scale:
            ba.app.set_ui_scale(target_scale)

    def _get_current_scale(self) -> int:
        current = ba.app.ui_v1.uiscale
        if current is ba.UIScale.LARGE:
            return 0
        elif current is ba.UIScale.MEDIUM:
            return 1
        else:
            return 2

    def has_settings_ui(self) -> bool:
        return True

    def show_settings_ui(self, source_widget: ba.Widget | None) -> None:
        ChangeUIPopup()