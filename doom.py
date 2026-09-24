# ba_meta require api 9

from __future__ import annotations

import random
import math
from typing import TYPE_CHECKING, Optional

import babase
import bascenev1 as bs
from bascenev1lib.actor.playerspaz import PlayerSpaz
from bascenev1lib.actor.spaz import Spaz
from bascenev1lib.actor.bomb import Blast, Bomb
from bascenev1lib.actor.onscreentimer import OnScreenTimer
from bascenev1lib.actor.spazbot import SpazBotSet, StickyBot, SpazBot
from bascenev1lib.actor.scoreboard import Scoreboard
from bascenev1lib.actor.spazfactory import SpazFactory
from bascenev1lib.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any, Sequence, Union, Callable


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


def chasattr(obj: Any, name: str) -> bool:
    try:
        getattr(obj, name)
        return True
    except Exception:
        return False


class BlackHole(bs.Actor):
    def __init__(
        self,
        position: Sequence[float] = (0.0, 0.0, 0.0),
        source_player: bs.Player | None = None,
        radius: float = 22.0,
        xspeed: float = 1.8,
        ssize: float = 0.0,
    ):
        super().__init__()
        self._source_player = source_player
        shared = SharedObjects.get()

        dev_material = bs.Material()
        dev_material.add_actions(
            conditions=('they_have_material', shared.object_material),
            actions=('modify_part_collision', 'collide', True),
        )
        dev_material.add_actions(
            actions=(
                ('modify_part_collision', 'physical', False),
                ('call', 'at_connect', self.kill),
            )
        )

        self.node = bs.newnode(
            'region',
            delegate=self,
            attrs={
                'position': position,
                'scale': (0, 0, 0),
                'type': 'sphere',
                'materials': [dev_material],
            },
        )

        bs.animate_array(
            self.node,
            'scale',
            3,
            {
                0: (ssize, ssize, ssize),
                radius / xspeed: (radius / 10, radius / 10, radius / 10),
            },
        )

        un_material = bs.Material()
        un_material.add_actions(
            actions=('modify_part_collision', 'collide', False)
        )

        self.visual_node0 = bs.newnode(
            'prop',
            owner=self.node,
            attrs={
                'body': 'sphere',
                'mesh': bs.getmesh('shield'),
                'color_texture': bs.gettexture('black'),
                'shadow_size': 0,
                'reflection_scale': [0],
                'materials': [un_material],
                'gravity_scale': 0,
                'density': 0,
            },
        )
        self.visual_node0.is_area_of_interest = True

        mnode = bs.newnode(
            'math',
            owner=self.node,
            attrs={'input1': (0, 0.1, 0), 'operation': 'add'},
        )
        self.node.connectattr('position', mnode, 'input2')
        mnode.connectattr('output', self.visual_node0, 'position')

        bs.animate(
            self.visual_node0,
            'mesh_scale',
            {0: ssize, radius / xspeed: radius / 10},
        )

        self.visual_node1 = bs.newnode(
            'shield', owner=self.node, attrs={'color': (8, 8, 8)}
        )
        self.node.connectattr('position', self.visual_node1, 'position')
        bs.animate(
            self.visual_node1,
            'radius',
            {0: ssize * 2.1, radius / xspeed: radius / 10 * 2.1},
        )

        self.big_light = bs.newnode(
            'light',
            owner=self.node,
            attrs={
                'position': position,
                'color': (1.5, 0.2, 0.8),
                'radius': 0.9,
                'height_attenuated': False,
                'intensity': 3.0,
            }
        )
        self.node.connectattr('position', self.big_light, 'position')
        bs.animate(self.big_light, 'intensity', {0: 0.5, 2.5: 4.0, 3.0: 5.0})

        self._update_timer = bs.Timer(
            0.016666667, bs.WeakCallStrict(self._update), repeat=True
        )
        self._dtimer: bs.Timer | None = None

        self._skid_sound = bs.getsound('gravelSkid')
        self.snode = bs.newnode(
            'sound', owner=self.node, attrs={'sound': self._skid_sound}
        )
        bs.animate(self.snode, 'volume', {0: 0, radius / xspeed: radius / 5})

    def _update(self):
        for node in bs.getnodes():
            if (
                chasattr(node, 'materials')
                and chasattr(node, 'position')
                and SharedObjects.get().object_material in node.materials
                and not (chasattr(node, 'invincible') and node.invincible)
            ):
                drct = (
                    self.node.position[0] - node.position[0],
                    self.node.position[1] - node.position[1],
                    self.node.position[2] - node.position[2],
                )
                dstnc = math.sqrt(drct[0] ** 2 + drct[1] ** 2 + drct[2] ** 2)
                cradius = self.node.scale[0] * 10
                if dstnc != 0 and dstnc <= cradius:
                    nv = (drct[0] / dstnc, drct[1] / dstnc, drct[2] / dstnc)
                    node.handlemessage(
                        'impulse',
                        node.position[0],
                        node.position[1],
                        node.position[2],
                        nv[0],
                        nv[1],
                        nv[2],
                        cradius * 2,
                        0,
                        0,
                        0,
                        nv[0],
                        nv[1],
                        nv[2],
                    )

    def kill(self):
        node = bs.getcollision().opposingnode
        spaz = node.getdelegate(PlayerSpaz) or node.getdelegate(SpazBot)
        if spaz and (
            spaz.last_player_attacked_by in (None, spaz)
            or bs.time() - spaz.last_attacked_time >= 4
        ):
            spaz.last_attacked_time = bs.time()
            spaz.last_player_attacked_by = bs.existing(self._source_player)
            spaz.last_attacked_type = ('explosion', 'dev')

        light = bs.newnode(
            'light',
            attrs={
                'position': node.position,
                'height_attenuated': False,
                'color': (1, 0, 0),
                'intensity': 30,
                'radius': 1.5,
            },
        )
        bs.animate(light, 'radius', {0: 0, 0.1: 1.5, 0.2: 1.5, 0.3: 0})
        bs.timer(0.3, light.delete)

        node.handlemessage(bs.DieMessage())

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.DieMessage):
            if self.node:
                if msg.immediate:
                    self.node.delete()
                else:
                    bs.animate(
                        self.visual_node0,
                        'mesh_scale',
                        {
                            0: self.visual_node0.mesh_scale,
                            0.1: 0,
                            0.2: 0.25,
                            0.3: 0.25,
                            0.4: 0,
                        },
                    )
                    bs.animate(
                        self.visual_node1,
                        'radius',
                        {
                            0: self.visual_node1.radius,
                            0.1: 0,
                            0.2: 0.5,
                            0.3: 0.5,
                            0.4: 0,
                        },
                    )
                    bs.animate(
                        self.big_light, 'intensity', {0: self.big_light.intensity, 0.1: 0, 0.4: 0}
                    )
                    bs.animate(
                        self.snode, 'volume', {0: self.snode.volume, 0.1: 0}
                    )
                    bs.timer(0.4, self.last_breath)
                    bs.timer(0.4, self.node.delete)
                self._update_timer = None
        else:
            return super().handlemessage(msg)
        return None

    def last_breath(self):
        self._dtimer = bs.Timer(
            0.016666667,
            bs.CallStrict(
                bs.emitfx,
                self.node.position,
                count=200,
                spread=8,
                emit_type='distortion',
            ),
            repeat=True,
        )
        from bascenev1lib.actor.bomb import Blast

        Blast(
            position=self.node.position,
            blast_type='tnt',
            hit_subtype='tnt',
            blast_radius=6.0,
        ).autoretain()
        bs.timer(1, bs.CallStrict(self.__setattr__, '_dtimer', None))


