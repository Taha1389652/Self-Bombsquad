# ba_meta require api 9

from __future__ import annotations

import babase
import bascenev1 as bs
from bascenev1lib.actor.spaz import Spaz

#################### تنظیمات قابل تغییر ####################
PLAYER_NAME = "Player"  # نام بازیکن
PLAYER_NAME_SIZE = 0.014     # سایز نام بازیکن

TOP_TEXT = "Top 1"           # متن تاپ
TOP_TEXT_SIZE = 0.013        # سایز متن تاپ

TAG_TEXT = "@BsRush_Mod" # متن تگ
TAG_TEXT_SIZE = 0.011        # سایز متن تگ

IS_ADMIN = True          # آیا ادمین است؟

ALLY_TEXT = "< BigRome >"    # متن اتحاد
ALLY_TEXT_SIZE = 0.011       # سایز متن متحد
ALLY_COLOR = (1, 0, 0)       # رنگ اتحاد

INFINITE_HEALTH = True       # سلامتی بی‌نهایت برای بازیکنان
HEALTH_TEXT_ENABLED = True   # نمایش سلامتی
HEART_SYMBOL = "❤️"          # نماد قلب

BOT_TEXT = "\ue00cBOT\ue00c" # متن بات
BOT_COLOR = (1, 0.3, 0.3)    # رنگ پایه‌ی بات (قرمز روشن)
###########################################################

rainbow_counter_1 = 0
rainbow_counter_2 = 0

rainbow_colors = [
    (1.0, 0.0, 0.0), (1.0, 0.2, 0.0), (1.0, 0.4, 0.0), (1.0, 0.6, 0.0),
    (1.0, 0.8, 0.0), (1.0, 1.0, 0.0), (0.8, 1.0, 0.0), (0.6, 1.0, 0.0),
    (0.4, 1.0, 0.0), (0.2, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.2),
    (0.0, 1.0, 0.4), (0.0, 1.0, 0.6), (0.0, 1.0, 0.8), (0.0, 1.0, 1.0),
    (0.0, 0.8, 1.0), (0.0, 0.6, 1.0), (0.0, 0.4, 1.0), (0.0, 0.2, 1.0),
    (0.0, 0.0, 1.0), (0.2, 0.0, 1.0), (0.4, 0.0, 1.0), (0.6, 0.0, 1.0),
    (0.8, 0.0, 1.0), (1.0, 0.0, 1.0), (1.0, 0.0, 0.8), (1.0, 0.0, 0.6),
    (1.0, 0.0, 0.4), (1.0, 0.0, 0.2)
]

rainbow_colors_short = [
    (1.0, 1.0, 0.0), (0.9, 1.0, 0.0), (0.8, 1.0, 0.0), (0.7, 1.0, 0.0),
    (0.6, 1.0, 0.0), (0.5, 1.0, 0.0), (0.6, 1.0, 0.0), (0.7, 1.0, 0.0),
    (0.8, 1.0, 0.0), (0.9, 1.0, 0.0), (1.0, 1.0, 0.0)
]


def is_bot_spaz(spaz: Spaz) -> bool:
    try:
        if not hasattr(spaz, 'source_player') or spaz.source_player is None:
            return True
        if hasattr(spaz.source_player, 'is_connected') and not spaz.source_player.is_connected:
            return True
    except:
        pass
    return False


