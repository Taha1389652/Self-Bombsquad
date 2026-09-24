# Released under the MIT License. See LICENSE for details.
# ba_meta require api 9

from __future__ import annotations

from typing import TYPE_CHECKING

import bascenev1 as bs
import bauiv1 as bui
import babase
from bascenev1lib.actor.playerspaz import PlayerSpaz
from bascenev1lib.actor.scoreboard import Scoreboard
from bascenev1lib.gameutils import SharedObjects
from bascenev1lib.maps import *
from bascenev1lib.actor.popuptext import PopupText
from bascenev1 import _map
from bascenev1lib.actor.spaz import Spaz
import random

from bascenev1lib import maps

if TYPE_CHECKING:
    from typing import Any, Sequence, Dict, Type, List, Optional, Union



def getlanguage(text, sub: str = ''):
    lang = bs.app.lang.language
    translate = {
        "Name":
        {"Spanish": "Baloncesto",
         "English": "Basketball",
         "Portuguese": "Basquetebol"},
        "Info":
        {"Spanish": "Anota una canasta.",
         "English": "Score a hoop.",
         "Portuguese": "Fazer uma cesta."},
        "Info-Short":
        {"Spanish": f"Anota {sub} canastas",
         "English": f"Score {sub} hoops.",
         "Portuguese": f"Marcar {sub} cestas."},
        "Info-Short No Caps":
        {"Spanish": f"anota {sub} canastas",
         "English": f"score {sub} hoops",
         "Portuguese": f"marcar {sub} cestas"},
        "Info One Basket":
        {"Spanish": f"anota una canasta",
         "English": f"score a hoop",
         "Portuguese": f"fazer uma cesta"},
        "S: Powerups":
        {"Spanish": "Aparecer Potenciadores",
         "English": "Powerups Spawn",
         "Portuguese": "Habilitar Potenciadores"},
        "S: Velocity":
            {"Spanish": "Activar velocidad",
             "English": "Enable speed",
             "Portuguese": "Ativar velocidade"},
        "S: Invincible":
            {"Spanish": "Modo invencible",
             "English": "Invincible Mode",
             "Portuguese": "Modo Invencível"},
    }

    languages = ['Spanish', 'Portuguese', 'English']
    if lang not in languages:
        lang = 'English'

    if text not in translate:
        return text
    return translate[text][lang]


class BallDiedMessage:
    def __init__(self, ball: Ball):
        self.ball = ball


class Ball(bs.Actor):
    def __init__(self, position: Sequence[float] = (0.0, 1.0, 0.0)):
        super().__init__()
        shared = SharedObjects.get()
        activity = self.getactivity()
        velocty = (0.0, 3, 0.0)
        _scale = 1.2

        self._spawn_pos = (position[0], position[1] + 0.5, position[2])
        self.last_players_to_touch: Dict[int, Player] = {}
        self.scored = False

        assert activity is not None
        assert isinstance(activity, BasketGame)

        pmats = [shared.object_material, activity.ball_material]
        self.node = bs.newnode('prop',
                               delegate=self,
                               attrs={
                                   'mesh': activity.ball_mesh,
                                   'color_texture': activity.ball_tex,
                                   'body': 'sphere',
                                   'reflection': 'soft',
                                   'body_scale': 1.0 * _scale,
                                   'reflection_scale': [0.2],
                                   'shadow_size': 1.0,
                                   'gravity_scale': 1,
                                   'density': max(0.4 * _scale, 0.3),
                                   'position': self._spawn_pos,
                                   'velocity': velocty,
                                   'materials': pmats})
        self.scale = scale = 0.25 * _scale
        bs.animate(self.node, 'mesh_scale', {0: 0, 0.2: scale*1.3, 0.26: scale})

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.DieMessage):
            assert self.node
            self.node.delete()
            activity = self._activity()
            if activity and not msg.immediate:
                activity.handlemessage(BallDiedMessage(self))

        elif isinstance(msg, bs.OutOfBoundsMessage):
            assert self.node
            self.node.position = self._spawn_pos
            self.node.velocity = (0.0, 0.0, 0.0)

        elif isinstance(msg, bs.HitMessage):
            assert self.node
            assert msg.force_direction is not None
            self.node.handlemessage(
                'impulse',
                msg.pos[0],
                msg.pos[1],
                msg.pos[2],
                msg.velocity[0],
                msg.velocity[1],
                msg.velocity[2],
                1.0 * msg.magnitude,
                1.0 * msg.velocity_magnitude,
                msg.radius,
                0,
                msg.force_direction[0],
                msg.force_direction[1],
                msg.force_direction[2],
            )
            s_player = msg.get_source_player(Player)
            if s_player is not None:
                activity = self._activity()
                if activity:
                    if s_player in activity.players:
                        self.last_players_to_touch[s_player.team.id] = s_player
        else:
            super().handlemessage(msg)
            
