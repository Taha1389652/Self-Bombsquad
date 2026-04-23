# Released under the MIT License. See LICENSE for details.
#
"""Implements football games with flags and score on wall."""

# ba_meta require api 9

from __future__ import annotations

from typing import TYPE_CHECKING

import babase
import bascenev1 as bs
import random
import math
from bascenev1lib.actor.playerspaz import PlayerSpaz
from bascenev1lib.actor.scoreboard import Scoreboard
from bascenev1lib.actor.powerupbox import PowerupBoxFactory
from bascenev1lib.actor.flag import Flag
from bascenev1lib.gameutils import SharedObjects
from bascenev1lib.actor.spazfactory import SpazFactory

if TYPE_CHECKING:
    from typing import Any, Sequence, Dict, Type, List, Optional, Union


class PuckDiedMessage:
    """Inform something that a puck has died."""

    def __init__(self, puck: Puck):
        self.puck = puck


class PlayerSpazHurtMessage:
    """Inform something that a spaz was hurt."""

    def __init__(self, spaz: PlayerSpaz) -> None:
        self.spaz = spaz


class StarEffectOnObject:
    """Stars effect around any object (flag, ball, etc)"""
    
    def __init__(self, target_node, duration: float = 5.0):
        self.target_node = target_node
        self.active = True
        self.timer = None
        self.stars = []
        self.angle = 0
        self.duration = duration
        
    def start(self):
        try:
            activity = bs.get_foreground_host_activity()
            if activity:
                with activity.context:
                    self.create_stars()
                    # Auto stop after duration
                    bs.timer(self.duration, self.stop)
            else:
                bs.timer(0.5, self.start)
        except Exception:
            pass
    
    def create_star(self, offset_angle):
        """Create one star with shield"""
        try:
            if not self.target_node or not self.target_node.exists():
                return
            
            pos = self.target_node.position
            
            # Create flash (star)
            flash = bs.newnode("flash",
                owner=self.target_node,
                attrs={
                    'position': pos,
                    'size': 0.3,
                    'color': (1, 1, 0.5)
                })
            
            # RGB color animation
            bs.animate_array(flash, 'color', 3, {
                0: (2, 1, 0),
                0.2: (1, 0, 2),
                0.4: (0, 2, 1),
                0.6: (2, 0, 1),
                0.8: (1, 2, 0)
            }, loop=True)
            
            # Pulse animation
            bs.animate(flash, 'size', {
                0: 0.3,
                0.5: 0.4,
                1.0: 0.3
            }, loop=True)
            
            # Create shield
            shield = bs.newnode("shield",
                owner=self.target_node,
                attrs={
                    'color': (1, 1, 0.5),
                    'position': pos,
                    'radius': 0.35
                })
            
            # Shield color animation
            bs.animate_array(shield, 'color', 3, {
                0: (2, 1, 0),
                0.2: (1, 0, 2),
                0.4: (0, 2, 1),
                0.6: (2, 0, 1),
                0.8: (1, 2, 0)
            }, loop=True)
            
            star = {'node': flash, 'shield': shield, 'offset_angle': offset_angle, 'last_pos': pos}
            self.stars.append(star)
            
        except Exception:
            pass
    
    def create_particles(self, pos):
        """Create small particles around star"""
        try:
            for _ in range(1):
                angle = random.uniform(0, 2 * math.pi)
                x = pos[0] + math.cos(angle) * 0.12
                z = pos[2] + math.sin(angle) * 0.12
                
                bs.emitfx(
                    position=(x, pos[1] + 0.1, z),
                    velocity=(math.cos(angle) * 0.3, random.uniform(0.1, 0.2), math.sin(angle) * 0.3),
                    count=1,
                    scale=0.07,
                    spread=0.02,
                    chunk_type='spark'
                )
        except:
            pass
    
    def create_stars(self):
        """Create 3 stars around object"""
        self.create_star(0)      # First star
        self.create_star(120)    # Second star
        self.create_star(240)    # Third star
        
        if self.active:
            self.timer = bs.timer(0.05, self.update_rotation)
    
    def update_rotation(self):
        if not self.target_node or not self.target_node.exists() or not self.active:
            return
        
        try:
            pos = self.target_node.position
            self.angle += 10  # Faster rotation
            
            for star in self.stars:
                if star['node'] and star['node'].exists():
                    current_angle = math.radians(self.angle + star['offset_angle'])
                    
                    x = pos[0] + math.cos(current_angle) * 0.9
                    z = pos[2] + math.sin(current_angle) * 0.9
                    y = pos[1] + 0.3
                    
                    new_pos = (x, y, z)
                    star['node'].position = new_pos
                    
                    if star['shield'] and star['shield'].exists():
                        star['shield'].position = new_pos
                    
                    # Small particles
                    if random.random() < 0.15:
                        self.create_particles(new_pos)
                    
                    star['last_pos'] = new_pos
                        
        except Exception:
            pass
        
        if self.active:
            self.timer = bs.timer(0.05, self.update_rotation)
    
    def stop(self):
        self.active = False
        for star in self.stars:
            if star['node'] and star['node'].exists():
                star['node'].delete()
            if star['shield'] and star['shield'].exists():
                star['shield'].delete()
        self.stars.clear()
        if self.timer:
            self.timer = None


