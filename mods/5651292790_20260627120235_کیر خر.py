#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Decoded By @Techhossein
"""

import baplus
import bauimodel as ar
from bauiparty import popup
from bauiparty.party import PartyWindow
from typing import cast
import json
import babase
import bau
import os
import base64
import re

# File paths
PATH = os.path.dirname(os.path.abspath(__file__)) + '/SD.WonderBomb'
file_path = os.path.abspath(__file__)
file_name = os.path.basename(file_path)

# Persian/Arabic character mappings to English
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

# Reserved words mapping
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
    """Convert Persian/Arabic text to English."""
    original = text
    result = text
    no_space = text.replace(' ', '')
    
    # Apply reserved words first
    for persian, english in reserved_words.items():
        if persian in no_space:
            result = result.replace(persian, english)
    
    # Apply character mappings
    for persian, english in persian_maps_to_english.items():
        result = result.replace(persian, english)
    
    return result

# Global variables
trans_to_english = True
val = 0
DATA = {}
POWERS_ARE_SAVED = False
LAST_MESSAGE_TIME = 1

# Store original methods
old_init = PartyWindow.__init__
send_chat1 = ar.chatmessage

def handle_chat_msg(message):
    """Handle incoming chat messages."""
    copy0 = message
    copy1 = copy0.split()
    
    try:
        # Handle 'set' command for powers
        if len(copy1) > 1 and copy1[1] == 'set' and 0 < len(copy1[1:]) <= 10:
            data_file = os.path.dirname(os.path.abspath(__file__)) + '/voc.WonderBomb'
            config_file = os.path.dirname(os.path.abspath(__file__)) + '/SD.WonderBomb'
            
            with open(data_file, "r") as f:
                data = json.load(f)
                
            with open(config_file, "r") as f:
                config = json.load(f)
            
            for key in data.keys():
                if copy1[0] == config['PO'][key]['name']:
                    data[key]['powers'] = [int(x) for x in copy1[1:]]
                    with open(data_file, 'w') as f:
                        f.write(json.dumps(data))
            
            send_chat1(copy0)
            
        # Handle 'on'/'off' commands
        elif len(copy1) == 1 and copy1[0] in ['on', 'off']:
            data_file = os.path.dirname(os.path.abspath(__file__)) + '/voc.WonderBomb'
            config_file = os.path.dirname(os.path.abspath(__file__)) + '/SD.WonderBomb'
            
            with open(data_file, "r") as f:
                data = json.load(f)
                
            with open(config_file, "r") as f:
                config = json.load(f)
            
            for key in data.keys():
                if copy1[0] == config['PO'][key]['name']:
                    data[key]['active'] = True if copy1[0] == 'on' else False
                    with open(data_file, 'w') as f:
                        f.write(json.dumps(data))
            
            send_chat1(copy0)
        else:
            send_chat1(copy0)
            
    except IndexError:
        pass

UPDATED = False

def party_main(name_obj, origin=(1, 1)):
    """Main party initialization function."""
    global UPDATED
    
    # Decode some base64 strings (these were obfuscated in original)
    player_key = "player_id"
    roster_key = "roster"
    
    try:
        roster = ar.get_game_roster()
        
        # Get account info
        name_obj.my_account_name = account_name = baplus.PlusAppSubsystem.get_v1_account_display_string(True)
        
        for player in roster:
            connection = ar.get_connection_to_host_info()
            
            if connection is not None:
                connection_str = str(connection)
                
                # Check for specific connection type
                if "PBCLIFE" in connection_str.split("=")[0]:
                    try:
                        send_powers()
                    except FileNotFoundError:
                        update_numeric_and_powers_data(player['data'][1]['info'])
                    
                    if player[player_key] == account_name:
                        if UPDATED:
                            pass
                        else:
                            name_part = player['data'][1]['info'][:8].rstrip()
                            name_obj.my_name = name_part.split('[')[1]
                            UPDATED = True
                        
                        update_numeric_and_powers_data(player['data'][1]['info'])
                        ar.chatmessage = handle_chat_msg
        
        name_obj.server_name = roster[1][player_key]
        name_obj.wonder_popup = WonderPopup()
        name_obj.last_chat_message = None
        
        old_init(name_obj, origin)
        
    except IndexError:
        connection = ar.get_connection_to_host_info()
        if connection is not None:
            pass
        
        name_obj.wonder_popup = WonderPopup()
        old_init(name_obj, origin)
    
    # Add UI checkbox
    ui_scale = bau.app.ui_v1.uiscale
    bau.checkboxwidget(
        parent=name_obj._root_widget,
        scale=1.5,
        text_scale=0.1,
        value=val,
        position=(name_obj._width / 4, 10 if ui_scale == babase.UIScale.SMALL else 1),
        size=(40, 40),
        on_value_change_call=toggle_translation,
        autoselect=True,
        color=(0.34, 0.52, 0.04),
        text="WonderBomb Translation"
    )

# Replace the original init
PartyWindow.__init__ = party_main

def send_powers():
    """Send powers data to chat."""
    global LAST_MESSAGE_TIME
    
    separator = '|'
    header = '#!#'
    data_file = os.path.dirname(os.path.abspath(__file__)) + '/voc.WonderBomb'
    
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
    
    # Split long messages
    if len(message) > 88:
        temp = ""
        parts = message.split(separator)
        
        for part in parts:
            temp += part + separator
            if len(temp) > 84:
                index = parts.index(part)
                temp = temp.replace(parts[index], '').replace('||', '')
                ar.chatmessage(temp)
                temp = header + parts[index] + separator
            
            if len(parts) - 1 == parts.index(part):
                ar.chatmessage(temp)
    else:
        ar.chatmessage(message)
    
    # Save data
    if data is not None:
        with open(data_file, 'w') as f:
            f.write(json.dumps(data))

def save_powers(power_list):
    """Save powers to file."""
    global POWERS_ARE_SAVED
    
    data_file = os.path.dirname(os.path.abspath(__file__)) + '/voc.WonderBomb'
    data = {}
    
    try:
        with open(data_file, "r") as f:
            data = json.load(f)
        
        # Remove old entries
        for key in list(data.keys()):
            if key in power_list:
                power_list.remove(key)
            else:
                del data[key]
        
        # Add new entries
        for power in power_list:
            data[power] = {
                'powers': [],
                'active': True,
                'registered': True
            }
        
        with open(data_file, 'w') as f:
            f.write(json.dumps(data))
            
    except:
        # Create new file if doesn't exist
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
    """Update numeric and powers data from text."""
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

# Store original send chat message method
old_send_chat_message = PartyWindow._send_chat_message

def new_send_chat_message(chat_obj):
    """New send chat message handler."""
    chat_obj.last_chat_message = cast(str, bau.textwidget(query=chat_obj._text_field))
    old_send_chat_message(chat_obj)

PartyWindow._send_chat_message = new_send_chat_message

def toggle_translation(value):
    """Toggle translation on/off."""
    global trans_to_english, val
    
    if value == 0:
        val = 0
        trans_to_english = True
    elif value == 1:
        val = 1
        trans_to_english = False

messages = []

def new_add_msg(choice, msg):
    """Add new message with translation support."""
    global trans_to_english
    
    message = msg
    choice_obj = choice
    messages.append(message)
    
    # Save messages to file
    all_messages = ""
    for m in messages:
        all_messages += m + '\n'
    
    with open('messages.txt', 'w') as f:
        f.write(all_messages)
    
    # Apply translation if enabled
    if trans_to_english:
        if not message.isascii():
            message = convert_text(message)
    
    # UI positioning variables
    height = 15
    left_margin = 7
    spacing = 4
    line_height = 4
    text_height = 40
    color = (0.12, 0.12, 0.45)
    is_own_message = False
    
    try:
        # Check if message is from server or self
        if message.find(choice_obj.server_name) == 1:
            color = (0.5, 0.5, 0.12)
        
        if (message.find(choice_obj.my_name) == 1 or 
            message.find(choice_obj.my_account_name) == 1 or 
            message.find(choice_obj.my_account_name[:]) == 1):
            is_own_message = True
        
        if is_own_message:
            color = (0.12, 0.45, 0.12)
            
    except:
        color = (0.1, 0.1, 0.1)
    
    # Create message container
    container = bau.containerwidget(
        size=(choice_obj._scroll_width, height),
        color=(0.3, 0.44, 0.1),
        background=False,
        parent=choice_obj._columnwidget
    )
    
    # Create message button
    button = bau.buttonwidget(
        parent=container,
        size=(choice_obj._scroll_width * 0.8 + 7 * 1 + 4 * 1, 40 + 4 * 1),
        position=(
            -7 + (7 + 280 * 0.04 if not is_own_message else -7) + 4,
            -40 / 1 + 15 / 1 - 4
        ),
        text_scale=0.34,
        color=color,
        textcolor=(0, 0, 0.0),
        label='',
        autoselect=True
    )
    
    def open_popup(version, response):
        choice_obj.wonder_popup.open(version, response, choice_obj._text_field)
    
    bau.buttonwidget(edit=button, on_activate_call=bau.Call(open_popup, message, button))
    
    # Create message text
    text_widget = bau.textwidget(
        parent=container,
        text=message,
        h_align='left',
        v_align='center',
        size=(1, text_height),
        scale=0.44,
        position=(
            (left_margin + 260 * 0.04 if not is_own_message else -left_margin) + spacing,
            -text_height / 1 + height / 1.2
        ),
        maxwidth=choice_obj._scroll_width * 0.8,
        shadow=0.2,
        flatness=0.1
    )
    
    choice_obj._chat_texts.append(container)
    
    # Remove old messages if too many
    if len(choice_obj._chat_texts) > 30:
        old_widget = choice_obj._chat_texts.pop(0)
        old_widget.delete()
    
    bau.containerwidget(edit=choice_obj._columnwidget, visible_child=text_widget)

PartyWindow._add_msg = new_add_msg

class WonderPopup:
    """Custom popup for message interactions."""
    
    def __init__(self):
        self.tel = None
        self._text_field = None
        self.msg = None
        self.links = None
        self._popup_type = None
    
    def open(self, text_box, pos1, set_text):
        """Open popup with message options."""
        message = text_box
        
        self._text_field = set_text
        self.msg = message
        
        # Find URLs in message
        url_pattern = r'(?:https?://)?(?:www\.)?(?:[a-zA-Z0-9][-a-zA-Z0-9%_\+~#=]+\.)+[a-zA-Z][a-zA-Z0-9]{1,5}(?:#(?:[a-zA-Z][a-zA-Z0-9]+=[a-zA-Z0-9]*,)*(?:[a-zA-Z][a-zA-Z0-9]+=[a-zA-Z0-9]*))?'
        self.links = re.findall(url_pattern, self.msg)
        
        # Check for @ symbol
        self.tel = message.find('@')
        
        # Get current activity
        activity = ar.getactivity(False)
        
        # Setup popup options
        choices = ['Copy', 'Reply']
        choice_displays = [
            ar.Lstr(value='Copy'),
            ar.Lstr(value='Reply')
        ]
        
        # Add telegram option if @ found
        if self.tel != -1:
            choices.append('Telegram')
            choice_displays.append(ar.Lstr(value='Open Telegram ID'))
        
        # Add link option if URLs found
        if self.links:
            choices.append('Links')
            choice_displays.append(ar.Lstr(value='Open Links'))
        
        # Add translate option if non-ASCII
        if not message.isascii():
            choices.append('Translate')
            choice_displays.append(ar.Lstr(value='Translate'))
        
        ui_scale = bau.app.ui_v1.uiscale
        
        popup.PopupMenuWindow(
            position=pos1.get_screen_space_center(),
            scale=1.2 if ui_scale is babase.UIScale.SMALL else 0.54 if ui_scale is babase.UIScale.MEDIUM else 0.12,
            choices=choices,
            choices_display=choice_displays,
            current_choice='Copy',
            delegate=self
        )
    
    def popup_menu_selected_choice(self, popup_window, choice):
        """Handle popup menu selection."""
        if choice == 'Copy':
            babase.clipboard_set_text(self.msg)
        
        elif choice == 'Telegram':
            telegram_id = self.msg[self.tel + 1:].split()[0]
            bau.open_url(f'https://t.me/{telegram_id}')
        
        elif choice == 'Links':
            for link in self.links:
                if not link.startswith('http'):
                    link = 'https://' + link
                bau.open_url(link)
        
        elif choice == 'Translate':
            translated = convert_text(self.msg)
            bau.textwidget(edit=self._text_field, text=translated)
        
        elif choice == 'Reply':
            colon_pos = self.msg.find(': ') + 1
            reply_text = self.msg[colon_pos:] + ' | ' if len(self.msg[colon_pos:]) < 10 else self.msg[colon_pos:colon_pos + 10] + '... | '
            bau.textwidget(edit=self._text_field, text=reply_text)
        
        else:
            print(f"Unhandled popup type: {choice}")
    
    def popup_menu_closing(self, popup_window):
        """Handle popup closing."""
        pass

# Plugin metadata
class ByMorteza(babase.Plugin):
    """WonderBomb plugin by Morteza."""
    pass

# ba_meta require api 8
# ba_meta export plugin