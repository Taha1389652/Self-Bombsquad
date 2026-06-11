# ba_meta require api 9

#==============================================================================#             
#     
#     Version v2.0
#     Create by Unknown_#7004 ( @uwu.user )
#         - Github https://github.com/uwu-user
#         - https://gamebanana.com/members/2496091
#
#==============================================================================#             

from __future__ import annotations
from typing import TYPE_CHECKING, cast

import random
import babase
import bauiv1 as bs
import bascenev1 as ba
from bascenev1 import _map
import math
import datetime
from bascenev1._gameutils import animate
from bascenev1lib.actor.text import Text
from bascenev1lib.actor.spaz import Spaz
from bascenev1lib.actor.spazfactory import SpazFactory
from bascenev1._coopsession import CoopSession
from bascenev1lib.gameutils import SharedObjects
from bascenev1._gameactivity import GameActivity
from bascenev1lib.actor.zoomtext import ZoomText
from bascenev1lib.actor.popuptext import PopupText
from bascenev1lib.actor.playerspaz import PlayerSpaz
from bascenev1lib.actor.scoreboard import Scoreboard
from bascenev1lib.actor.zoomtext import ZoomText
from bascenev1._messages import PlayerDiedMessage, DeathType, StandMessage, DieMessage

if TYPE_CHECKING:
    from typing import Any, Sequence, Callable, List, Dict, Tuple, Optional, Union

#==============================================================================#             

# babase.Colors

Black = (0 , 0 , 0)
White = (2.55 , 2.55 , 2.55)
Red = (2 , 0 , 0)
Lime = (0 , 2.55 , 0)
Blue = (0 , 0 , 2.55)
Yellow = (2.55 , 2.55 , 0)
Cyan = (0 , 2.55 , 2.55)
Aqua = (0 , 2.55 , 2.55)
Magenta = (2.55 , 0 , 2.55)
Fuchsia = (2.55 , 0 , 2.55)
Silver = (1.92 , 1.92 , 1.92)
Maroon = (1.28 , 0 , 0)
Olive = (1.28 , 1.28 , 0)
Green = (0 , 1.28 , 0)
Purple = (0.65 , 0 , 1.28)
Teal = (0 , 1.28 , 1.28)
Navy = (0 , 0 , 1.28)
Orange = (1.5, 0.5, 0)
Pink = (1.8, 0.5, 1.6)
Gray = (0.5, 0.5, 0.5)
 
#==============================================================================#             

class Mapdefs:
    def Points(x=0, y=0, z=0):
        return ((x, y, z) + (x, y, z) + (x, y, z))

    boxes = {
        "area_of_interest_bounds": (-0.5, -0.5056858119, 0.0) + (0, 0, 0) + (0, 0, 0),
        "map_bounds": (0.0, 0.7956858119, -0.4689020853) + (0, 0, 0) + (35.16182389, 12.18696164, 21.52869693),
        "level_bounds": (0.0, 1.185751251, 0.4326226188) + (0, 0, 0) + (42.09506485, 22.81173179, 29.76723155),
        "edge_box": Points(),
    }
    
    points = {
        "spawn1": (7, 0.3, 0),
        "spawn2": (-6, 0.3, 0)
    }

#==============================================================================#                      

class GameMessages:
    class _Button:
        def __init__(self, lang):
            self.pickup = ": \ue003"
            self.punch = ": \ue001"
            self.bomb = ": \ue002"
            self.jump = ": \ue004"
            
            self.pickup_button = "\ue006"
            self.punch_button = "\ue005"
            self.bomb_button = "\ue007"
            self.jump_button = "\ue008"

    class _Time:
        def __init__(self, lang):
            if lang == 'ja':
                self.second = "秒"
                self.minute = "分"
                self.hour = "時間"
                self.time_limit = "制限時間"
                self.no_time = "時間なし"
            else:
                self.second = "second"
                self.minute = "minute"
                self.hour = "hour"
                self.time_limit = "Time Limit"
                self.no_time = "No Time"

    class _Warning:
        def __init__(self, lang):
            self.icon = "\u26A0"
            if lang == 'ja':
                self.leaving = "警告 » プレイヤーが2人必要です!"
                self.error = "エラー! "
            else:
                self.leaving = "Warning » need 2 players!"
                self.error = "Error! "

    class _System:
        def __init__(self, lang):
            self.format_bytes = ["", "k", "m", "g", "t", "p"]
            if lang == 'ja':
                self.format_time = ["年", "日", "時間", "分", "秒"]
            else:
                self.format_time = ["y", "d", "h", "m", "s"]
                
    def __init__(self, language='en'): 
        self._messages = {
            'en': self._english_version(language),
            'ja': self._japanese_version(language)
        }
        self._set_language(language)

    def _set_language(self, language):
        messages = self._messages.get(language, self._messages[language])
        for key, value in messages.items():
            setattr(self, key, value)

    def _english_version(self, language):
        return {
            'name': "tictactoe",
            'description': "» Who need description anyway",
            'version': "Version: v2.0",
            'type': "tictactoe",
            'game_over': "Game Over",
            'winner': "Winner!",
            'draw': 'Draw',
            'buttons_cooldown': "Button Cooldown",
            'default_team_colors': "default team colors",
            'icon': "discordServer",
            'empty': " ",
            'button': self._Button(language),
            'time': self._Time(language),
            'warning': self._Warning(language),
            'system': self._System(language)
        }

    def _japanese_version(self, language):
        return {
            'name': "tictactoe",
            'description': "» 説明なんて必要ないよね",
            'version': "バージョン: v2.0",
            'type': "tictactoe",
            'game_over': "ゲームオーバー",
            'winner': "勝者!",
            'draw': '引き分け',
            'buttons_cooldown': "ボタンクールダウン",
            'default_team_colors': "デフォルトのチームカラー",
            'icon': "discordServer",
            'empty': " ",
            'button': self._Button(language),
            'time': self._Time(language),
            'warning': self._Warning(language),
            'system': self._System(language)
        }

