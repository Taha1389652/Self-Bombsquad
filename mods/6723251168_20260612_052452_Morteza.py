# ba_meta require api 9
# ba_meta export babase.Plugin

"""
پلاگین پیشرفته چت و مدیریت بازی برای BombSquad
ارتقا یافته به جدیدترین نسخه API 9
"""

from __future__ import annotations

from typing import Sequence, Optional, cast, Any
from decimal import Decimal as deci
import logging
import babase
import baenv
import bascenev1 as bs
import bauiv1 as bui
from bauiv1lib import party, ingamemenu
from bauiv1lib.party import PartyWindow
from bauiv1lib.popup import PopupMenuWindow

# ========== متغیرهای سراسری ==========

# متغیرهای وضعیت
current_username: Optional[str] = None
first_name = None
client_id = None
nickname = None
msg_status = None
spam_status = None
buy_status = None
ad_status = None
spam_delay = None
spam_text: Optional[str] = None
ad_text: Optional[str] = None
single_first_name = None
single_client_id = None
saved_sell_id = None
current_seller = None
spam_active = True
ad_active = True
spam_toggle = None
ad_toggle = None

# ========== مقادیر ثابت ==========

single_text = "SINGLE"
math_operators = ["*", "×", "/", "+", "-", "÷"]
chat_commands = ["fr", "cu", "chat", "sl"]

# ========== دریافت نسخه بازی ==========

game_version = baenv.TARGET_BALLISTICA_VERSION
version_parts = [int(x) for x in game_version.split('.')]

# ========== لیست پیام‌های قبلی ==========
previous_messages = []
max_messages = 40

# ========== قیمت‌های آیتم‌ها ==========
item_prices = {
    "item1": 100,
    "item2": 200,
}

# ========== کلاس منوی درون بازی سفارشی ==========