BLACKHOLE_LIFETIME: float = 20.0
BLACKHOLE_RADIUS: float = 22.0
BLACKHOLE_XSPEED: float = 1.8
BLACKHOLE_SSIZE: float = 0.0


class UFODiedMessage:
    def __init__(self, ufo: UFO, killerplayer: bs.Player | None, how: bs.DeathType):
        self.spazbot = ufo
        self.killerplayer = killerplayer
        self.how = how


class RoboBot(StickyBot):
    character = 'B-9000'
    default_bomb_type = 'land_mine'
    color = (0, 0, 0)
    highlight = (3, 3, 3)


class MidBossRoboBot(RoboBot):
    hitpoints = 1000
    hitpoints_max = 1000

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.HitMessage):
            ht = getattr(msg, 'hit_type', '')
            if str(ht).lower() != 'punch':
                return None
        return super().handlemessage(msg)


class UFO(bs.Actor):
    node: bs.Node

    BOMB_GRAVITY: float = 9.8

    def __init__(self, hitpoints: int = 1000):
        super().__init__()
        shared = SharedObjects.get()

        self.update_callback: Callable[[UFO], Any] | None = None
        activity = self.activity
        assert isinstance(activity, bs.GameActivity)

        self.platform_material = bs.Material()
        self.platform_material.add_actions(
            conditions=('they_have_material', shared.footing_material),
            actions=('modify_part_collision', 'collide', True))
        self.ice_material = bs.Material()
        self.ice_material.add_actions(
            actions=('modify_part_collision', 'friction', 0.0))

        self._player_pts: list[tuple[bs.Vec3, bs.Vec3]] = []
        self._ufo_update_timer: bs.Timer | None = None
        self.last_player_attacked_by: bs.Player | None = None
        self.last_attacked_time = 0.0
        self.last_attacked_type: tuple[str, str] | None = None

        self.to_target: bs.Vec3 = bs.Vec3(0, 0, 0)
        self.dist = (0, 0, 0)

        self._bots = SpazBotSet()
        self.frozen = False
        self.bot_count = 3

        self.hitpoints = hitpoints
        self.hitpoints_max = hitpoints
        self._rage_mode = False
        self._low_health_triggered = False
        self._dead = False
        self._mid_health_triggered = False

        self._mid_boss_bot: Optional[SpazBot] = None
        self._mid_boss_ready: bool = False
        self._remaining_hp: int = 0
        self._mid_boss_ui_timer: Optional[bs.Timer] = None
        self._mid_boss_killed: bool = False

        self._width = 240
        self._width_max = 240
        self._height = 35
        self._bar_width = 240
        self._bar_height = 35
        self._bar_tex = self._backing_tex = bs.gettexture('bar')
        self._cover_tex = bs.gettexture('uiAtlas')
        self._mesh = bs.getmesh('meterTransparent')
        self.bar_posx = -120

        self._last_hit_time: int | None = None
        self.impact_scale = 1.0
        self._num_times_hit = 0

        self._sucker_mat = bs.Material()

        self.ufo_material = bs.Material()
        self.ufo_material.add_actions(
            conditions=('they_have_material', shared.player_material),
            actions=(('modify_node_collision', 'collide', True),
                     ('modify_part_collision', 'physical', True)))

        self.ufo_material.add_actions(
            conditions=(('they_have_material', shared.object_material), 'or',
                        ('they_have_material', shared.footing_material), 'or',
                        ('they_have_material', self.ufo_material)),
            actions=('modify_part_collision', 'physical', False))

        activity = bs.getactivity()
        point = activity.map.get_flag_position(None)
        boss_spawn_pos = (point[0], point[1] + 3.5, point[2])

        self.node = bs.newnode('prop', delegate=self, attrs={
            'position': boss_spawn_pos,
            'velocity': (2, 0, 0),
            'color_texture': bs.gettexture('achievementFootballShutout'),
            'mesh': bs.getmesh('landMine'),
            'mesh_scale': 3.3,
            'body': 'landMine',
            'body_scale': 3.3,
            'gravity_scale': 0.2,
            'density': 1,
            'reflection': 'soft',
            'reflection_scale': [0.25],
            'shadow_size': 0.1,
            'max_speed': 1.5,
            'is_area_of_interest': True,
            'materials': [shared.footing_material, shared.object_material]})

        self.holder = bs.newnode('region', attrs={
            'position': (boss_spawn_pos[0], boss_spawn_pos[1] - 0.25, boss_spawn_pos[2]),
            'scale': [6, 0.1, 2.5 - 0.1],
            'type': 'box',
            'materials': (self.platform_material, self.ice_material, shared.object_material)})

        self.blocks = []

        self._sucker_mat.add_actions(
            conditions=(('they_have_material', shared.player_material)),
            actions=(('modify_part_collision', 'collide', True),
                     ('modify_part_collision', 'physical', False),
                     ('call', 'at_connect', self._levitate)))

        self.suck = bs.newnode('region',
                               attrs={'position': (boss_spawn_pos[0], boss_spawn_pos[1] - 2, boss_spawn_pos[2]),
                                      'scale': [1, 10, 1],
                                      'type': 'box',
                                      'materials': [self._sucker_mat]})

        self.node.connectattr('position', self.holder, 'position')
        self.node.connectattr('position', self.suck, 'position')

        bs.animate(self.node, 'mesh_scale', {
            0: 0,
            0.2: self.node.mesh_scale * 1.1,
            0.26: self.node.mesh_scale})

        self.shield_deco = bs.newnode('shield', owner=self.node,
                                      attrs={'color': (4, 4, 4), 'radius': 1.2})
        self.node.connectattr('position', self.shield_deco, 'position')

        self._scoreboard()
        self._update()
        self.drop_bomb_timer = bs.Timer(1.5, bs.CallStrict(self._drop_bomb), repeat=True)
        self.drop_bots_timer = bs.Timer(15.0, bs.CallStrict(self._drop_bots), repeat=True)
        self._move_timer = bs.Timer(0.05, bs.WeakCallStrict(self.update_ai), repeat=True)

    def _sync_mid_boss_hp(self) -> None:
        bot = self._mid_boss_bot
        if bot is None:
            return
        try:
            hp = int(getattr(bot, 'hitpoints', 0))
            hp_max = int(getattr(bot, 'hitpoints_max', 1)) or 1
        except Exception:
            return

        if hp < 0:
            hp = 0

        self.hitpoints = hp
        self.hitpoints_max = hp_max

        try:
            if (self._score_text and self._score_text.node
                    and self._score_text.node.exists()):
                self._score_text.node.text = str(hp)
        except Exception:
            pass

        try:
            self._bar_width = hp * self._width_max / hp_max
            if self._bar_scale:
                cur_width = self._bar_scale.input0
                bs.animate(self._bar_scale, 'input0',
                           {0.0: cur_width, 0.1: self._bar_width})
            if self._bar_position:
                cur_x = self._bar_position.input0
                bs.animate(self._bar_position, 'input0',
                           {0.0: cur_x, 0.1: self.bar_posx + self._bar_width / 2})
        except Exception:
            pass

        hp_percent = hp / hp_max if hp_max else 0
        try:
            if self._bar:
                if hp_percent <= 0.25:
                    self._bar.node.color = (1, 0.1, 0.1)
                elif hp_percent <= 0.5:
                    self._bar.node.color = (1, 0.6, 0.1)
                else:
                    self._bar.node.color = (0.5, 0.5, 0.5)
        except Exception:
            pass

        if hp <= 0 and not self._mid_boss_killed:
            self._mid_boss_killed = True
            try:
                if bot.node and bot.node.exists():
                    bot.handlemessage(bs.DieMessage())
            except Exception:
                pass

    def _drop_bots(self) -> None:
        if not self.node or not self.node.exists():
            return
        pos = self.node.position
        for i in range(self.bot_count):
            bs.timer(1.0 + i, lambda p=pos: self._bots.spawn_bot(
                RoboBot, pos=(p[0], p[1] - 1, p[2]), spawn_time=0.0))

    def _skullify_bomb(self, bomb):
        try:
            if bomb.node and bomb.node.exists():
                bomb.node.mesh = bs.getmesh('bonesHead')
                bomb.node.color_texture = bs.gettexture('bonesColor')
                bomb.node.mesh_scale = 1.15
        except Exception:
            pass

    def _launch_skull_bomb(self, origin_pos, aim_point: bs.Vec3, target_vel: bs.Vec3 | None = None):
        if not self.node or not self.node.exists():
            return

        start = bs.Vec3(origin_pos[0], origin_pos[1] - 1.0, origin_pos[2])
        horiz_dist = math.sqrt((aim_point.x - start.x) ** 2 + (aim_point.z - start.z) ** 2)

        desired_speed = 15.0 if self._rage_mode else 11.0
        flight_time = max(0.35, horiz_dist / desired_speed)

        target = aim_point
        if target_vel is not None:
            lead = 0.5
            target = bs.Vec3(
                aim_point.x + target_vel.x * flight_time * lead,
                aim_point.y,
                aim_point.z + target_vel.z * flight_time * lead,
            )

        dx = target.x - start.x
        dy = target.y - start.y
        dz = target.z - start.z

        vx = dx / flight_time
        vz = dz / flight_time
        vy = (dy + 0.5 * self.BOMB_GRAVITY * flight_time ** 2) / flight_time

        bomb_pos = (
            start.x + random.uniform(-0.2, 0.2),
            start.y,
            start.z + random.uniform(-0.2, 0.2),
        )
        bomb_vel = (vx, vy, vz)
        bomb = Bomb(position=bomb_pos, velocity=bomb_vel, bomb_type='impact')
        bomb.autoretain()
        self._skullify_bomb(bomb)
        dark_effect = BombDarkMagicEffect(bomb.node)
        dark_effect.start()
        bs.emitfx(position=bomb_pos, count=10, scale=1.2, spread=0.5, chunk_type='spark')

    def _drop_bomb(self) -> None:
        if not self.node or not self.node.exists() or self.frozen or self._dead:
            return
        target_pt, target_vel = self._get_target_player_pt()
        if target_pt is None:
            return
        p = self.node.position
        bomb_count = 2 if self._rage_mode else 1
        spread = 0.8 if self._rage_mode else 0.4
        for i in range(bomb_count):
            offset = (i - (bomb_count - 1) / 2) * spread
            aim_point = bs.Vec3(target_pt.x + offset, target_pt.y, target_pt.z + offset)
            bs.timer(i * 0.12, bs.CallPartial(self._launch_skull_bomb, p, aim_point, target_vel))

    def _levitate(self):
        node = bs.getcollision().opposingnode
        if node.exists():
            spaz = node.getdelegate(Spaz, True)

            def raise_player(target_spaz):
                if target_spaz and target_spaz.node and target_spaz.node.exists():
                    node = target_spaz.node
                    try:
                        node.handlemessage("impulse", node.position[0],
                                           node.position[1] + .5,
                                           node.position[2], 0, 5, 0, 3, 10, 0,
                                           0, 0, 5, 0)
                    except Exception:
                        pass

            if not self.frozen:
                for i in range(7):
                    bs.timer(0.05 + i / 20, bs.CallPartial(raise_player, spaz))

    def on_punched(self, damage: int) -> None:
        pass

    def do_damage(self, msg: Any) -> None:
        if not self.node or self._dead:
            return None
        damage = abs(msg.magnitude)
        if msg.hit_type == 'explosion':
            damage /= 20
        self.hitpoints -= int(damage)
        if self.hitpoints <= 0:
            self.handlemessage(bs.DieMessage())
        self._update()

    def _get_target_player_pt(self) -> tuple[bs.Vec3 | None, bs.Vec3 | None]:
        assert self.node
        botpt = bs.Vec3(self.node.position)
        closest_dist: float | None = None
        closest_vel: bs.Vec3 | None = None
        closest: bs.Vec3 | None = None
        if not self._player_pts:
            return None, None
        for plpt, plvel in self._player_pts:
            dist = (plpt - botpt).length()
            if closest_dist is None or dist < closest_dist:
                closest_dist = dist
                closest_vel = plvel
                closest = plpt
        if closest_dist is not None:
            assert closest_vel is not None
            assert closest is not None
            return (
                bs.Vec3(closest[0], closest[1], closest[2]),
                bs.Vec3(closest_vel[0], closest_vel[1], closest_vel[2]),
            )
        return None, None

    def set_player_points(self, pts: list[tuple[bs.Vec3, bs.Vec3]]) -> None:
        self._player_pts = pts

    def exists(self) -> bool:
        return bool(self.node)

    def show_damage_count(self, damage: str, position: Sequence[float], direction: Sequence[float]) -> None:
        lifespan = 1.0
        app = bs.app
        do_big = app.ui_v1.uiscale is bs.UIScale.SMALL or app.vr_mode
        txtnode = bs.newnode('text',
                             attrs={
                                 'text': damage,
                                 'in_world': True,
                                 'h_align': 'center',
                                 'flatness': 1.0,
                                 'shadow': 1.0 if do_big else 0.7,
                                 'color': (1, 0.25, 0.25, 1),
                                 'scale': 0.035 if do_big else 0.03
                             })
        tcombine = bs.newnode('combine', owner=txtnode, attrs={'size': 3})
        tcombine.connectattr('output', txtnode, 'position')
        v_vals = []
        pval = 0.0
        vval = 0.07
        count = 6
        for i in range(count):
            v_vals.append((float(i) / count, pval))
            pval += vval
            vval *= 0.5
        p_start = position[0]
        p_dir = direction[0]
        bs.animate(tcombine, 'input0',
                   {i[0] * lifespan: p_start + p_dir * i[1] for i in v_vals})
        p_start = position[1]
        p_dir = direction[1]
        bs.animate(tcombine, 'input1',
                   {i[0] * lifespan: p_start + p_dir * i[1] for i in v_vals})
        p_start = position[2]
        p_dir = direction[2]
        bs.animate(tcombine, 'input2',
                   {i[0] * lifespan: p_start + p_dir * i[1] for i in v_vals})
        bs.animate(txtnode, 'opacity', {0.7 * lifespan: 1.0, lifespan: 0.0})
        bs.timer(lifespan, txtnode.delete)

    def _scoreboard(self) -> None:
        self._backing = bs.NodeActor(
            bs.newnode('image',
                       attrs={
                           'position': (self.bar_posx + self._width / 2, -100),
                           'scale': (self._width, self._height),
                           'opacity': 0.7,
                           'color': (0.3, 0.3, 0.3),
                           'vr_depth': -3,
                           'attach': 'topCenter',
                           'texture': self._backing_tex
                       }))
        self._bar = bs.NodeActor(
            bs.newnode('image',
                       attrs={
                           'opacity': 1.0,
                           'color': (0.5, 0.5, 0.5),
                           'attach': 'topCenter',
                           'texture': self._bar_tex
                       }))
        self._bar_scale = bs.newnode('combine', owner=self._bar.node,
                                     attrs={'size': 2, 'input0': self._bar_width, 'input1': self._bar_height})
        self._bar_scale.connectattr('output', self._bar.node, 'scale')
        self._bar_position = bs.newnode('combine', owner=self._bar.node,
                                        attrs={'size': 2, 'input0': self.bar_posx + self._bar_width / 2, 'input1': -100})
        self._bar_position.connectattr('output', self._bar.node, 'position')
        self._cover = bs.NodeActor(
            bs.newnode('image',
                       attrs={
                           'position': (self.bar_posx + 120, -100),
                           'scale': (self._width * 1.15, self._height * 1.6),
                           'opacity': 1.0,
                           'color': (0.3, 0.3, 0.3),
                           'vr_depth': 2,
                           'attach': 'topCenter',
                           'texture': self._cover_tex,
                           'mesh_transparent': self._mesh
                       }))
        self._score_text = bs.NodeActor(
            bs.newnode('text',
                       attrs={
                           'position': (self.bar_posx + 120, -100),
                           'h_attach': 'center',
                           'v_attach': 'top',
                           'h_align': 'center',
                           'v_align': 'center',
                           'maxwidth': 130,
                           'scale': 0.9,
                           'text': '',
                           'shadow': 0.5,
                           'flatness': 1.0,
                           'color': (1, 1, 1, 0.8)
                       }))

    def _update(self) -> None:
        if self._dead:
            return
        self._score_text.node.text = str(self.hitpoints)
        self._bar_width = self.hitpoints * self._width_max / self.hitpoints_max
        cur_width = self._bar_scale.input0
        bs.animate(self._bar_scale, 'input0', {0.0: cur_width, 0.1: self._bar_width})
        cur_x = self._bar_position.input0
        bs.animate(self._bar_position, 'input0', {0.0: cur_x, 0.1: self.bar_posx + self._bar_width / 2})

        hp_percent = self.hitpoints / self.hitpoints_max

        if hp_percent <= 0.5 and not self._mid_health_triggered:
            self._mid_health_triggered = True
            self._trigger_mid_health_event()
            return

        if hp_percent <= 0.25 and not self._rage_mode:
            self._rage_mode = True
            self._bar.node.color = (1, 0.1, 0.1)
            bs.camerashake(intensity=2.0)
            try:
                self.shield_deco.color = (5, 0.2, 0.2)
            except:
                pass
        elif hp_percent < 0.2 and not self._low_health_triggered:
            self._low_health_triggered = True
            bs.emitfx(position=self.node.position, count=60, scale=3.0, spread=3.0, chunk_type='spark')
            bs.camerashake(intensity=1.5)

        if self.hitpoints > self.hitpoints_max * 3 / 4:
            bs.animate_array(self.shield_deco, 'color', 3,
                             {0: self.shield_deco.color, 0.2: (4, 4, 4)})
        elif self.hitpoints > self.hitpoints_max * 1 / 2:
            bs.animate_array(self.shield_deco, 'color', 3,
                             {0: self.shield_deco.color, 0.2: (3, 3, 5)})
            self.bot_count = 4
        elif self.hitpoints > self.hitpoints_max * 1 / 4:
            bs.animate_array(self.shield_deco, 'color', 3,
                             {0: self.shield_deco.color, 0.2: (1, 5, 1)})
            self.bot_count = 5
        else:
            bs.animate_array(self.shield_deco, 'color', 3,
                             {0: self.shield_deco.color, 0.2: (5, 0.2, 0.2)})
            self.bot_count = 6

    def _trigger_mid_health_event(self) -> None:
        if self._dead:
            return

        self._remaining_hp = max(1, self.hitpoints)

        self._dead = True
        self.frozen = True

        if self.node:
            bs.animate(self.node, 'mesh_scale', {0: self.node.mesh_scale, 0.3: 0})
            bs.timer(0.35, self.node.delete)
        if self.suck:
            bs.timer(0.1, self.suck.delete)
        if self.shield_deco:
            bs.timer(0.3, self.shield_deco.delete)

        for timer_name in ('drop_bomb_timer', 'drop_bots_timer', '_move_timer'):
            timer = getattr(self, timer_name, None)
            if timer is not None:
                try:
                    timer.cancel()
                except Exception:
                    pass
                setattr(self, timer_name, None)

        try:
            gnode = bs.getactivity().globalsnode
            if gnode:
                bs.animate_array(gnode, 'tint', 3, {
                    0: gnode.tint,
                    1.0: (0.02, 0.02, 0.04),
                })
        except Exception:
            pass

        self._spawn_dual_black_holes()

    def _spawn_dual_black_holes(self) -> None:
        try:
            point = bs.getactivity().map.get_flag_position(None)
            center_pos = (point[0], point[1] + 2.0, point[2])

            start_offset = 20.0
            start_y = center_pos[1] + 2.0

            un_material = bs.Material()
            un_material.add_actions(
                actions=('modify_part_collision', 'collide', False)
            )

            red_core = bs.newnode('prop', attrs={
                'body': 'sphere',
                'position': (center_pos[0] + start_offset, start_y, center_pos[2]),
                'mesh': bs.getmesh('shield'),
                'color_texture': bs.gettexture('black'),
                'shadow_size': 0.0,
                'reflection_scale': [0.0],
                'gravity_scale': 0.0,
                'density': 0.0,
                'body_scale': 0.0001,
                'mesh_scale': 0.5,
                'materials': [un_material],
            })
            red_ring = bs.newnode('shield', attrs={
                'position': (center_pos[0] + start_offset, start_y, center_pos[2]),
                'color': (10, 0.5, 0.5),
                'radius': 0.8,
            })
            red_light = bs.newnode('light', attrs={
                'position': (center_pos[0] + start_offset, start_y, center_pos[2]),
                'color': (1.5, 0.2, 0.2),
                'radius': 1.2,
                'height_attenuated': False,
                'intensity': 3.0,
            })
            red_core.connectattr('position', red_ring, 'position')
            red_core.connectattr('position', red_light, 'position')

            blue_core = bs.newnode('prop', attrs={
                'body': 'sphere',
                'position': (center_pos[0] - start_offset, start_y, center_pos[2]),
                'mesh': bs.getmesh('shield'),
                'color_texture': bs.gettexture('black'),
                'shadow_size': 0.0,
                'reflection_scale': [0.0],
                'gravity_scale': 0.0,
                'density': 0.0,
                'body_scale': 0.0001,
                'mesh_scale': 0.5,
                'materials': [un_material],
            })
            blue_ring = bs.newnode('shield', attrs={
                'position': (center_pos[0] - start_offset, start_y, center_pos[2]),
                'color': (0.5, 0.5, 10),
                'radius': 0.8,
            })
            blue_light = bs.newnode('light', attrs={
                'position': (center_pos[0] - start_offset, start_y, center_pos[2]),
                'color': (0.2, 0.2, 1.5),
                'radius': 1.2,
                'height_attenuated': False,
                'intensity': 3.0,
            })
            blue_core.connectattr('position', blue_ring, 'position')
            blue_core.connectattr('position', blue_light, 'position')

            move_duration = 2.5
            bs.animate_array(red_core, 'position', 3, {
                0: (center_pos[0] + start_offset, start_y, center_pos[2]),
                move_duration: center_pos,
            })
            bs.animate_array(blue_core, 'position', 3, {
                0: (center_pos[0] - start_offset, start_y, center_pos[2]),
                move_duration: center_pos,
            })

            hum_sound = bs.getsound('gravelSkid')
            hum_sound.play()

            bs.timer(move_duration, bs.CallStrict(self._spawn_bot_at_center, center_pos))

            def cleanup_nodes():
                for n in (red_core, red_ring, red_light, blue_core, blue_ring, blue_light):
                    if n and n.exists():
                        try:
                            n.delete()
                        except Exception:
                            pass
            bs.timer(move_duration + 0.2, cleanup_nodes)

        except Exception:
            pass

    def _spawn_bot_at_center(self, center_pos: tuple) -> None:
        try:
            bs.emitfx(position=center_pos, count=100, scale=3.0, spread=4.0, chunk_type='spark')
            bs.cameraflash()
            bs.camerashake(intensity=2.5)
            bs.getsound('tnt').play()

            hp_for_mid = self._remaining_hp

            def _on_spawn(bot):
                self._mid_boss_bot = bot
                try:
                    bot.hitpoints = hp_for_mid
                    bot.hitpoints_max = hp_for_mid
                except Exception:
                    pass

                try:
                    if self._score_text and self._score_text.node:
                        self._score_text.node.text = str(hp_for_mid)
                except Exception:
                    pass

                self._mid_boss_ui_timer = bs.Timer(
                    0.05, bs.WeakCallStrict(self._sync_mid_boss_hp), repeat=True
                )

                bs.timer(0.5, self._mark_mid_boss_ready)

            try:
                self._bots.spawn_bot(
                    MidBossRoboBot,
                    pos=center_pos,
                    spawn_time=0.0,
                    on_spawn_call=_on_spawn,
                )
            except TypeError:
                bot = self._bots.spawn_bot(MidBossRoboBot, pos=center_pos, spawn_time=0.0)
                if bot is not None:
                    _on_spawn(bot)
                else:
                    try:
                        for b in self._bots.get_bots():
                            _on_spawn(b)
                            break
                    except Exception:
                        pass

            self.hitpoints = hp_for_mid
            self.hitpoints_max = hp_for_mid
            self._bar_width = self._width_max
            try:
                if self._bar:
                    self._bar.node.color = (0.5, 0.5, 0.5)
                if self._bar_scale:
                    bs.animate(self._bar_scale, 'input0',
                               {0.0: self._bar_scale.input0, 0.1: self._width_max})
                if self._bar_position:
                    bs.animate(self._bar_position, 'input0',
                               {0.0: self._bar_position.input0, 0.1: self.bar_posx + self._width_max / 2})
                if self._score_text and self._score_text.node:
                    self._score_text.node.text = str(hp_for_mid)
            except Exception:
                pass

            gnode = bs.getactivity().globalsnode
            if gnode:
                bs.animate_array(gnode, 'tint', 3, {
                    0: gnode.tint,
                    0.8: (0.6, 0.7, 0.8),
                })

        except Exception:
            pass

    def _mark_mid_boss_ready(self) -> None:
        self._mid_boss_ready = True

    def update_ai(self) -> None:
        if self.update_callback is not None:
            if self.update_callback(self):
                return
        if not self.node or self._dead:
            return
        if not self._player_pts:
            return

        pos = self.node.position
        our_pos = bs.Vec3(pos[0], pos[1] - 3, pos[2])
        target_pt_raw, target_vel = self._get_target_player_pt()
        if target_pt_raw is None:
            return

        try:
            dist_raw = (target_pt_raw - our_pos).length()
            target_pt = target_pt_raw + target_vel * dist_raw * 0.3
        except:
            return
        diff = target_pt - our_pos
        self.dist = diff
        self.to_target = diff.normalized()

        speed = 1.8 if self._rage_mode else 1.5
        accel = 90 if self._rage_mode else 70

        if self.hitpoints == 0:
            self.node.velocity = (0, self.to_target.y, 0)
            self.node.extra_acceleration = (0, self.to_target.y * 80 + 70, 0)
        elif not self.frozen:
            self.node.velocity = (self.to_target.x * speed, self.to_target.y * speed * 0.6, self.to_target.z * speed)
            self.node.extra_acceleration = (self.to_target.x, self.to_target.y * 80 + accel, self.to_target.z)

    def on_expire(self) -> None:
        super().on_expire()
        self.update_callback = None
        if self._mid_boss_ui_timer:
            try:
                self._mid_boss_ui_timer.cancel()
            except Exception:
                pass
            self._mid_boss_ui_timer = None

    def animate_mesh(self) -> None:
        if not self.node:
            return None
        bs.emitfx(position=self.node.position,
                  velocity=self.node.velocity,
                  count=int(6 + random.random() * 10),
                  scale=0.5,
                  spread=0.4,
                  chunk_type='metal')

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.HitMessage):
            self.animate_mesh()
            if self.hitpoints != 0 and not self._dead:
                self.do_damage(msg)
            self._update()

        elif isinstance(msg, bs.DieMessage):
            if self._dead:
                return None
            self._dead = True
            if self.node:
                self.hitpoints = 0
                self.frozen = True

                for timer_name in ('drop_bomb_timer', 'drop_bots_timer', '_move_timer'):
                    timer = getattr(self, timer_name, None)
                    if timer is not None:
                        try:
                            timer.cancel()
                        except Exception:
                            pass
                        setattr(self, timer_name, None)

                p = self.node.position

                try:
                    black_hole = BlackHole(
                        position=p,
                        radius=BLACKHOLE_RADIUS,
                        xspeed=BLACKHOLE_XSPEED,
                        ssize=BLACKHOLE_SSIZE,
                    )

                    try:
                        gnode = bs.getactivity().globalsnode
                        if gnode:
                            current_tint = gnode.tint
                            bs.animate_array(gnode, 'tint', 3, {
                                0: current_tint,
                                0.3: (0.06, 0.06, 0.08),
                                0.6: (0.03, 0.03, 0.05),
                            })
                    except Exception:
                        pass

                    bs.timer(3.0, lambda: black_hole.handlemessage(bs.DieMessage()))
                except Exception:
                    pass

                bs.timer(0.5, self.node.delete)
                bs.timer(0.1, self.suck.delete)

        elif isinstance(msg, bs.OutOfBoundsMessage):
            if self._dead:
                return None
            activity = bs.getactivity()
            try:
                point = activity.map.get_flag_position(None)
                boss_spawn_pos = (point[0], point[1] + 3.5, point[2])
                assert self.node
                self.node.position = boss_spawn_pos
            except:
                self.handlemessage(bs.DieMessage())

        elif isinstance(msg, bs.FreezeMessage):
            if self._dead:
                return None
            if not self.frozen:
                self.frozen = True
                for timer_name in ('drop_bomb_timer', 'drop_bots_timer'):
                    timer = getattr(self, timer_name, None)
                    if timer is not None:
                        try:
                            timer.cancel()
                        except Exception:
                            pass
                        setattr(self, timer_name, None)
                self.node.velocity = (0, self.to_target.y, 0)
                self.node.extra_acceleration = (0, 0, 0)
                self.node.reflection_scale = [2]

                def unfrozen():
                    if self._dead:
                        return
                    self.frozen = False
                    self.drop_bomb_timer = bs.Timer(1.5, bs.CallStrict(self._drop_bomb), repeat=True)
                    self.drop_bots_timer = bs.Timer(15.0, bs.CallStrict(self._drop_bots), repeat=True)
                    self.node.reflection_scale = [0.25]

                bs.timer(3.0, unfrozen)

        else:
            super().handlemessage(msg)


