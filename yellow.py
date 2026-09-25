# ba_meta require api 9
"""Adds glowing yellow ring effects around every player.

Ballistica API 9 plugin. Features:
- A bright outline ring on the ground (base ring)
- A floating ring above the player's head (aerial ring)

Both rings track the player's position and are hollow/outline only.
The rings use 'locator' nodes attached to each PlayerSpaz's node via
connectattr, so they always follow the player. The nodes are owned by the 
spaz's node, so they're cleaned up automatically when the player 
dies/respawns -- no extra bookkeeping needed.
"""

from __future__ import annotations

import babase
import bascenev1 as bs
from bascenev1lib.actor.playerspaz import PlayerSpaz

_orig_spaz_init = PlayerSpaz.__init__

_RING_COLOR = (1.0, 0.85, 0.0)  # yellow
_RING_SIZE = 1.5  # matches the roughly torso-width ring
_FLYING_RING_HEIGHT = 2.0  # height above player for the floating ring


def _ring_spaz_init(self, *args, **kwargs) -> None:
    _orig_spaz_init(self, *args, **kwargs)
    _attach_rings(self)


def _attach_rings(spaz: PlayerSpaz) -> None:
    """Attach both ground and floating rings to the player."""
    node = spaz.node
    if not node:
        return

    # ===== GROUND RING (Base) =====
    # Crisp outline ring on the ground.
    ground_ring = bs.newnode(
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

    # Soft filled glow underneath the ground ring.
    ground_glow = bs.newnode(
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

    # ===== FLOATING RING (Aerial) =====
    # Crisp outline ring floating above the player.
    # This is positioned at player position + height offset
    flying_ring = bs.newnode(
        'locator',
        owner=node,
        attrs={
            'shape': 'circleOutline',
            'position': (node.position[0], node.position[1] + _FLYING_RING_HEIGHT, node.position[2]),
            'color': _RING_COLOR,
            'opacity': 0.8,  # slightly less opaque than ground ring
            'draw_beauty': False,
            'additive': True,
        },
    )

    # Keep all rings glued to the player as they move.
    # For ground rings: direct position tracking
    node.connectattr('position', ground_ring, 'position')
    node.connectattr('position', ground_glow, 'position')
    
    # For flying ring: we need to offset the position by the height
    # We'll use an animcurve or manual positioning in a timer.
    # For simplicity, we'll create a timer that updates the flying ring position
    def _update_flying_ring() -> None:
        """Update flying ring position to stay above player."""
        try:
            if node and flying_ring:
                player_pos = node.position
                flying_ring.position = (
                    player_pos[0],
                    player_pos[1] + _FLYING_RING_HEIGHT,
                    player_pos[2],
                )
        except Exception:
            pass  # Node may have been deleted
    
    # Update flying ring position frequently
    bs.timer(0.05, _update_flying_ring, repeat=True)

    # Pop in, then pulse gently forever for ground rings.
    bs.animate_array(ground_ring, 'size', 1, {0.0: [0.0], 0.25: [_RING_SIZE]})
    bs.animate_array(ground_glow, 'size', 1, {0.0: [0.0], 0.25: [_RING_SIZE]})
    bs.animate(ground_ring, 'opacity', {0.0: 1.0, 0.6: 0.55, 1.2: 1.0}, loop=True)
    
    # Pop in for flying ring with slight delay.
    bs.animate_array(flying_ring, 'size', 1, {0.0: [0.0], 0.25: [_RING_SIZE]})
    bs.animate(flying_ring, 'opacity', {0.0: 0.8, 0.6: 0.45, 1.2: 0.8}, loop=True)


# ba_meta export babase.Plugin
class YellowFloatingRingsPlugin(babase.Plugin):
    """Enables yellow ring effects for all players (ground + flying)."""

    def __init__(self) -> None:
        PlayerSpaz.__init__ = _ring_spaz_init
