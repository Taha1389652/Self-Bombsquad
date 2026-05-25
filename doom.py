# ba_meta require api 9

from __future__ import annotations

from typing import TYPE_CHECKING
import random
import math
import time
import babase
import bascenev1 as bs
from bascenev1 import _map
from bascenev1lib.gameutils import SharedObjects
from bascenev1lib.actor.bomb import Blast, Bomb
from bascenev1lib.actor.playerspaz import PlayerSpaz
from bascenev1lib.actor.scoreboard import Scoreboard
from bascenev1lib.actor.spazfactory import SpazFactory
from bascenev1lib.actor.spazbot import SpazBotSet, StickyBot

if TYPE_CHECKING:
    from typing import Any, Dict, Sequence, Optional


# ========== متن‌های داستانی ==========
BOSS_QUOTES = {
    'spawn': ["Man arbabe tariki hastam", "Be jahanam khosh amadid", "Rouhetan mahkome be azab ast", "Marg bar zendegan"],
    'attack': ["Taame marg ra bechashid", "Khakestar khahid shod", "Naboodi hatmiasat", "Jahannam dar entezare shomast"],
    'spawn_bot': ["Sarbazane jahannam barkhizid", "Anhara dar ham beshkanid", "Janetan ra nabood konid", "Ghtele am aghaz shavad"],
    'death': ["Man bar migardam", "Nahayat payan nist", "Doobareh khahid did"],
    'low_health': ["Nazdike ast margetan ra his mikonam", "Akharin nafashetan ra bekeshid", "Payane kar nazdikast"],
    'rage': ["Kheshme man bi payan ast", "Jahannam azad mishavad", "Tamame nirouyam ra bekar migiram", "Biaid bebinim chi kasi zende mimanad"]
}

BOT_QUOTES = [
    "Naboodetan mikonam", "Farar fayde nadarad", "Marg bar shoma",
    "Jahannam dar entezar ast", "Khakestar khahid shod", "Taame naboodi ra bechashid"
]

WIN_QUOTES = [
    "Man pirooz shodam", "Shokaste shoma ghati bod", "Ghodrate man shekast napazir ast", "Hala bebinid chi kasi ghodratmand ast"
]

LOSE_QUOTES = [
    "Shekast khordim", "Nirooyam tamam shod", "Dafe bad mibarim", "Baz ham bar migardim"
]


class ScreenMessage:
    _last_message_time = 0
    
    def __init__(self, text: str, sender: str = "Skeleton King", color=(1, 0.3, 0), duration=3.0):
        current_time = time.time()
        if current_time - ScreenMessage._last_message_time < 3.0:
            return
        ScreenMessage._last_message_time = current_time
        full_text = f"{sender}: {text}"
        bs.screenmessage(babase.Lstr(value=full_text), color=color)


class FloatingText:
    _last_quote_time = {}
    
    def __init__(self, text: str, node, color=(1, 1, 1), duration=2.0, y_offset=1.5, owner_id=None):
        self.node = node
        self.duration = duration
        
        if owner_id:
            now = time.time()
            if owner_id in FloatingText._last_quote_time and now - FloatingText._last_quote_time[owner_id] < 3.0:
                return
            FloatingText._last_quote_time[owner_id] = now
        
        try:
            if not node or not node.exists():
                return
            pos = node.position
            self.text_node = bs.newnode('text',
                                        attrs={
                                            'text': text,
                                            'in_world': True,
                                            'shadow': 1.0,
                                            'flatness': 1.0,
                                            'scale': 0.025,
                                            'h_align': 'center',
                                            'color': color,
                                            'position': (pos[0], pos[1] + y_offset, pos[2])
                                        })
            bs.animate(self.text_node, 'scale', {0: 0.02, 0.15: 0.028, duration: 0.02})
            bs.animate(self.text_node, 'opacity', {0: 0, 0.15: 1, duration: 0})
            def move_up():
                if self.text_node and self.text_node.exists():
                    p = self.text_node.position
                    self.text_node.position = (p[0], p[1] + 0.02, p[2])
            self.move_timer = bs.Timer(0.03, move_up, repeat=True)
            bs.timer(duration, self._cleanup)
        except Exception:
            pass
    
    def _cleanup(self):
        if hasattr(self, 'move_timer') and self.move_timer:
            self.move_timer = None
        if self.text_node and self.text_node.exists():
            self.text_node.delete()


# بات با کاراکتر B-9000 و رنگ سفید
class WhiteBot(StickyBot):
    character = 'B-9000'
    default_bomb_type = 'impact'
    color = (1, 1, 1)
    highlight = (1, 1, 1)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, 'node') and self.node:
            self.node.name = ''
            self.node.color = (1, 1, 1)
            self.node.highlight = (1, 1, 1)
        if random.random() < 0.35 and hasattr(self, 'node') and self.node:
            quote = random.choice(BOT_QUOTES)
            bs.timer(0.5, lambda: FloatingText(quote, self.node, color=(1, 1, 1), duration=2.0, y_offset=1.5, owner_id=f"bot_{id(self)}"))
    
    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.DieMessage):
            if random.random() < 0.3 and hasattr(self, 'node') and self.node:
                quote = random.choice(["Nabood shodam", "Af..."])
                FloatingText(quote, self.node, color=(0.8, 0.2, 0.2), duration=1.2, y_offset=1.3)
        return super().handlemessage(msg)


