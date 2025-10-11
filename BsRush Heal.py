# ba_meta require api 9

from __future__ import annotations

import babase
import bascenev1lib.actor.spaz
from bascenev1lib.actor.spaz import Spaz
import bascenev1 as bs
import bascenev1lib


def is_bot_spaz(spaz):
    """تشخیص اینکه آیا اسپاز یک بات است"""
    try:
        # اگر source_player وجود نداشته باشد یا None باشد، این یک بات است
        if not hasattr(spaz, 'source_player') or spaz.source_player is None:
            return True
            
        # اگر source_player داشته باشد اما بازیکن واقعی نباشد
        if hasattr(spaz.source_player, 'is_connected') and not spaz.source_player.is_connected:
            return True
            
    except:
        pass
    
    return False


def new_init_spaz_(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        
        # تشخیص اینکه آیا این یک بات است یا بازیکن انسانی
        is_bot = is_bot_spaz(args[0])
        
        # اگر بازیکن انسانی است، سلامت را بی‌نهایت می‌کنیم
        if not is_bot:
            args[0].hitpoints = 9999  # سلامت بسیار بالا
            args[0].hitpoints_max = 9999
        
        # ایجاد تگ سلامت زیر بازیکن
        health_math = bs.newnode('math',
                       owner=args[0].node,
                       attrs={'input1': (0, -0.7, 0),
                              'operation': 'add'})
        args[0].node.connectattr('position', health_math, 'input2')
        args[0]._hitpoint_text = bs.newnode(
            'text',
            owner=args[0].node,
            attrs={'text': "❤️" + str(args[0].hitpoints),
                   'in_world': True,
                   'shadow': 1.0,
                   'flatness': 1.0,
                   'color': (0, 1, 0),  # سبز پیش‌فرض
                   'scale': 0.01,
                   'h_align': 'center'})
        health_math.connectattr('output', args[0]._hitpoint_text, 'position')
        
        # ایجاد متن بالای بازیکن
        text_math = bs.newnode('math',
                      owner=args[0].node,
                      attrs={'input1': (0, 0.7, 0),
                             'operation': 'add'})
        args[0].node.connectattr('position', text_math, 'input2')
        
        if is_bot:
            # برای بات‌ها
            args[0]._bsrush_text = bs.newnode(
                'text',
                owner=args[0].node,
                attrs={'text': "\ue00cBOT\ue00c",
                       'in_world': True,
                       'shadow': 1.0,
                       'flatness': 1.0,
                       'color': (1, 0.3, 0.3),  # رنگ قرمز برای بات‌ها
                       'scale': 0.012,
                       'h_align': 'center'})
        else:
            # برای بازیکنان انسانی
            args[0]._bsrush_text = bs.newnode(
                'text',
                owner=args[0].node,
                attrs={'text': "BsRush",
                       'in_world': True,
                       'shadow': 1.0,
                       'flatness': 1.0,
                       'color': (0.2, 0.8, 1.0),  # آبی روشن برای بازیکنان
                       'scale': 0.012,
                       'h_align': 'center'})
        
        text_math.connectattr('output', args[0]._bsrush_text, 'position')
        
        # به‌روزرسانی رنگ سلامت بر اساس مقدار فعلی
        update_health_color(args[0])

    return wrapper


def update_health_color(spaz):
    """به‌روزرسانی رنگ تگ سلامت بر اساس مقدار سلامت"""
    health = spaz.hitpoints
    
    # برای بازیکنان انسانی که سلامت بی‌نهایت دارند، همیشه سبز نمایش داده می‌شود
    if not is_bot_spaz(spaz):
        color = (0, 1, 0)  # همیشه سبز
    else:
        # برای بات‌ها رنگ بر اساس سلامت تغییر می‌کند
        if health >= 800:  # سلامت بالا (800 تا 1000) - سبز
            color = (0, 1, 0)  # سبز
        elif health >= 500:  # سلامت متوسط (500 تا 799) - نارنجی
            color = (1, 0.5, 0)  # نارنجی
        elif health >= 200:  # سلامت پایین (200 تا 499) - زرد
            color = (1, 1, 0)  # زرد
        else:  # سلامت بسیار پایین (0 تا 199) - قرمز
            color = (1, 0, 0)  # قرمز
    
    if hasattr(spaz, '_hitpoint_text') and spaz._hitpoint_text:
        spaz._hitpoint_text.color = color


def new_handlemessage_spaz_(func):
    def wrapper(*args, **kwargs):
        def update_hitpoint_text(spaz):
            spaz._hitpoint_text.text = "❤️" + str(spaz.hitpoints)
            update_health_color(spaz)

        func(*args, **kwargs)
        if isinstance(args[1], bs.PowerupMessage):
            if args[1].poweruptype == 'health':
                update_hitpoint_text(args[0])
        if isinstance(
                args[1], bs.HitMessage) or isinstance(
                args[1], bs.ImpactDamageMessage):
            # اگر بازیکن انسانی است، سلامت را دوباره بی‌نهایت می‌کنیم
            if not is_bot_spaz(args[0]):
                args[0].hitpoints = 9999
            update_hitpoint_text(args[0])

    return wrapper


# ba_meta export babase.Plugin
class ByCrossJoy(babase.Plugin):

    def __init__(self):
        pass

    def on_app_running(self) -> None:
        # اعمال تغییرات به کلاس Spaz
        Spaz.__init__ = new_init_spaz_(Spaz.__init__)
        Spaz.handlemessage = new_handlemessage_spaz_(Spaz.handlemessage)