class CustomInGameMenu(ingamemenu.InGameMenuWindow):
    """منوی درون بازی سفارشی"""
    
    def __init__(self, transition: str | None = 'in_right',
                 origin_widget: bui.Widget | None = None):
        super().__init__(transition=transition, origin_widget=origin_widget)
        try:
            babase.set_main_ui_input_device(0)
            logging.info("ورودی به عنوان دستگاه ورودی UI تنظیم شد.")
        except Exception as e:
            logging.warning(f"خطا در تنظیم دستگاه ورودی UI: {e}")

    def _refresh_in_game(self, positions_list: list[tuple[float, float, float]]) -> tuple[float, float, float]:
        """بازسازی منوی درون بازی با آیتم‌های سفارشی"""
        assert bui.app.classic is not None
        custom_entries: list[dict[str, Any]] = []
        current_session = bs.get_foreground_host_session()
        
        if current_session is not None:
            try:
                custom_entries = current_session.get_custom_menu_entries()
                for entry in custom_entries:
                    if (not isinstance(entry, dict) or 
                        'label' not in entry or 
                        not isinstance(entry['label'], (str, bui.Lstr)) or 
                        'call' not in entry or 
                        not callable(entry['call'])):
                        raise ValueError('ورودی منوی سفارشی نامعتبر: ' + str(entry))
            except Exception:
                custom_entries = []
                logging.exception('خطا در دریافت ورودی‌های منوی سفارشی برای %s.', current_session)

        # تشخیص حالت آرکید یا دمو
        env_variant = bui.app.env.variant
        variant_type = type(env_variant)
        is_arcade_demo = (env_variant is variant_type.ARCADE or 
                          env_variant is variant_type.DEMO)

        self.menu_width = 250.0
        self.menu_height = 250.0 if self._input_player else 180.0

        if is_arcade_demo and self._input_player:
            self.menu_height -= 40
        self.menu_height -= 50
        
        self.menu_height += 50 * len(custom_entries)
        self.menu_height += 50

        ui_scale = bui.app.ui_v1.uiscale
        bui.containerwidget(
            edit=self._root_widget,
            size=(self.menu_width, self.menu_height),
            scale=(2.15 if ui_scale is bui.UIScale.SMALL else 
                   1.6 if ui_scale is bui.UIScale.MEDIUM else 1.0)
        )

        h = 125.0
        v = self.menu_height - 80.0 if self._input_player else self.menu_height - 60
        h_offset = 0
        d_h_offset = 0
        v_offset = -50

        for _i in range(2 + len(custom_entries) + 1):
            positions_list.append((h, v, 1.0))
            v += v_offset
            h += h_offset
            h_offset += d_h_offset

        if self._input_player:
            player_name = self._input_player.getname()
            h, v, scale = positions_list[self._p_index]
            v += 35
            bui.textwidget(
                parent=self._root_widget,
                position=(h - self._button_width / 2, v),
                size=(self._button_width, self._button_height),
                color=(1, 1, 1, 0.5),
                scale=0.7,
                h_align='center',
                text=bui.Lstr(value=player_name)
            )

        h, v, scale = positions_list[self._p_index]
        self._p_index += 1
        resume_btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(h - self._button_width / 2, v),
            size=(self._button_width, self._button_height),
            scale=scale,
            label=bui.Lstr(resource=f'{self._r}.resumeText'),
            autoselect=self._use_autoselect,
            on_activate_call=super()._resume
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=resume_btn)

        for entry in custom_entries:
            h, v, scale = positions_list[self._p_index]
            self._p_index += 1
            resume = bool(entry.get('resume_on_call', True))
            if resume:
                call = lambda: self._resume_and_call(entry['call'])
            else:
                call = lambda: entry['call'](lambda: self._resume())
            
            bui.buttonwidget(
                parent=self._root_widget,
                position=(h - self._button_width / 2, v),
                size=(self._button_width, self._button_height),
                scale=scale,
                on_activate_call=call,
                label=entry['label'],
                autoselect=self._use_autoselect
            )

        h, v, scale = positions_list[self._p_index]
        self._p_index += 1
        bui.buttonwidget(
            parent=self._root_widget,
            position=(h - self._button_width / 2, v),
            size=(self._button_width, self._button_height),
            scale=scale,
            on_activate_call=self.leave_game,
            label=bui.Lstr(value='خروج از بازی'),
            autoselect=self._use_autoselect
        )

        return h, v, scale

    def leave_game(self):
        """خروج از بازی"""
        input_device = bs.get_ui_input_device()
        player = input_device.player if input_device else None
        is_attached = (input_device.is_attached_to_player() if 
                      (input_device and player is None) else False)

        if player:
            player.remove_from_game()
        elif is_attached:
            input_device.detach_from_player()

        classic_app = bui.app.classic
        assert classic_app is not None
        classic_app.resume()

        bui.app.ui_v1.clear_main_window()

        for callback in classic_app.main_menu_resume_callbacks:
            try:
                callback()
            except Exception:
                logging.exception('خطا در callback بازگشت به منوی اصلی.')

        classic_app.main_menu_resume_callbacks.clear()


# ========== توابع اصلی ==========

