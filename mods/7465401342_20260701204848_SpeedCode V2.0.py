# ba_meta require api 9
# لطفا دست نزن
# این نسخه تستی است
import babase
import random
import bascenev1 as bs
import bauiv1 as bui
from bauiv1lib import party
import re
import json
import os
from babase import (
    clipboard_is_supported as CIS,
    clipboard_get_text as CGT,
    clipboard_has_text as CHT,
    Plugin
)
from bascenev1 import (
    disconnect_from_host as BYE,
    connect_to_party as CON,
    protocol_version as PT,
    get_game_roster as GGR
)
from typing import Any
from bauiv1 import (
    get_special_widget as gsw,
    containerwidget as cw,
    screenmessage as push,
    checkboxwidget as chk,
    scrollwidget as sw,
    buttonwidget as bw,
    SpecialChar as sc,
    textwidget as tw,
    checkboxwidget as cb,
    gettexture as gt,
    apptimer as teck,
    getsound as gs,
    UIScale as uis,
    charstr as cs,
    app as APP,
    Call
)
from bascenev1 import (
    get_chat_messages as GCM,
    chatmessage as CM
)
from _babase import get_string_width as strw
import _babase

# تنظیمات تبلیغات
ADVERTISEMENT_MESSAGE = u"این مود کاملا رایگان است نفروشید @BsRush⚡"
ADVERTISEMENT_INTERVAL = 60  # هر ۱ دقیقه یک‌بار (۶۰ ثانیه)

def send_ad_message():
    try:
        _babase.chatmessage(ADVERTISEMENT_MESSAGE)
    except Exception:
        try:
            bs.chatmessage(ADVERTISEMENT_MESSAGE)
        except Exception:
            pass
    # تمدید تایمر تبلیغات
    _babase.timer(ADVERTISEMENT_INTERVAL, send_ad_message, timetype=_babase.TimeType.REAL)

# این بخش وقتی بازی بالا می‌آید خودکار اجرا می‌شود
def on_app_loading():
    _babase.timer(10, send_ad_message, timetype=_babase.TimeType.REAL)

pr = 'autoresponder_'

def get_file(button_index=None):
    if button_index is not None:
        config_path = os.path.join(os.path.dirname(__file__), f'custom_commands_button_{button_index}.json')
    else:
        config_path = os.path.join(os.path.dirname(__file__), 'custom_commands.json')
    return config_path