class Text(bs.Actor):
    def __init__(self, text: Str='' , scale: Float=1.0, position: Tuple(Float, Float, Float)=(0,0,0), color: Tuple(Float, Float, Float)=(1,0,0), shadow: float=1.0, h_align=None, v_attach=None, in_world=True):
        super().__init__()
        activity = bs.getactivity()
        self.node = bs.newnode('text', attrs={
            'text': text,
            'color': color,
            'opacity':1, 
            'position': position, 
            'scale': scale, 
            'in_world': in_world,
            'shadow': shadow
            })
        if h_align is not None:
            self.node.h_align = h_align
        if v_attach is not None:
            self.node.v_attach = v_attach

    def delete(self) -> None:
        self.node.delete()



class Player(bs.Player['Team']):
    """Our player type for this game."""


class Team(bs.Team[Player]):
    """Our team type for this game."""

    def __init__(self) -> None:
        self.score = 0


class Points:
    postes = dict()
    # 10.736066818237305, 0.3002409040927887, 0.5281256437301636
    postes['pal_0'] = (10.64702320098877, 0.0000000000000000, 0.0000000000000000)
    postes['pal_1'] = (-10.64702320098877, 0.0000000000000000, 0.0000000000000000)

# ba_meta export bascenev1.GameActivity