class BombDarkMagicEffect:
    def __init__(self, bomb_node):
        self.bomb_node = bomb_node
        self.active = True
        self.timer = None
        self.nodes = []

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
        if not self.active or not self.bomb_node or not self.bomb_node.exists():
            self.stop()
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
            bpos = self.bomb_node.position
            c = 0.6
            pos_list = [
                (c, 0, 0), (0, 0, c), (-c, 0, 0), (0, 0, -c),
                (c*0.8, 0, c*0.8), (-c*0.8, 0, -c*0.8),
                (c*0.8, 0, -c*0.8), (-c*0.8, 0, c*0.8),
            ]
            for p in pos_list:
                pos = (bpos[0] + p[0], bpos[1] + p[1] + 0.15, bpos[2] + p[2])
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
                    attrs={
                        'body': 'sphere',
                        'position': pos,
                        'velocity': (random.uniform(-0.5, 0.5), random.uniform(1.0, 2.0), random.uniform(-0.5, 0.5)),
                        'mesh': mesh,
                        'mesh_scale': 0.25,
                        'body_scale': 0.0,
                        'shadow_size': 0.0,
                        'gravity_scale': 0.2,
                        'color_texture': tex,
                        'reflection': 'soft',
                        'reflection_scale': [0.0],
                        'materials': [mat]
                    })
                light = bs.newnode('light',
                    owner=node,
                    attrs={
                        'intensity': 1.0,
                        'volume_intensity_scale': 0.4,
                        'color': (0.8, 0.2, 1.0),
                        'radius': 0.06
                    })
                node.connectattr('position', light, 'position')
                self.nodes.append(node)
                bs.timer(0.2, lambda n=node: die(n))
        except Exception:
            pass
        if self.active and self.bomb_node and self.bomb_node.exists():
            self.timer = bs.timer(0.15, self.create_darkmagic)

    def stop(self):
        self.active = False
        for node in self.nodes:
            if node and node.exists():
                try:
                    node.delete()
                except:
                    pass
        self.nodes.clear()
        if self.timer:
            self.timer = None


# پلیر سفارشی با بمب ایمپکت
class CustomPlayerSpaz(PlayerSpaz):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_bomb_type = 'impact'
        self.bomb_type = 'impact'
        self.bomb_type_default = 'impact'


