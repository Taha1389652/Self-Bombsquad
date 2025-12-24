import bascenev1 as bs
import babase
import random
from typing import TYPE_CHECKING, Optional, Any
from bascenev1lib.actor import spaz
from bascenev1lib.actor.spaz import Spaz
from bascenev1lib.actor.bomb import Blast
from bascenev1lib.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Union, Sequence

STORAGE_ATTR_NAME = f'_shared_super_punch_rocket_factory'

# ================== ROCKET SYSTEM ==================
class RocketFactory:
    """Factory for creating rockets"""
    
    def __init__(self) -> None:
        self.ball_material = bs.Material()
        
        self.ball_material.add_actions(
            conditions=((('we_are_younger_than', 5), 'or',
                         ('they_are_younger_than', 5)), 'and',
                        ('they_have_material',
                         SharedObjects.get().object_material)),
            actions=('modify_node_collision', 'collide', False))
        
        self.ball_material.add_actions(
            conditions=('they_have_material',
                        SharedObjects.get().pickup_material),
            actions=('modify_part_collision', 'use_node_collide', False))
        
        self.ball_material.add_actions(actions=('modify_part_collision',
                                                'friction', 0))
        
        self.ball_material.add_actions(
            conditions=(('they_have_material',
                         SharedObjects.get().footing_material), 'or',
                        ('they_have_material',
                         SharedObjects.get().object_material)),
            actions=('message', 'our_node', 'at_connect', ImpactMessage()))
    
    @classmethod
    def get(cls):
        """Get factory if exists else create new"""
        activity = bs.getactivity()
        if hasattr(activity, STORAGE_ATTR_NAME):
            return getattr(activity, STORAGE_ATTR_NAME)
        factory = cls()
        setattr(activity, STORAGE_ATTR_NAME, factory)
        return factory


class RocketLauncher:
    """Rocket launcher weapon for Spaz"""
    
    def __init__(self):
        self.last_shot: Optional[float] = 0
    
    def give(self, spaz: Spaz) -> None:
        """Give spaz a rocket launcher"""
        # Store original punch callback
        self.original_punch_callback = spaz.punch_callback
        spaz.punch_callback = self.shot
        self.last_shot = bs.time()
    
    def shot(self, spaz: Spaz) -> None:
        """Launch a rocket AND do normal punch"""
        time = bs.time()
        
        # First, do the original punch if exists
        if self.original_punch_callback:
            self.original_punch_callback(spaz)
        
        # Then launch rocket with cooldown
        if time - self.last_shot > 0.6:  # Cooldown time
            self.last_shot = time
            
            # Calculate direction based on spaz orientation
            center = spaz.node.position_center
            forward = spaz.node.position_forward
            direction = [
                center[0] - forward[0],
                forward[1] - center[1],
                center[2] - forward[2]
            ]
            direction[1] = 0.0  # Keep it horizontal
            
            # Normalize and set velocity
            mag = 10.0 / babase.Vec3(*direction).length()
            vel = [v * mag for v in direction]
            
            # Create rocket with spaz's color
            Rocket(
                position=spaz.node.position,
                velocity=vel,
                source_player=spaz.getplayer(bs.Player),
                owner=spaz.getplayer(bs.Player),
                color=spaz.node.color  # Use original spaz color
            ).autoretain()


class ImpactMessage:
    """Message when rocket hits something"""