class BasketGame(bs.TeamGameActivity[Player, Team]):

    name = getlanguage('Name')
    description = getlanguage('Info')
    available_settings = [
        bs.IntSetting(
            'Score to Win',
            min_value=1,
            default=10,
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
                ('12 Minutes', 720),
                ('20 Minutes', 1200),
                ('48 Minutes', 2880),
            ],
            default=720,
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
            default=0.25,
        ),
        bs.BoolSetting(getlanguage('S: Powerups'), default=False),
        bs.BoolSetting(getlanguage('S: Velocity'), default=False),
        bs.BoolSetting(getlanguage('S: Invincible'), default=True),
        bs.BoolSetting('Epic Mode', default=True),
    ]
    default_music = bs.MusicType.HOCKEY

    @classmethod
    def supports_session_type(cls, sessiontype: Type[bs.Session]) -> bool:
        return issubclass(sessiontype, bs.DualTeamSession)

    @classmethod
    def get_supported_maps(cls, sessiontype: Type[bs.Session]) -> List[str]:
        return ['BasketBall Stadium OG', 'BasketBall Stadium OG V2', 'Basketball Stadium']

    def __init__(self, settings: dict):
        super().__init__(settings)
        shared = SharedObjects.get()
        self._scoreboard = Scoreboard()
        self._cheer_sound = bs.getsound('cheer')
        self._chant_sound = bs.getsound('crowdChant')
        self._foghorn_sound = bs.getsound('foghorn')
        self._swipsound = bs.getsound('swip')
        self._whistle_sound = bs.getsound('refWhistle')
        self.ball_mesh = bs.getmesh('shield')
        self.ball_tex = bs.gettexture('circleOutlineNoAlpha')
        self._ball_sound = bs.getsound('footImpact01')
        self._powerups = bool(settings[getlanguage('S: Powerups')])
        self.invincible_mode = bool(settings[getlanguage('S: Invincible')])
        self._speed = bool(settings[getlanguage('S: Velocity')])
        self._epic_mode = bool(settings['Epic Mode'])
        self.slow_motion = self._epic_mode

        self.ball_material = bs.Material()
        self.ball_material.add_actions(actions=(('modify_part_collision',
                                                 'friction', 0.5)))
        self.ball_material.add_actions(conditions=('they_have_material',
                                                   shared.pickup_material),
                                       actions=('modify_part_collision',
                                                'collide', True))
        self.ball_material.add_actions(
            conditions=(
                ('we_are_younger_than', 100),
                'and',
                ('they_have_material', shared.object_material),
            ),
            actions=('modify_node_collision', 'collide', False),
        )
        self.ball_material.add_actions(conditions=('they_have_material',
                                                   shared.footing_material),
                                       actions=('impact_sound',
                                                self._ball_sound, 0.2, 5))
        self.ball_material.add_actions(conditions=('they_have_material',
                                                   shared.footing_material),
                                       actions=('roll_sound',
                                                bs.getsound('gravelSkid'), 0.2, 0.25))

        # Keep track of which player last touched the ball
        self.ball_material.add_actions(
            conditions=('they_have_material', shared.player_material),
            actions=(('call', 'at_connect',
                      self._handle_ball_player_collide), ))

        self._score_region_material = bs.Material()
        self._score_region_material.add_actions(
            conditions=('they_have_material', self.ball_material),
            actions=(('modify_part_collision', 'collide',
                      True), ('modify_part_collision', 'physical', False),
                     ('call', 'at_connect', self._handle_score)))
        self._ball_spawn_pos: Optional[Sequence[float]] = None
        self._score_regions: Optional[List[bs.NodeActor]] = None
        self._ball: Optional[Ball] = None
        self._score_to_win = int(settings['Score to Win'])
        self._time_limit = float(settings['Time Limit'])
        self.emojis = ["\ue043","\ue04f",'\ue046','\ue048'] # for scoring suspense
        self.expressions = ['LESSFUGCKINGO!','FAAH!','BOOOM!','EEEAAAOOH!', 'HEE HEE!', 'RAAAAOH!', 'FE!N!']

    def get_instance_description(self) -> Union[str, Sequence]:
        if self._score_to_win == 1:
            return getlanguage('Info', sub=self._score_to_win)
        return getlanguage('Info-Short', sub=self._score_to_win)
    

    def get_instance_description_short(self) -> Union[str, Sequence]:
        if self._score_to_win == 1:
            return getlanguage('Info One Basket', sub=self._score_to_win)
        return getlanguage('Info-Short No Caps', sub=self._score_to_win)
    

    def on_begin(self) -> None:
        super().on_begin()

        self.setup_standard_time_limit(self._time_limit)

        if self._powerups:
            self.setup_standard_powerup_drops()

        self._ball_spawn_pos = self.map.get_flag_position(None)
        self._spawn_ball()
        self.team1 = self.teams[0]
        self.team2 = self.teams[1]
        ###
        vs_text = bs.newnode('text',
                 attrs={
                    'position': (0,325),
                    'text': 'VS',
                    'color': (1,1,1),
                    'h_align': 'center','v_align': 'center', 'vr_depth': 410, 'maxwidth': 600, 'shadow': 0.9, 'flatness': 1.0, 'scale':3, 'h_attach': 'center', 'v_attach': 'bottom', 'opacity': 0.9})
        team1 = bs.newnode('text',
                attrs={
                    'position': (-1500,350),
                    'text': self.team1.name,
                    'color': self.team1.color,
                    'h_align': 'center','v_align': 'center', 'vr_depth': 410, 'maxwidth': 600, 'shadow': 1.0, 'flatness': 1.0, 'scale':1.5, 'h_attach': 'center', 'v_attach': 'bottom', 'big': True})
        team2 = bs.newnode('text',
                attrs={
                    'position': (1500,70),
                    'text': self.team2.name,
                    'color': self.team2.color,
                    'h_align': 'center','v_align': 'center', 'vr_depth': 410, 'maxwidth': 600, 'shadow': 1.0, 'flatness': 1.0, 'scale':1.5, 'h_attach': 'center', 'v_attach': 'bottom', 'big': True})
        bs.animate_array(team1, 'position', 2, {0:(-1500,350), 1:(-1500,350), 2:(-250,350), 3:(300,350), 4:(1500,350)}, loop=False)
        bs.animate_array(team2, 'position', 2, {0:(1500,70), 1:(1500,70), 2:(250,70), 3:(-300,70), 4:(-1500,70)}, loop=False)
        bs.animate(vs_text, 'opacity', {0:0, 1:0, 2:0.9, 2.1:1, 2.15:0.9, 2.20:1, 2.25:0.9, 2.30:1, 2.35:0.9, 2.40:1, 2.45:0.9, 2.50:1, 2.55:0.9, 4:0}, loop=False)
        bs.timer(5, team1.delete)
        bs.timer(5, team2.delete)
        bs.timer(5, vs_text.delete)
        
        defs = self.map.defs
        self._score_regions = []
        self._score_regions.append(
            bs.NodeActor(
                bs.newnode('region',
                           attrs={
                               'position': defs.boxes['goal1'][0:3],
                               'scale': defs.boxes['goal1'][6:9],
                               'type': 'box',
                               'materials': []
                           })))
        self._score_regions.append(
            bs.NodeActor(
                bs.newnode('region',
                           attrs={
                               'position': defs.boxes['goal2'][0:3],
                               'scale': defs.boxes['goal2'][6:9],
                               'type': 'box',
                               'materials': []
                           })))
        self._update_scoreboard()
        self._chant_sound.play()
        
        for id, team in enumerate(self.teams):
            self.postes(id)

    def on_team_join(self, team: Team) -> None:
        self._update_scoreboard()

    def _handle_ball_player_collide(self) -> None:
        collision = bs.getcollision()
        try:
            ball = collision.sourcenode.getdelegate(Ball, True)
            player = collision.opposingnode.getdelegate(PlayerSpaz,
                                                        True).getplayer(
                                                            Player, True)
        except bs.NotFoundError:
            return

        ball.last_players_to_touch[player.team.id] = player

    def _kill_ball(self) -> None:
        self._ball = None

    def _handle_score(self, team_index: int = None) -> None:
        assert self._ball is not None
        assert self._score_regions is not None
        if self._ball.scored:
            return

        region = bs.getcollision().sourcenode
        index = 0
        scorer_celebration_txt = random.choice(self.expressions) + ' ' + random.choice(self.emojis)
        for index in range(len(self._score_regions)):
            if region == self._score_regions[index].node:
                break

        if team_index is not None:
            index = team_index

        for team in self.teams:
            if team.id == index:
                scoring_team = team
                team.score += 1
                team_color = team.color

                for player in team.players:
                    if player.actor:
                        player.actor.handlemessage(bs.CelebrateMessage(2.0))

                if (scoring_team.id in self._ball.last_players_to_touch
                        and self._ball.last_players_to_touch[scoring_team.id]):
                    self.scorer = self._ball.last_players_to_touch[scoring_team.id]
                    self.stats.player_scored(self.scorer,100,color=team_color)
                    glow_color = (10, 10, 10)
                    prev_color = self.scorer.actor.node.color
                    bs.animate_array(self.scorer.actor.node, 'color', 3, {0:prev_color, 0.10:glow_color, 1.5:prev_color})

                    self.stats.player_scored(
                        self._ball.last_players_to_touch[scoring_team.id],
                        100, big_message=False)
                    bs.broadcastmessage(f"Scorer: {self.scorer.getname()}", color=(0,1,0)) 
                    pos = self.scorer.actor.node.position
                    self.scorer_txt = Text(scorer_celebration_txt, 0.020, (pos[0], pos[1]+1.25, pos[2]), team_color,2)
                    bs.animate(self.scorer_txt.node, 'opacity', {0:0, 0.10:1, 1.5:0})     
                    self.follow_scorer()
                    

                if team.score >= self._score_to_win:
                    self.end_game()

        # self._foghorn_sound.play()
        self._cheer_sound.play()

        self._ball.scored = True

        # Kill the ball (it'll respawn itself shortly).
        bs.timer(1.0, self._kill_ball)

        light = bs.newnode('light',
                           attrs={
                               'position': bs.getcollision().position,
                               'height_attenuated': False,
                               'color': (1, 0, 0)
                           })
        bs.animate(light, 'intensity', {0: 0, 0.5: 1, 1.0: 0}, loop=True)
        bs.timer(1.0, light.delete)
        gnode = bs.getactivity().globalsnode
        bs.animate_array(gnode, 'tint', 3, {0:gnode.tint, 0.07:(0, 0, 0) , 0.30:gnode.tint})
        
        bs.cameraflash(duration=10.0)
        self._update_scoreboard()
        PopupText(
                    position=(-0.0, -2.5, -3.5),
                    text='SHOOTTT!!!',
                    random_offset=0.0,
                    scale=5.0,
                    color=team_color,
                ).autoretain()
        # Big Bang 
        explosion = bs.newnode('explosion',attrs={
            'position': bs.getcollision().position, 
            'color': team_color, 
            'radius':4 
            })

    def end_game(self) -> None:
        results = bs.GameResults()
        for team in self.teams:
            results.set_team_score(team, team.score)
        self.end(results=results)
        
    def _update_scoreboard(self) -> None:
        winscore = self._score_to_win
        for id, team in enumerate(self.teams):
            self._scoreboard.set_team_value(team, team.score, winscore)
            # self.postes(id)

    def spawn_player(self, player: Player) -> bs.Actor:
        if self.invincible_mode:
            spaz = self.spawn_player_spaz(player)
            spaz.equip_boxing_gloves()
            spaz.impact_scale = 0

        if self._speed:
            spaz.node.hockey = True
        return spaz

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.PlayerDiedMessage):
            super().handlemessage(msg)
            self.respawn_player(msg.getplayer(Player))
        elif isinstance(msg, BallDiedMessage):
            if not self.has_ended():
                bs.timer(3.0, self._spawn_ball)
        else:
            super().handlemessage(msg)
            
    def follow_scorer(self) -> None:
        if not self.scorer_txt.node:
            return
        pos = self.scorer.actor.node.position
        self.scorer_txt.node.position = (pos[0], pos[1] + 1.5, pos[2])
        bs.timer(0, self.follow_scorer)

    def postes(self, team_id: int):
        if not hasattr(self._map, 'poste_'+str(team_id)):
            setattr(self._map, 'poste_'+str(team_id),
                    Palos(team=team_id,
                          position=Points.postes['pal_' +
                                                 str(team_id)]).autoretain())

    def _flash_ball_spawn(self) -> None:
        light = bs.newnode('light',
                           attrs={
                               'position': self._ball_spawn_pos,
                               'height_attenuated': False,
                               'color': (1, 0, 0)
                           })
        bs.animate(light, 'intensity', {0.0: 0, 0.25: 1, 0.5: 0}, loop=False)
        bs.timer(1.0, light.delete)

    def _spawn_ball(self) -> None:
        self._swipsound.play()
        self._whistle_sound.play()
        self._flash_ball_spawn()
        assert self._ball_spawn_pos is not None
        self._ball = Ball(position=self._ball_spawn_pos)