def process_chat_message(self):
    """جایگزین متد _send_chat_message اصلی"""
    global first_name, single_first_name, msg_status, single_client_id, current_seller
    
    chat_text = cast(str, bui.textwidget(query=self._text_field)).strip()
    words = chat_text.strip().split(" ")
    lower_text = chat_text.strip().lower()
    
    # دستور "ss"
    if chat_text[:2].lower() == "ss":
        new_message = "b " + chat_text[1:].lower()
        bs.chatmessage(new_message)
        bui.textwidget(edit=self._text_field, text='')
        return
    
    # بررسی فرمت خرید (4 کلمه)
    if len(lower_text.split(" ")) == 4:
        parts = lower_text.split(" ")
        if parts[0] == "c" and parts[1].isdigit() and parts[2] in item_prices.keys() and parts[3].isdigit():
            result = check_purchase(parts[1], parts[2], parts[3])
            if result:
                bs.screenmessage(f"شما می‌توانید {parts[2]} را بخرید.", color=(0, 1, 0))
            elif result == 0:
                bs.screenmessage(f"شما نمی‌توانید {parts[2]} را بخرید.", color=(1, 0, 0))
            else:
                bs.chatmessage(chat_text)
            bui.textwidget(edit=self._text_field, text='')
            return
    
    # بررسی فرمت خرید (5 کلمه)
    if len(lower_text.split(" ")) == 5:
        parts = lower_text.split(" ")
        if parts[0] == "c" and parts[1].isdigit() and parts[2] in item_prices.keys() and parts[3].isdigit() and parts[4].isdigit():
            result = check_purchase_with_price(parts[1], parts[2], parts[3], parts[4])
            if result:
                bs.screenmessage(f"شما می‌توانید {parts[2]} را با قیمت {parts[4]} بخرید.", color=(0, 1, 0))
            elif result == 0:
                bs.screenmessage(f"شما نمی‌توانید {parts[2]} را با قیمت {parts[4]} بخرید.", color=(1, 0, 0))
            else:
                bs.chatmessage(chat_text)
            bui.textwidget(edit=self._text_field, text='')
            return
    
    # دستورات دو کلمه‌ای
    elif len(lower_text.split(" ")) == 2 and lower_text.split(" ")[1] not in [str(first_name), str(single_first_name)]:
        cmd = lower_text.split(" ")[0]
        target = lower_text.split(" ")[1]
        
        if cmd in ["fr", "cu"] and msg_status:
            hug_msg = "hug " + target
            bs.chatmessage(lower_text)
            bs.apptimer(0.03, lambda: bs.chatmessage(hug_msg))
        
        elif cmd == "hug" and msg_status:
            cu_msg = "cu " + target
            bs.chatmessage(lower_text)
            bs.apptimer(0.9, lambda: bs.chatmessage(cu_msg))
        
        else:
            bs.chatmessage(chat_text)
    
    # ماشین حساب
    elif len(words) == 3:
        if words[1] in math_operators:
            if "×" == words[1] or "*" == words[1]:
                num1 = deci(words[0])
                num2 = deci(words[2])
                bs.chatmessage(f"{num1} × {num2} = {num1 * num2:,}🪙")
            
            elif "÷" == words[1] or "/" == words[1]:
                num1 = deci(words[0])
                num2 = deci(words[2])
                if num2 == 0:
                    bs.screenmessage("تقسیم بر صفر ممکن نیست!", color=(1, 0, 0))
                else:
                    bs.chatmessage(f"{num1} ÷ {num2} = {num1 / num2:,}🪙")
            
            elif "-" == words[1]:
                num1 = deci(words[0])
                num2 = deci(words[2])
                bs.chatmessage(f"{num1} - {num2} = {num1 - num2:,}🪙")
            
            elif "+" == words[1]:
                num1 = deci(words[0])
                num2 = deci(words[2])
                bs.chatmessage(f"{num1} + {num2} = {num1 + num2:,}🪙")
            
            else:
                bs.chatmessage(chat_text)
        else:
            bs.chatmessage(chat_text)
    
    else:
        bs.chatmessage(chat_text)
    
    bui.textwidget(edit=self._text_field, text='')


def update_player_list():
    """به‌روزرسانی اطلاعات بازیکنان"""
    global first_name, client_id, current_username, single_first_name, single_client_id, current_seller
    
    try:
        roster = bs.get_game_roster()
        if roster:
            for player_data in roster:
                try:
                    player_id = str(player_data).replace(" ", "").split(':')[3].split(",")[0].replace('"', "")
                    
                    if player_id == babase.app.plus.get_v1_account_name() and player_data.get('players'):
                        first_name = player_data['players'][0]['name_full'].split(" ")[0]
                        client_id = str(player_data['client_id'])
                        nickname = player_data['players'][0]['name']
                        current_username = nickname
                    
                    elif player_id == single_text and player_data.get('players'):
                        single_first_name = player_data['players'][0]['name_full'].split(" ")[0]
                        single_client_id = str(player_data['client_id'])
                except (IndexError, KeyError, ValueError):
                    pass
    except Exception:
        pass
    
    bs.apptimer(0.1, update_player_list)