class Rocket(bs.Actor):
    """Rocket projectile with enhanced effects"""
    
    def __init__(self,
                 position=(0, 5, 0),
                 velocity=(1, 0, 0),
                 source_player=None,
                 owner=None,
                 color=(1.0, 0.2, 0.2)) -> None:
        super().__init__()
        self.source_player = source_player
        self.owner = owner
        self._color = color
        factory = RocketFactory.get()
        
        self.node = bs.newnode('prop',
                               delegate=self,
                               attrs={
                                   'position': position,
                                   'velocity': velocity,
                                   'mesh': bs.getmesh('impactBomb'),
                                   'body': 'sphere',
                                   'color_texture': bs.gettexture('bunnyColor'),
                                   'mesh_scale': 0.2,
                                   'is_area_of_interest': True,
                                   'body_scale': 0.8,
                                   'materials': [
                                       SharedObjects.get().object_material,
                                       factory.ball_material]
                               })
        
        # Add forward acceleration
        self.node.extra_acceleration = (self.node.velocity[0] * 200, 0,
                                        self.node.velocity[2] * 200)
        
        # Auto-destroy after 5 seconds
        self._life_timer = bs.Timer(
            5, bs.WeakCall(self.handlemessage, bs.DieMessage()))
        
        # Emission trail effect - ORIGINAL TIMING
        self._emit_timer = bs.Timer(0.001, bs.WeakCall(self.emit), repeat=True)
        self.base_pos_y = self.node.position[1]
        
        # Camera shake - ORIGINAL STRENGTH
        bs.camerashake(5.0)
    
    def emit(self) -> None:
        """Create trail effect"""
        if not self.node:
            return
        
        # ORIGINAL EMITFX
        bs.emitfx(position=self.node.position,
                  scale=0.4,
                  spread=0.01,
                  chunk_type='spark')
        
        # Keep horizontal movement
        self.node.position = (self.node.position[0], self.base_pos_y,
                              self.node.position[2])
        
        # ORIGINAL EXPLOSION EFFECT
        bs.newnode('explosion',
                   owner=self.node,
                   attrs={
                       'position': self.node.position,
                       'radius': 0.2,
                       'color': self._color
                   })
    
    def handlemessage(self, msg: Any) -> Any:
        """Handle messages"""
        super().handlemessage(msg)
        
        if isinstance(msg, ImpactMessage):
            self.node.handlemessage(bs.DieMessage())
        
        elif isinstance(msg, bs.DieMessage):
            if self.node:
                # ORIGINAL BLAST with bomb type
                Blast(position=self.node.position,
                      blast_radius=2,
                      blast_type='impactBomb',  # Original bomb type
                      source_player=self.source_player,
                      hit_type='impact')

                self.node.delete()
                self._emit_timer = None
        
        elif isinstance(msg, bs.OutOfBoundsMessage):
            self.handlemessage(bs.DieMessage())


# ================== MAIN PLUGIN ==================
# ba_meta require api 9
# ba_meta export babase.Plugin


class SuperPunchJumpBsRush(babase.Plugin):
    def on_app_running(self) -> None:
        from bascenev1lib.actor import spaz
        
        # Save original methods
        original_punch_press = spaz.Spaz.on_punch_press
        original_jump_press = spaz.Spaz.on_jump_press
        
        def new_on_jump_press(self):
            """Jump button now does super jump"""
            if not self.node or not self.node.exists():
                if original_jump_press:
                    return original_jump_press(self)
                return
            
            # Get current position and velocity
            pos = self.node.position
            vel = self.node.velocity
            
            # Apply super jump impulse - ORIGINAL VALUES
            self.node.handlemessage(
                "impulse",
                pos[0], pos[1] + 1.0, pos[2],
                vel[0], vel[1], vel[2],
                80, 20, 0, 0,
                vel[0], vel[1] + 12, vel[2]
            )
            
            self.node.punch_pressed = True
            
            # Play jump sound - ORIGINAL
            try:
                bs.getsound('powerup01').play(volume=0.3)
            except:
                pass
            
            # Also call original jump if exists
            if original_jump_press:
                original_jump_press(self)
        
        def new_on_punch_press(self):
            if not hasattr(self, '_rocket_launcher'):
                self._rocket_launcher = RocketLauncher()
                self._rocket_launcher.give(self)
            
            # Call the rocket launcher shot (which also calls original punch)
            self._rocket_launcher.shot(self)
            
            # Play rocket sound - ORIGINAL
            try:
                bs.getsound('explosion01').play(volume=0.5)
            except:
                pass
            
            # Also call original punch press if exists
            if original_punch_press:
                original_punch_press(self)
        
        # Override the methods
        spaz.Spaz.on_jump_press = new_on_jump_press
        spaz.Spaz.on_punch_press = new_on_punch_press

        original_jump_release = spaz.Spaz.on_jump_release
        
        def new_on_jump_release(self):
            if original_jump_release:
                original_jump_release(self)
        
        spaz.Spaz.on_jump_release = new_on_jump_release
        
        # Also override punch release
        original_punch_release = spaz.Spaz.on_punch_release
        
        def new_on_punch_release(self):
            # Just call original if exists
            if original_punch_release:
                original_punch_release(self)
        
        spaz.Spaz.on_punch_release = new_on_punch_release
