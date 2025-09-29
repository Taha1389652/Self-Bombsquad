# Porting to api 8 made easier by baport
# ba_meta require api 9

"""
    TNT Respawn Countdown + Bold Channel Tag
"""

from __future__ import annotations
from typing import TYPE_CHECKING

import babase
import bauiv1 as bui
import bascenev1 as bs
import bascenev1lib
import math
import random
from bascenev1lib.actor.bomb import Bomb

if TYPE_CHECKING:
    pass


# ba_meta export babase.Plugin
class TNTRespawnText(babase.Plugin):
    """نمایش شمارش معکوس ثانیه‌ای همراه با برچسب BsRush."""

    @staticmethod
    def clamp(num, min_value, max_value):
        return max(min(num, max_value), min_value)

    def on_tnt_exploded(self):
        self.tnt_has_callback = False
        self._respawn_text.color = (1.0, 1.0, 1.0)
        bs.animate(
            self._respawn_text,
            'opacity',
            {
                0: 0.0,
                self._respawn_time * 0.5: 0.175,
                self._respawn_time: 0.4
            },
        )

    def new_init(func):
        def wrapper(*args, **kwargs):
            args[0]._respawn_text = None
            func(*args, **kwargs)

            args[0].tnt_has_callback = True
            respawn_text_position = (
                args[0]._position[0],
                args[0]._position[1] - 0.4,
                args[0]._position[2],
            )
            args[0]._respawn_text = bs.newnode(
                'text',
                attrs={
                    'text': "",
                    'in_world': True,
                    'position': respawn_text_position,
                    'shadow': 1.0,
                    'flatness': 1.0,
                    'color': (1.0, 1.0, 1.0),
                    'opacity': 0.0,
                    'scale': 0.0225,
                    'h_align': 'center',
                    'v_align': 'center',
                },
            )

            def tnt_callback():
                TNTRespawnText.on_tnt_exploded(args[0])

            args[0]._tnt.node.add_death_action(tnt_callback)
        return wrapper

    bascenev1lib.actor.bomb.TNTSpawner.__init__ = new_init(
        bascenev1lib.actor.bomb.TNTSpawner.__init__)

    def new_update(func):
        def wrapper(*args, **kwargs):
            tnt_alive = args[0]._tnt is not None and args[0]._tnt.node

            func(*args, **kwargs)

            if args[0]._respawn_text:
                remaining_time = args[0]._respawn_time - args[0]._wait_time
                if remaining_time < 0:
                    remaining_time = 0
                args[0]._respawn_text.text = f"{int(math.ceil(remaining_time))}s\nBsRush"

            if not tnt_alive:
                if ((args[0]._tnt is None
                     or args[0]._wait_time >= args[0]._respawn_time)
                        and args[0]._respawn_text):

                    # متن نهایی با افکت RGB
                    args[0]._respawn_text.text = "0s\n@BsRush_Games"
                    
                    # ایجاد افکت RGB با انیمیشن
                    def update_rgb_color():
                        if not args[0]._respawn_text:
                            return
                        
                        # محاسبه رنگ RGB متغیر بر اساس زمان
                        time_val = bs.time() * 5  # سرعت تغییر رنگ
                        r = (math.sin(time_val) + 1) / 2  # مقدار بین 0 تا 1
                        g = (math.sin(time_val + 2) + 1) / 2  # فاز متفاوت
                        b = (math.sin(time_val + 4) + 1) / 2  # فاز متفاوت
                        
                        args[0]._respawn_text.color = (r, g, 1.0)  # آبی ثابت برای کنتراست بهتر
                        
                        # ادامه انیمیشن تا زمانی که متن وجود دارد
                        if args[0]._respawn_text.opacity > 0:
                            bs.apptimer(0.1, update_rgb_color)
                    
                    # شروع انیمیشن RGB
                    update_rgb_color()

                    bs.animate(
                        args[0]._respawn_text,
                        'scale',
                        {
                            0: args[0]._respawn_text.scale * 1.6,
                            0.3: args[0]._respawn_text.scale * 1.3,
                            0.6: args[0]._respawn_text.scale * 1.1,
                            1.1: args[0]._respawn_text.scale * 1.2
                        },
                    )
                    bs.animate(
                        args[0]._respawn_text,
                        'opacity',
                        {0: args[0]._respawn_text.opacity, 1.5: 0.0},
                    )

                    # جلوه‌های ویژه
                    for ctype, scale in [('spark', 2.8),
                                         ('ice', 1.8),
                                         ('metal', 2.8)]:
                        bs.emitfx(
                            position=args[0]._position,
                            count=int(50 + random.random() * 100),
                            scale=scale,
                            spread=1.25,
                            chunk_type=ctype,
                        )
            else:
                if args[0].tnt_has_callback:
                    return

                def tnt_callback():
                    TNTRespawnText.on_tnt_exploded(args[0])
                args[0]._tnt.node.add_death_action(tnt_callback)
        return wrapper

    bascenev1lib.actor.bomb.TNTSpawner._update = new_update(
        bascenev1lib.actor.bomb.TNTSpawner._update)
