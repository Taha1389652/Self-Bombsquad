import babase
import bauiv1 as bui
import bascenev1 as bs
from typing import cast
import json
import os
import re

PATH = os.path.dirname(os.path.abspath(__file__)) + '/SD.BsRush'
file_path = os.path.abspath(__file__)
file_name = os.path.basename(file_path)

persian_maps_to_english = {
    'ی': 'y',
    'ک': 'k', 
    'گ': 'g',
    'چ': 'ch',
    'پ': 'p',
    'ژ': 'zh',
    'ش': 'sh',
    'ض': 'z',
    'ص': 's',
    'ث': 's',
    'ق': 'gh',
    'ف': 'f',
    'غ': 'gh',
    'ع': 'a',
    'ه': 'h',
    'خ': 'kh',
    'ح': 'h',
    'ج': 'j',
    'ت': 't',
    'ب': 'b',
    'ل': 'l',
    'ا': 'a',
    'س': 's',
    'د': 'd',
    'ر': 'r',
    'ز': 'z',
    'ط': 't',
    'ظ': 'z',
    'ن': 'n',
    'م': 'm',
    'و': 'v',
    'ء': '',
    ' ': ' '
}

reserved_words = {
    'سلام': 'hello',
    'خداحافظ': 'goodbye', 
    'ممنون': 'thanks',
    'بله': 'yes',
    'نه': 'no',
    'چطوری': 'how are you',
    'خوبم': 'I am fine',
    'تو چطوری': 'how about you',
    'بازی': 'game',
    'تیم': 'team',
    'دشمن': 'enemy',
    'کمک': 'help',
    'بیا': 'come',
    'برو': 'go',
    'بدو': 'run',
    'توقف': 'stop',
    'آتش': 'fire',
    'نارنجک': 'grenade',
    'پزشک': 'medic',
    'مهمات': 'ammo'
}

def convert_text(text):
    original = text
    result = text
    no_space = text.replace(' ', '')
    
    for persian, english in reserved_words.items():
        if persian in no_space:
            result = result.replace(persian, english)
    
    for persian, english in persian_maps_to_english.items():
        result = result.replace(persian, english)
    
    return result

trans_to_english = True
val = 0
DATA = {}
POWERS_ARE_SAVED = False
LAST_MESSAGE_TIME = 1

from bauiv1lib.party import PartyWindow

old_init = PartyWindow.__init__

def handle_chat_msg(message):
    copy0 = message
    copy1 = copy0.split()
    
    try:
        if len(copy1) > 1 and copy1[1] == 'set' and 0 < len(copy1[1:]) <= 10:
            data_file = os.path.dirname(os.path.abspath(__file__)) + '/voc.BsRush'
            config_file = os.path.dirname(os.path.abspath(__file__)) + '/SD.BsRush'
            
            with open(data_file, "r") as f:
                data = json.load(f)
                
            with open(config_file, "r") as f:
                config = json.load(f)
            
            for key in data.keys():
                if copy1[0] == config['PO'][key]['name']:
                    data[key]['powers'] = [int(x) for x in copy1[1:]]
                    with open(data_file, 'w') as f:
                        f.write(json.dumps(data))
            
            bs.chatmessage(copy0)
            
        elif len(copy1) == 1 and copy1[0] in ['on', 'off']:
            data_file = os.path.dirname(os.path.abspath(__file__)) + '/voc.BsRush'
            config_file = os.path.dirname(os.path.abspath(__file__)) + '/SD.BsRush'
            
            with open(data_file, "r") as f:
                data = json.load(f)
                
            with open(config_file, "r") as f:
                config = json.load(f)
            
            for key in data.keys():
                if copy1[0] == config['PO'][key]['name']:
                    data[key]['active'] = True if copy1[0] == 'on' else False
                    with open(data_file, 'w') as f:
                        f.write(json.dumps(data))
            
            bs.chatmessage(copy0)
        else:
            bs.chatmessage(copy0)
            
    except IndexError:
        pass

UPDATED = False