class Aro(bs.Actor):
    def __init__(self, team: int = 0,
                 position: Sequence[float] = (0.0, 1.0, 0.0)):
        super().__init__()
        act = self.getactivity()
        shared = SharedObjects.get()
        setattr(self, 'team', team)
        setattr(self, 'locs', [])

        # Material Para; Traspasar Objetos
        self.no_collision = bs.Material()
        self.no_collision.add_actions(
            actions=(('modify_part_collision', 'collide', False)))

        self.collision = bs.Material()
        self.collision.add_actions(
            actions=(('modify_part_collision', 'collide', True)))

        # Score
        self._score_region_material = bs.Material()
        self._score_region_material.add_actions(
            conditions=('they_have_material', act.ball_material),
            actions=(('modify_part_collision', 'collide',
                      True), ('modify_part_collision', 'physical', False),
                     ('call', 'at_connect', self._annotation)))

        self._spawn_pos = (position[0], position[1], position[2])
        self._materials_region0 = [self.collision,
                                   shared.footing_material]

        mesh = None
        tex = bs.gettexture('null')

        pmats = [self.no_collision]
        self.node = bs.newnode('prop',
                               delegate=self,
                               attrs={
                                   'mesh': mesh,
                                   'color_texture': tex,
                                   'body': 'box',
                                   'reflection': 'soft',
                                   'reflection_scale': [1.5],
                                   'shadow_size': 0.1,
                                   'position': self._spawn_pos,
                                   'materials': pmats})

        self.scale = scale = 1.4
        bs.animate(self.node, 'mesh_scale', {0:  0})

        pos = (position[0], position[1]+0.6, position[2])
        self.regions: List[bs.Node] = [
            bs.newnode('region',
                       attrs={'position': position,
                              'scale': (0.6, 0.05, 0.6),
                              'type': 'box',
                              'materials': self._materials_region0}),

            bs.newnode('region',
                       attrs={'position': pos,
                              'scale': (0.5, 0.3, 0.9),
                              'type': 'box',
                              'materials': [self._score_region_material]})
        ]
        self.regions[0].connectattr('position', self.node, 'position')
        # self.regions[0].connectattr('position', self.regions[1], 'position')

        locs_count = 9
        pos = list(position)

        try:
            id = 0 if team == 1 else 1
            color = act.teams[id].color
        except:
            color = (1, 1, 1)

        while locs_count > 1:
            scale = (1.5 * 0.1 * locs_count) + 0.8

            self.locs.append(bs.newnode('locator',
                                        owner=self.node,
                                        attrs={'shape': 'circleOutline',
                                               'position': pos,
                                               'color': color,
                                               'opacity': 1.0,
                                               'drawShadow': False,
                                               'size': [scale],
                                               'draw_beauty': True,
                                               'additive': False}))

            pos[1] -= 0.1
            locs_count -= 1

    def _annotation(self):
        assert len(self.regions) >= 2
        ball = self.getactivity()._ball

        if ball:
            p = self.regions[0].position
            ball.node.position = p
            ball.node.velocity = (0.0, 0.0, 0.0)

        act = self.getactivity()
        act._handle_score(self.team)

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.DieMessage):
            if self.node.exists():
                self.node.delete()
        else:
            super().handlemessage(msg)