class SkeletonBoss(bs.Actor):
    def __init__(self, position: Sequence[float] = (0.29, 7.5, -7.5), hitpoints: int = 1000, player_count: int = 0):
        super().__init__()
        shared = SharedObjects.get()

        self.hitpoints = hitpoints
        self.hitpoints_max = hitpoints
        self.position = position
        self.attack_timer: Optional[bs.Timer] = None
        self.update_timer: Optional[bs.Timer] = None
        self.bot_timer: Optional[bs.Timer] = None
        self.effects_timer: Optional[bs.Timer] = None
        self.talk_timer: Optional[bs.Timer] = None
        self.is_alive = True
        self._player_pts: list[tuple[bs.Vec3, bs.Vec3]] | None = None
        self._low_health_triggered = False
        self._rage_mode = False
        self._rage_effect_timer: Optional[bs.Timer] = None
        self._player_count = max(1, player_count)
        self._rage_active = False
        
        self._bots = SpazBotSet()
        # محاسبه تعداد بات: بر اساس تعداد بازیکنان (حداقل 2، حداکثر 6)
        self.bot_count = max(2, min(6, self._player_count + 1))
        self._spawn_points = []

        self.boss_material = bs.Material()
        self.boss_material.add_actions(
            conditions=('they_have_material', shared.player_material),
            actions=(('modify_node_collision', 'collide', True),
                     ('modify_part_collision', 'physical', True)))

        self.node = bs.newnode('prop',
                               delegate=self,
                               attrs={
                                   'position': position,
                                   'mesh': bs.getmesh('bonesHead'),
                                   'color_texture': bs.gettexture('bonesColor'),
                                   'mesh_scale': 5.7,
                                   'body': 'sphere',
                                   'body_scale': 4.0,
                                   'gravity_scale': 0.0,
                                   'velocity': (0, 0, 0),
                                   'damping': 999999,
                                   'density': 999999,
                                   'shadow_size': 0.8,
                                   'reflection': 'soft',
                                   'reflection_scale': [0.2],
                                   'is_area_of_interest': True,
                                   'materials': [self.boss_material, shared.object_material, shared.footing_material]
                               })

        self.boss_name_shadow = bs.newnode('text',
                                           owner=self.node,
                                           attrs={
                                               'text': 'SKELETON KING',
                                               'in_world': True,
                                               'shadow': 1.0,
                                               'flatness': 1.0,
                                               'scale': 0.03,
                                               'h_align': 'center',
                                               'color': (0, 0, 0),
                                               'position': (position[0], position[1] + 1.8, position[2])
                                           })

        self.boss_name_text = bs.newnode('text',
                                         owner=self.node,
                                         attrs={
                                             'text': 'SKELETON KING',
                                             'in_world': True,
                                             'shadow': 1.0,
                                             'flatness': 1.0,
                                             'scale': 0.03,
                                             'h_align': 'center',
                                             'color': (1, 0.2, 0.2),
                                             'position': (position[0], position[1] + 1.85, position[2])
                                         })

        def animate_boss_color():
            if self.boss_name_text and self.boss_name_text.exists():
                colors = [(1, 0.2, 0.2), (1, 0.5, 0), (1, 0.8, 0), (1, 0.5, 0)]
                for i, col in enumerate(colors):
                    bs.timer(i * 0.3, lambda c=col: self._set_boss_color(c))
        self._boss_color_timer = bs.Timer(0.3, animate_boss_color, repeat=True)

        def update_text_position():
            if self.node and self.node.exists() and self.boss_name_text and self.boss_name_shadow:
                pos = self.node.position
                self.boss_name_shadow.position = (pos[0], pos[1] + 1.8, pos[2])
                self.boss_name_text.position = (pos[0], pos[1] + 1.85, pos[2])
        self.position_update_timer = bs.Timer(0.05, update_text_position, repeat=True)

        def lock_position():
            if self.node and self.node.exists() and self.is_alive:
                self.node.position = self.position
                self.node.velocity = (0, 0, 0)
        self.position_lock = bs.Timer(0.1, lock_position, repeat=True)

        self._width = 240
        self._width_max = 240
        self._height = 55
        self._bar_width = 240
        self._bar_height = 35
        self._bar_tex = self._backing_tex = bs.gettexture('bar')
        self._cover_tex = bs.gettexture('uiAtlas')
        self._mesh = bs.getmesh('meterTransparent')
        self.bar_posx = -120

        self._backing = bs.NodeActor(
            bs.newnode('image', attrs={
                'position': (self.bar_posx + self._width / 2, -100),
                'scale': (self._width, self._height),
                'opacity': 0.7,
                'color': (0.3, 0.3, 0.3),
                'vr_depth': -3,
                'attach': 'topCenter',
                'texture': self._backing_tex
            }))

        self._bar = bs.NodeActor(
            bs.newnode('image', attrs={
                'opacity': 1.0,
                'color': (0.8, 0.2, 0.2),
                'attach': 'topCenter',
                'texture': self._bar_tex
            }))

        self._bar_scale = bs.newnode('combine', owner=self._bar.node, attrs={'size': 2, 'input0': self._bar_width, 'input1': self._bar_height})
        self._bar_scale.connectattr('output', self._bar.node, 'scale')

        self._bar_position = bs.newnode('combine', owner=self._bar.node, attrs={'size': 2, 'input0': self.bar_posx + self._bar_width / 2, 'input1': -100})
        self._bar_position.connectattr('output', self._bar.node, 'position')

        self._cover = bs.NodeActor(
            bs.newnode('image', attrs={
                'position': (self.bar_posx + 120, -100),
                'scale': (self._width * 1.15, self._height * 1.6),
                'opacity': 1.0,
                'color': (0.3, 0.3, 0.3),
                'vr_depth': 2,
                'attach': 'topCenter',
                'texture': self._cover_tex,
                'mesh_transparent': self._mesh
            }))

        self._title_text = bs.NodeActor(
            bs.newnode('text', attrs={
                'position': (self.bar_posx + 120, -80),
                'h_attach': 'center',
                'v_attach': 'top',
                'h_align': 'center',
                'v_align': 'center',
                'maxwidth': 130,
                'scale': 0.65,
                'text': 'SKELETON KING',
                'shadow': 0.5,
                'flatness': 1.0,
                'color': (1, 0.5, 0, 0.9)
            }))

        self._score_text = bs.NodeActor(
            bs.newnode('text', attrs={
                'position': (self.bar_posx + 120, -105),
                'h_attach': 'center',
                'v_attach': 'top',
                'h_align': 'center',
                'v_align': 'center',
                'maxwidth': 130,
                'scale': 0.9,
                'text': str(self.hitpoints),
                'shadow': 0.5,
                'flatness': 1.0,
                'color': (1, 1, 1, 0.8)
            }))

        bs.timer(1.0, self._say_spawn_quote)
        self.start_attacking()
        self.start_update()
        self.start_player_tracking()
        self.collect_spawn_points()
        self.start_spawning_bots()
        self.start_effects()
        self.start_talking()
    
    def _set_boss_color(self, color):
        if self.boss_name_text and self.boss_name_text.exists():
            self.boss_name_text.color = color
    
    def _create_rage_effect(self):
        if not self.node or not self.node.exists():
            return
        
        pos = self.node.position
        
        for _ in range(12):
            angle = random.uniform(0, 2 * math.pi)
            rad = random.uniform(2.5, 5.0)
            x = pos[0] + math.cos(angle) * rad
            z = pos[2] + math.sin(angle) * rad
            
            tex = bs.gettexture('impactBombColor')
            mesh = bs.getmesh('impactBomb')
            
            node = bs.newnode('prop',
                attrs={
                    'body': 'sphere',
                    'position': (x, pos[1] + random.uniform(0.5, 4.0), z),
                    'velocity': (random.uniform(-3, 3), random.uniform(4, 10), random.uniform(-3, 3)),
                    'mesh': mesh,
                    'mesh_scale': 0.6,
                    'body_scale': 0.0,
                    'shadow_size': 0.0,
                    'gravity_scale': 0.12,
                    'color_texture': tex,
                    'reflection': 'soft',
                    'reflection_scale': [0.0]
                })
            
            light = bs.newnode('light',
                owner=node,
                attrs={
                    'intensity': 2.0,
                    'color': (1.5, 0.4, 1.5),
                    'radius': 0.28
                })
            node.connectattr('position', light, 'position')
            
            node2 = bs.newnode('prop',
                attrs={
                    'body': 'sphere',
                    'position': (x + random.uniform(-1.0, 1.0), 
                                pos[1] + random.uniform(0.5, 3.5), 
                                z + random.uniform(-1.0, 1.0)),
                    'velocity': (random.uniform(-2.5, 2.5), random.uniform(3, 8), random.uniform(-2.5, 2.5)),
                    'mesh': mesh,
                    'mesh_scale': 0.4,
                    'body_scale': 0.0,
                    'shadow_size': 0.0,
                    'gravity_scale': 0.18,
                    'color_texture': tex,
                    'reflection': 'soft',
                    'reflection_scale': [0.0]
                })
            
            light2 = bs.newnode('light',
                owner=node2,
                attrs={
                    'intensity': 1.3,
                    'color': (1.2, 0.3, 1.2),
                    'radius': 0.16
                })
            node2.connectattr('position', light2, 'position')
            
            bs.timer(1.0, node.delete)
            bs.timer(1.0, node2.delete)
    
    def _activate_rage_mode(self):
        if self._rage_mode:
            return
        self._rage_mode = True
        quote = random.choice(BOSS_QUOTES['rage'])
        ScreenMessage(quote, "Skeleton King", color=(1, 0.2, 0), duration=3.0)
        self._bar.node.color = (1, 0.1, 0.1)
        
        # افزایش تعداد بات در حالت خشم
        self.bot_count = min(6, self.bot_count + 1)
        
        def rage_effect():
            if self._rage_mode and self.is_alive:
                self._create_rage_effect()
        
        self._rage_effect_timer = bs.Timer(0.2, rage_effect, repeat=True)
        self._play_rage_sound()
    
    def _remove_rage_effect(self):
        if self._rage_effect_timer:
            self._rage_effect_timer = None
    
    def _play_rage_sound(self):
        try:
            sound = bs.getsound('metalHit')
            sound.play(position=self.node.position, volume=1.0)
        except:
            pass
    
    def _say_spawn_quote(self):
        if self.is_alive:
            quote = random.choice(BOSS_QUOTES['spawn'])
            ScreenMessage(quote, "Skeleton King", color=(1, 0.3, 0), duration=3.0)
    
    def _say_attack_quote(self):
        if self.is_alive and random.random() < 0.4:
            if self._rage_mode:
                quote = random.choice(BOSS_QUOTES['rage'])
            else:
                quote = random.choice(BOSS_QUOTES['attack'])
            ScreenMessage(quote, "Skeleton King", color=(1, 0.5, 0), duration=2.5)
    
    def _say_spawn_bot_quote(self):
        if self.is_alive:
            quote = random.choice(BOSS_QUOTES['spawn_bot'])
            ScreenMessage(quote, "Skeleton King", color=(1, 0.3, 0), duration=2.5)
    
    def _say_low_health_quote(self):
        if self.is_alive and not self._low_health_triggered:
            self._low_health_triggered = True
            quote = random.choice(BOSS_QUOTES['low_health'])
            ScreenMessage(quote, "Skeleton King", color=(1, 0.2, 0), duration=3.0)
    
    def _say_win_quote(self):
        quote = random.choice(WIN_QUOTES)
        ScreenMessage(quote, "Skeleton King", color=(1, 0.5, 0), duration=3.0)
    
    def _say_lose_quote(self):
        quote = random.choice(LOSE_QUOTES)
        ScreenMessage(quote, "Skeleton King", color=(1, 0.2, 0.2), duration=3.0)
    
    def start_talking(self):
        def say_random_quote():
            if self.is_alive and self.node and self.node.exists():
                if self._rage_mode:
                    quote = random.choice(BOSS_QUOTES['rage'])
                else:
                    quote = random.choice(BOSS_QUOTES['attack'])
                ScreenMessage(quote, "Skeleton King", color=(1, 0.4, 0), duration=2.5)
        self.talk_timer = bs.Timer(10.0, say_random_quote, repeat=True)

    def collect_spawn_points(self):
        activity = bs.getactivity()
        if activity and hasattr(activity.map, 'defs'):
            map_defs = activity.map.defs
            if hasattr(map_defs, 'points'):
                for key, value in map_defs.points.items():
                    if key.startswith('spawn') or key.startswith('ffa_spawn'):
                        if len(value) >= 3:
                            pos = (value[0], value[1], value[2])
                            if pos not in self._spawn_points:
                                self._spawn_points.append(pos)
        
        if len(self._spawn_points) == 0:
            self._spawn_points = [
                (-4.745706238, 5.051501304, -4.247934288),
                (5.838590388, 5.051501304, -4.259627405),
                (0.5006944438, 5.051501304, -5.79356326),
                (0.5006944438, 5.051501304, -2.435321368),
                (7.941690444946289, -4.203672409057617, -10.778594017028809),
                (-7.941690444946289, -4.203672409057617, -10.778594017028809)
            ]

    def start_player_tracking(self):
        self.player_track_timer = bs.Timer(0.1, self._update_player_points, repeat=True)

    def _update_player_points(self):
        activity = bs.getactivity()
        if not activity or not self.is_alive:
            return
        player_pts = []
        for player in activity.players:
            if player.is_alive() and player.actor and player.actor.node:
                player_pts.append((
                    bs.Vec3(player.actor.node.position),
                    bs.Vec3(player.actor.node.velocity)
                ))
        self._player_pts = player_pts

    def _get_closest_player(self):
        if not self.node or not self._player_pts:
            return None, None
        botpt = bs.Vec3(self.node.position)
        closest_dist = None
        closest_pt = None
        for plpt, _ in self._player_pts:
            dist = (plpt - botpt).length()
            if (closest_dist is None or dist < closest_dist) and (plpt[1] > botpt[1] - 5.0):
                closest_dist = dist
                closest_pt = plpt
        return closest_pt, closest_dist

    def start_attacking(self):
        self.attack_timer = bs.Timer(self._get_attack_interval(), self.attack, repeat=True)

    def _get_attack_interval(self):
        if self._rage_mode:
            return 1.5
        return 3.0

    def start_spawning_bots(self):
        self.bot_timer = bs.Timer(self._get_spawn_interval(), self._drop_bots, repeat=True)

    def _get_spawn_interval(self):
        if self._rage_mode:
            return 5.0
        return 8.0

    def _drop_bots(self):
        """اسپاون بات بر اساس تعداد تعیین شده (با توجه به تعداد بازیکنان)"""
        if not self.is_alive or not self.node or len(self._spawn_points) < self.bot_count:
            return
        self._say_spawn_bot_quote()
        
        # انتخاب نقاط اسپاون
        selected = random.sample(self._spawn_points, min(self.bot_count, len(self._spawn_points)))
        
        for i, spawn_pos in enumerate(selected):
            y_pos = spawn_pos[1] + 0.8
            bs.timer(i * 0.3, lambda pos=spawn_pos, y=y_pos: self._bots.spawn_bot(
                WhiteBot, pos=(pos[0], y, pos[2]), spawn_time=0.0))

    def start_update(self):
        self.update_timer = bs.Timer(0.1, self._update_health_bar, repeat=True)

    def _update_health_bar(self):
        if not self.is_alive:
            return
        self.hitpoints = max(0, self.hitpoints)
        self._score_text.node.text = str(self.hitpoints)
        self._bar_width = self.hitpoints * self._width_max / self.hitpoints_max
        cur_width = self._bar_scale.input0
        bs.animate(self._bar_scale, 'input0', {0.0: cur_width, 0.1: self._bar_width})
        cur_x = self._bar_position.input0
        bs.animate(self._bar_position, 'input0', {0.0: cur_x, 0.1: self.bar_posx + self._bar_width / 2})

        hp_percent = self.hitpoints / self.hitpoints_max
        
        if hp_percent <= 0.3 and not self._rage_mode:
            self._activate_rage_mode()
            if self.attack_timer:
                self.attack_timer = None
            if self.bot_timer:
                self.bot_timer = None
            self.start_attacking()
            self.start_spawning_bots()
        
        if hp_percent < 0.2 and not self._low_health_triggered:
            self._say_low_health_quote()
            self._low_health_triggered = True

        if self.hitpoints <= 0:
            self.is_alive = False
            self.handlemessage(bs.DieMessage())

    def attack(self):
        if not self.is_alive or not self.node:
            return
        target_pt, _ = self._get_closest_player()
        if target_pt is None:
            return
        self._say_attack_quote()
        p = self.node.position
        bomb_count = 2 if self._rage_mode else 1
        for b in range(bomb_count):
            if b == 1:
                dx = random.uniform(-0.8, 0.8)
                dz = random.uniform(-0.8, 0.8)
            else:
                dx = target_pt[0] - p[0]
                dz = target_pt[2] - p[2]
                dist = (dx**2 + dz**2)**0.5
                if dist > 0:
                    dx /= dist
                    dz /= dist
            bomb_pos = (p[0] + random.uniform(-0.5, 0.5), p[1] - 1.5, p[2] + random.uniform(-0.5, 0.5))
            bomb_vel = (dx * 15, 3 + random.uniform(-0.5, 0.5), dz * 15)
            bomb = Bomb(position=bomb_pos, velocity=bomb_vel, bomb_type='impact')
            bomb.autoretain()
            dark_effect = BombDarkMagicEffect(bomb.node)
            dark_effect.start()
        bs.emitfx(position=(p[0], p[1] - 1, p[2]), count=12, scale=1.5, spread=0.6, chunk_type='spark')

    def start_effects(self):
        def sparks():
            if self.is_alive and self.node and self.node.exists():
                count = random.randint(30, 60) if self._rage_mode else random.randint(20, 40)
                scale = random.uniform(2, 3) if self._rage_mode else random.uniform(1.5, 2.5)
                bs.emitfx(position=self.node.position, count=count, scale=scale,
                          spread=random.uniform(2, 3) if self._rage_mode else random.uniform(1.5, 2.5),
                          chunk_type='spark')
        
        def explosions():
            if self.is_alive and self.node and self.node.exists():
                bs.newnode('explosion', attrs={
                    'position': self.node.position,
                    'color': (random.uniform(0.8, 1), random.uniform(0.3, 0.6), random.uniform(0, 0.3)),
                    'radius': random.uniform(2.5, 3.5) if self._rage_mode else random.uniform(2.0, 3.0)
                })
        self.spark_timer = bs.Timer(0.12, sparks, repeat=True)
        self.explosion_timer = bs.Timer(0.4, explosions, repeat=True)

    def stop_effects(self):
        if hasattr(self, 'spark_timer') and self.spark_timer:
            self.spark_timer = None
        if hasattr(self, 'explosion_timer') and self.explosion_timer:
            self.explosion_timer = None

    def do_damage(self, damage: int):
        if not self.is_alive:
            return
        self.hitpoints -= damage
        if self.node:
            count = 35 if self._rage_mode else 25
            bs.emitfx(position=self.node.position, count=count, scale=2.2, spread=1.8, chunk_type='spark')

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.DieMessage):
            self.is_alive = False
            quote = random.choice(BOSS_QUOTES['death'])
            ScreenMessage(quote, "Skeleton King", color=(1, 0.2, 0.2), duration=3.0)
            if self.attack_timer:
                self.attack_timer = None
            if self.update_timer:
                self.update_timer = None
            if self.bot_timer:
                self.bot_timer = None
            if self.talk_timer:
                self.talk_timer = None
            if self.position_lock:
                self.position_lock = None
            if self.player_track_timer:
                self.player_track_timer = None
            if self._boss_color_timer:
                self._boss_color_timer = None
            if self.position_update_timer:
                self.position_update_timer = None
            if self._rage_effect_timer:
                self._rage_effect_timer = None
            self.stop_effects()
            if self.node:
                pos = self.node.position
                for i in range(15):
                    bs.timer(i * 0.1, lambda p=pos: Blast(position=p, blast_radius=4.5).autoretain())
                bs.emitfx(position=pos, count=150, scale=4.5, spread=4, chunk_type='spark')
                self.node.delete()
            if self.boss_name_text:
                self.boss_name_text.delete()
            if self.boss_name_shadow:
                self.boss_name_shadow.delete()
            if hasattr(self, '_backing') and self._backing:
                self._backing.node.delete()
            if hasattr(self, '_bar') and self._bar:
                self._bar.node.delete()
            if hasattr(self, '_cover') and self._cover:
                self._cover.node.delete()
            if hasattr(self, '_title_text') and self._title_text:
                self._title_text.node.delete()
            if hasattr(self, '_score_text') and self._score_text:
                self._score_text.node.delete()
        elif isinstance(msg, bs.HitMessage):
            damage = int(abs(msg.magnitude) / 15)
            if damage < 3:
                damage = 3
            if damage > 15:
                damage = 15
            self.do_damage(damage)
        elif isinstance(msg, bs.OutOfBoundsMessage):
            if self.node and self.node.exists():
                self.node.position = self.position
                self.node.velocity = (0, 0, 0)
        else:
            super().handlemessage(msg)