def find_overlap(prev, current):
    """پیدا کردن overlap بین دو رشته"""
    overlap = 0
    max_possible = min(len(prev), len(current))
    for k in range(max_possible, 0, -1):
        if prev[-k:] == current[:k]:
            overlap = k
            break
    return overlap


def monitor_chat():
    """نظارت بر پیام‌های چت"""
    global empty_list, spam_toggle, msg_status, ad_status, buy_status, previous_messages
    
    try:
        current_messages = bs.get_chat_messages()
        
        if not previous_messages:
            new_messages = current_messages
        else:
            overlap_len = find_overlap(previous_messages, current_messages)
            new_messages = current_messages[overlap_len:]
        
        for msg in new_messages:
            if msg_status:
                process_msg_handler(msg)
            if spam_toggle:
                process_spam_handler(msg)
            if buy_status:
                process_buy_handler(msg)
            if ad_status:
                process_ad_handler(msg)
        
        previous_messages = current_messages.copy()
        if len(previous_messages) > max_messages:
            previous_messages = previous_messages[-max_messages:]
    
    except Exception:
        pass
    
    bs.apptimer(0.1, monitor_chat)


def process_msg_handler(msg="!"):
    """پردازش پیام‌های عادی"""
    global msg_status, first_name, client_id
    
    if not msg_status:
        return None
    
    try:
        command_part = msg.split(": ")[1].split(" ")[0].casefold()
        
        for cmd in chat_commands:
            if cmd in command_part:
                cmd_parts = msg.split(": ")[1].split(" ")
                target = cmd_parts[1] if len(cmd_parts) >= 2 else ""
                
                if cmd == chat_commands[0] and target in [first_name, client_id]:
                    bs.chatmessage("u")
                
                if cmd == chat_commands[1] and target in [first_name, client_id]:
                    bs.chatmessage("h")
                
                if cmd == chat_commands[3] and target in [first_name, client_id]:
                    bs.chatmessage("sh")
    except Exception:
        pass


def process_buy_handler(msg="!"):
    """پردازش پیام‌های خرید"""
    global buy_status, saved_sell_id, current_seller
    
    if not buy_status:
        return None
    
    try:
        sender = msg.split(": ")[0]
        
        if "🛒Server" in sender and "👉Sell ID" in msg.split(":")[1]:
            saved_sell_id = msg.split(": ")[2]
            bs.chatmessage("b " + saved_sell_id)
        
        item_name = None
        price_sold = None
        
        if len(msg.split(" ")) > 6 and msg.split(" ")[6][1:-1].lower() in item_prices.keys():
            item_name = msg.split(" ")[6][1:-1].lower()
            price_sold = int(msg.split(" ")[9].replace(",", ""))
            current_seller = msg.split(": ", 1)[1].split("🔒Buy", 1)[0]
        
        if len(msg.split(" ")) > 5 and msg.split(" ")[5].lower() in item_prices.keys():
            item_name = msg.split(" ")[5].lower()
            price_sold = int(msg.split(" ")[8].replace(",", ""))
            current_seller = msg.split(": ", 1)[1].split("🔒Buy", 1)[0]
        
        if item_name and price_sold and current_seller == saved_sell_id:
            count = int(msg.split(" ")[4])
            total_value = count * item_prices[item_name]
            profit = total_value - price_sold
            
            if is_profitable(price_sold, profit):
                bs.chatmessage("1")
                saved_sell_id = None
    except Exception:
        pass


def is_profitable(sell_price, profit):
    """بررسی سودآوری معامله"""
    thresholds = [(300, 100), (1000, 600), (5000, 3000), (15000, 10000), (30000, 20000)]
    for max_price, min_profit in thresholds:
        if sell_price <= max_price and profit >= min_profit:
            return True
    return False