def setup_custom_text(spaz: Spaz):

    def create_text_nodes():
        if not spaz.node or not spaz.node.exists():
            return

        try:
            # متن سلامتی
            if HEALTH_TEXT_ENABLED:
                health_math = bs.newnode('math',
                    owner=spaz.node,
                    attrs={'input1': (0, -0.7, 0), 'operation': 'add'}
                )
                spaz.node.connectattr('position', health_math, 'input2')

                spaz.health_text = bs.newnode('text',
                    owner=spaz.node,
                    attrs={
                        'text': f"{HEART_SYMBOL}{spaz.hitpoints}",
                        'in_world': True,
                        'shadow': 1.0,
                        'flatness': 1.0,
                        'color': (0, 1, 0),
                        'scale': 0.01,
                        'h_align': 'center'
                    }
                )
                health_math.connectattr('output', spaz.health_text, 'position')

            is_bot = is_bot_spaz(spaz)

            if is_bot:
                bot_shadow_math = bs.newnode('math',
                    owner=spaz.node,
                    attrs={'input1': (0, 0.88, 0), 'operation': 'add'}
                )
                spaz.node.connectattr('torso_position', bot_shadow_math, 'input2')

                spaz.bot_name_shadow = bs.newnode('text',
                    owner=spaz.node,
                    attrs={
                        'text': '',
                        'in_world': True,
                        'shadow': 1.0,
                        'flatness': 1.0,
                        'scale': PLAYER_NAME_SIZE,
                        'h_align': 'center',
                        'color': (0, 0, 0)
                    }
                )
                bot_shadow_math.connectattr('output', spaz.bot_name_shadow, 'position')

                # لایه اصلی
                bot_main_math = bs.newnode('math',
                    owner=spaz.node,
                    attrs={'input1': (0, 0.9, 0), 'operation': 'add'}
                )
                spaz.node.connectattr('torso_position', bot_main_math, 'input2')

                spaz.bot_name_main = bs.newnode('text',
                    owner=spaz.node,
                    attrs={
                        'text': '',
                        'in_world': True,
                        'shadow': 1.0,
                        'flatness': 1.0,
                        'scale': PLAYER_NAME_SIZE - 0.001,
                        'h_align': 'center',
                    }
                )
                bot_main_math.connectattr('output', spaz.bot_name_main, 'position')

            else:
                text_shadow_math = bs.newnode('math',
                    owner=spaz.node,
                    attrs={'input1': (0, 0.88, 0), 'operation': 'add'}
                )
                spaz.node.connectattr('torso_position', text_shadow_math, 'input2')

                spaz.name_shadow = bs.newnode('text',
                    owner=spaz.node,
                    attrs={
                        'text': '',
                        'in_world': True,
                        'shadow': 1.0,
                        'flatness': 1.0,
                        'scale': PLAYER_NAME_SIZE,
                        'h_align': 'center',
                    }
                )
                text_shadow_math.connectattr('output', spaz.name_shadow, 'position')
                spaz.name_shadow.color = (0, 0, 0) if IS_ADMIN else (0, 0, 1)

                text_main_math = bs.newnode('math',
                    owner=spaz.node,
                    attrs={'input1': (0, 0.9, 0), 'operation': 'add'}
                )
                spaz.node.connectattr('torso_position', text_main_math, 'input2')

                spaz.name_main = bs.newnode('text',
                    owner=spaz.node,
                    attrs={
                        'text': '',
                        'in_world': True,
                        'shadow': 1.0,
                        'flatness': 1.0,
                        'scale': PLAYER_NAME_SIZE - 0.001,
                        'h_align': 'center',
                    }
                )
                text_main_math.connectattr('output', spaz.name_main, 'position')
                spaz.name_main.color = (1, 0, 0) if IS_ADMIN else (1, 1, 1)

                ally_math = bs.newnode('math',
                    owner=spaz.node,
                    attrs={'input1': (0, 1.3, 0), 'operation': 'add'}
                )
                spaz.node.connectattr('torso_position', ally_math, 'input2')

                spaz.ally_text = bs.newnode('text',
                    owner=spaz.node,
                    attrs={
                        'text': '',
                        'in_world': True,
                        'shadow': 1.5,
                        'flatness': 1.0,
                        'scale': ALLY_TEXT_SIZE,
                        'h_align': 'center',
                    }
                )
                ally_math.connectattr('output', spaz.ally_text, 'position')

                top_math = bs.newnode('math',
                    owner=spaz.node,
                    attrs={'input1': (0, 1.6, 0), 'operation': 'add'}
                )
                spaz.node.connectattr('torso_position', top_math, 'input2')

                spaz.top_text = bs.newnode('text',
                    owner=spaz.node,
                    attrs={
                        'text': '',
                        'in_world': True,
                        'shadow': 1.5,
                        'flatness': 1.0,
                        'scale': TOP_TEXT_SIZE,
                        'h_align': 'center',
                    }
                )
                top_math.connectattr('output', spaz.top_text, 'position')

                tag_math = bs.newnode('math',
                    owner=spaz.node,
                    attrs={'input1': (0, 2.0, 0), 'operation': 'add'}
                )
                spaz.node.connectattr('torso_position', tag_math, 'input2')

                spaz.tag_text = bs.newnode('text',
                    owner=spaz.node,
                    attrs={
                        'text': '',
                        'in_world': True,
                        'shadow': 1.5,
                        'flatness': 1.0,
                        'scale': TAG_TEXT_SIZE,
                        'h_align': 'center',
                    }
                )
                tag_math.connectattr('output', spaz.tag_text, 'position')
                spaz.tag_text.color = (1.0, 0.0, 0.0)

            start_text_update_timer(spaz)

        except Exception as e:
            print(f"خطا در ایجاد متن: {e}")

    bs.timer(0.2, create_text_nodes)