def party_main(self, *args, **kwargs):
    global UPDATED
    
    old_init(self, *args, **kwargs)
    
    self.my_account_name = account_name = babase.app.plus.get_v1_account_display_string()
    self.wonder_popup = WonderPopup()
    self.last_chat_message = ""
    self.my_name = account_name
    
    try:
        roster = bs.get_game_roster()
        if roster and len(roster) > 1:
            for player in roster:
                if 'spec' in player and player['spec']:
                    self.server_name = player.get('display_string', 'Unknown Server')
                    break
            else:
                self.server_name = roster[1].get('display_string', 'Unknown Server')
    except:
        self.server_name = "Local Server"
    
    window_width = self._width
    window_height = self._height
    
    button_width = 180
    button_height = 40
    button_x = (window_width - button_width) / 2
    button_y = 60
    
    bui.buttonwidget(
        parent=self._root_widget,
        size=(button_width, button_height),
        position=(button_x, button_y),
        label="BsRush Mod",
        on_activate_call=lambda: bui.open_url("https://t.me/bsrush_mod"),
        color=(0.34, 0.52, 0.04),
        textcolor=(1, 1, 1),
        autoselect=True,
        scale=0.8
    )
    
    checkbox_x = window_width * 0.3 - 20
    checkbox_y = 10
    
    bui.checkboxwidget(
        parent=self._root_widget,
        scale=0.9,
        text_scale=0.9,
        value=val,
        position=(checkbox_x, checkbox_y),
        size=(40, 40),
        on_value_change_call=toggle_translation,
        autoselect=True,
        color=(0.34, 0.52, 0.04),
        text="BsRush Translate"
    )

PartyWindow.__init__ = party_main

def send_powers():
    global LAST_MESSAGE_TIME
    
    separator = '|'
    header = '#!#'
    data_file = os.path.dirname(os.path.abspath(__file__)) + '/voc.BsRush'
    
    data = None
    with open(data_file, "r") as f:
        data = json.load(f)
    
    message = header
    
    for key in data.keys():
        if data[key]['registered']:
            continue
        
        if data[key]['powers']:
            powers_str = ''.join(str(p) for p in data[key]['powers'])
            message += f"{DATA['PO'][key]['name']}{powers_str}|"
            LAST_MESSAGE_TIME += 1
        
        status = 'on' if data[key]['active'] else 'off'
        message += f"{DATA['PO'][key]['name']}:{status}|"
        LAST_MESSAGE_TIME += 1
        data[key]['registered'] = True
    
    if message == header and len(message) == 3:
        return
    
    if len(message) > 88:
        temp = ""
        parts = message.split(separator)
        
        for part in parts:
            temp += part + separator
            if len(temp) > 84:
                index = parts.index(part)
                temp = temp.replace(parts[index], '').replace('||', '')
                bs.chatmessage(temp)
                temp = header + parts[index] + separator
            
            if len(parts) - 1 == parts.index(part):
                bs.chatmessage(temp)
    else:
        bs.chatmessage(message)
    
    if data is not None:
        with open(data_file, 'w') as f:
            f.write(json.dumps(data))

def save_powers(power_list):
    global POWERS_ARE_SAVED
    
    data_file = os.path.dirname(os.path.abspath(__file__)) + '/voc.BsRush'
    data = {}
    
    try:
        with open(data_file, "r") as f:
            data = json.load(f)
        
        for key in list(data.keys()):
            if key in power_list:
                power_list.remove(key)
            else:
                del data[key]
        
        for power in power_list:
            data[power] = {
                'powers': [],
                'active': True,
                'registered': True
            }
        
        with open(data_file, 'w') as f:
            f.write(json.dumps(data))
            
    except:
        for power in power_list:
            data[power] = {
                'powers': [],
                'active': True,
                'registered': True
            }
        
        with open(data_file, 'w') as f:
            f.write(json.dumps(data))
    
    POWERS_ARE_SAVED = True

def update_numeric_and_powers_data(text_data):
    if POWERS_ARE_SAVED:
        return
    
    try:
        end_index = text_data.index(']')
    except Exception:
        pass
    
    data_part = text_data[end_index:]
    parts = data_part.split('\t111a')
    del parts[1]
    
    power_list = []
    keys = tuple(DATA['PO'].keys())
    
    for part in parts:
        power_list.append(keys[part.count('\t111b') - 1])
    
    save_powers(power_list)

old_send_chat_message = PartyWindow._send_chat_message

def new_send_chat_message(self):
    self.last_chat_message = cast(str, bui.textwidget(query=self._text_field))
    old_send_chat_message(self)

PartyWindow._send_chat_message = new_send_chat_message

def toggle_translation(value):
    global trans_to_english, val
    
    if value == 0:
        val = 0
        trans_to_english = True
    elif value == 1:
        val = 1
        trans_to_english = False

messages = []