class Cuadro(bs.Actor):
    def __init__(self, team: int = 0,
                 position: Sequence[float] = (0.0, 1.0, 0.0)):
        super().__init__()
        act = self.getactivity()
        shared = SharedObjects.get()
        setattr(self, 'locs', [])

        self.collision = bs.Material()
        self.collision.add_actions(
            actions=(('modify_part_collision', 'collide', True)))

        pos = (position[0], position[1]+0.9, position[2]+1.5)
        self.region: bs.Node = bs.newnode('region',
                                          attrs={'position': pos,
                                                 'scale': (0.5, 2.7, 2.5),
                                                 'type': 'box',
                                                 'materials': [self.collision,
                                                               shared.footing_material]})

        # self.shield = bs.newnode('shield', attrs={'radius': 1.0, 'color': (0,10,0)})
        # self.region.connectattr('position', self.shield, 'position')

        position = (position[0], position[1], position[2]+0.09)
        pos = list(position)
        oldpos = list(position)
        old_count = 14

        count = old_count
        count_y = 9

        try:
            id = 0 if team == 1 else 1
            color = act.teams[id].color
        except:
            color = (1, 1, 1)

        while (count_y != 1):

            while (count != 1):
                pos[2] += 0.19

                self.locs.append(
                    bs.newnode('locator',
                               owner=self.region,
                               attrs={'shape': 'circle',
                                      'position': pos,
                                      'size': [0.5],
                                      'color': color,
                                      'opacity': 1.0,
                                      'drawShadow': False,
                                      'draw_beauty': True,
                                      'additive': False}))
                count -= 1

            count = old_count
            pos[1] += 0.2
            pos[2] = oldpos[2]
            count_y -= 1

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.DieMessage):
            if self.node.exists():
                self.node.delete()
        else:
            super().handlemessage(msg)