class DarkMagicEffect:
    """Dark magic effect for players"""
    
    def __init__(self, spaz):
        self.spaz = spaz
        self.node = spaz.node
        self.active = True
        self.timer = None
        
    def start(self):
        try:
            activity = bs.get_foreground_host_activity()
            if activity:
                with activity.context:
                    self.create_darkmagic()
            else:
                bs.timer(0.5, self.start)
        except Exception:
            pass
        
    def create_darkmagic(self):
        if not self.node or not self.node.exists() or not self.active:
            self.timer = None
            return
            
        def die(node):
            if node and node.exists():
                try:
                    m = node.mesh_scale
                    bs.animate(node, 'mesh_scale', {0: m, 0.1: 0})
                    bs.timer(0.1, node.delete)
                except:
                    pass
        
        try:
            c = 0.5
            pos_list = [
                (c, 0, 0), (0, 0, c),
                (-c, 0, 0), (0, 0, -c),
                (c*0.7, 0, c*0.7), (-c*0.7, 0, -c*0.7),
                (c*0.7, 0, -c*0.7), (-c*0.7, 0, c*0.7),
                (c*0.3, 0, c), (c, 0, c*0.3),
                (-c*0.3, 0, -c), (-c, 0, -c*0.3)
            ]
            
            for p in pos_list:
                for _ in range(2):
                    m = 2.0
                    np = self.node.position
                    pos = (np[0] + p[0], np[1] + p[1] + 0.2, np[2] + p[2])
                    vel = (random.uniform(-m, m), random.uniform(5.0, 10.0), random.uniform(-m, m))

                    tex = bs.gettexture('impactBombColor')
                    mesh = bs.getmesh('impactBomb')
                    factory = SpazFactory.get()
                    
                    mat = bs.Material()
                    mat.add_actions(
                        conditions=('they_have_material', factory.punch_material),
                        actions=(
                            ('modify_part_collision', 'collide', False),
                            ('modify_part_collision', 'physical', False),
                        ))

                    node = bs.newnode('prop',
                        owner=self.node,
                        attrs={
                            'body': 'sphere',
                            'position': pos,
                            'velocity': vel,
                            'mesh': mesh,
                            'mesh_scale': 0.3,
                            'body_scale': 0.0,
                            'shadow_size': 0.0,
                            'gravity_scale': 0.3,
                            'color_texture': tex,
                            'reflection': 'soft',
                            'reflection_scale': [0.0],
                            'materials': [mat]
                        })
                    
                    light = bs.newnode('light',
                        owner=node,
                        attrs={
                            'intensity': 0.8,
                            'volume_intensity_scale': 0.3,
                            'color': (0.5, 0.0, 1.0),
                            'radius': 0.03
                        })
                    node.connectattr('position', light, 'position')
                    bs.timer(0.25, lambda n=node: die(n))
                
        except Exception:
            pass
        
        if self.node and self.node.exists() and self.active:
            self.timer = bs.timer(0.2, self.create_darkmagic)
    
    def stop(self):
        self.active = False
        if self.timer:
            self.timer = None