def check_purchase(count="", item="", sold="", price=""):
    """بررسی امکان خرید"""
    if price:
        profit = (int(count) * int(price)) - int(sold)
    else:
        profit = (int(count) * item_prices[item]) - int(sold)
    
    return "معامله سودآور است" if is_profitable(int(sold), profit) else 0


def check_purchase_with_price(count="", item="", sold="", price=""):
    """بررسی امکان خرید با قیمت مشخص"""
    return check_purchase(count, item, sold, price)


def process_spam_handler(msg="!"):
    """پردازش پیام‌های اسپم"""
    global spam_toggle, spam_delay, spam_text, spam_status
    
    if not spam_delay:
        return None
    
    try:
        if spam_toggle or spam_delay:
            sender = msg.split(": ")[0]
            if sender in [current_username, babase.app.plus.get_v1_account_name()]:
                parts = msg.split(": ")[1].split(" ")
                if parts[0].replace(".", "").isdigit():
                    delay = float(parts[0])
                    remaining = msg.split(": ")[1].replace(parts[0] + " ", "")
                    
                    if delay > 2.2 and spam_delay:
                        spam_delay = None
                        spam_text = remaining
                        spam_status = delay
                        spam_toggle = None
                        start_spam_timer()
    except Exception:
        pass


def spam_timer_tick():
    """تیک تایمر اسپم"""
    global spam_status, spam_text, spam_toggle, spam_delay
    
    if not spam_delay and not spam_toggle or spam_toggle:
        return None
    
    if not spam_status:
        spam_status = True
        if spam_text or spam_text == "":
            bs.chatmessage(spam_text + "\u00A0")
            start_spam_timer()
            return None
    
    elif spam_status:
        spam_status = None
        if spam_text or spam_text == "":
            bs.chatmessage(spam_text)
            start_spam_timer()
            return None


def start_spam_timer():
    """شروع تایمر اسپم"""
    global spam_toggle, spam_text, spam_status
    
    if not spam_toggle and not spam_delay or spam_toggle:
        return None
    
    bs.apptimer(spam_status, spam_timer_tick)


def process_ad_handler(msg="!"):
    """پردازش پیام‌های تبلیغاتی"""
    global nickname, ad_text, ad_toggle, spam_active
    
    try:
        spam_active = None
        if nickname:
            sender = msg.split(": ")[0]
            if sender in [current_username, babase.app.plus.get_v1_account_name()]:
                text = msg.split(": ")[1].lower()
                if text.split(" ")[0].lower() == "ad" and len(text.split(" ")) > 1 and text not in [ad_text, "ad auto", "ad auto ch", "ad off"]:
                    ad_text = text
                    nickname = None
                    ad_toggle = True
                    start_ad_timer()
                    return None
    except Exception:
        pass


def ad_timer_callback():
    """Callback تایمر تبلیغات"""
    global ad_active, ad_text
    
    if ad_active:
        ad_active = None
        return ad_active
    
    bs.chatmessage(ad_text)
    start_ad_timer()


def start_ad_timer():
    """شروع تایمر تبلیغات"""
    bs.apptimer(20.2, ad_timer_callback)