class FadeEffect():
    def __init__(self, map_tint=(1, 1, 1)):
        gnode = bs.getactivity().globalsnode
        bs.animate_array(gnode, 'tint', 3, {0: (0, 0, 0), 1.5: map_tint})
        text = bs.newnode('text', attrs={
            'position': (0, 250), 'text': 'Loading...', 'color': (1, 0, 0),
            'h_align': 'center', 'v_align': 'center', 'vr_depth': 410,
            'maxwidth': 600, 'shadow': 1.0, 'flatness': 1.0,
            'scale': 2.5, 'h_attach': 'center', 'v_attach': 'bottom', 'big': True
        })
        bs.animate(text, 'opacity', {0: 0, 0.2: 1, 0.4: 1, 2: 0})
        bs.timer(2.5, text.delete)
        text = bs.newnode('text', attrs={
            'position': (0, 270), 'text': 'BSLIFE PRESENT', 'color': (1, 0.55, 0),
            'h_align': 'center', 'v_align': 'center', 'vr_depth': 410,
            'maxwidth': 600, 'shadow': 1.0, 'flatness': 1.0,
            'scale': 2.5, 'h_attach': 'center', 'v_attach': 'bottom'
        })
        bs.animate(text, 'opacity', {0: 0, 0.2: 1, 0.4: 1, 2: 0})
        bs.timer(2.5, text.delete)