class Palos(bs.Actor):
    def __init__(self, team: int = 0,
                 position: Sequence[float] = (0.0, 1.0, 0.0)):
        super().__init__()
        shared = SharedObjects.get()
        activity = self.getactivity()
        self._pos = position
        self.aro = None
        self.cua = None

        # Material Para; Traspasar Objetos
        self.no_collision = bs.Material()
        self.no_collision.add_actions(
            actions=(('modify_part_collision', 'collide', False)))

        #
        self.collision = bs.Material()
        self.collision.add_actions(
            actions=(('modify_part_collision', 'collide', True)))

        # Spawn just above the provided point.
        self._spawn_pos = (position[0], position[2]+2.5, position[2])

        mesh = bs.getmesh('flagPole')
        tex = bs.gettexture('flagPoleColor')

        pmats = [self.no_collision]
        self.node = bs.newnode('prop',
                               delegate=self,
                               attrs={
                                   'mesh': mesh,
                                   'color_texture': tex,
                                   'body': 'puck',
                                   'reflection': 'soft',
                                   'reflection_scale': [2.6],
                                   'shadow_size': 0,
                                   'is_area_of_interest': True,
                                   'position': self._spawn_pos,
                                   'materials': pmats
                               })
        self.scale = scale = 4.0
        bs.animate(self.node, 'mesh_scale', {0:  scale})

        self.loc = bs.newnode('locator',
                              owner=self.node,
                              attrs={'shape': 'circle',
                                     'position': position,
                                     'size': [3.0],
                                     'drawShadow': True,
                                     'color': (0.15, 0.15, 0.15),
                                     'opacity': 0.5,
                                     'draw_beauty': False,
                                     'additive': True})

        self._y = _y = 0.001
        _x = -0.25 if team == 1 else 0.25
        _pos = (position[0]+_x, position[1]-1.5 + _y, position[2])
        self.region = bs.newnode('region',
                                 attrs={
                                     'position': _pos,
                                     'scale': (0.4, 8, 0.4),
                                     'type': 'box',
                                     'materials': [self.collision]})
        self.region.connectattr('position', self.node, 'position')

        _y = self._y
        position = self._pos
        if team == 0:
            pos = (position[0]-0.8, position[1] + 2.0 + _y, position[2])
        else:
            pos = (position[0]+0.8, position[1] + 2.0 + _y, position[2])

        if self.aro is None:
            self.aro = Aro(team, pos).autoretain()

        if self.cua is None:
            pos = (position[0], position[1] + 1.8 + _y, position[2]-1.4)
            self.cua = Cuadro(team, pos).autoretain()

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.DieMessage):
            if self.node.exists():
                self.node.delete()
        else:
            super().handlemessage(msg)


class BasketMap(maps.FootballStadium):
    name = 'BasketBall Stadium OG'

    @classmethod
    def get_play_types(cls) -> List[str]:
        """Return valid play types for this map."""
        return []

    def __init__(self) -> None:
        super().__init__()

        gnode = bs.getactivity().globalsnode
        gnode.tint = [(0.806, 0.8, 1.0476), (1.3, 1.2, 1.0)][0]
        gnode.ambient_color = (1.3, 1.2, 1.0)
        gnode.vignette_outer = (0.57, 0.57, 0.57)
        gnode.vignette_inner = (0.9, 0.9, 0.9)
        gnode.vr_camera_offset = (0, -0.8, -1.1)
        gnode.vr_near_clip = 0.5