def handle_command(choice: str = "M"):
    """پردازش دستورات انتخاب شده از منو"""
    global msg_status, buy_status, spam_toggle, spam_delay, nickname, spam_active, ad_toggle, ad_active, ad_status
    
    cmd = choice.lower()
    
    if cmd == "msg" and not msg_status:
        bs.screenmessage("پیام فعال شد ;) | rub : @im_oringinals", color=(1, 1, 0))
        bs.screenmessage("چت مرتضا فعال است :)", color=(0, 1, 0))
        bs.broadcastmessage("@BombSquad_PFBS", color=(0.8, 0.46, 0))
        msg_status = True
    
    elif cmd == "msg off" and msg_status:
        bs.screenmessage("چت مرتضا غیرفعال شد ;(", color=(1, 0, 0))
        bs.broadcastmessage("@BombSquad_PFBS", color=(0.8, 0.46, 0))
        msg_status = None
    
    elif cmd == "buy" and not buy_status:
        bs.screenmessage("خرید فعال شد ;) | rub : @im_oringinals", color=(1, 1, 0))
        bs.screenmessage("فروشگاه مرتضا فعال است :)", color=(0, 1, 0))
        bs.broadcastmessage("@BombSquad_PFBS", color=(0.8, 0.46, 0))
        buy_status = True
    
    elif cmd == "buy off" and buy_status:
        bs.screenmessage("خرید مرتضا غیرفعال شد ;(", color=(1, 0, 0))
        bs.broadcastmessage("@BombSquad_PFBS", color=(0.8, 0.46, 0))
        buy_status = None
    
    elif cmd == "spam" and not spam_toggle:
        bs.screenmessage("مرتضا: 2.3 ثانیه تاخیر | ثانیه/پیام", color=(1, 1, 0))
        bs.screenmessage("تکرار مرتضا فعال است ;) | tm: @mortezaam032", color=(0, 1, 0))
        bs.broadcastmessage("@BombSquad_PFBS", color=(0.8, 0.46, 0))
        spam_toggle = True
        spam_delay = True
    
    elif cmd == "spam ch" and spam_toggle and not spam_delay:
        bs.screenmessage("مرتضا: 2.3 ثانیه تاخیر | ثانیه/پیام", color=(1, 1, 0))
        bs.screenmessage("تکرار مرتضا فعال است ;)", color=(0, 1, 0))
        bs.broadcastmessage("@BombSquad_PFBS", color=(0.8, 0.46, 0))
        spam_delay = True
        spam_toggle = True
    
    elif cmd == "spam off" and spam_toggle:
        bs.screenmessage("تکرار مرتضا غیرفعال شد ;(", color=(1, 0, 0))
        bs.broadcastmessage("@BombSquad_PFBS", color=(0.8, 0.46, 0))
        spam_toggle = None
        spam_delay = None
    
    elif cmd == "ad auto" and not nickname and not ad_toggle:
        bs.screenmessage("مرتضا: متن تبلیغ خود را وارد کنید | Ad a, Ad name, ...", color=(1, 1, 0))
        bs.screenmessage("تبلیغات خودکار مرتضا فعال است ;)", color=(0, 1, 0))
        bs.broadcastmessage("@BombSquad_PFBS", color=(0.8, 0.46, 0))
        nickname = True
        ad_status = True
        ad_active = None
    
    elif cmd == "ad auto ch" and ad_toggle and not nickname:
        bs.screenmessage("مرتضا: متن تبلیغ خود را وارد کنید | Ad a, Ad name, ...", color=(1, 1, 0))
        bs.screenmessage("تبلیغات خودکار مرتضا فعال است ;)", color=(0, 1, 0))
        bs.broadcastmessage("@BombSquad_PFBS", color=(0.8, 0.46, 0))
        spam_active = True
        ad_active = True
        nickname = True
        ad_toggle = None
    
    elif cmd == "ad off" and not spam_active:
        bs.screenmessage("تبلیغات خودکار مرتضا غیرفعال شد ;(", color=(1, 0, 0))
        bs.broadcastmessage("@BombSquad_PFBS", color=(0.8, 0.46, 0))
        spam_active = True
        ad_active = True
        ad_status = None
        nickname = None
        ad_toggle = None


# ========== کلاس پنجره پارتی سفارشی ==========