class Player(bs.Player['Team']):
    pass


class Team(bs.Team[Player]):
    def __init__(self) -> None:
        self.score = 0


# ba_meta export bascenev1.GameActivity
class DoomBossFightGame(bs.TeamGameActivity[Player, Team]):
    name = 'Doom Island'
    description = 'Defeat the Skeleton King!\nBSLIFE PRESENT'

    @classmethod
    def get_available_settings(cls, sessiontype: type[bs.Session]) -> list:
        return [
            bs.IntSetting('Boss Health', min_value=100, default=1000, increment=50),
            bs.IntChoiceSetting('Time Limit', choices=[('None', 0), ('5 Minutes', 300), ('10 Minutes', 600)], default=0),
            bs.BoolSetting('Epic Mode', default=True),
        ]

    @classmethod
    def supports_session_type(cls, sessiontype: type[bs.Session]) -> bool:
        return (issubclass(sessiontype, bs.DualTeamSession) or issubclass(sessiontype, bs.FreeForAllSession))

    @classmethod
    def get_supported_maps(cls, sessiontype: type[bs.Session]) -> list[str]:
        return ['Doom Island']

    def __init__(self, settings: dict):
        super().__init__(settings)
        self._scoreboard = Scoreboard()
        
        # تعداد بازیکنان
        self._player_count = 0
        
        # محاسبه هیل بر اساس تعداد بازیکنان (هیل پایه 1000)
        player_count = len(self.players) if hasattr(self, 'players') else 0
        base_health = 1000
        extra_health = max(0, (player_count - 2) * 50) if player_count > 0 else 0
        final_health = base_health + extra_health
        
        self._boss_health = final_health
        self._time_limit = float(settings.get('Time Limit', 0))
        self._epic_mode = bool(settings.get('Epic Mode', True))
        self.slow_motion = self._epic_mode
        self.default_music = bs.MusicType.EPIC if self._epic_mode else bs.MusicType.TO_THE_DEATH
        self.boss = None
        self._check_timer = None
        self._game_over = False
        self._players_joined = False
        self._game_won = False

    def spawn_player(self, player: Player) -> bs.Actor:
        """اسپاون پلیر با بمب ایمپکت"""
        if isinstance(self.session, bs.DualTeamSession):
            position = self.map.get_start_position(player.team.id)
        else:
            position = self.map.get_ffa_start_position(self.players)
        
        spaz = CustomPlayerSpaz(color=player.color,
                                highlight=player.highlight,
                                character=player.character,
                                player=player)
        
        player.actor = spaz
        assert spaz.node
        
        spaz.node.name = player.getname()
        spaz.node.name_color = babase.safecolor(player.color, target_intensity=0.75)
        
        spaz.default_bomb_type = 'impact'
        spaz.bomb_type = 'impact'
        spaz.bomb_type_default = 'impact'
        
        spaz.connect_controls_to_player()
        spaz.handlemessage(bs.StandMessage(position, random.uniform(0, 360)))
        
        self._spawn_sound.play(1, position=spaz.node.position)
        
        return spaz

    def on_begin(self):
        super().on_begin()
        self.setup_standard_time_limit(self._time_limit)
        self.setup_standard_powerup_drops()
        
        # شمارش تعداد بازیکنان واقعی (نه بات)
        self._player_count = max(1, len([p for p in self.players if p]))
        
        # پیام خرید اشتراک
        self._subscribe_text = bs.newnode('text',
                                          attrs={
                                              'position': (-600, 650),
                                              'text': 'Telegram / Rubika : @Taha_OstadSharif',
                                              'h_align': 'left',
                                              'v_attach': 'bottom',
                                              'color': (1, 0.8, 0),
                                              'scale': 0.8,
                                              'shadow': 0.5
                                          })
        
        self.boss = SkeletonBoss(position=(0.29, 7.5, -7.5), hitpoints=self._boss_health, player_count=self._player_count)
        self._check_timer = bs.Timer(0.5, self._check_game_state, repeat=True)
        self._boss_text = bs.newnode('text', attrs={
            'position': (0, 200), 'text': 'DEFEAT THE SKELETON KING',
            'h_align': 'center', 'v_attach': 'bottom', 'color': (1, 0.3, 0),
            'scale': 1.2, 'shadow': 0.5
        })
        bs.animate(self._boss_text, 'opacity', {0: 0, 2: 1, 3: 0.8}, loop=False)
        bs.timer(8, self._boss_text.delete)
        self._players_joined = True
        self._spawn_players()

    def on_player_join(self, player: Player) -> None:
        if self.has_begun() and self._players_joined:
            bs.screenmessage(babase.Lstr(value="Bazi dar jaryan ast nemitavanid vared shavid"), color=(1, 0.2, 0.2))
            return
        super().on_player_join(player)

    def _spawn_players(self):
        for player in self.players:
            if not player.is_alive():
                self.spawn_player(player)

    def _check_game_state(self):
        if self._game_over:
            return
        if self.boss and not self.boss.is_alive and not self._game_won:
            self._game_won = True
            self._game_over = True
            if self._check_timer:
                self._check_timer = None
            self.boss._say_lose_quote()
            self._end_game_won()
            return
        alive_players = [p for p in self.players if p.is_alive()]
        if len(alive_players) == 0 and not self._game_over:
            self._game_over = True
            if self._check_timer:
                self._check_timer = None
            if self.boss and self.boss.is_alive:
                self.boss._say_win_quote()
            self._end_game_lose()

    def _end_game_won(self):
        results = bs.GameResults()
        for team in self.teams:
            results.set_team_score(team, 1)
        bs.cameraflash()
        bs.getsound('score').play()
        win_text = bs.newnode('text', attrs={
            'position': (0, 200), 'text': 'VICTORY', 'h_align': 'center',
            'v_attach': 'bottom', 'color': (1, 0.8, 0), 'scale': 1.5, 'shadow': 0.8
        })
        bs.animate(win_text, 'opacity', {0: 0, 0.5: 1, 3: 0})
        bs.timer(3, win_text.delete)
        self.end(results=results)

    def _end_game_lose(self):
        results = bs.GameResults()
        for team in self.teams:
            results.set_team_score(team, 0)
        dead_names = [p.getname(full=True) for p in self.players if not p.is_alive()]
        if dead_names:
            names_str = ", ".join(dead_names[:3])
            bs.screenmessage(babase.Lstr(value=f"{names_str} tavasote Skeleton King shekast khordand"), color=(1, 0.2, 0.2))
        lose_text = bs.newnode('text', attrs={
            'position': (0, 200), 'text': 'GAME OVER', 'h_align': 'center',
            'v_attach': 'bottom', 'color': (1, 0.2, 0.2), 'scale': 1.5, 'shadow': 0.8
        })
        bs.animate(lose_text, 'opacity', {0: 0, 0.5: 1, 3: 0})
        bs.timer(3, lose_text.delete)
        bs.getsound('error').play()
        self.end(results=results)

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.PlayerDiedMessage):
            super().handlemessage(msg)
        else:
            super().handlemessage(msg)

    def end(self, results: bs.GameResults) -> None:
        if self.boss and self.boss.is_alive:
            self.boss.handlemessage(bs.DieMessage())
        super().end(results)