#==============================================================================#                      
  
class TictactoeMap(ba.Map):
    defs = Mapdefs()
    name = GameMessages().name

    @classmethod
    def get_play_types(cls) -> List[str]:
        return [GameMessages().type]

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return GameMessages().icon

    @classmethod
    def on_preload(cls) -> Any:
        data: Dict[str, Any] = {
            "bgtex": ba.gettexture('menuBG'),
            "bgmesh": ba.getmesh('thePadBG')
        }
        return data        

    def __init__(self) -> None:
        super().__init__()
                
        self.background = ba.newnode("terrain",
            attrs={
                "mesh": self.preloaddata["bgmesh"],
                "lighting": False,
                "background": True,
                "color_texture": self.preloaddata["bgtex"]
            })
                       
        settings = {
            "floor_reflection": False,
            "camera_mode": "follow",
            "tint": (0.5, 0.5, 0.5),
            "ambient_color": (0.2, 0.2, 0.2),
            "vignette_outer": (0.60, 0.62, 0.66),
            "vignette_inner": (0.97, 0.95, 0.93),
            "vr_camera_offset": (0, 0, 0),
            "vr_near_clip": 0,
            "debris_friction": 0,
            "debris_kill_height": 0,
        }

        gnode = ba.getactivity().globalsnode
        for key, value in settings.items():
            setattr(gnode, key, value)
                      
#==============================================================================#             

class Player(ba.Player["Team"]):
    """Our player type for this game."""

    def __init__(self) -> None:
        self.last_position = (0, 0, 0)
        
class Team(ba.Team[Player]):
    """Our team type for this game."""

    def __init__(self) -> None:
        self.score = 0
        
#==============================================================================# 