class Player(bs.Player['Team']):
    pass


class Team(bs.Team[Player]):
    def __init__(self) -> None:
        self.score = 0


class CustomPlayerSpaz(PlayerSpaz):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_bomb_type = 'impact'
        self.bomb_type = 'impact'
        self.bomb_type_default = 'impact'


class FadeEffect:
    def __init__(self, map_tint=(1, 1, 1)):
        gnode = bs.getactivity().globalsnode
        bs.animate_array(gnode, 'tint', 3, {0: (0, 0, 0), 1.5: map_tint})


# ba_meta export bascenev1.Map
class BasketMapV2(bs.Map):
    name = 'BasketBall Stadium OG V2'

    @classmethod
    def get_play_types(cls) -> list[str]:
        return ['melee', 'team_flag', 'keep_away', 'conquest', 'king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'hockeyStadiumPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'mesh': bs.getmesh('hockeyStadiumInner'),
            'bg_mesh': bs.getmesh('thePadBG'),
        }
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, -0.8, -1.1))
        shared = SharedObjects.get()

        try:
            data = self.preloaddata
            if not data:
                raise Exception
        except Exception:
            data = self.on_preload()

        self.node = bs.newnode('terrain', delegate=self, attrs={
            'mesh': data['bg_mesh'],
            'color_texture': bs.gettexture('menuBG'),
            'materials': [shared.footing_material],
            'color': (1.0, 0.2, 1.0),
        })
        self.floor = bs.newnode('terrain', attrs={
            'mesh': data['mesh'],
            'color_texture': bs.gettexture('white'),
            'opacity': 0.92,
            'color': (0.7, 0.4, 0.1),
            'materials': [shared.footing_material],
        })
        gnode = bs.getactivity().globalsnode
        gnode.floor_reflection = True
        gnode.debris_friction = 0.3
        gnode.debris_kill_height = -0.3
        gnode.tint = (0.6, 0.7, 0.8)
        gnode.ambient_color = (1.15, 1.25, 1.6)
        gnode.vignette_outer = (0.66, 0.67, 0.73)
        gnode.vignette_inner = (0.93, 0.93, 0.95)
        gnode.vr_camera_offset = (0, -0.8, -1.1)
        gnode.vr_near_clip = 0.5