class DoomIslandMapData():
    points = {}
    boxes = {}
    boxes['area_of_interest_bounds'] = ((0.3544110667, 7.616383286, 3.066055072) + (0.0, 0.0, 0.0) + (30, 30, 30))
    boxes['edge_box'] = ((0.3544110667, 5.438284793, -4.100357672) + (0.0, 0.0, 0.0) + (12.57718032, 4.645176013, 3.605557343))
    points['ffa_spawn1'] = (0.5006944438, 5.051501304, -5.79356326) + (6.626174027, 1.0, 0.3402012662)
    points['ffa_spawn2'] = (0.5006944438, 5.051501304, -2.435321368) + (6.626174027, 1.0, 0.3402012662)
    points['ffa_spawn3'] = (7.941690444946289, -4.203672409057617, -10.778594017028809) + (2.0, 1.0, 0.3402012662)
    points['ffa_spawn4'] = (-7.941690444946289, -4.203672409057617, -10.778594017028809) + (2.0, 1.0, 0.3402012662)
    points['ffa_spawn5'] = (7.941690444946289, -4.203672409057617, 5) + (2.0, 1.0, 0.0)
    points['ffa_spawn6'] = (-7.941690444946289, -4.203672409057617, 5) + (2.0, 1.0, 0.0)
    points['flag1'] = (-5.885814199, 5.112162255, -4.251754911)
    points['flag2'] = (6.700855451, 5.10270501, -4.259912982)
    points['flag_default'] = (0.3196701116, 5.110914413, -4.292515158)
    boxes['map_bounds'] = ((0.4528955042, 4.899663734, -3.543675157) + (0.0, 0.0, 0.0) + (30, 30, 30))
    points['powerup_spawn1'] = (-2.645358507, 6.426340583, -4.226597191)
    points['powerup_spawn2'] = (3.540102796, 6.549722855, -4.198476335)
    points['powerup_spawn3'] = (-8.462557792663574, -4.203629970550537, -8.088696479797363)
    points['powerup_spawn4'] = (-8.349356651306152, -4.203611850738525, -4.202945232391357)
    points['powerup_spawn5'] = (-8.560944557189941, -4.203898906707764, 0.43137887120246887)
    points['powerup_spawn6'] = (8.462557792663574, -4.203629970550537, -8.088696479797363)
    points['powerup_spawn7'] = (8.349356651306152, -4.203611850738525, -4.202945232391357)
    points['powerup_spawn8'] = (8.560944557189941, -4.203898906707764, 0.43137887120246887)
    points['powerup_spawn9'] = (0.17930641770362854, -4.203766822814941, 3.233539581298828)
    points['spawn1'] = (-4.745706238, 5.051501304, -4.247934288) + (0.9186962739, 1.0, 0.5153189341)
    points['spawn2'] = (5.838590388, 5.051501304, -4.259627405) + (0.9186962739, 1.0, 0.5153189341)


