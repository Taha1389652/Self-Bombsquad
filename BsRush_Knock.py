# ba_meta require api 9

from __future__ import annotations

from typing import TYPE_CHECKING

import bascenev1 as bs
from bascenev1lib.actor.spaz import Spaz

if TYPE_CHECKING:
    pass


# Knockout Mod | Created: byBsRush
knockout_jump = False
knockout_pickup = False
knockout_punch = False
knockout_bomb = True
knockout_time = 1.0
# knockout_time: time in seconds

# ba_meta export plugin
class BsRush(bs.Plugin):
    
    Spaz.old_on_jump_press = Spaz.on_jump_press
    def on_jump_press(self) -> None:
        if knockout_jump:
            if not self.node:
                return
            self.node.handlemessage(
                'knockout', knockout_time * 1000)
        else:
            self.old_on_jump_press()
    Spaz.on_jump_press = on_jump_press
    
    Spaz.old_on_pickup_press = Spaz.on_pickup_press
    def on_pickup_press(self) -> None:
        if knockout_pickup:
            if not self.node:
                return
            self.node.handlemessage(
                'knockout', knockout_time * 1000)
        else:
            self.old_on_pickup_press()
    Spaz.on_pickup_press = on_pickup_press
    
    Spaz.old_on_punch_press = Spaz.on_punch_press
    def on_punch_press(self) -> None:
        if knockout_punch:
            if not self.node:
                return
            self.node.handlemessage(
                'knockout', knockout_time * 1000)
        else:
            self.old_on_punch_press()
    Spaz.on_punch_press = on_punch_press
    
    Spaz.old_on_bomb_press = Spaz.on_bomb_press
    def on_bomb_press(self) -> None:
        if knockout_bomb:
            if not self.node:
                return
            self.node.handlemessage(
                'knockout', knockout_time * 1000)
        else:
            self.old_on_bomb_press()
    Spaz.on_bomb_press = on_bomb_press
