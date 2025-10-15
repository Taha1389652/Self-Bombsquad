# ba_meta require api 9
# ba_meta name BsRush Taha
# ba_meta description Gives the host player a glowing, shifting aura every second.

import bascenev1 as bs
import babase
import random

def overload_aura(player: bs.Player) -> None:
    if not player or not player.actor:
        return

    bs.emitfx(
        position=player.actor.node.position,
        velocity=(0, 3, 0),
        count=20,
        scale=2.0,
        spread=0.2,
        chunk_type='spark'
    )
    
    bs.emitfx(
        position=player.actor.node.position,
        velocity=(0, 3, 0),
        count=20,
        scale=1.0,
        spread=0.2,
        chunk_type='metal'
    )
    
    bs.emitfx(
        position=player.actor.node.position,
        velocity=(0, 3, 0),
        count=20,
        scale=1.0,
        spread=0.2,
        chunk_type='ice'
    )

    color = random.choice([
        (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 1, 0), (0, 1, 1), (1, 0, 1)
    ])
    player.actor.node.color = color

    light = bs.newnode('light',
        attrs={
            'position': player.actor.node.position,
            'color': color,
            'radius': 0.3,
            'intensity': 0.8,
            'volume_intensity_scale': 1.0
        })
    
    bs.timer(1.0, light.delete)

def loop_fx(activity: bs.Activity) -> None:
    if not activity.players:
        return

    player = activity.players[0]  # Host player
    overload_aura(player)

# ba_meta export plugin
class AuraOverloadFX(babase.Plugin):
    def __init__(self):
        bs.Activity.__init__ = self._wrap_activity_init(bs.Activity.__init__)
    
    def _wrap_activity_init(self, original):
        def new_init(activity_self, settings):
            original(activity_self, settings)
            bs.timer(0.1, lambda: bs.timer(0.3, lambda: loop_fx(activity_self), repeat=True))
        return new_init