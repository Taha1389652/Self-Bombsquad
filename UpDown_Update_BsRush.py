from bauiv1lib import party
from babase import (
    SpecialChar as sc,
    charstr as cs,
    Plugin,
    Call
)
from bauiv1 import (
    containerwidget as cw,
    buttonwidget as bw,
    textwidget as tw,
    getsound as gs,
    scrollwidget as sw,
    get_special_widget as gsw,
    UIScale
)
from bascenev1 import (
    get_chat_messages as gcm,
    screenmessage as push
)
from babase import clipboard_set_text, clipboard_is_supported
import webbrowser
import re


class VeryPW(party.PartyWindow):
    def __init__(s, *args, **kwargs):
        super().__init__(*args, **kwargs)
        s._n = 0
        s._o = ""
        s._f = True
        s._selected_widgets = {}  
        s._current_selected_message = None

        for i in range(2):
            bw(
                parent=s._root_widget,
                size=(30, 30),
                label=cs(getattr(sc, f"{['UP', 'DOWN'][i]}_ARROW")),
                button_type='square',
                enable_sound=False,
                position=(-15, 70-(i*40)),
                on_activate_call=[s._p, s._d][i]
            )

    def _c(s, t=""): 
        tw(edit=s._text_field, text=t)
    
    def _d(s): 
        s._p(1)

    def _extract_telegram_id(s, message):

        patterns = [
            r'@(\w+)',  # @username
            r't\.me/(\w+)',  # t.me/username
            r'telegram\.me/(\w+)',  # telegram.me/username
            r'https?://t\.me/(\w+)',  # http://t.me/username
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, message)
            if matches:
                return matches[0]
        return None

    def _search_telegram(s, username):

        try:
            if username:
                url = f"https://t.me/{username}"

                from _babase import open_url
                open_url(url)
                push(f"🔍 باز کردن {username} در مرورگر", color=(0, 1, 1))
                gs('dingSmallHigh').play()
            else:
                push("❌ آیدی تلگرام یافت نشد", color=(1, 0, 0))
        except Exception as e:
            push(f"❌ خطا در باز کردن مرورگر: {str(e)}", color=(1, 0, 0))

    def _copy_msg(s, message):
        """کپی پیام به کلیپ‌بورد"""
        try:
            if clipboard_is_supported():
                clipboard_set_text(message)
                push("✅ متن کپی شد!", color=(0, 1, 0))
                gs('dingSmall').play()
            else:
                push("❌ کلیپ‌بورد پشتیبانی نمی‌شود", color=(1, 0, 0))
        except Exception as e:
            push(f"❌ خطا در کپی: {str(e)}", color=(1, 0, 0))

    def _show_context_menu(s, message):

        if hasattr(s, '_context_menu') and s._context_menu and s._context_menu.exists():
            s._close_context_menu()

        telegram_id = s._extract_telegram_id(message)
        has_telegram = telegram_id is not None

        menu_height = 220
        menu_width = 350

        s._context_menu = cw(
            parent=gsw('overlay_stack'),
            size=(menu_width, menu_height),
            color=(0.05, 0.05, 0.05, 0.98),  
            on_outside_click_call=lambda: s._close_context_menu(),
            transition='in_scale',  
            scale=1.2,
            background=True
        )

        screen_center = s._root_widget.get_screen_space_center()
        if screen_center:
            menu_x = screen_center[0] - menu_width / 2
            menu_y = screen_center[1] - menu_height / 2
        else:
            menu_x = 80
            menu_y = 200

        cw(edit=s._context_menu, position=(menu_x, menu_y))

        tw(
            parent=s._context_menu,
            text=u"\ue010 عملیات پیام",
            position=(155 , 200),
            scale=1.0,
            color=(0, 1, 1),  
            h_align='center'
        )

        tw(
            parent=s._context_menu,
            text="─" * 20,
            position=(150 , 170),
            scale=0.7,
            color=(0.6, 0.6, 0.6),
            h_align='center'
        )

        display_message = message[:50] + "..." if len(message) > 50 else message
        tw(
            parent=s._context_menu,
            text=f"📝: {display_message}",
            position=(150 , 160),
            scale=0.6,
            color=(0.8, 0.9, 1),
            h_align='center',
            maxwidth=menu_width - 20
        )
        
        y_position = menu_height - 110

        copy_btn = bw(
            parent=s._context_menu,
            label=u"\ue022 کپی متن کامل",
            size=(menu_width - 40, 40),
            position=(20, y_position),
            on_activate_call=lambda: [s._copy_msg(message), s._close_context_menu()],
            color=(0.3, 0.6, 0.8),
            textcolor=(1, 1, 1),
            text_scale=0.8,
            button_type='square'
        )
        y_position -= 50

        if has_telegram:
            telegram_btn = bw(
                parent=s._context_menu,
                label=u"\ue025 جستجوی " + telegram_id,
                size=(menu_width - 40, 40),
                position=(20, y_position),
                on_activate_call=lambda: [s._search_telegram(telegram_id), s._close_context_menu()],
                color=(0.2, 0.7, 0.4),
                textcolor=(1, 1, 1),
                text_scale=0.7,
                button_type='square'
            )
            y_position -= 50

        close_btn = bw(
            parent=s._context_menu,
            label=u"\ue023 بستن منو",
            size=(menu_width - 40, 40),
            position=(20, y_position),
            on_activate_call=s._close_context_menu,
            color=(0.7, 0.2, 0.2),
            textcolor=(1, 1, 1),
            text_scale=0.8,
            button_type='square'
        )

        gs('swish').play()

    def _close_context_menu(s):

        if hasattr(s, '_context_menu') and s._context_menu and s._context_menu.exists():
            cw(edit=s._context_menu, transition='out_scale')

            from babase import apptimer
            apptimer(0.3, lambda: s._context_menu.delete() if hasattr(s, '_context_menu') and s._context_menu and s._context_menu.exists() else None)
            gs('swish').play()

    def _handle_container_click(s, message, txt_widget):

        for w in s._selected_widgets.values():
            if w.exists():
                tw(edit=w, color=(1, 1, 1))
        
        tw(edit=txt_widget, color=(0, 0.8, 0))
        s._selected_widgets[message] = txt_widget
        s._current_selected_message = message

        s._show_context_menu(message)

    def _highlight_selected_message(s, message, txt_widget):

        for w in s._selected_widgets.values():
            if w.exists():
                tw(edit=w, color=(1, 1, 1))

        tw(edit=txt_widget, color=(0, 0.8, 0))
        s._selected_widgets[message] = txt_widget
        s._current_selected_message = message

    def _p(s, i=0):
        s._w1 = gcm()
        if s._f:
            s._o = tw(query=s._text_field)
            s._f = False
            s._n = 0 if i else len(s._w1)
        
        s._n = (s._n + (1 if i else -1)) % len(s._w1)
        
        try:
            current_message = (s._w1+[s._o])[s._n]
            if ": " in current_message:
                message_text = current_message.split(": ", 1)[1]
            else:
                message_text = current_message
            s._c(message_text)
        except IndexError:
            if not s._w1:
                push("❌ چت خالی است", color=(1, 0.5, 0))
                gs('block').play()
                s._n = 0
                return
            s._n = -1
            s._c(s._o)
        
        gs('deek').play()

        [z.delete() for z in s._columnwidget.get_children()]
        s._selected_widgets.clear()

        for z in range(len(s._w1)):

            message_container = cw(
                parent=s._columnwidget,
                size=(700, 30),
                background=True,
                color=(0.1, 0.1, 0.1, 0.8),  
                selectable=True,
                click_activate=True
            )

            txt = tw(
                parent=message_container,
                text=s._w1[z],
                h_align='left',
                v_align='center',
                size=(900, 13),
                scale=0.55,
                color=(1, 1, 1) if z != s._n else (0, 1, 0),
                position=(-1, 8),
                selectable=True,
                autoselect=True,
                click_activate=True,
                maxwidth=900,
                shadow=0.5,
                flatness=1.0
            )

            invisible_click_area = cw(
                parent=message_container,
                size=(920, 45),
                background=False,  
                selectable=True,
                click_activate=True
            )

            click_handler = Call(s._handle_container_click, s._w1[z], txt)

            tw(edit=txt, on_activate_call=click_handler)
            cw(edit=message_container, on_activate_call=click_handler)
            cw(edit=invisible_click_area, on_activate_call=click_handler)

            if z == s._n:
                s._highlight_selected_message(s._w1[z], txt)
            
            cw(edit=s._columnwidget, visible_child=message_container)

    def __del__(s):

        s._close_context_menu()


# ba_meta require api 9
# ba_meta export babase.Plugin


class byBordd(Plugin):
    def __init__(s):
        party.PartyWindow = VeryPW
