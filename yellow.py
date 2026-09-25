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
_FLOATING_HEIGHT = 0.8  # ارتفاع دایره شناور از زمین (به متر)


def _ring_spaz_init(self, *args, **kwargs) -> None:
    _orig_spaz_init(self, *args, **kwargs)
    _attach_ring(self)


def _attach_ring(spaz: PlayerSpaz) -> None:
    node = spaz.node
    if not node:
        return

    # --- حلقه‌ی روی زمین (مثل قبل) ---
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

    node.connectattr('position', ring, 'position')
    node.connectattr('position', glow, 'position')

    # --- حلقه‌ی شناور جدید ---
    floating_ring = bs.newnode(
        'locator',
        owner=node,
        attrs={
            'shape': 'circleOutline',
            'position': node.position,
            'color': _RING_COLOR,
            'opacity': 0.8,
            'draw_beauty': False,
            'additive': True,
        },
    )

    floating_glow = bs.newnode(
        'locator',
        owner=node,
        attrs={
            'shape': 'circle',
            'position': node.position,
            'color': _RING_COLOR,
            'opacity': 0.15,
            'draw_beauty': False,
            'additive': True,
        },
    )

    bs.animate_array(floating_ring, 'size', 1, {0.0: [0.0], 0.25: [_RING_SIZE]})
    bs.animate_array(floating_glow, 'size', 1, {0.0: [0.0], 0.25: [_RING_SIZE]})
    bs.animate(floating_ring, 'opacity', {0.0: 0.8, 0.6: 0.4, 1.2: 0.8}, loop=True)

    # --- به‌روزرسانی دستی موقعیت دایره‌های شناور ---
    def _update_floating_rings() -> None:
        if not node.exists():
            return
        pos = node.position
        new_pos = (pos[0], pos[1] + _FLOATING_HEIGHT, pos[2])
        floating_ring.position = new_pos
        floating_glow.position = new_pos

    # ✅ رفع خطا: حذف 'with bs.Context(node)' و استفاده مستقیم از bs.Timer
    # تایمر به صورت خودکار با مرگ کاراکتر متوقف نمی‌شود، بنابراین با owner=node
    # آن را به گره متصل می‌کنیم تا عمر آن مدیریت شود.
    bs.Timer(0.01, _update_floating_rings, repeat=True, owner=node)


# ba_meta export babase.Plugin
class YellowRingEffectPlugin(babase.Plugin):
    """Enables the always-on yellow ring effect for all players."""

    def __init__(self) -> None:
        PlayerSpaz.__init__ = _ring_spaz_init