class DoomIsland(bs.Map):
    defs = DoomIslandMapData()
    name = 'Doom Island'

    @classmethod
    def get_play_types(cls) -> list[str]:
        return ['melee', 'keep_away', 'team_flag']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'rampageBGColor2'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'mesh': bs.getmesh('rampageLevel'),
            'bottom_mesh': bs.getmesh('rampageLevelBottom'),
            'collision_mesh': bs.getcollisionmesh('rampageLevelCollide'),
            'tex': bs.gettexture('bg'),
            'bgtex': bs.gettexture('rampageBGColor'),
            'bgtex2': bs.gettexture('impactBombColorLit'),
            'bgmesh': bs.getmesh('rampageBG'),
            'bgmesh2': bs.getmesh('thePadBG'),
            'vr_fill_mesh': bs.getmesh('rampageVRFill'),
            'railing_collision_mesh': bs.getcollisionmesh('rampageBumper'),
        }
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, 0, 2))
        shared = SharedObjects.get()
        self.collide_material = bs.Material()
        self.collide_material.add_actions(
            conditions=('we_are_older_than', 1),
            actions=('modify_part_collision', 'collide', True))
        self.node = bs.newnode('terrain', delegate=self, attrs={
            'collision_mesh': self.preloaddata['collision_mesh'],
            'mesh': self.preloaddata['mesh'],
            'color_texture': self.preloaddata['tex'],
            'materials': [shared.footing_material],
            'color': (2, 2, 2),
            'reflection': 'soft',
            'reflection_scale': (2.5, 0, 0),
        })
        self.background = bs.newnode('terrain', attrs={
            'mesh': self.preloaddata['bgmesh'],
            'lighting': False,
            'background': True,
            'color_texture': self.preloaddata['bgtex'],
            'color': (0.45, 0, 0),
            'reflection': 'soft',
            'reflection_scale': (1.5, 0, 0),
        })
        self.bg2 = bs.newnode('terrain', attrs={
            'mesh': self.preloaddata['bgmesh2'],
            'lighting': False,
            'background': True,
            'color_texture': self.preloaddata['bgtex2'],
            'color': (0.45, 0.45, 0.45),
        })
        self.bottom = bs.newnode('terrain', attrs={
            'mesh': self.preloaddata['bottom_mesh'],
            'lighting': False,
            'color_texture': bs.gettexture('rampageLevelColor'),
            'reflection': 'soft',
            'reflection_scale': (2.5, 0, 0),
        })
        bs.newnode('terrain', attrs={
            'mesh': self.preloaddata['vr_fill_mesh'],
            'lighting': False,
            'vr_only': True,
            'background': True,
            'color_texture': self.preloaddata['bgtex2'],
        })
        self.railing = bs.newnode('terrain', attrs={
            'collision_mesh': self.preloaddata['railing_collision_mesh'],
            'materials': [shared.railing_material],
            'bumper': True,
        })
        self.collision_region = bs.newnode('region', attrs={
            'position': (0.0, -20, -5), 'type': 'box', 'scale': (1, 1, 1)
        })
        self.no_collision = bs.Material()
        self.no_collision.add_actions(
            conditions=('they_have_material', shared.player_material),
            actions=(('modify_part_collision', 'collide', False), ('modify_part_collision', 'physical', False)))
        self.skull_left = bs.newnode('prop', attrs={
            'position': (-3.0, 6.5, -7.5), 'mesh': bs.getmesh('bonesHead'),
            'color_texture': bs.gettexture('bonesColor'), 'mesh_scale': 1.2,
            'body': 'crate', 'body_scale': 0.0, 'gravity_scale': 0.0,
            'shadow_size': 0.0, 'reflection': 'soft', 'reflection_scale': [0.45],
            'damping': float("inf"), 'density': float("inf"), 'materials': [self.no_collision]
        })
        self.skull_right = bs.newnode('prop', attrs={
            'position': (3.5, 6.5, -7.5), 'mesh': bs.getmesh('bonesHead'),
            'color_texture': bs.gettexture('bonesColor'), 'mesh_scale': 1.2,
            'body': 'crate', 'body_scale': 0.0, 'gravity_scale': 0.0,
            'shadow_size': 0.0, 'reflection': 'soft', 'reflection_scale': [0.45],
            'damping': float("inf"), 'density': float("inf"), 'materials': [self.no_collision]
        })
        self.skull_front = bs.newnode('prop', attrs={
            'position': (0.29, 6.5, -4.0), 'mesh': bs.getmesh('bonesHead'),
            'color_texture': bs.gettexture('bonesColor'), 'mesh_scale': 1.2,
            'body': 'crate', 'body_scale': 0.0, 'gravity_scale': 0.0,
            'shadow_size': 0.0, 'reflection': 'soft', 'reflection_scale': [0.45],
            'damping': float("inf"), 'density': float("inf"), 'materials': [self.no_collision]
        })
        self.skull_back = bs.newnode('prop', attrs={
            'position': (0.29, 6.5, -11.5), 'mesh': bs.getmesh('bonesHead'),
            'color_texture': bs.gettexture('bonesColor'), 'mesh_scale': 1.2,
            'body': 'crate', 'body_scale': 0.0, 'gravity_scale': 0.0,
            'shadow_size': 0.0, 'reflection': 'soft', 'reflection_scale': [0.45],
            'damping': float("inf"), 'density': float("inf"), 'materials': [self.no_collision]
        })
        bs.animate_array(self.skull_left, 'position', 3, {
            0: (-3.0, 6.5, -7.5), 1: (0.29, 6.5, -4.0), 2: (3.5, 6.5, -7.5),
            3: (0.29, 6.5, -11.5), 4: (-3.0, 6.5, -7.5)
        }, loop=True)
        bs.animate_array(self.skull_front, 'position', 3, {
            0: (0.29, 6.5, -4.0), 1: (3.5, 6.5, -7.5), 2: (0.29, 6.5, -11.5),
            3: (-3.0, 6.5, -7.5), 4: (0.29, 6.5, -4.0)
        }, loop=True)
        bs.animate_array(self.skull_right, 'position', 3, {
            0: (3.5, 6.5, -7.5), 1: (0.29, 6.5, -11.5), 2: (-3.0, 6.5, -7.5),
            3: (0.29, 6.5, -4.0), 4: (3.5, 6.5, -7.5)
        }, loop=True)
        bs.animate_array(self.skull_back, 'position', 3, {
            0: (0.29, 6.5, -11.5), 1: (-3.0, 6.5, -7.5), 2: (0.29, 6.5, -4.0),
            3: (3.5, 6.5, -7.5), 4: (0.29, 6.5, -11.5)
        }, loop=True)
        gnode = bs.getactivity().globalsnode
        gnode.tint = (1.2, 1.1, 0.97)
        gnode.ambient_color = (1.3, 1.2, 1.03)
        gnode.vignette_outer = (0.62, 0.64, 0.69)
        gnode.vignette_inner = (0.97, 0.95, 0.93)
        FadeEffect(gnode.tint)

    def on_expire(self):
        super().on_expire()


try:
    _map.register_map(DoomIsland)
except RuntimeError:
    pass


# ba_meta export babase.Plugin
class BSLIFEPRESENT(babase.Plugin):
    def on_app_running(self):
        pass