def load(button_index=None):
    try:
        commands_file = get_file(button_index)
        if os.path.exists(commands_file):
            with open(commands_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            default_texts = [
                "hug a", "e", "a chat", "sl a", "bm", "f i", "vip$", "k$", "i",
                "fish$", "spidy$", "cbb$", "g$", "z$", "fr a", "1", "2", "d a", "sol$",
                "Player 1", "Player 2", "Player 3", "Player 4", "Player 5", 
                "Player 6", "Player 7", "Player 8"
            ]
            if button_index is not None and button_index < len(default_texts):
                default_commands = [default_texts[button_index]]
                save(default_commands, button_index)
                return default_commands
            else:
                return [buttons[button_index]["label"]]
    except Exception:
        return [buttons[button_index]["label"]] if button_index is not None else [""]

def save(commands_data, button_index=None):
    try:
        commands_file = get_file(button_index)
        with open(commands_file, 'w', encoding='utf-8') as f:
            json.dump(commands_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

kj = []
player_buttons = []  # لیست برای ذخیره دکمه‌های پخش کننده

def update_players():
    global kj
    df = []
    kj = []
    try:
        gh = GGR()
        for i in gh:
            if 'players' in i and 'client_id' in i:
                df.append((i['players'], i['client_id']))
        
        for u in range(len(df)):
            try:
                if df[u][0]:
                    kj.append((df[u][0][0]['name'], df[u][1]))
            except:
                pass
    except Exception:
        pass
    
    while len(kj) < 8:
        kj.append(('None', ' '))

def update_player_buttons():
    """بروزرسانی دکمه‌های پخش کننده"""
    global player_buttons, kj
    update_players()
    
    for i, btn_data in enumerate(player_buttons):
        if i < len(kj):
            player_name = kj[i][0]
            player_id = kj[i][1]
            
            if len(player_name) > 8:
                display_name = player_name[:8] + '...'
            else:
                display_name = player_name
                
            try:
                bui.buttonwidget(edit=btn_data['button'], label=display_name)
                if player_id != ' ':
                    bui.buttonwidget(edit=btn_data['button'], color=(0, 1, 0))
                else:
                    bui.buttonwidget(edit=btn_data['button'], color=(1, 0, 0))
            except Exception:
                pass

def send_commands(client_id, button_index=None, player_idx=None):
    # اگر دکمه بازیکن است، آی‌دی لحظه‌ای را از لیست kj استخراج کن
    if player_idx is not None:
        global kj
        if player_idx < len(kj):
            client_id = kj[player_idx][1]

    if client_id == " " or client_id is None:
        player_commands = load(button_index)
        if player_commands and len(player_commands) == 1 and '*' in player_commands[0]:
            commands = [cmd.strip() for cmd in player_commands[0].split('*') if cmd.strip()]
            for cmd in commands:
                bs.chatmessage(cmd)
        else:
            for cmd in player_commands:
                bs.chatmessage(cmd)
    else:
        player_commands = load(button_index)
        if player_commands and len(player_commands) == 1 and '*' in player_commands[0]:
            commands = [cmd.strip() for cmd in player_commands[0].split('*') if cmd.strip()]
            for cmd in commands:
                bs.chatmessage(f'%{cmd} {client_id}')
        else:
            for cmd in player_commands:
                bs.chatmessage(f'%{cmd} {client_id}')

class ButtonWindow:
    def __init__(self, button_index, button_label="Button", button_type="chat"):
        self.window = None
        self.input_field = None
        self.button_index = button_index
        self.button_label = button_label
        self.button_type = button_type
    
    def show(self):
        if self.window:
            try:
                self.window.delete()
            except:
                pass
        
        button_commands = load(self.button_index)
        
        self.window = cw(
            size=(400, 300),
            parent=bui.get_special_widget('overlay_stack'),
            position=(200, 200),
            background=True,
            on_outside_click_call=self.close
        )
        
        title_text = f"Button {self.button_index + 1}"
        if self.button_type == "player":
            title_text += " - Player Button"
        else:
            title_text += " - Chat Button"
            
        tw(
            parent=self.window,
            text=title_text,
            position=(200, 260),
            scale=1.0,
            color=(1, 1, 1),
            h_align='center'
        )
        
        self.input_field = tw(
            parent=self.window,
            text=button_commands[0] if button_commands else '',
            editable=True,
            position=(50, 180),
            size=(300, 40),
            scale=0.8,
            color=(1, 1, 1),
            h_align='left',
            v_align='center',
            max_chars=200
        )
        
        def save_commands():
            if self.input_field:
                new_text = str(tw(query=self.input_field)).strip()
                if new_text:
                    new_commands = [new_text]
                    if save(new_commands, self.button_index):
                        bui.screenmessage("Commands saved", color=(0, 1, 0))
                        self.close()
                    else:
                        bui.screenmessage("Error", color=(1, 0, 0))
                else:
                    bui.screenmessage("Enter commands", color=(1, 0, 0))
     
        tw(
            parent=self.window,
            position=(180, 220),
            size=(300, 30), 
            h_align='center',
            v_align='center',
            text="Menu «E» code",
            scale=1.0
        )
              
        bw(
            parent=self.window,
            position=(60, 110),
            size=(120, 40),
            label="Save",
            on_activate_call=save_commands
        )
        
        bw(
            parent=self.window,
            position=(220, 110),
            size=(120, 40),
            label="Cancel",
            on_activate_call=self.close
        )
        
        def reset_default():
            default_texts = [
                "hug a", "e", "a chat", "sl a", "bm", "f i", "vip$", "k$", "i",
                "fish$", "spidy$", "cbb$", "g$", "z$", "fr a", "1", "2", "d a", "sol$",
                "Player 1", "Player 2", "Player 3", "Player 4", "Player 5", 
                "Player 6", "Player 7", "Player 8"
            ]
            if self.button_index < len(default_texts):
                default_commands = [default_texts[self.button_index]]
            else:
                default_commands = [buttons[self.button_index]["label"]]
                
            if save(default_commands, self.button_index):
                bui.screenmessage("It was reset", color=(0, 1, 0))
                self.close()
            else:
                bui.screenmessage("Error", color=(1, 0, 0))
        
        bw(
            parent=self.window,
            position=(140, 60),
            size=(150, 40),
            label="Reset code",
            on_activate_call=reset_default
        )
    
    def close(self):
        if self.window:
            self.window.delete()
            self.window = None
            self.input_field = None

buttons = [
    # دکمه‌های چت (19 دکمه)
    {"label": "hug a", "x": -190, "y": 50, "width": 130, "height": 43, "type": "chat"},
    {"label": "e", "x": -190, "y": 83, "width": 130, "height": 43, "type": "chat"},
    {"label": "a chat", "x": -190, "y": 116, "width": 130, "height": 43, "type": "chat"},
    {"label": "sl a", "x": -190, "y": 149, "width": 130, "height": 43, "type": "chat"},
    {"label": "bm", "x": -190, "y": 182, "width": 130, "height": 43, "type": "chat"},
    {"label": "f i", "x": -190, "y": 215, "width": 130, "height": 43, "type": "chat"},
    {"label": "vip$", "x": -190, "y": 248, "width": 130, "height": 43, "type": "chat"},
    {"label": "k$", "x": -190, "y": 281, "width": 130, "height": 43, "type": "chat"},
    {"label": "i", "x": -190, "y": 314, "width": 130, "height": 43, "type": "chat"},
    {"label": "fish$", "x": -300, "y": 50, "width": 130, "height": 43, "type": "chat"},
    {"label": "spidy$", "x": -300, "y": 83, "width": 130, "height": 43, "type": "chat"},
    {"label": "cbb$", "x": -300, "y": 116, "width": 130, "height": 43, "type": "chat"},
    {"label": "g$", "x": -300, "y": 149, "width": 130, "height": 43, "type": "chat"},
    {"label": "z$", "x": -300, "y": 182, "width": 130, "height": 43, "type": "chat"},
    {"label": "fr a", "x": -300, "y": 215, "width": 130, "height": 43, "type": "chat"},
    {"label": "1", "x": -300, "y": 248, "width": 130, "height": 43, "type": "chat"},
    {"label": "2", "x": -300, "y": 281, "width": 130, "height": 43, "type": "chat"},
    {"label": "d a", "x": -300, "y": 314, "width": 130, "height": 43, "type": "chat"},
    {"label": "sol$", "x": -300, "y": 347, "width": 130, "height": 43, "type": "chat"},
    
    # دکمه‌های پخش کننده (8 دکمه)
    {"label": "Player 1", "x": -90, "y": 10, "width": 100, "height": 43, "type": "player"},
    {"label": "Player 2", "x": -10, "y": 10, "width": 100, "height": 43, "type": "player"},
    {"label": "Player 3", "x": 70, "y": 10, "width": 100, "height": 43, "type": "player"},
    {"label": "Player 4", "x": 150, "y": 10, "width": 100, "height": 43, "type": "player"},
    {"label": "Player 5", "x": 230, "y": 10, "width": 100, "height": 43, "type": "player"},
    {"label": "Player 6", "x": 310, "y": 10, "width": 100, "height": 43, "type": "player"},
    {"label": "Player 7", "x": 390, "y": 10, "width": 100, "height": 43, "type": "player"},
    {"label": "Player 8", "x": 470, "y": 10, "width": 100, "height": 43, "type": "player"},
]

# ba_meta export babase.Plugin
class speed(babase.Plugin):
    def __init__(self):
        super().__init__()
        self.update_timer = None
        o = party.PartyWindow.__init__
        
        def custom_party_init(s_party, *a, **k):
            global player_buttons, kj
            
            rr = o(s_party, *a, **k)
            update_players()
            player_buttons = [] 
            
            for i, btn in enumerate(buttons):
                button_window = ButtonWindow(i, btn["label"], btn["type"])
                
                if btn["type"] == "player":
                    player_index = i - 19  
                    if player_index < len(kj):
                        player_name = kj[player_index][0]
                        player_id = kj[player_index][1]
                        display_name = player_name[:8] + '...' if len(player_name) > 8 else player_name
                    else:
                        display_name = "None"
                        player_id = " "

                    player_button = bw(
                        parent=s_party._root_widget,
                        position=(btn["x"], s_party._height - btn["y"]),
                        size=(btn["width"], btn["height"]),
                        on_activate_call=Call(send_commands, player_id, i, player_index),
                        label=display_name,
                        color=(0.6, 0.8, 1) if player_id != ' ' else (0.5, 0.5, 0.5),
                        autoselect=True,
                        button_type='square',
                        scale=0.7,
                        iconscale=1.2
                    )

                    player_buttons.append({
                        'button': player_button,
                        'index': player_index,
                        'original_index': i
                    })
                    
                else:
                    button_commands = load(i)
                    display_text = button_commands[0] if button_commands else btn["label"]
                    if len(display_text) > 12:
                        display_text = display_text[:12] + '...'
                    
                    bw(
                        parent=s_party._root_widget,
                        position=(btn["x"], s_party._height - btn["y"]),
                        size=(btn["width"], btn["height"]),
                        label=display_text,
                        autoselect=True,
                        button_type='square',
                        on_activate_call=Call(send_commands, " ", i),  
                        color=(0.2, 0.2, 0.2),
                        scale=0.7,
                        iconscale=1.2
                    )

                bw(
                    parent=s_party._root_widget,
                    position=(btn["x"] + btn["width"] - 40, s_party._height - btn["y"] + 20),
                    size=(20, 20),
                    label="E",
                    on_activate_call=button_window.show,
                    color=(0, 0, 0),
                    text_scale=0.5,
                    textcolor=(1, 0, 0)
                )

            self.start_update_timer()
            return rr
        
        party.PartyWindow.__init__ = custom_party_init
    
    def start_update_timer(self):
        def update_cycle():
            if player_buttons: 
                try:
                    update_player_buttons()
                except Exception:
                    pass

        # ایجاد تایمر تکرارشونده بومی بمب اسکواد
        self.update_timer = bui.AppTimer(1.0, update_cycle, repeat=True)
    
    def on_app_running(self):
        bui.screenmessage("Speedcode loaded \nTelegram : @BsRush \nEditor : @BsNokia", color=(1, 1, 0))
        # اجرای بهینه‌تر بارگذاری تبلیغات اولیه
        _babase.timer(10, send_ad_message, timetype=_babase.TimeType.REAL)