def start_text_update_timer(spaz: Spaz):

    def update_texts():
        global rainbow_counter_1, rainbow_counter_2

        is_bot = is_bot_spaz(spaz)

        if is_bot:
            if not hasattr(spaz, 'bot_name_main') or not spaz.bot_name_main.exists():
                return
            try:
                spaz.node.name = ' '
                spaz.bot_name_shadow.text = BOT_TEXT
                spaz.bot_name_main.text = BOT_TEXT

                rainbow_counter_1 += 1
                if rainbow_counter_1 >= len(rainbow_colors):
                    rainbow_counter_1 = 0

                spaz.bot_name_main.color = rainbow_colors[rainbow_counter_1]

                if HEALTH_TEXT_ENABLED and hasattr(spaz, 'health_text') and spaz.health_text.exists():
                    spaz.health_text.text = f"{HEART_SYMBOL}{spaz.hitpoints}"
                    update_health_color(spaz)
            except Exception as e:
                print(f"خطا در آپدیت متن بات: {e}")

        else:
            if not hasattr(spaz, 'name_main') or not spaz.name_main.exists():
                return
            try:
                spaz.node.name = ' '
                spaz.name_shadow.text = PLAYER_NAME
                spaz.name_main.text = PLAYER_NAME
                spaz.ally_text.text = ALLY_TEXT
                spaz.ally_text.color = ALLY_COLOR
                spaz.top_text.text = TOP_TEXT
                spaz.tag_text.text = f"[{TAG_TEXT}]"

                rainbow_counter_1 += 1
                rainbow_counter_2 += 1
                if rainbow_counter_1 >= len(rainbow_colors):
                    rainbow_counter_1 = 0
                if rainbow_counter_2 >= len(rainbow_colors_short):
                    rainbow_counter_2 = 0

                spaz.top_text.color = rainbow_colors_short[rainbow_counter_2]
                spaz.tag_text.color = rainbow_colors[rainbow_counter_1]

                if HEALTH_TEXT_ENABLED and hasattr(spaz, 'health_text') and spaz.health_text.exists():
                    spaz.health_text.text = f"{HEART_SYMBOL}{spaz.hitpoints}"
                    update_health_color(spaz)

            except Exception as e:
                print(f"خطا در آپدیت متن بازیکن: {e}")

    spaz.text_update_timer = bs.Timer(0.05, update_texts, repeat=True)


def update_health_color(spaz: Spaz):
    if not hasattr(spaz, 'health_text') or not spaz.health_text:
        return
    health = spaz.hitpoints
    if not is_bot_spaz(spaz) and INFINITE_HEALTH:
        color = (0, 1, 0)
    else:
        if health >= 800:
            color = (0, 1, 0)
        elif health >= 500:
            color = (1, 0.5, 0)
        elif health >= 200:
            color = (1, 1, 0)
        else:
            color = (1, 0, 0)
    spaz.health_text.color = color


def new_spaz_init(original_init):
    def wrapper(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        if not is_bot_spaz(self) and INFINITE_HEALTH:
            self.hitpoints = 9999
            self.hitpoints_max = 9999
        setup_custom_text(self)
    return wrapper


def new_spaz_handlemessage(original_handlemessage):
    def wrapper(self, msg):
        old_hitpoints = self.hitpoints
        result = original_handlemessage(self, msg)
        if self.hitpoints != old_hitpoints:
            if not is_bot_spaz(self) and INFINITE_HEALTH:
                self.hitpoints = 9999
                self.hitpoints_max = 9999
            if (HEALTH_TEXT_ENABLED and hasattr(self, 'health_text')
                    and self.health_text and self.health_text.exists()):
                self.health_text.text = f"{HEART_SYMBOL}{self.hitpoints}"
                update_health_color(self)
        return result
    return wrapper


# ba_meta export plugin
class CustomSpazMod(babase.Plugin):
    def __init__(self):
        self.original_spaz_init = Spaz.__init__
        self.original_spaz_handlemessage = Spaz.handlemessage
        Spaz.__init__ = new_spaz_init(self.original_spaz_init)
        Spaz.handlemessage = new_spaz_handlemessage(self.original_spaz_handlemessage)

        print("✅ مود سفارشی اسپاز فعال شد!")
        print(f"نام بازیکن: {PLAYER_NAME}")
        print(f"متن بات: {BOT_TEXT}")

    def on_app_launch(self) -> None:
        print("🎮 مود اسپاز آماده است!")


print("=" * 50)
print("🎯 مود سفارشی اسپاز نصب شد!")
print(f"نام بازیکن: {PLAYER_NAME}")
print(f"متن بات: {BOT_TEXT}")
print(f"سلامتی بی‌نهایت: {'✅ فعال' if INFINITE_HEALTH else '❌ غیرفعال'}")
print(f"نمایش سلامتی: {'✅ فعال' if HEALTH_TEXT_ENABLED else '❌ غیرفعال'}")
print("=" * 50)