# ba_meta export bascenev1.GameActivity
class SkylineGame(ba.TeamGameActivity[Player, Team]):
    name = GameMessages().name
    description = GameMessages().description
    announce_player_deaths = False

    @classmethod
    def get_available_settings(cls, sessiontype: Type[ba.Session]) -> List[babase.Setting]:
        settings = [
            ba.IntChoiceSetting(GameMessages().time.time_limit,
                choices=[
                    (GameMessages().time.no_time, 0),
                    (f'1 {GameMessages().time.minute}', 60),
                    (f'2 {GameMessages().time.minute}', 120),
                    (f'5 {GameMessages().time.minute}', 300),
                ], default=0,
            ),
            ba.BoolSetting(GameMessages().default_team_colors, default=True)
        ]
        return settings

    @classmethod
    def get_supported_maps(cls, sessiontype: Type[ba.Session]) -> List[str]:
        return bs.app.classic.getmaps(GameMessages().type)
        
    @classmethod
    def supports_session_type(cls, sessiontype: Type[ba.Session]) -> bool:
        return (issubclass(sessiontype, ba.DualTeamSession))
        
    def __init__(self, settings: dict):
        super().__init__(settings)
        self.shared = SharedObjects.get()
        self.warning_window = WarningWindow()
        self.turn_window = TurnWindow()
        self._initialize_game_state()
        self._initialize_map()
        self._apply_settings(settings)

        self.default_music = ba.MusicType.GRAND_ROMP

    def _apply_settings(self, settings: Dict[str, float]) -> None:
        attr_config = {
            '_time_limit': (float, GameMessages().time.time_limit),
            'default_team_colors': (bool, GameMessages().default_team_colors),
        }
        
        for attr, (converter, setting_key) in attr_config.items():
            setattr(self, attr, converter(settings[setting_key]))

    def _initialize_game_state(self) -> None:
        for attr, value in {
            '_respawn_times': 0.01,
            'Turn': random.choice([0, 1]),
            'on_cooldown': False,
            'game_over': False,
            'wait': False,
        }.items():
            setattr(self, attr, value)

    def _initialize_map(self):
        self.buttonMap = {
            **{f"button[{i}]": {"label": GameMessages().empty, "disabled": False} for i in range(1, 10)},
            "button[OK]": {"winner": None, "end": False}
        }
                          
    def on_begin(self) -> None:
        super().on_begin()
        self._initialize_materials()
        self._create_region()
        self._create_box_region()
        self._add_game_elements()
        self.turn_window.show(self.Turn)
        self._team_data()    
        ba.timer(0.1, self._player_check)
        ba.timer(0.001, ba.Call(self.check_players), repeat = True)
        ba.timer(1, ba.Call(self._winners_check), repeat = True)
        self.setup_standard_time_limit(self._time_limit)

    def _initialize_materials(self):
        self._player_floor = ba.Material()
        self._player_floor.add_actions(
            conditions=("we_are_older_than", 1),
            actions=("modify_part_collision", "collide", True)
        )
        
    def _create_region(self):
        ba.newnode("region", attrs={
            "position": (0, 0, 0),
            "scale": (500, 0.1, 500),
            "type": "box",
            "materials": [self._player_floor, self.shared.footing_material]
        })

    def _create_box_region(self):
        for position, scale in [((-8, 1, 0),(0.15, 3, 18)), ((8, 1, 0),(0.15, 3, 18)), ((0, 1, -7),(18, 3, 0.15)), ((0, 1, 7),(18, 3, 0.15))]:                         	
            ba.newnode("region", attrs={"position": position, "scale": scale, "type": "box", "materials": [self._player_floor, self.shared.footing_material]})
            if bool(False):  # debug flag, keep it False
                ba.newnode('locator', attrs={ 'shape': 'box', 'position': position, 'color': (0,1,0), 'opacity': 0.3, 'draw_beauty': True, 'additive': False, 'size': list(scale)})

    def _add_game_elements(self) -> None:
        x_positions = [-2.600873119354248, 0.0025263208389282, 2.653714027404785]
        z_positions = [-2.860033082962036, 0.04995027929544449, 2.860033082962036]
        
        y_positions = {
            'floor': -0.16906466331481934,
            'text': -0.01006466331481934,
            'game_floor': 0.2506466331481934,
            'shield': 0.35906466331481934,
            'light': 0.35906466331481934
        }
        
        for i, x in enumerate(x_positions):
            for j, z in enumerate(z_positions):
                element_num = i * 3 + j + 1
                
                setattr(self, f'locator_floor{element_num}', 
                       ba.newnode("locator", attrs={
                           "shape": "box", "position": (x, y_positions['floor'], z - 0.4),
                           "color": Black, "opacity": 1, "draw_beauty": True,
                           "drawShadow": True, "additive": False, "size": [2.3, 0, 2.3]
                       }))
                
                setattr(self, f'text{element_num}', 
                       ba.newnode("text", attrs={
                           "position": (x, y_positions['text'], z), "text": GameMessages().empty,
                           "in_world": True, "shadow": 0, "flatness": 1.0,
                           "scale": 0.030, "h_align": "center"
                       }))
                
                setattr(self, f'floor{element_num}', 
                       ba.newnode("locator", attrs={
                           "shape": "circleOutline", "position": (x, y_positions['game_floor'], z),
                           "color": White, "opacity": 1, "draw_beauty": True,
                           "drawShadow": False, "additive": False, "size": [0]
                       }))
                
                shield = ba.newnode("shield", attrs={
                    "position": (x, y_positions['shield'], z),
                    "color": White, "radius": 0
                })
                setattr(self, f'shield{element_num}', shield)
                shield.always_show_health_bar = False
                
                setattr(self, f'light{element_num}', 
                       ba.newnode("light", attrs={
                           "position": (x, y_positions['light'], z),
                           "volume_intensity_scale": 0.9, "radius": 0.0,
                           "intensity": 0.4, "color": White
                       }))
                       
    def _update_floor(self, floor: int, color: list[float] = None, team: str = None, remove: bool = False) -> None:
        if not 1 <= floor <= 9: return
        button_key = f"button[{floor}]"
        if not remove and self.buttonMap[button_key]["disabled"]: return
        
        params = {
            True: {"text": " ", "text_color": White, "size": (0, 0, 0), "floor_color": White,
                    "shield_radius": 0.0, "shield_color": White, "light_radius": 0.0, "light_color": White,
                    "disabled": False, "label": 0},
            False: {"text": f"»  {team}  «", "text_color": color, "size": (1.5, 0.1, 1.5), "floor_color": color,
                    "shield_radius": 1, "shield_color": color, "light_radius": 0.25, "light_color": color,
                    "disabled": True, "label": team}
        }[remove]
        
        components = ["text", "floor", "shield", "light"]
        for comp in components:
            node = getattr(self, f"{comp}{floor}")
            if comp == "text":
                node.text = params["text"]
                node.color = params["text_color"]
            elif comp == "floor":
                node.size = params["size"]
                node.color = params["floor_color"]
            else:
                node.radius = params[f"{comp}_radius"]
                node.color = params[f"{comp}_color"]
        
        self.buttonMap[button_key].update({"disabled": params["disabled"], "label": params["label"]})
        
        if not remove:
            self.Turn = 1 - self.Turn 
            self.Playsound("laserReverse" if self.Turn == 1 else "laser")
            self.turn_window.update(self.Turn)
                    
    def check_players(self):
        for player in self.players:
            if self.is_valid_player(player):
                self.assign_player_inputs(player)
        
    def is_valid_player(self, player):
        return player.actor is not None and player.actor.is_alive()

    def assign_player_inputs(self, player):
        if not self.is_valid_player(player): return
        input_assignments = {
            'PICK_UP_PRESS': lambda: self.handle_input("action", "PickUp", player),
            'BOMB_PRESS': lambda: self.handle_input("action", "Bomb", player),
            'JUMP_PRESS': lambda: self.handle_input("action", "Jump", player),
            'PUNCH_PRESS': lambda: self.handle_input("action", "Punch", player),
        }

        for input_type, handler in input_assignments.items():
            player.assigninput(getattr(ba.InputType, input_type), handler)

    def handle_input(self, input_type: str, action: str, player: ba.Player) -> None:
        if self.on_cooldown or self.game_over or self.wait:
            return
        
        if input_type == "action":
            action_map = {
                "PickUp": self._Remove,
                "Punch": self._Choice,
            }
            if action in action_map:
                action_map[action](player)
                self.cooldown_set()

    def _Choice(self, player):
        if self.buttonMap["button[OK]"]["end"] or self.wait:
            return
            
        if player.team.id == self.Turn:
            return
            
        self._process_player_floor_interaction(player, self._floor_info)
                    
    def _Remove(self, player):
        if self.buttonMap["button[OK]"]["end"]:
            return
            
        if bool(False):
            self._process_player_floor_interaction(player, self._update_floor, remove=True)
    
    def _process_player_floor_interaction(self, player, callback, **kwargs):
        """Process player interaction with floors using a callback function."""
        player_pos = player.actor.node.position
        
        for floor_num in range(1, 10):
            floor_attr = getattr(self, f'floor{floor_num}')
            floor_vec = ba.Vec3(
                player_pos[0] - floor_attr.position[0],
                0.0,
                player_pos[2] - floor_attr.position[2]
            )
            
            if floor_vec.length() <= 1.25:
                callback(floor=floor_num, team=player.team, **kwargs)
                break

    def _team_data(self):
        if bool(self.default_team_colors):
            self.Oteam = {"Name": "O", "Full_name": "Blue", "Color": (0, 0, 9.5)}
            self.Xteam = {"Name": "X", "Full_name": "Red", "Color": (9.5, 0, 0)}
        else:
            team_data = {0: ("Oteam", "O"), 1: ("Xteam", "X")}
            for team in self.teams:
                if team.id in team_data:
                    attr, name = team_data[team.id]
                    setattr(self, attr, {
                        "Name": name, 
                        "Full_name": str(team.name.evaluate()), 
                        "Color": team.color
                    })
    
        self.turn_window.update_teams(self.Oteam, self.Xteam)
        
    def _floor_info(self, floor: int, team: ba.Team) -> None:
        if team.id == 0:
            self._update_floor(floor = floor, color = self.Oteam["Color"], team = self.Oteam["Name"])
        elif team.id == 1:
            self._update_floor(floor = floor, color = self.Xteam["Color"], team = self.Xteam["Name"])
        else: pass
    
    def _winners_check(self) -> None:
        O, X, GG = "O", "X", "GG"
    
        wins = [[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]
    
        for combo in wins:
            labels = [self.buttonMap[f"button[{i}]"]["label"] for i in combo]
            if labels == [O,O,O] or labels == [X,X,X]:
                self.END(labels[0]); return
     
        if all(self.buttonMap[f"button[{i}]"]["disabled"] for i in range(1,10)) and not self.buttonMap["button[OK]"]["end"]:
            self.END("×"); return

    def END(self, Who: int) -> None: 
            if not self.buttonMap["button[OK]"]["end"]:
                self.buttonMap["button[OK]"]["end"] = True
                self.buttonMap["button[OK]"]["winner"] = Who
                self.WinnerWindow(Who)
                self.turn_window.update(-1)
            else: pass

    def WinnerWindow(self, winner: str):
        if winner == "×":
            name, color = GameMessages().draw, White
        elif winner == "X":
            name = GameMessages().winner
            color = self._get_team_color(1, (9, 0, 0))
            self._update_team_score(1)
        elif winner == "O":
            name = GameMessages().winner
            color = self._get_team_color(0, (0, 0, 9))
            self._update_team_score(0)
        else:
            name, color = GameMessages().empty, White 
        
        ZoomText(str(name),
                 maxwidth=400,
                 lifespan=4.5,
                 jitter=2.0,
                 color=color,
                 trailcolor=(0.0, 0.0, 0.0, 0.0)).autoretain()
    
    def _get_team_color(self, team_id, default_color):
        if not self.default_team_colors:
            for team in self.teams:
                if team.id == team_id:
                    return team.color
        return default_color
    
    def _update_team_score(self, team_id):
        for team in self.teams:
            if team.id == team_id:
                team.score += 10 # team scores
                return 
                 
    def on_team_join(self, team: ba.Team) -> None:
        if not self.has_begun():
            return
            
        self._update_player_count()
        ba.timer(0.1, self._player_check)

    def on_player_join(self, player: Player) -> None:
        if self.has_begun():
            ba.screenmessage(ba.Lstr(resource='playerDelayedJoinText', subs=[('${PLAYER}', player.getname(full=True))]), color=(0, 1, 0))
            return
        self.spawn_player(player)
            
    def on_player_leave(self, player: ba.Player) -> None:
        if not self.has_begun():
            return
            
        self._update_player_count()
        ba.timer(0.1, self._player_check)
        
    def _player_check(self):
        if self.game_over: return
        self._update_player_count()
        valid_player_count = (self._active_players == 2)
        action, self.wait = ("start", True) if not valid_player_count else ("stop", False)
        self.warning_window.update(action)
            
    def _update_player_count(self) -> None:
        self._active_players = sum(
            1 for player in self.players 
            if self.is_valid_player(player)
        )
        
    def Playsound(self, sound: str) -> None:
        ba.getsound(sound).play()
        
    def _Error(self, info: str) -> None:
        ba.screenmessage(f"» {GameMessages().warning.error}: {info}", color=(1, 0, 0))
        self.Playsound("ticking")

    def format_bytes(self, Number):
        Format = GameMessages().system.format_bytes
        FormatUp = 1000.0
        Magnitude = 0
        
        Number = float("{:.3g}".format(Number))
        while abs(Number) >= FormatUp:
            Magnitude += 1
            Number /= FormatUp
        return "{}{}".format("{:f}".format(Number).rstrip("0").rstrip("."), Format[Magnitude])

    def format_time(self, Seconds):
        if Seconds < 0: Seconds = 0    
        Format = GameMessages().system.format_time
        FormatUp = [365 * 24 * 60 * 60, 24 * 60 * 60, 60 * 60, 60, 1]
    
        parts = []
    
        for i in range(len(FormatUp)):
            if Seconds >= FormatUp[i]:
                count = Seconds // FormatUp[i]
                Seconds %= FormatUp[i]
                parts.append(f"{int(count)}{Format[i]}")
    
        return " ".join(parts) if parts else "0s"

    def spawn_player(self, player: Player) -> ba.Actor:
        """Create and wire up a ba.PlayerSpaz for the provided ba.Player."""
        # pylint: disable=too-many-locals
        # pylint: disable=cyclic-import
        from babase import _math
        from bascenev1._gameutils import animate
        from bascenev1._coopsession import CoopSession
        from bascenev1lib.actor.playerspaz import PlayerSpaz
        name = player.getname(icon=True)
        color = player.color
        highlight = player.highlight
        account_id = player.sessionplayer.get_v1_account_id()
        
        light_color = color
        display_color = color
        spaz = PlayerSpaz(color=color,
                          highlight=highlight,
                          character=player.character,
                          player=player)

        player.actor = spaz
        assert spaz.node

        # If this is co-op and we're on Courtyard or Runaround, add the
        # material that allows us to collide with the player-walls.
        # FIXME: Need to generalize this.
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
        spaz.connect_controls_to_player()

        spaz.connect_controls_to_player(
                                        enable_punch=True,
                                        enable_bomb=False,
                                        enable_pickup=True,
                                        enable_jump=True)
                           
        position = (player.last_position[0], player.last_position[1], player.last_position[2])
       
        if position == (0, 0, 0):
            if isinstance(self.session, ba.DualTeamSession):
                _position = self.map.get_start_position(player.team.id)
            else:
                _position = self.map.get_ffa_start_position(self.players)
        else: _position = position
                    
        spaz.handlemessage(
            StandMessage(
                _position,
                random.uniform(0, 360)))
        light = ba.newnode('light', attrs={'color': light_color})
        spaz.node.connectattr('position', light, 'position')
        animate(light, 'intensity', {0: 0, 0.25: 1, 0.5: 0})
        ba.timer(0.5, light.delete)
        return spaz

    def handlemessage(self, msg: Any) -> Any: 
        if isinstance(msg, ba.PlayerDiedMessage):
            super().handlemessage(msg)
            player = msg.getplayer(Player)
            
            if isinstance(self.session, ba.DualTeamSession): 
                Normal_position = self.map.get_start_position(player.team.id)
            else:
                Normal_position = self.map.get_ffa_start_position(self.players)
            
            killer = msg.getkillerplayer(Player)

            if killer is None:
                player.last_position = Normal_position
                return None
                
            if killer.team is player.team:
                if isinstance(self.session, ba.FreeForAllSession):
                    
                    if msg.how == DeathType.FALL or msg.how == DeathType.OUT_OF_BOUNDS:
                        player.last_position = Normal_position
                    else: player.last_position = killer.position 

                else: 
                    if msg.how == DeathType.FALL or msg.how == DeathType.OUT_OF_BOUNDS:
                        player.last_position = Normal_position 
                    else: player.last_position = killer.position
            else:
                if msg.how == DeathType.FALL or msg.how == DeathType.OUT_OF_BOUNDS:
                    player.last_position = Normal_position
                else: 
                    player.last_position = Normal_position
            self.respawn_player(player)            
        else:
            return super().handlemessage(msg)
        return None                
                
    def cooldown_set(self):
        self.on_cooldown = True
        def off():
            self.on_cooldown = False       
        ba.timer(0.5, off)
            
    def end_game(self) -> None:
        if self.game_over: return
        results = ba.GameResults()
        for team in self.teams:
            results.set_team_score(team, team.score)
        self.end(results=results)
        self.game_over = True          

#==============================================================================#             
               
class TurnWindow:
    def __init__(self):
        for attr, value in {
            '_is_active': False,
            'game_over': False,
            'team_times': [0, 0],
            '_active_nodes': [],
            '_current_team': None,
            '_last_time_update': None,
            'time': 15,
        }.items():
            setattr(self, attr, value)

    def show(self, turn: int) -> None:
        if self.game_over: 
            return
            
        self.turn = turn
        
        if not self._is_active:
            self._create_ui()
            self._is_active = True
            ba.timer(0.1, ba.Call(self.update, self.turn))
            self._switch_team(turn)
        return

    def create_text_node(self, text: str, position: tuple[float, float], 
                        color: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0), 
                        scale: float = 1.0, rotate: float = 0, shadow: float = 0.5, 
                        maxwidth: float = 150.0, opacity: float = 1.0, flatness: float = 1.0):
        node = ba.newnode("text", attrs={
            "text": text,
            "shadow": shadow,
            "flatness": flatness,
            "h_attach": "center",
            "v_attach": "top",
            "position": position,
            "opacity": opacity,
            "color": color,
            "scale": scale,
            "rotate": rotate,
            "maxwidth": maxwidth
        })
        self._active_nodes.append(node)
        return node
            
    def create_image_node(self, texture: str, position: tuple[float, float] = (0.0, 0.0), 
                         scale: tuple[float, float] = (100.0, 100.0), rotate: float = 0, 
                         color: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0), 
                         opacity: float = 1.0):
        node = ba.newnode("image", attrs={
            "texture": ba.gettexture(texture),
            "position": position,
            "attach": "topCenter",
            "scale": scale,
            "color": color,
            "rotate": rotate,
            "opacity": opacity,
        })
        self._active_nodes.append(node)
        return node

    def _create_ui(self) -> None:
        nodes = [
            ("background_right_up_dot", "image", ["circle"], {"color": White, "position": (150, -90), "scale": (31.35, 26.35)}),            
            ("background_right_up", "image", ["bar"], {"color": White, "position": (70, -90), "scale": (160.0, 25.0)}),            
            ("background_right_down_dot", "image", ["circle"], {"color": White, "position": (130, -110), "scale": (31.35, 26.35)}),            
            ("background_right_down", "image", ["bar"], {"color": White, "position": (80, -110), "scale": (100.0, 25.0)}),
            
            ("background_left_up_dot", "image", ["circle"], {"color": White, "position": (-120, -90), "scale": (31.35, 26.35)}),            
            ("background_left_up", "image", ["bar"], {"color": White, "position": (-40, -90), "scale": (160.0, 25.0)}),            
            ("background_left_down_dot", "image", ["circle"], {"color": White, "position": (-100, -110), "scale": (31.35, 26.35)}),            
            ("background_left_down", "image", ["bar"], {"color": White, "position": (-50, -110), "scale": (100.0, 25.0)}),
           
            ("image_bg", "image", ["circleZigZag"], {"position": (20, -100), "scale": (95.0, 95.0), "color": (0.0, 0.0, 0.0, 1.0)}),            
            ("image", "image", ["circleZigZag"], {"position": (20, -100), "scale": (85.0, 85.0)}),        
    
            ("trun_image", "image", ["nextLevelIcon"], {"position": (20, -100), "scale": (50.0, 50.0), "rotate": -180 if self.turn == 0 else 0, "color": (0.0, 0.0, 0.0, 1.0)}),            
            ("X_team", "text", ["? » ???"], {"position": (80.0, -118.5), "scale": 0.5, "color": (0.0, 0.0, 0.0, 1.0)}),            
            ("O_team", "text", ["? » ???"], {"position": (-85.0, -118.5), "scale": 0.5, "color": (0.0, 0.0, 0.0, 1.0)}),            
            ("X_time", "text", ["00:00:00"], {"position": (80.0, -95.5), "scale": 0.5, "color": (0.0, 0.0, 0.0, 1.0)}),
            ("O_time", "text", ["00:00:00"], {"position": (-90.0, -95.5), "scale": 0.5, "color": (0.0, 0.0, 0.0, 1.0)}),
            ("end_time", "text", [""], {"position": (12, -135), "scale": 0.5, "color": (0.0, 0.0, 0.0, 1.0)}),
        ]
        
        for var_name, node_type, args, kwargs in nodes:
            node = getattr(self, f"create_{node_type}_node")(*args, **kwargs)
            setattr(self, var_name, node)
            
        self._last_time_update = ba.time()
        ba.timer(0.1, self._update_time_ui, repeat=True)

    def _switch_team(self, new_team: int) -> None:
        """Switch active team and update timers accordingly"""
        current_time = ba.time()
       
        if self._current_team is not None and not self.game_over:
            elapsed = current_time - self._last_time_update
            self.team_times[self._current_team] += elapsed
            self.Playsound('click01')
        
        self._current_team = new_team
        self._last_time_update = current_time

    def _update_time_ui(self) -> None:
        if hasattr(self, 'X_time') and hasattr(self, 'O_time'):
            current_time = ba.time()
            if self._current_team is not None and not self.game_over:
                elapsed = current_time - self._last_time_update
                current_display_time = self.team_times[self._current_team] + elapsed
                
                if self._current_team == 0:
                    self.X_time.text = self.format_time(current_display_time)
                    self.O_time.text = self.format_time(self.team_times[1])
                else:
                    self.X_time.text = self.format_time(self.team_times[0])
                    self.O_time.text = self.format_time(current_display_time)
            else:
                self.X_time.text = self.format_time(self.team_times[0])
                self.O_time.text = self.format_time(self.team_times[1])
    
    def update(self, turn: int):
        if self.game_over:
            return
            
        if turn == -1: 
            self._handle_game_end()
        else: 
            self._switch_team(turn)
            self._animate_turn_indicator(turn)
            
    def update_teams(self, Oteam, Xteam):
        if self.O_team and self.X_team:
            teams = [(self.O_team, Oteam), (self.X_team, Xteam)]
            for team, data in teams:
                team.text, team.color = f"{data['Name']} » {data['Full_name']}", data['Color']
                team.position = (team.position[0] - len(data['Full_name']), team.position[1])
            
    def _handle_game_end(self):
        self.game_over = True
        self._start_end_timer()
        self._switch_team(None)
        self.trun_image.rotate = 0
        self.trun_image.texture = ba.gettexture("googlePlayLeaderboardsIcon")
    
    def _start_end_timer(self) -> None:
        def _update():
            if not self._is_active:
                self._stop_countdown()
                return
                
            self.end_time.text = f"{int(self.time):02d}"
            self.time -= 1.0
           
            if self.time <= 0.0:
                ba.get_foreground_host_activity().end_game()
            else: ba.timer(1.0, _update)                
        ba.timer(1.0, _update)
    
    def _animate_turn_indicator(self, turn: int):
        rotation_config = {
            0: {'target_rot': 0, 'anim_dir': -1},
            1: {'target_rot': -180, 'anim_dir': 1}
        }
        
        config = rotation_config[turn]
        
        ba.animate(self.trun_image, "rotate", {
            0.0: self.trun_image.rotate, 
            0.5: config['target_rot']
        })
        
        dir_multiplier = config['anim_dir']
        for node in [self.image, self.image_bg]:
            ba.animate(node, "rotate", {
                0.0: 0.0, 
                0.1: 10.0 * dir_multiplier, 
                3.6: 360.0 * dir_multiplier
            }, loop=True)
            
    def format_time(self, seconds: float) -> str:
        if seconds < 0: 
            seconds = 0
            
        hours = int(seconds) // 3600
        minutes = (int(seconds) % 3600) // 60
        seconds = int(seconds) % 60
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
    def Playsound(self, sound: str) -> None:
        ba.getsound(sound).play()
        