class BasketMapV2(maps.HockeyStadium):
    name = 'BasketBall Stadium OG V2'

    def __init__(self) -> None:
        super().__init__()

        shared = SharedObjects.get()
        self.node.materials = [shared.footing_material]
        self.node.collision_mesh = bs.getcollisionmesh('footballStadiumCollide')
        self.node.mesh = None
        self.stands.mesh = None
        self.floor.reflection = 'soft'
        self.floor.reflection_scale = [1.6]
        self.floor.color = (1.1, 0.05, 0.8)

        self.background = bs.newnode('terrain',
                                     attrs={'mesh': bs.getmesh('thePadBG'),
                                            'lighting': False,
                                            'background': True,
                                            'color': (1.0, 0.2, 1.0),
                                            'color_texture': bs.gettexture('menuBG')})

        gnode = bs.getactivity().globalsnode
        gnode.floor_reflection = True
        gnode.debris_friction = 0.3
        gnode.debris_kill_height = -0.3
        gnode.tint = [(1.2, 1.3, 1.33), (0.7, 0.9, 1.0)][1]
        gnode.ambient_color = (1.15, 1.25, 1.6)
        gnode.vignette_outer = (0.66, 0.67, 0.73)
        gnode.vignette_inner = (0.93, 0.93, 0.95)
        gnode.vr_camera_offset = (0, -0.8, -1.1)
        gnode.vr_near_clip = 0.5
        self.is_hockey = False

        ##################
        self.collision = bs.Material()
        self.collision.add_actions(
            actions=(('modify_part_collision', 'collide', True)))

        self.regions: List[bs.Node] = [
            bs.newnode('region',
                       attrs={'position': (12.676897048950195, 0.2997918128967285, 5.583303928375244),
                              'scale': (1.01, 12, 28),
                              'type': 'box',
                              'materials': [self.collision]}),

            bs.newnode('region',
                       attrs={'position': (11.871315956115723, 0.29975247383117676, 5.711406707763672),
                              'scale': (50, 12, 0.9),
                              'type': 'box',
                              'materials': [self.collision]}),

            bs.newnode('region',
                       attrs={'position': (-12.776557922363281, 0.30036890506744385, 4.96237850189209),
                              'scale': (1.01, 12, 28),
                              'type': 'box',
                              'materials': [self.collision]}),
        ]


bs._map.register_map(BasketMap)
bs._map.register_map(BasketMapV2)

class BasketballStadiumMapData():
    points = {}
    boxes = {}

    boxes['area_of_interest_bounds'] = (
        (0.0, 1.185751251, 0.4326226188)
        + (0.0, 0.0, 0.0)
        + (70, 70, 70)
    )
    boxes['edge_box'] = (
        (-0.103873591, 0.4133341891, 0.4294651013)
        + (0.0, 0.0, 0.0)
        + (22.48295719, 1.290242794, 8.990252454)
    )
    points['ffa_spawn1'] =(-0.08015551329, 0.02275111462, -4.373674593) + (
    8.895057015,
    1.0,
    0.444350722,
    )
    points['ffa_spawn2'] =  (-0.08015551329, 0.02275111462, 4.076288941) + (
    8.895057015,
    1.0,
    0.444350722,
    )
    boxes['map_bounds'] = (
        (0.0, 1.185751251, 0.4326226188)
        + (0.0, 0.0, 0.0)
        + (42.09506485, 22.81173179, 29.76723155)
    )
    points['flag1'] = (-11.21689747, 0.09527878981, -0.07659307272)
    points['flag2'] = (11.08204909, 0.04119542459, -0.07659307272)
    points['flag_default'] = (-0.01690735171, 0.06139940044, -0.07659307272)
    boxes['goal1'] = (8.45, 1.0, 0.0) + (0.0, 0.0, 0.0) + (0.4334079123, 1.6, 3.0)
    boxes['goal2'] = (-8.45, 1.0, 0.0) + (0.0, 0.0, 0.0) + (0.4334079123, 1.6, 3.0)
    points['powerup_spawn1'] = (5.414681236, 0.9515026107, -5.037912441)
    points['powerup_spawn2'] = (-5.555402285, 0.9515026107, -5.037912441)
    points['powerup_spawn3'] = (5.414681236, 0.9515026107, 5.148223181)
    points['powerup_spawn4'] = (-5.737266365, 0.9515026107, 5.148223181)
    points['spawn1'] = (-6.835352227, 0.02305323209, 0.0) + (1.0, 1.0, 3.0)
    points['spawn2'] = (6.857415055, 0.03938567998, 0.0) + (1.0, 1.0, 3.0)
    points['tnt1'] = (-0.05791962398, 1.080990833, -4.765886164)
    points['box1'] = (-5.08421587483, 0.9515026107, -2.7762602271)