def new_add_msg(self, msg):
    global trans_to_english
    
    message = msg
    messages.append(message)
    
    all_messages = ""
    for m in messages:
        all_messages += m + '\n'
    
    with open('messages.txt', 'w') as f:
        f.write(all_messages)
    
    if trans_to_english:
        if not message.isascii():
            message = convert_text(message)
    
    height = 40
    left_margin = 10
    spacing = 8
    text_height = 35
    
    uniform_color = (0.12, 0.45, 0.12)
    
    text_x = self._scroll_width * 0.5
    button_x = self._scroll_width * 0.45
    h_align = 'right'
    
    is_own_message = False
    is_server_message = False
    
    try:
        if hasattr(self, 'server_name') and self.server_name and message.find(self.server_name) != -1:
            is_server_message = True
        
        elif (hasattr(self, 'my_name') and self.my_name and message.find(self.my_name) != -1) or \
             (hasattr(self, 'my_account_name') and self.my_account_name and message.find(self.my_account_name) != -1):
            is_own_message = True
    except:
        pass
    
    container = bui.containerwidget(
        size=(self._scroll_width, height),
        color=(0, 0, 0),
        background=False,
        parent=self._columnwidget
    )
    
    button = bui.buttonwidget(
        parent=container,
        size=(self._scroll_width * 0.97, text_height),
        position=(button_x, -text_height / 2 + height / 2 - 8),
        text_scale=0.34,
        color=uniform_color,
        textcolor=(1, 1, 1),
        label='',
        autoselect=True
    )
    
    def open_popup(msg_text, btn_widget):
        self.wonder_popup.open(msg_text, btn_widget, self._text_field)
    
    bui.buttonwidget(
        edit=button, 
        on_activate_call=bui.CallPartial(open_popup, message, button)
    )
    
    text_widget = bui.textwidget(
        parent=container,
        text=message,
        h_align=h_align,
        v_align='center',
        size=(self._scroll_width * 0.8, text_height),
        scale=0.42,
        position=(text_x, -text_height / 1.5 + height / 2),
        maxwidth=self._scroll_width * 0.6,
        shadow=0.3,
        flatness=0.1,
        color=(1, 1, 1)
    )
    
    self._chat_texts.append(container)
    
    if len(self._chat_texts) > 30:
        old_widget = self._chat_texts.pop(0)
        old_widget.delete()
    
    bui.containerwidget(edit=self._columnwidget, visible_child=text_widget)

PartyWindow._add_msg = new_add_msg

class WonderPopup:
    
    def __init__(self):
        self.tel = None
        self._text_field = None
        self.msg = None
        self.links = None
        self._popup_type = None
    
    def open(self, text_box, pos1, set_text):
        message = text_box
        
        self._text_field = set_text
        self.msg = message
        
        url_pattern = r'https?://[^\s]+|www\.[^\s]+'
        self.links = re.findall(url_pattern, self.msg)
        
        self.tel = message.find('@')
        
        choices = ['Copy', 'Reply']
        choice_displays = [
            bui.Lstr(value='Copy'),
            bui.Lstr(value='Reply')
        ]
        
        if self.tel != -1:
            telegram_text = message[self.tel:].split()[0] if ' ' in message[self.tel:] else message[self.tel:]
            if len(telegram_text) > 1:
                choices.append('Telegram')
                choice_displays.append(bui.Lstr(value='Open Telegram ID'))
        
        if self.links:
            choices.append('Links')
            choice_displays.append(bui.Lstr(value='Open Links'))
        
        if not message.isascii():
            choices.append('Translate')
            choice_displays.append(bui.Lstr(value='Translate'))
        
        ui_scale = bui.app.ui_v1.uiscale
        
        from bauiv1lib.popup import PopupMenuWindow
        
        PopupMenuWindow(
            position=pos1.get_screen_space_center(),
            scale=1.2 if ui_scale is babase.UIScale.SMALL else 0.54 if ui_scale is babase.UIScale.MEDIUM else 0.12,
            choices=choices,
            choices_display=choice_displays,
            current_choice='Copy',
            delegate=self
        )
    
    def popup_menu_selected_choice(self, popup_window, choice):
        if choice == 'Copy':
            babase.clipboard_set_text(self.msg)
        
        elif choice == 'Telegram':
            telegram_id = self.msg[self.tel + 1:].split()[0]
            bui.open_url(f'https://t.me/{telegram_id}')
        
        elif choice == 'Links':
            for link in self.links:
                if link.startswith('www.'):
                    link = 'https://' + link
                elif not link.startswith(('http://', 'https://')):
                    link = 'https://' + link
                
                link = link.rstrip('.,!?;:')
                
                try:
                    bui.open_url(link)
                except Exception as e:
                    print(f"Error opening URL {link}: {e}")
        
        elif choice == 'Translate':
            translated = convert_text(self.msg)
            bui.textwidget(edit=self._text_field, text=translated)
        
        elif choice == 'Reply':
            colon_pos = self.msg.find(': ') + 1
            if colon_pos > 0:
                reply_text = self.msg[colon_pos:] + ' | ' if len(self.msg[colon_pos:]) < 10 else self.msg[colon_pos:colon_pos + 10] + '... | '
            else:
                reply_text = self.msg + ' | '
            bui.textwidget(edit=self._text_field, text=reply_text)
        
        else:
            print(f"Unhandled popup type: {choice}")
    
    def popup_menu_closing(self, popup_window):
        pass

# ba_meta require api 9
# ba_meta export babase.Plugin

class BsRushPlugin(babase.Plugin):
    pass