class CustomPartyMenu(PartyWindow):
    """کلاس پنجره پارتی سفارشی با دکمه منوی اضافی"""
    
    menu_options = {
        "Message": "Msg",
        "Spam": "Spam",
        "Buy": "Buy",
        "Ad global": "Ad Auto",
        "Spam change": "Spam ch",
        "Ad change": "Ad Auto ch",
        "Message off": "Msg off",
        "Spam off": "Spam off",
        "Buy off": "Buy off",
        "Ad off": "Ad off",
    }
    
    button_position = (477, 147)
    
    def __init__(self, origin: Sequence[float] = (0, 0)) -> None:
        self._popup_window: Optional[PopupMenuWindow] = None
        super().__init__(origin)
        
        self._texture = bui.gettexture('googlePlayLeaderboardsIcon')
        
        self._button1 = bui.buttonwidget(
            parent=self._root_widget,
            size=(27, 27),
            label="",
            button_type='square',
            autoselect=True,
            position=(self.button_position[0] + 1, self.button_position[1]),
            texture=self._texture,
            color=(1.0, 0.84, 0.0)
        )
        
        self._button2 = bui.buttonwidget(
            parent=self._root_widget,
            size=(27, 27),
            label="",
            button_type='square',
            autoselect=True,
            on_activate_call=self.open_menu,
            position=self.button_position,
            color=(0.3, 0.3, 0.2)
        )
    
    def open_menu(self) -> None:
        """باز کردن منوی پاپ‌آپ"""
        if self._popup_window is not None:
            self._popup_window = None
            return
        
        ui_scale = bui.app.ui_v1.uiscale
        self._popup_window = PopupMenuWindow(
            position=self._button2.get_screen_space_center(),
            scale=(2.3 if ui_scale is bui.UIScale.SMALL else 
                   1.65 if ui_scale is bui.UIScale.MEDIUM else 1.23),
            choices=list(self.menu_options.keys()),
            current_choice=list(self.menu_options.keys())[0],
            delegate=self
        )
    
    def popup_menu_selected_choice(self, popup_window: PopupMenuWindow, choice: str) -> None:
        """زمانی که گزینه‌ای از منو انتخاب می‌شود"""
        if popup_window == self._popup_window:
            if choice in self.menu_options:
                bs.chatmessage(self.menu_options[choice])
                handle_command(self.menu_options[choice])
                self._popup_window = None
        else:
            super().popup_menu_selected_choice(popup_window, choice)
    
    def popup_menu_closing(self, popup_window: PopupMenuWindow) -> None:
        """وقتی منو بسته می‌شود"""
        if popup_window == self._popup_window:
            self._popup_window = None
        else:
            super().popup_menu_closing(popup_window)
    
    def __del__(self) -> None:
        bui.set_party_window_open(False)
    
    def close(self) -> None:
        """بستن پنجره"""
        if not self._root_widget:
            return
        if self._popup_window is not None:
            self._popup_window = None
        bui.containerwidget(edit=self._root_widget, transition='out_scale')
    
    def close_with_sound(self) -> None:
        """بستن پنجره با صدا"""
        if not self._root_widget:
            return
        bui.getsound('swish').play()
        self.close()


# ========== کلاس اصلی پلاگین ==========

class ByMorteza(babase.Plugin):
    """کلاس اصلی پلاگین"""
    
    def __init__(self) -> None:
        # جایگزینی کلاس‌ها
        if version_parts[1] == 7 and version_parts[2] < 45:
            ingamemenu.InGameMenuWindow = CustomInGameMenu
        
        # نمایش پیام‌های خوش‌آمدگویی
        bs.broadcastmessage('Message Plugin Version API 9', color=(0.18, 0.01, 0.36))
        bs.broadcastmessage('Morteza Plugin: ON', color=(0.13, 0.55, 0.13))
        bs.broadcastmessage('@BombSquad_PFBS', color=(0.8, 0.46, 0))
        
        # جایگزینی کلاس پنجره پارتی
        party.PartyWindow = CustomPartyMenu
        
        # جایگزینی متد ارسال پیام
        party.PartyWindow._send_chat_message = process_chat_message
        
        # شروع توابع نظارتی
        update_player_list()
        monitor_chat()
    
    def has_settings_ui(self) -> bool:
        return False