#==============================================================================#             

class WarningWindow:
    def __init__(self):
        for attr, value in {
            '_countdown_timer': None,
            'warning_time': 15,
            'time_left': 15,
            '_active_nodes': [],
            '_is_active': False,
            '_countdown_text': None,
            'game_over': False
        }.items():
            setattr(self, attr, value)

    def update(self, action: str) -> None:
        if not isinstance(action, str):
            raise TypeError("Action must be a string")
            
        action = action.lower().strip()
        if self.game_over: return
        
        if action == "stop":
            if self._is_active:
                self._stop_countdown()
            return
            
        if action == "start":
            if not self._is_active:
                self._create_ui()
                self._start_countdown()
                self._is_active = True
            return
            
        raise ValueError(f"Invalid action: '{action}'. Expected 'start' or 'stop'")

    def create_text_node(self, text: str, position: tuple[float, float], 
                        color: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0), 
                        scale: float = 1.0, shadow: float = 0.5, 
                        maxwidth: float = 150.0, flatness: float = 1.0):
        node = ba.newnode("text", attrs={
            "text": text,
            "shadow": shadow,
            "flatness": flatness,
            "h_attach": "center",
            "v_attach": "center",
            "position": position,
            "color": color,
            "scale": scale,
            "maxwidth": maxwidth
        })
        self._active_nodes.append(node)
        return node
            
    def create_image_node(self, texture: str, position: tuple[float, float] = (0.0, 0.0), 
                         scale: tuple[float, float] = (100.0, 100.0), 
                         color: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0), 
                         opacity: float = 1.0):
        node = ba.newnode("image", attrs={
            "texture": ba.gettexture(texture),
            "position": position,
            "attach": "center",
            "scale": scale,
            "color": color,
            "opacity": opacity,
        })
        self._active_nodes.append(node)
        return node

    def _create_ui(self) -> None:
        nodes = [
            ("background_dot", "image", ["circle"], {"color": White, "position": (37.5, 159.85), "scale": (31.35, 31.35)}),            
            ("background", "image", ["bar"], {"color": White, "position": (-70.0, 160.0), "scale": (220.0, 30.0)}),            
            ("image_bg", "image", ["circleZigZag"], {"position": (-200.0, 160.0), "scale": (95.0, 95.0), "color": (0.0, 0.0, 0.0, 1.0)}),            
            ("image", "image", ["circleZigZag"], {"position": (-200.0, 160.0), "scale": (85.0, 85.0)}),            
            ("_warm_icon", "text", [GameMessages().warning.icon], {"position": (-221.5, 132.5), "scale": 1.75, "color": (0.0, 0.0, 0.0, 1.0)}),            
            ("_warm_text", "text", [GameMessages().warning.leaving], {"position": (-150.0, 147.5), "scale": 1.25, "color": (0.0, 0.0, 0.0, 1.0)}),            
            ("_countdown_text", "text", [str(str(self.format_time(self.time_left)))], {"position": (-20.0, 17.5), "scale": 1.75})
        ]
        
        for var_name, node_type, args, kwargs in nodes:
            node = getattr(self, f"create_{node_type}_node")(*args, **kwargs)
            setattr(self, var_name, node)
            
        ba.animate(self.image, "rotate", {0.0: 0.0, 0.1: -10.0, 3.6: -360.0}, loop=True)
        ba.animate(self.image_bg, "rotate", {0.0: 0.0, 0.1: -10.0, 3.6: -360.0}, loop=True)
        ba.animate(self._countdown_text, 'scale', {0.0:1.5, 0.5:1.7, 0.6:1.5, 0.7:1.7, 1.0:1.5}, loop=True)

    def _start_countdown(self) -> None:
        def _update():
            if not self._is_active or not self._countdown_text.exists():
                self._stop_countdown()
                return
                
            self.time_left -= 1.0
            try:
                self._countdown_text.text = str(self.format_time(self.time_left))
                if int(self.time_left) <= 10: 
                    self._countdown_text.color = Red
                    self.Playsound("warnBeeps")
            except:
                self._stop_countdown()
                self._countdown_text.color = White
                return
            
            if self.time_left <= 0.0:
                self._complete()
            else:
                self._countdown_timer = ba.timer(1.0, _update)

        self._countdown_timer = ba.timer(1.0, _update)

    def _complete(self) -> None:
        self._cleanup()
        self._is_active = False
        self.game_over = True
        self.Playsound("boo")
        ba.get_foreground_host_activity().end_game()
        
    def _stop_countdown(self) -> None:
        if self._countdown_timer:
            self._countdown_timer = None
        self._cleanup()
        self._is_active = False

    def _cleanup(self) -> None:
        for node in self._active_nodes:
            try:
                if node.exists():
                    node.delete()
            except:
                continue
                
        self._active_nodes.clear()
        self.time_left = self.warning_time
        self._countdown_text = None

    def format_time(self, Seconds):
        if Seconds < 0: Seconds = 0    
        Format = GameMessages().system.format_time
        FormatUp = [365 * 24 * 60 * 60, 24 * 60 * 60, 60 * 60, 60, 1]
    
        parts = []
    
        for i in range(len(FormatUp)):
            if Seconds >= FormatUp[i]:
                count = Seconds // FormatUp[i]
                Seconds %= FormatUp[i]
                parts.append(f"{int(count)}{Format[i]}")
    
        return " ".join(parts) if parts else f"0{Format[0]}"
        
    def Playsound(self, sound: str) -> None:
        ba.getsound(sound).play()
                
#==============================================================================#             
                                               
# ba_meta export babase.Plugin
class UwUuser(babase.Plugin):
    _map.register_map(TictactoeMap)