class CustomPlayerSpaz(PlayerSpaz):
    """Custom Spaz with team name display"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._team_name_text = None
        self._team_name_shadow = None
        # Remove jump cooldown for rapid jumping
        self._jump_cooldown = 0
        
    def add_team_name_text(self, team_name: str, team_color: Sequence[float]):
        """Add team name above player"""
        if not self.node or not self.node.exists():
            return
        
        # Shadow text
        shadow_math = bs.newnode('math',
                                 owner=self.node,
                                 attrs={'input1': (0, 2.3, 0), 'operation': 'add'})
        self.node.connectattr('position', shadow_math, 'input2')
        
        self._team_name_shadow = bs.newnode('text',
                                            owner=self.node,
                                            attrs={
                                                'text': team_name,
                                                'in_world': True,
                                                'shadow': 1.0,
                                                'flatness': 1.0,
                                                'scale': 0.012,
                                                'h_align': 'center',
                                                'color': (0, 0, 0)
                                            })
        shadow_math.connectattr('output', self._team_name_shadow, 'position')
        
        # Main text
        main_math = bs.newnode('math',
                               owner=self.node,
                               attrs={'input1': (0, 2.35, 0), 'operation': 'add'})
        self.node.connectattr('position', main_math, 'input2')
        
        self._team_name_text = bs.newnode('text',
                                          owner=self.node,
                                          attrs={
                                              'text': team_name,
                                              'in_world': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'scale': 0.012,
                                              'h_align': 'center',
                                              'color': team_color
                                          })
        main_math.connectattr('output', self._team_name_text, 'position')
    
    def remove_team_name_text(self):
        if self._team_name_text:
            self._team_name_text.delete()
            self._team_name_text = None
        if self._team_name_shadow:
            self._team_name_shadow.delete()
            self._team_name_shadow = None


class Puck(bs.Actor):
    """A lovely giant hockey puck."""

    def __init__(self, position: Sequence[float] = (0.0, 1.0, 0.0)):
        super().__init__()
        shared = SharedObjects.get()
        activity = self.getactivity()

        self._spawn_pos = (position[0], position[1] + 1.0, position[2])
        self.last_players_to_touch: Dict[int, Player] = {}
        self.scored = False
        self._spawn_effect = None
        assert activity is not None
        assert isinstance(activity, SoccerGame)
        pmats = [shared.object_material, activity.puck_material]
        
        self.node = bs.newnode('prop',
                               delegate=self,
                               attrs={
                                   'mesh': bs.getmesh('frostyPelvis'),
                                   'color_texture': bs.gettexture('eggTex1'),
                                   'body': 'sphere',
                                   'reflection': 'soft',
                                   'reflection_scale': [0.2],
                                   'shadow_size': 0.5,
                                   'is_area_of_interest': True,
                                   'position': self._spawn_pos,
                                   'materials': pmats
                               })
        bs.animate(self.node, 'mesh_scale', {0: 0, 0.2: 1.2, 0.26: 1.0})
        
        # Start spawn effect (stars around ball for 1 second)
        self._start_spawn_effect()
    
    def _start_spawn_effect(self):
        """Start the rotating stars effect around the ball for 1 second"""
        try:
            self._spawn_effect = StarEffectOnObject(self.node, duration=1.0)
            self._spawn_effect.start()
        except Exception:
            pass
    
    def _stop_spawn_effect(self):
        """Stop the spawn effect"""
        if self._spawn_effect:
            self._spawn_effect.stop()
            self._spawn_effect = None

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.DieMessage):
            # Stop effect when ball dies
            if self._spawn_effect:
                self._spawn_effect.stop()
                self._spawn_effect = None
            assert self.node
            self.node.delete()
            activity = self._activity()
            if activity and not msg.immediate:
                activity.handlemessage(PuckDiedMessage(self))
        elif isinstance(msg, bs.OutOfBoundsMessage):
            assert self.node
            self.node.position = self._spawn_pos
        elif isinstance(msg, bs.HitMessage):
            assert self.node
            assert msg.force_direction is not None
            self.node.handlemessage(
                'impulse', msg.pos[0], msg.pos[1], msg.pos[2], msg.velocity[0],
                msg.velocity[1], msg.velocity[2], 1.0 * msg.magnitude,
                1.0 * msg.velocity_magnitude, msg.radius, 0,
                msg.force_direction[0], msg.force_direction[1],
                msg.force_direction[2])
            s_player = msg.get_source_player(Player)
            if s_player is not None:
                activity = self._activity()
                if activity:
                    if s_player in activity.players:
                        self.last_players_to_touch[s_player.team.id] = s_player
        else:
            super().handlemessage(msg)


class Player(bs.Player['Team']):
    """Our player type for this game."""


class Team(bs.Team[Player]):
    """Our team type for this game."""

    def __init__(self) -> None:
        self.score = 0


# ba_meta export bascenev1.GameActivity
class SoccerGame(bs.TeamGameActivity[Player, Team]):
    """Football game with flags and score on wall."""

    name = 'Football Bslife'
    description = 'BSRUSH Match - Beautiful Soccer Game'
    available_settings = [
        bs.IntSetting(
            'Score to Win',
            min_value=1,
            default=1,
            increment=1,
        ),
        bs.IntChoiceSetting(
            'Time Limit',
            choices=[
                ('None', 0),
                ('1 Minute', 60),
                ('2 Minutes', 120),
                ('5 Minutes', 300),
                ('10 Minutes', 600),
                ('20 Minutes', 1200),
            ],
            default=0,
        ),
        bs.FloatChoiceSetting(
            'Respawn Times',
            choices=[
                ('Shorter', 0.25),
                ('Short', 0.5),
                ('Normal', 1.0),
                ('Long', 2.0),
                ('Longer', 4.0),
            ],
            default=1.0,
        ),
        bs.BoolSetting('پانچ بینهایت', default=False),
        bs.BoolSetting('اسپاون باکس های کمکی', default=True),
        bs.BoolSetting('صدمه زدن به پلیر', default=True),
        bs.BoolSetting('Epic Mode', default=True),
        bs.BoolSetting('Flags Around Field', default=True),
    ]
    default_music = bs.MusicType.HOCKEY

    @classmethod
    def supports_session_type(cls, sessiontype: Type[bs.Session]) -> bool:
        return issubclass(sessiontype, bs.DualTeamSession)

    @classmethod
    def get_supported_maps(cls, sessiontype: Type[bs.Session]) -> List[str]:
        return ['Hockey Stadium', 'Football Stadium']

    def __init__(self, settings: dict):
        super().__init__(settings)
        shared = SharedObjects.get()
        self._scoreboard = Scoreboard()
        self._cheer_sound = bs.getsound('cheer')
        self._chant_sound = bs.getsound('crowdChant')
        self._foghorn_sound = bs.getsound('foghorn')
        self._swipsound = bs.getsound('swip')
        self._whistle_sound = bs.getsound('refWhistle')
        self._boxing_gloves = bool(settings.get('پانچ بینهایت', False))
        self._enable_powerups = bool(settings.get('اسپاون باکس های کمکی', True))
        self._hit_players = bool(settings['صدمه زدن به پلیر'])
        self._epic_mode = bool(settings['Epic Mode'])
        self._flags_around_field = bool(settings.get('Flags Around Field', True))
        self.slow_motion = self._epic_mode
        self.default_music = (bs.MusicType.EPIC
                              if self._epic_mode else bs.MusicType.FOOTBALL)
        self.puck_material = bs.Material()
        self.puck_material.add_actions(actions=(('modify_part_collision',
                                                 'friction', 0.5)))
        self.puck_material.add_actions(conditions=('they_have_material',
                                                   shared.pickup_material),
                                       actions=('modify_part_collision',
                                                'collide', True))
        self.puck_material.add_actions(
            conditions=(
                ('we_are_younger_than', 100),
                'and',
                ('they_have_material', shared.object_material),
            ),
            actions=('modify_node_collision', 'collide', False),
        )
        self.puck_material.add_actions(
            conditions=('they_have_material', shared.player_material),
            actions=('call', 'at_connect', self._handle_puck_player_collide))
        self.puck_material.add_actions(
            conditions=('they_have_material',
                        PowerupBoxFactory.get().powerup_material),
            actions=(('modify_part_collision', 'physical', False),
                     ('message', 'their_node', 'at_connect', bs.DieMessage())))
        self._score_region_material = bs.Material()
        self._score_region_material.add_actions(
            conditions=('they_have_material', self.puck_material),
            actions=(('modify_part_collision', 'collide',
                      True), ('modify_part_collision', 'physical', False),
                     ('call', 'at_connect', self._handle_score)))
        self._puck_spawn_pos: Optional[Sequence[float]] = None
        self._score_regions: Optional[List[bs.NodeActor]] = None
        self._puck: Optional[Puck] = None
        self._score_to_win = int(settings['Score to Win'])
        self._time_limit = float(settings['Time Limit'])
        self._flags: List[Flag] = []
        self._flag_lights: List[bs.Node] = []
        self._current_flag_effects: List[StarEffectOnObject] = []
        self._right_flags: List[bs.Node] = []
        self._left_flags: List[bs.Node] = []

    def get_instance_description(self) -> Union[str, Sequence]:
        if self._score_to_win == 1:
            return 'Score a goal.'
        return 'Score ${ARG1} goals.', self._score_to_win

    def get_instance_description_short(self) -> Union[str, Sequence]:
        if self._score_to_win == 1:
            return 'score a goal'
        return 'score ${ARG1} goals', self._score_to_win

    def on_transition_in(self) -> None:
        super().on_transition_in()
        shared = SharedObjects.get()
        activity = bs.getactivity()
        
        # ========== HOCKEY MODE COMPLETELY DISABLED ==========
        # Force disable hockey mode (no ice, no speed boost)
        if hasattr(activity.map, 'is_hockey'):
            activity.map.is_hockey = False
        
        # ========== BRIGHT LIGHTING ==========
        gnode = bs.getactivity().globalsnode
        gnode.tint = (1.2, 1.25, 1.3)
        gnode.ambient_color = (1.1, 1.15, 1.2)
        gnode.vignette_outer = (0.5, 0.5, 0.5)
        gnode.vignette_inner = (0.95, 0.95, 0.95)
        gnode.shadow_offset = (0.0, 1.5, 0.0)
        
        # Change floor color to grass green
        if hasattr(activity.map, 'floor') and activity.map.floor:
            activity.map.floor.color = (0.25, 0.7, 0.18)
            activity.map.floor.reflection = 'soft'
            activity.map.floor.reflection_scale = [1.5]
        
        # Add corner flags
        self._add_corner_flags()
        
        if hasattr(activity.map, 'node') and activity.map.node:
            activity.map.node.materials = [shared.footing_material]
        
        if hasattr(activity.map, 'floor') and activity.map.floor:
            activity.map.floor.materials = [shared.footing_material]
    
    def _add_corner_flags(self):
        """Add corner flags"""
        corners = [(-14.5, -8.5), (-14.5, 8.5), (14.5, -8.5), (14.5, 8.5)]
        for cx, cz in corners:
            try:
                flag = Flag(position=(cx, 1.3, cz), touchable=False, color=(1, 1, 0))
                self._flags.append(flag)
            except Exception:
                pass

    def on_begin(self) -> None:
        super().on_begin()
        self.setup_standard_time_limit(self._time_limit)
        if self._enable_powerups:
            self.setup_standard_powerup_drops()
        self._puck_spawn_pos = self.map.get_flag_position(None)
        self._spawn_puck()

        defs = self.map.defs
        self._score_regions = []
        self._score_regions.append(
            bs.NodeActor(
                bs.newnode('region',
                           attrs={
                               'position': defs.boxes['goal1'][0:3],
                               'scale': defs.boxes['goal1'][6:9],
                               'type': 'box',
                               'materials': [self._score_region_material]
                           })))
        self._score_regions.append(
            bs.NodeActor(
                bs.newnode('region',
                           attrs={
                               'position': defs.boxes['goal2'][0:3],
                               'scale': defs.boxes['goal2'][6:9],
                               'type': 'box',
                               'materials': [self._score_region_material]
                           })))
        
        # ========== SCORE TEXT ON WALL ==========
        # Big title on wall - BSRUSH MATCH
        self._title_wall_text = bs.newnode(
            'text',
            attrs={
                'text': '⚽ BSRUSH MATCH ⚽',
                'in_world': True,
                'position': (0, 3.2, -5.8),
                'scale': 0.055,
                'shadow': 0.8,
                'color': (1, 0.85, 0.3),
                'h_align': 'center',
                'v_align': 'center'
            }
        )
        
        # Team names with VS in middle
        self._team_names_text = bs.newnode(
            'text',
            attrs={
                'text': 'TEAM 1     VS     TEAM 2',
                'in_world': True,
                'position': (0, 2.0, -5.8),
                'scale': 0.032,
                'shadow': 0.8,
                'color': (1, 1, 1),
                'h_align': 'center',
                'v_align': 'center'
            }
        )
        
        # Decorative line under team names
        self._line_wall_text = bs.newnode(
            'text',
            attrs={
                'text': '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
                'in_world': True,
                'position': (0, 1.75, -5.5),
                'scale': 0.028,
                'shadow': 0.5,
                'color': (0.7, 0.7, 0.7),
                'h_align': 'center',
                'v_align': 'center'
            }
        )
        
        # Score text (below the line)
        self._score_wall_text = bs.newnode(
            'text',
            attrs={
                'text': '0  -  0',
                'in_world': True,
                'position': (0, 1.45, -5.0),
                'scale': 0.045,
                'shadow': 0.8,
                'color': (1, 1, 0.5),
                'h_align': 'center',
                'v_align': 'center'
            }
        )
        
        # Add flags
        if self._flags_around_field:
            self._add_flags_around_field()
        
        self._update_scoreboard()
        self._update_score_wall()
        self._update_team_names()
        self._chant_sound.play()
    
    def _start_flag_effect(self, flag_node):
        """Start star effect on a flag for 5 seconds"""
        try:
            effect = StarEffectOnObject(flag_node, duration=5.0)
            effect.start()
            self._current_flag_effects.append(effect)
        except Exception:
            pass
    
    def _add_flags_around_field(self):
        """Add only 4 flags - close to the field (inside bounds)"""
        
        # Colors for flags
        red_color = (1, 0.2, 0.2)
        blue_color = (0.2, 0.2, 1)
        
        # ===== TWO FLAGS NEAR RIGHT GOAL =====
        right_flag_positions = [(11.5, -2.5), (11.5, 2.5)]
        for x, z in right_flag_positions:
            try:
                flag = Flag(position=(x, 1.2, z), touchable=False, color=red_color)
                self._flags.append(flag)
                self._right_flags.append(flag.node)
                light = bs.newnode('light',
                                   attrs={
                                       'position': (x, 1.8, z),
                                       'color': red_color,
                                       'radius': 0.4,
                                       'intensity': 0.25,
                                       'height_attenuated': True
                                   })
                self._flag_lights.append(light)
            except Exception:
                pass
        
        # ===== TWO FLAGS NEAR LEFT GOAL =====
        left_flag_positions = [(-11.5, -2.5), (-11.5, 2.5)]
        for x, z in left_flag_positions:
            try:
                flag = Flag(position=(x, 1.2, z), touchable=False, color=blue_color)
                self._flags.append(flag)
                self._left_flags.append(flag.node)
                light = bs.newnode('light',
                                   attrs={
                                       'position': (x, 1.8, z),
                                       'color': blue_color,
                                       'radius': 0.4,
                                       'intensity': 0.25,
                                       'height_attenuated': True
                                   })
                self._flag_lights.append(light)
            except Exception:
                pass
    
    def _update_score_wall(self):
        """Update the score text on the wall"""
        if hasattr(self, '_score_wall_text') and self._score_wall_text:
            score1 = self.teams[0].score if len(self.teams) > 0 else 0
            score2 = self.teams[1].score if len(self.teams) > 1 else 0
            self._score_wall_text.text = f'{score1}  -  {score2}'
    
    def _get_team_name_string(self, team_name):
        """Convert team name to string properly"""
        if team_name is None:
            return None
        if hasattr(team_name, 'evaluate'):
            return str(team_name.evaluate())
        return str(team_name)
    
    def _update_team_names(self):
        """Update team names on the wall with their colors"""
        if hasattr(self, '_team_names_text') and self._team_names_text and len(self.teams) >= 2:
            # Convert Lstr to string properly
            team1_name = self._get_team_name_string(self.teams[0].name)
            if team1_name is None:
                team1_name = "TEAM 1"
            
            team2_name = self._get_team_name_string(self.teams[1].name)
            if team2_name is None:
                team2_name = "TEAM 2"
            
            # Shorten names if too long
            if len(team1_name) > 12:
                team1_name = team1_name[:10] + ".."
            if len(team2_name) > 12:
                team2_name = team2_name[:10] + ".."
            self._team_names_text.text = f'{team1_name}     VS     {team2_name}'
    
    def _update_player_team_names(self):
        """Update team name text above each player"""
        for player in self.players:
            if player.actor and hasattr(player.actor, 'add_team_name_text'):
                team = player.team
                team_name = self._get_team_name_string(team.name)
                if team_name is None:
                    team_name = f"Team {team.id + 1}"
                player.actor.add_team_name_text(team_name, team.color)

    def on_team_join(self, team: Team) -> None:
        self._update_scoreboard()
        self._update_team_names()
        bs.timer(0.5, self._update_player_team_names)

    def _handle_puck_player_collide(self) -> None:
        collision = bs.getcollision()
        try:
            puck = collision.sourcenode.getdelegate(Puck, True)
            player = collision.opposingnode.getdelegate(PlayerSpaz,
                                                        True).getplayer(
                                                            Player, True)
        except bs.NotFoundError:
            return
        puck.last_players_to_touch[player.team.id] = player

    def _kill_puck(self) -> None:
        self._puck = None

    def _handle_score(self) -> None:
        """A point has been scored."""
        
        assert self._puck is not None
        assert self._score_regions is not None

        if self._puck.scored:
            return

        region = bs.getcollision().sourcenode
        index = 0
        for index, score_region in enumerate(self._score_regions):
            if region == score_region.node:
                break

        scoring_team = None
        scoring_player = None
        
        for team in self.teams:
            if team.id == index:
                scoring_team = team
                team.score += 1

                if (scoring_team.id in self._puck.last_players_to_touch
                        and self._puck.last_players_to_touch[scoring_team.id]):
                    scoring_player = self._puck.last_players_to_touch[scoring_team.id]
                    self.stats.player_scored(scoring_player, 100, big_message=True)

                for player in team.players:
                    if player.actor:
                        player.actor.handlemessage(bs.CelebrateMessage(2.0))

                if team.score >= self._score_to_win:
                    self.end_game()

        self._foghorn_sound.play()
        self._cheer_sound.play()

        self._puck.scored = True
        
        # Update score on wall
        self._update_score_wall()
        
        # ===== ADD STAR EFFECT ON FLAGS OF THE SCORING TEAM FOR 5 SECONDS =====
        if scoring_team:
            if scoring_team.id == 0:  # Left team scored - effect on left flags
                for flag_node in self._left_flags:
                    if flag_node and flag_node.exists():
                        self._start_flag_effect(flag_node)
            else:  # Right team scored - effect on right flags
                for flag_node in self._right_flags:
                    if flag_node and flag_node.exists():
                        self._start_flag_effect(flag_node)

        # ========== GOAL EFFECT ==========
        goal_pos = self._score_regions[index].node.position
        
        # Dimmer light at goal
        goal_light = bs.newnode('light',
                                attrs={
                                    'position': goal_pos,
                                    'height_attenuated': False,
                                    'color': scoring_team.color if scoring_team else (1, 1, 0),
                                    'radius': 1.2,
                                    'intensity': 0.8
                                })
        bs.animate(goal_light, 'intensity', {0: 0, 0.1: 1.0, 0.3: 0.8, 4.5: 0.4, 5.0: 0}, loop=False)
        bs.animate(goal_light, 'radius', {0: 0.3, 0.3: 1.2, 4.5: 1.5, 5.0: 0}, loop=False)
        bs.timer(5.0, goal_light.delete)
        
        # Particles from goal
        for i in range(25):
            delay = i * 0.08
            bs.timer(delay, lambda: self._emit_goal_particle(goal_pos, scoring_team.color if scoring_team else (1, 1, 0)))
        
        # BIG "GOAL!" TEXT
        goal_text = bs.newnode('text',
                               attrs={
                                   'text': 'GOAL!',
                                   'scale': 2.5,
                                   'position': (0, 180),
                                   'h_align': 'center',
                                   'v_attach': 'bottom',
                                   'color': (1, 1, 0),
                                   'shadow': 0.5,
                                   'flatness': 0.5,
                                   'vr_depth': 400
                               })
        bs.animate(goal_text, 'scale', {0: 0.5, 0.2: 2.5, 0.5: 2.5, 4.5: 2.0, 5.0: 0}, loop=False)
        bs.animate(goal_text, 'opacity', {0: 0, 0.2: 1, 4.5: 0.8, 5.0: 0}, loop=False)
        bs.timer(5.0, goal_text.delete)
        
        # ========== DARK MAGIC EFFECT on scorer ==========
        if scoring_player and scoring_player.actor and scoring_player.actor.node:
            dark_magic = DarkMagicEffect(scoring_player.actor)
            dark_magic.start()
            
            def stop_dark_magic():
                if dark_magic:
                    dark_magic.stop()
            bs.timer(5.0, stop_dark_magic)

        bs.timer(1.0, self._kill_puck)
        bs.cameraflash(duration=5.0)
        self._update_scoreboard()
    
    def _emit_goal_particle(self, pos: Sequence[float], color: Sequence[float]) -> None:
        """Emit a particle from goal position."""
        if not self.has_ended():
            vel = (random.uniform(-3, 3), random.uniform(3, 8), random.uniform(-3, 3))
            bs.emitfx(position=pos,
                      velocity=vel,
                      count=1,
                      scale=0.5,
                      spread=0.6,
                      chunk_type='spark')

    def end_game(self) -> None:
        # Clean up flag effects
        for effect in self._current_flag_effects:
            effect.stop()
        self._current_flag_effects = []
        
        # Clean up flags and lights
        for flag in self._flags:
            try:
                if flag and flag.node:
                    flag.node.delete()
            except Exception:
                pass
        self._flags = []
        
        for light in self._flag_lights:
            try:
                if light:
                    light.delete()
            except Exception:
                pass
        self._flag_lights = []
        
        # Clean up wall texts
        if hasattr(self, '_score_wall_text') and self._score_wall_text:
            self._score_wall_text.delete()
        if hasattr(self, '_title_wall_text') and self._title_wall_text:
            self._title_wall_text.delete()
        if hasattr(self, '_line_wall_text') and self._line_wall_text:
            self._line_wall_text.delete()
        if hasattr(self, '_team_names_text') and self._team_names_text:
            self._team_names_text.delete()
        
        results = bs.GameResults()
        for team in self.teams:
            results.set_team_score(team, team.score)
        self.end(results=results)

    def _update_scoreboard(self) -> None:
        winscore = self._score_to_win
        for team in self.teams:
            self._scoreboard.set_team_value(team, team.score, winscore)

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.PlayerDiedMessage):
            super().handlemessage(msg)
            self.respawn_player(msg.getplayer(Player))
        elif isinstance(msg, PuckDiedMessage):
            if not self.has_ended():
                bs.timer(3.0, self._spawn_puck)
        else:
            super().handlemessage(msg)

    def _flash_puck_spawn(self) -> None:
        light = bs.newnode('light',
                           attrs={
                               'position': self._puck_spawn_pos,
                               'height_attenuated': False,
                               'color': (1, 0.5, 0),
                               'radius': 0.8,
                               'intensity': 0.5
                           })
        bs.animate(light, 'intensity', {0.0: 0, 0.25: 0.6, 0.5: 0}, loop=True)
        bs.timer(1.0, light.delete)

    def spawn_player(self, player: Player) -> bs.Actor:
        from babase import _math
        from bascenev1._gameutils import animate
        from bascenev1._coopsession import CoopSession

        if isinstance(self.session, bs.DualTeamSession):
            position = self.map.get_start_position(player.team.id)
        else:
            position = self.map.get_ffa_start_position(self.players)
        angle = None

        name = player.getname()
        color = player.color
        highlight = player.highlight

        light_color = _math.normalized_color(color)
        display_color = babase.safecolor(color, target_intensity=0.75)

        # Always use CustomPlayerSpaz to have add_team_name_text method
        spaz = CustomPlayerSpaz(color=color,
                                highlight=highlight,
                                character=player.character,
                                player=player)

        player.actor = spaz
        assert spaz.node

        if isinstance(self.session, CoopSession) and self.map.getname() in [
                'Courtyard', 'Tower D'
        ]:
            mat = self.map.preloaddata['collide_with_wall_material']
            assert isinstance(spaz.node.materials, tuple)
            assert isinstance(spaz.node.roller_materials, tuple)
            spaz.node.materials += (mat, )
            spaz.node.roller_materials += (mat, )

        spaz.node.name = name
        spaz.node.name_color = display_color
        
        # NORMAL SPEED (no hockey speed boost) - enable_run=False
        spaz.connect_controls_to_player(enable_bomb=False, enable_pickup=True, enable_run=True)

        if self._boxing_gloves:
            spaz.equip_boxing_gloves()

        spaz.handlemessage(
            bs.StandMessage(
                position,
                angle if angle is not None else random.uniform(0, 360)))
        self._spawn_sound.play(1, position=spaz.node.position)
        light = bs.newnode('light', attrs={'color': light_color})
        spaz.node.connectattr('position', light, 'position')
        animate(light, 'intensity', {0: 0, 0.25: 1, 0.5: 0})
        bs.timer(0.5, light.delete)
        
        # Add team name above player
        team_name = self._get_team_name_string(player.team.name)
        if team_name is None:
            team_name = f"Team {player.team.id + 1}"
        spaz.add_team_name_text(team_name, player.team.color)
        
        return spaz

    def _spawn_puck(self) -> None:
        self._swipsound.play()
        self._whistle_sound.play()
        self._flash_puck_spawn()
        assert self._puck_spawn_pos is not None
        self._puck = Puck(position=self._puck_spawn_pos)