class BasketballStadium(bs.Map):
    """Stadium map used for ice hockey games."""

    defs = BasketballStadiumMapData()
    name = 'Basketball Stadium'

    @override
    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'hockey', 'team_flag', 'keep_away']

    @override
    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'hockeyStadiumPreview'

    @override
    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'meshes': (
                bs.getmesh('thePadBG'),
                bs.getmesh('hockeyStadiumInner'),
                bs.getmesh('thePadBG'),
            ),
            'vr_fill_mesh': bs.getmesh('footballStadiumVRFill'),
            'collision_mesh': bs.getcollisionmesh('footballStadiumCollide'),
            'tex': bs.gettexture('black'),
            'stands_tex': bs.gettexture('black'),
        }
        mat = bs.Material()
        data['ice_material'] = mat
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = bs.newnode(
            'terrain',
            delegate=self,
            attrs={
                'mesh': self.preloaddata['meshes'][0],
                'collision_mesh': self.preloaddata['collision_mesh'],
                'color_texture': self.preloaddata['tex'],
                'materials': [
                    shared.footing_material,
                    self.preloaddata['ice_material'],
                ],
            },
        )
        bs.newnode(
            'terrain',
            attrs={
                'mesh': self.preloaddata['vr_fill_mesh'],
                'vr_only': True,
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['stands_tex'],
            },
        )
        mats = [shared.footing_material, self.preloaddata['ice_material']]
        self.floor = bs.newnode(
            'terrain',
            attrs={
                'mesh': self.preloaddata['meshes'][1],
                'color_texture': bs.gettexture('white'),
                'opacity': 0.92,
                'opacity_in_low_or_medium_quality': 1.0,
                'materials': mats,
                'color': (0.7, 0.4, 0.1),
            },
        )
        self.stands = bs.newnode(
            'terrain',
            attrs={
                'mesh': self.preloaddata['meshes'][2],
                'visible_in_reflections': False,
                'color_texture': self.preloaddata['stands_tex'],
            },
        )
        
        
        ###   
        color = (0,0,0)
        opacity = 1                                    
        pos1 = [(0.00000001,0.01,0.00000001)]
        for m_pos in pos1:
            node = bs.newnode('locator',attrs={'shape':'circleOutline','position':m_pos, 'color':color, 'opacity':opacity, 'drawShadow': False,  'draw_beauty':True, 'additive':False, 'size':[2.8]})  
            node = bs.newnode('locator',attrs={'shape':'circleOutline','position':(-11, 0.01, 0.00000001), 'color':color, 'opacity':opacity, 'drawShadow': False,  'draw_beauty':True, 'additive':False, 'size':(15,3.4,6)})  
            node = bs.newnode('locator',attrs={'shape':'circleOutline','position':(11, 0.01, 0.00000001), 'color':color, 'opacity':opacity, 'drawShadow': False,  'draw_beauty':True, 'additive':False, 'size':(15,3.4,6)}) 
            node = bs.newnode('locator',attrs={'shape':'circleOutline','position':(-5.9, 0.01, 0.00000001), 'color':color, 'opacity':opacity, 'drawShadow': False,  'draw_beauty':True, 'additive':False, 'size':[3.4]})  
            node = bs.newnode('locator',attrs={'shape':'circleOutline','position':(5.9, 0.01, 0.00000001), 'color':color, 'opacity':opacity, 'drawShadow': False,  'draw_beauty':True, 'additive':False, 'size':[3.4]})  


        pos2 = [(0.000001,0.02,0.0000001)]
        for m_pos1 in pos2:  
            node = bs.newnode('locator',attrs={'shape':'circle','position':(0.00000001,0.01,0.00000001), 'color':color, 'opacity':opacity, 'drawShadow': False,  'draw_beauty':True, 'additive':False, 'size':[0.4]})
            node = bs.newnode('locator',attrs={'shape':'circle','position':m_pos, 'color':color, 'opacity':opacity, 'drawShadow': False,  'draw_beauty':True, 'additive':False, 'size':(0.09,100,11)})
            node = bs.newnode('locator',attrs={'shape':'circle','position':(-5.9, 0.01, 0.00000001), 'color':color, 'opacity':opacity, 'drawShadow': False,  'draw_beauty':True, 'additive':False, 'size':(0.09,100,3.2)})
            node = bs.newnode('locator',attrs={'shape':'circle','position':(5.9, 0.01, 0.00000001), 'color':color, 'opacity':opacity, 'drawShadow': False,  'draw_beauty':True, 'additive':False, 'size':(0.09,100,3.2)})
 
        gnode = bs.getactivity().globalsnode
        gnode.floor_reflection = False
        gnode.debris_friction = 0.3
        gnode.debris_kill_height = -0.3
        gnode.tint = (1.2, 1.3, 1.33)
        gnode.ambient_color = (1.15, 1.25, 1.6)
        gnode.vignette_outer = (0.66, 0.67, 0.73)
        gnode.vignette_inner = (0.93, 0.93, 0.95)
        gnode.vr_camera_offset = (0, -0.8, -1.1)
        gnode.vr_near_clip = 0.5
        self.is_hockey = False
 
# ba_meta export babase.Plugin
class HWProgram(bs.Plugin):
    _map.register_map(BasketballStadium)