# ba_meta export bascenev1.GameActivity
class DoomBossFightGame(bs.TeamGameActivity[Player, Team]):
    name = 'UFO Boss Fight'
    description = 'Defeat the UFO King!\nBSRUSH PRESENT'

    @classmethod
    def get_available_settings(cls, sessiontype: type[bs.Session]) -> list:
        return [
            bs.IntSetting('Boss Health', min_value=100, default=1000, increment=100),
            bs.IntChoiceSetting('Time Limit', choices=[('None', 0), ('5 Minutes', 300), ('10 Minutes', 600)], default=0),
            bs.BoolSetting('Epic Mode', default=True),
        ]

    @classmethod
    def supports_session_type(cls, sessiontype: type[bs.Session]) -> bool:
        return (issubclass(sessiontype, bs.DualTeamSession) or issubclass(sessiontype, bs.FreeForAllSession))

    @classmethod
    def get_supported_maps(cls, sessiontype: type[bs.Session]) -> list[str]:
        return ['BasketBall Stadium OG V2']

    def __init__(self, settings: dict):
        settings = dict(settings)
        settings['map'] = 'BasketBall Stadium OG V2'

        super().__init__(settings)
        self._scoreboard = Scoreboard()
        self._player_count = 0
        base_health = int(settings.get('Boss Health', 1000))
        self._boss_health = base_health
        self._time_limit = float(settings.get('Time Limit', 0))
        self._epic_mode = bool(settings.get('Epic Mode', True))
        self.slow_motion = self._epic_mode
        self.default_music = bs.MusicType.EPIC if self._epic_mode else bs.MusicType.TO_THE_DEATH
        self.boss = None
        self._check_timer = None
        self._game_over = False
        self._players_joined = False
        self._game_won = False
        self._win_timer: Optional[bs.Timer] = None
        self._lose_timer: Optional[bs.Timer] = None
        self._boss_update_timer: bs.Timer | None = None
        self._boss_died = False
        self._game_end_delay = 4.0

        self._intro_nodes: list = []
        self._intro_spotlight = None
        self._intro_spawn_pos = None
        self._intro_finished = False
        self._intro_freeze_timer: bs.Timer | None = None
        self._player_spawn_positions: dict = {}
        self._player_intro_return_pos: dict = {}

    NORMAL_TINT = (0.6, 0.7, 0.8)
    NORMAL_AMBIENT = (1.15, 1.25, 1.6)

    def spawn_player(self, player: Player, connect_controls: bool = True) -> bs.Actor:
        if isinstance(self.session, bs.DualTeamSession):
            position = self.map.get_start_position(player.team.id)
        else:
            position = self.map.get_ffa_start_position(self.players)

        self._player_spawn_positions[player] = position

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

        if connect_controls:
            spaz.connect_controls_to_player()
        spaz.handlemessage(bs.StandMessage(position, random.uniform(0, 360)))

        self._spawn_sound.play(1, position=spaz.node.position)

        return spaz

    def _connect_all_controls(self) -> None:
        for player in self.players:
            if player.actor:
                try:
                    player.actor.connect_controls_to_player()
                except Exception:
                    pass

    def _update_boss_player_points(self):
        if not self.boss:
            return
        player_pts = []
        for player in self.players:
            if player.is_alive() and player.actor and player.actor.node:
                player_pts.append((
                    bs.Vec3(player.actor.node.position),
                    bs.Vec3(player.actor.node.velocity)
                ))
        self.boss.set_player_points(player_pts)

    def on_begin(self):
        super().on_begin()
        self.setup_standard_time_limit(self._time_limit)
        self.setup_standard_powerup_drops()

        try:
            gnode = self.globalsnode
            if gnode:
                gnode.tint = (0.6, 0.7, 0.8)
                gnode.ambient_color = (1.15, 1.25, 1.6)
                gnode.vignette_outer = (0.66, 0.67, 0.73)
                gnode.vignette_inner = (0.93, 0.93, 0.95)
        except Exception:
            pass
        FadeEffect((0.6, 0.7, 0.8))

        self._player_count = max(1, len([p for p in self.players if p]))

        self._players_joined = True
        self._spawn_players(connect_controls=False)

        self._start_boss_intro()

    def on_player_join(self, player: Player) -> None:
        if self.has_begun() and self._players_joined:
            return
        super().on_player_join(player)

    def _spawn_players(self, connect_controls: bool = True):
        for player in self.players:
            if not player.is_alive():
                self.spawn_player(player, connect_controls=connect_controls)

    def _start_boss_intro(self) -> None:
        try:
            point = self.map.get_flag_position(None)
            boss_spawn_pos = (point[0], point[1] + 3.5, point[2])
        except Exception:
            boss_spawn_pos = (0.0, 3.5, 0.0)
        self._intro_spawn_pos = boss_spawn_pos

        gnode = self.globalsnode
        if gnode:
            self._pre_intro_tint = self.NORMAL_TINT
            bs.animate_array(gnode, 'tint', 3, {
                0: gnode.tint,
                0.6: (0.015, 0.015, 0.02),
            })

        self._intro_saved_aoi_players: list = []
        for player in self.players:
            actor = player.actor
            if actor and getattr(actor, 'node', None) and actor.node.exists():
                try:
                    actor.node.is_area_of_interest = False
                    self._intro_saved_aoi_players.append(actor.node)
                except Exception:
                    pass

        self._intro_spotlight = bs.newnode('light', attrs={
            'position': boss_spawn_pos,
            'color': (1.2, 0.3, 1.4),
            'radius': 0.4,
            'height_attenuated': False,
            'intensity': 0.0,
        })
        bs.animate(self._intro_spotlight, 'intensity', {0: 0.0, 0.5: 4.0, 2.6: 4.0, 3.0: 0.5})

        core = bs.newnode('prop', attrs={
            'body': 'sphere',
            'position': boss_spawn_pos,
            'mesh': bs.getmesh('shield'),
            'color_texture': bs.gettexture('black'),
            'shadow_size': 0.0,
            'reflection_scale': [0.0],
            'gravity_scale': 0.0,
            'density': 0.0,
            'body_scale': 0.0001,
            'mesh_scale': 0.001,
            'is_area_of_interest': True,
        })
        ring = bs.newnode('shield', attrs={
            'position': boss_spawn_pos,
            'color': (6, 1, 8),
            'radius': 0.1,
        })
        bs.animate(core, 'mesh_scale', {0: 0.001, 0.7: 1.1, 2.4: 1.1, 2.9: 0.001})
        bs.animate(ring, 'radius', {0: 0.1, 0.7: 1.4, 2.4: 1.4, 2.9: 0.1})

        hum_sound = bs.newnode('sound', attrs={'sound': bs.getsound('gravelSkid')})
        bs.animate(hum_sound, 'volume', {0: 0, 0.6: 1.0, 2.4: 1.0, 3.0: 0})

        self._intro_nodes = [core, ring, hum_sound]

        bs.camerashake(intensity=0.5)

        bs.timer(3.0, self._finish_boss_intro)

    def _finish_boss_intro(self) -> None:
        if self._game_over:
            return

        if self._intro_spotlight and self._intro_spotlight.exists():
            bs.animate(self._intro_spotlight, 'intensity',
                      {0: self._intro_spotlight.intensity, 0.12: 9.0, 0.4: 0.0})
            bs.timer(0.5, self._intro_spotlight.delete)

        if self._intro_spawn_pos:
            bs.emitfx(position=self._intro_spawn_pos, count=80, scale=2.5, spread=3.0, chunk_type='spark')

        bs.cameraflash()
        bs.camerashake(intensity=3.0)
        bs.getsound('gravelSkid').play()

        for node in self._intro_nodes:
            if node and node.exists():
                bs.timer(0.05, node.delete)
        self._intro_nodes = []

        gnode = self.globalsnode
        if gnode:
            bs.animate_array(gnode, 'tint', 3, {0: gnode.tint, 0.8: self._pre_intro_tint})

        for node in getattr(self, '_intro_saved_aoi_players', []):
            if node and node.exists():
                try:
                    node.is_area_of_interest = True
                except Exception:
                    pass
        self._intro_saved_aoi_players = []

        self.boss = UFO(hitpoints=self._boss_health)
        self._check_timer = bs.Timer(0.25, self._check_game_state, repeat=True)
        self._boss_update_timer = bs.Timer(0.1, self._update_boss_player_points, repeat=True)

        self._connect_all_controls()
        self._intro_finished = True

    def _check_game_state(self):
        if self._game_over:
            return

        mid_triggered = bool(getattr(self.boss, '_mid_health_triggered', False)) if self.boss else False

        if mid_triggered:
            mid_ready = bool(getattr(self.boss, '_mid_boss_ready', False)) if self.boss else False
            mid_bot = getattr(self.boss, '_mid_boss_bot', None) if self.boss else None

            if mid_ready and mid_bot is not None:
                bot_alive = False
                bot_hp = 0
                try:
                    if mid_bot.node and mid_bot.node.exists():
                        bot_alive = True
                        bot_hp = int(getattr(mid_bot, 'hitpoints', 0))
                except Exception:
                    bot_alive = False

                if (not bot_alive or bot_hp <= 0) and not self._game_won:
                    self._game_won = True
                    self._game_over = True
                    if self._check_timer:
                        self._check_timer = None
                    if self._boss_update_timer:
                        self._boss_update_timer = None
                    self._win_timer = bs.timer(self._game_end_delay, self._end_game_won)
                    return
        else:
            if (self.boss and not self._game_won and not self._boss_died
                    and not getattr(self.boss, '_mid_health_triggered', False)):
                ufo_dead = bool(getattr(self.boss, '_dead', False))
                if ufo_dead:
                    self._boss_died = True
                    self._game_won = True
                    self._game_over = True
                    if self._check_timer:
                        self._check_timer = None
                    if self._boss_update_timer:
                        self._boss_update_timer = None
                    self._win_timer = bs.timer(self._game_end_delay, self._end_game_won)
                    return

        alive_players = [p for p in self.players if p.is_alive()]
        if len(alive_players) == 0 and not self._game_over:
            self._game_over = True
            if self._check_timer:
                self._check_timer = None
            if self._boss_update_timer:
                self._boss_update_timer = None

            if self.boss and self.boss.is_alive and not self._boss_died:
                self._boss_died = True
                self.boss.handlemessage(bs.DieMessage())

            if self._lose_timer:
                self._lose_timer = None
            self._lose_timer = bs.timer(self._game_end_delay, self._end_game_lose)

    def _end_game_won(self):
        results = bs.GameResults()
        for team in self.teams:
            results.set_team_score(team, 1)
        bs.cameraflash()
        bs.getsound('score').play()
        self.end(results=results, announce_delay=3.0)

    def _end_game_lose(self):
        results = bs.GameResults()
        for team in self.teams:
            results.set_team_score(team, 0)
        bs.getsound('error').play()
        self.end(results=results, announce_delay=3.0)

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.PlayerDiedMessage):
            super().handlemessage(msg)
        else:
            super().handlemessage(msg)

    def end(self, results: bs.GameResults = None, **kwargs) -> None:
        if self.boss and self.boss.is_alive:
            self.boss.handlemessage(bs.DieMessage())
        super().end(results, **kwargs)


# ba_meta export babase.Plugin
class BSRUSHPRESENT(babase.Plugin):
    def on_app_running(self):
        pass