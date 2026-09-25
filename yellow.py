# ba_meta require api 9
"""Adds a glowing yellow ring effect around every player at all times.

Ballistica API 9 plugin. Uses two 'locator' nodes (a bright outline ring
plus a soft filled glow) attached to each PlayerSpaz's node via
connectattr, so the ring always tracks the player's position. The nodes
are owned by the spaz's node, so they're cleaned up automatically when
the player dies/respawns -- no extra bookkeeping needed.
"""

from __future__ import annotations

import babase
import bascenev1 as bs
from bascenev1lib.actor.playerspaz import PlayerSpaz

_orig_spaz_init = PlayerSpaz.__init__

_RING_COLOR = (1.0, 0.85, 0.0)  # yellow
_RING_SIZE = 1.5  # matches the roughly torso-width ring in the reference


def _ring_spaz_init(self, *args, **kwargs) -> None:
    _orig_spaz_init(self, *args, **kwargs)
    _attach_ring(self)


def _attach_ring(spaz: PlayerSpaz) -> None:
    node = spaz.node
    if not node:
        return

    # Crisp outline ring.
    ring = bs.newnode(
        'locator',
        owner=node,
        attrs={
            'shape': 'circleOutline',
            'position': node.position,
            'color': _RING_COLOR,
            'opacity': 1.0,
            'draw_beauty': False,
            'additive': True,
        },
    )

    # Soft filled glow underneath it.
    glow = bs.newnode(
        'locator',
        owner=node,
        attrs={
            'shape': 'circle',
            'position': node.position,
            'color': _RING_COLOR,
            'opacity': 0.2,
            'draw_beauty': False,
            'additive': True,
        },
    )

    # Keep both rings glued to the player as they move.
    node.connectattr('position', ring, 'position')
    node.connectattr('position', glow, 'position')

    # Pop in, then pulse gently forever.
    bs.animate_array(ring, 'size', 1, {0.0: [0.0], 0.25: [_RING_SIZE]})
    bs.animate_array(glow, 'size', 1, {0.0: [0.0], 0.25: [_RING_SIZE]})
    bs.animate(ring, 'opacity', {0.0: 1.0, 0.6: 0.55, 1.2: 1.0}, loop=True)


# ba_meta export babase.Plugin
class YellowRingEffectPlugin(babase.Plugin):
    """Enables the always-on yellow ring effect for all players."""

    def __init__(self) -> None:
        PlayerSpaz.__init__ = _ring_spaz_init
