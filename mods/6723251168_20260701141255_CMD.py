# Ported by brostos to api 8
# Tool used to make porting easier.(https://github.com/bombsquad-community/baport)
"""python 3.9 | chatcmd for a beutiful game  - BombSquad OwO"""
# modded by IM_NOT_PRANAV#7874

# biggggggg thankssssssssssssss to FireFighter1037 for helping everything

# -*- coding: utf-8 -*-
# ba_meta require api 9

from __future__ import annotations

import threading
import time
from typing import TYPE_CHECKING

import babase
import bascenev1 as bs
import bauiv1 as bui
from bauiv1lib import mainmenu

if TYPE_CHECKING:
    from typing import Any

# our prefix that what we starts cmds with
px = '/'


# ==================== کلاس اصلی دستورات ====================
class ChatCommands:
    """کلاس مدیریت دستورات چت"""

    def __init__(self):
        self._last_message = ""
        self._last_message_time = 0
        self._cooldown = 0.5  # جلوگیری از اسپم دستورات

    def process_cmd(self):
        """پردازش دستورات از چت"""
        try:
            messages = bs.get_chat_messages()
            if not messages:
                return

            lastmsg = messages[-1]

            # جلوگیری از پردازش تکراری
            if lastmsg == self._last_message:
                return

            # بررسی زمان برای جلوگیری از اسپم
            current_time = time.time()
            if current_time - self._last_message_time < self._cooldown:
                return

            self._last_message = lastmsg
            self._last_message_time = current_time

            if ' ' not in lastmsg:
                return

            m = lastmsg.split(' ')[0]  # cmd (با پیشوند)
            n = lastmsg.split(' ')[1:]  # arguments

            if not m.startswith(px):
                return

            self._handle_command(m, n)

        except Exception as e:
            print(f"Error processing chat command: {e}")

    def _handle_command(self, m: str, n: list[str]):
        """مدیریت دستورات مختلف"""
        try:
            session = bs.get_foreground_host_session()
            activity = bs.get_foreground_host_activity()

            if session is None:
                return

            session_players = session.sessionplayers
            activity_players = activity.players if activity else []

            # ============== HELP ==============
            if m == px:
                bs.chatmessage(f'{px}help for help')

            elif m == px + 'help':
                self._handle_help(n)

            # ============== LIST / IDS ==============
            elif m in [px + 'list', px + 'l', px + 'clientids', px + 'ids', px + 'playerids']:
                bs.chatmessage('======= Indexs ======')
                for i, player in enumerate(session_players):
                    try:
                        bs.chatmessage(f'{player.getname()} --> {i}')
                    except:
                        pass

                # برای kick
                try:
                    roster = bs.get_game_roster()
                    if roster:
                        bs.chatmessage('====== For /kick only ======')
                        for i in roster:
                            if i.get('players'):
                                bs.chatmessage(
                                    f"{i['players'][0].get('name_full', 'Unknown')} - {i.get('client_id', '?')}")
                except:
                    pass

            # ============== UNIQUE ID ==============
            elif m in [px + 'uniqeid', px + 'id', px + 'pb-id', px + 'pb', px + 'accountid']:
                if not n:
                    bs.chatmessage(f'use : {px}uniqeid number of list')
                else:
                    try:
                        player = session_players[int(n[0])]
                        account_id = player.get_account_id()
                        if not account_id:
                            account_id = player.get_v1_account_id()
                        bs.chatmessage(f"{player.getname()}'s accountid is {account_id}")
                    except:
                        bs.chatmessage('could not found player')

            # ============== QUIT ==============
            elif m in [px + 'quit', px + 'restart']:
                babase.quit()

            # ============== MUTE / UNMUTE ==============
            elif m in [px + 'mute', px + 'mutechat']:
                cfg = babase.app.config
                cfg['Chat Muted'] = True
                cfg.apply_and_commit()
                bs.chatmessage('muted')
                bs.broadcastmessage(f'chat muted use {px}unmute and click on send to unmute')

            elif m in [px + 'unmute', px + 'unmutechat']:
                cfg = babase.app.config
                cfg['Chat Muted'] = False
                cfg.apply_and_commit()
                bs.chatmessage('un_muted')
                bs.broadcastmessage('chat un_muted')

            # ============== END GAME ==============
            elif m in [px + 'end', px + 'next']:
                if not n and activity:
                    try:
                        activity.end_game()
                        bs.chatmessage('Game ended Hope you scored great')
                    except:
                        bs.chatmessage('Game already ended')

            # ============== DAY / NIGHT ==============
            elif m in [px + 'dv', px + 'day']:
                if activity:
                    if activity.globalsnode.tint == (1.0, 1.0, 1.0):
                        bs.chatmessage(f'already {px}dv is on ,do {px}nv for night')
                    else:
                        activity.globalsnode.tint = (1.0, 1.0, 1.0)
                        bs.chatmessage('day mode on!')

            elif m in [px + 'nv', px + 'night']:
                if activity:
                    if activity.globalsnode.tint == (0.5, 0.7, 1.0):
                        bs.chatmessage(f'already {px}nv is on ,do {px}dv for day')
                    else:
                        activity.globalsnode.tint = (0.5, 0.7, 1.0)
                        bs.chatmessage('night mode on!')

            # ============== SLOW MOTION ==============
            elif m in [px + 'sm', px + 'slow', px + 'slowmo']:
                if activity and not n:
                    activity.globalsnode.slow_motion = not activity.globalsnode.slow_motion
                    bs.chatmessage('Game in Epic Mode Now' if activity.globalsnode.slow_motion else 'Game in normal mode now')

            # ============== PAUSE ==============
            elif m in [px + 'pause', px + 'pausegame']:
                if activity and not n:
                    activity.globalsnode.paused = not activity.globalsnode.paused
                    bs.chatmessage('Game Paused' if activity.globalsnode.paused else 'Game un paused')

            # ============== CAMERA MODE ==============
            elif m in [px + 'cameraMode', px + 'camera_mode', px + 'rotate_camera']:
                if activity and not n:
                    if activity.globalsnode.camera_mode != 'rotate':
                        activity.globalsnode.camera_mode = 'rotate'
                        bs.chatmessage('camera mode is rotate now')
                    else:
                        activity.globalsnode.camera_mode = 'follow'
                        bs.chatmessage('camera mode is normal now')

            # ============== REMOVE PLAYER ==============
            elif m in [px + 'remove', px + 'rm']:
                if not n:
                    bs.chatmessage(f'{px}remove all or {px}remove number in list')
                elif n[0] == 'all':
                    for player in session_players:
                        try:
                            player.remove_from_game()
                        except:
                            pass
                    bs.chatmessage('Removed All')
                else:
                    try:
                        session_players[int(n[0])].remove_from_game()
                        bs.chatmessage('Removed')
                    except:
                        bs.chatmessage('could not found player')

            # ============== INVISIBLE ==============
            elif m in [px + 'inv', px + 'invisible']:
                self._apply_to_players(activity_players, n, 'invisible')

            # ============== HEADLESS ==============
            elif m in [px + 'hl', px + 'headless']:
                self._apply_to_players(activity_players, n, 'headless')

            # ============== CREEPY ==============
            elif m in [px + 'creepy', px + 'creep']:
                self._apply_to_players(activity_players, n, 'creepy')

            # ============== KILL ==============
            elif m in [px + 'kill', px + 'die']:
                self._apply_to_players(activity_players, n, 'kill')

            # ============== HEAL ==============
            elif m in [px + 'heal', px + 'heath']:
                self._apply_to_players(activity_players, n, 'heal')

            # ============== CURSE ==============
            elif m in [px + 'curse', px + 'cur']:
                self._apply_to_players(activity_players, n, 'curse')

            # ============== SLEEP ==============
            elif m in [px + 'sleep']:
                self._apply_to_players(activity_players, n, 'sleep')

            # ============== SUPER PUNCH ==============
            elif m in [px + 'sp', px + 'superpunch']:
                self._apply_to_players(activity_players, n, 'superpunch')

            # ============== GLOVES ==============
            elif m in [px + 'gloves', px + 'punch']:
                self._apply_to_players(activity_players, n, 'gloves')

            # ============== SHIELD ==============
            elif m in [px + 'shield', px + 'protect']:
                self._apply_to_players(activity_players, n, 'shield')

            # ============== FREEZE ==============
            elif m in [px + 'freeze', px + 'ice']:
                self._apply_to_players(activity_players, n, 'freeze')

            # ============== UNFREEZE ==============
            elif m in [px + 'unfreeze', px + 'thaw']:
                self._apply_to_players(activity_players, n, 'unfreeze')

            # ============== FALL ==============
            elif m in [px + 'fall']:
                self._apply_to_players(activity_players, n, 'fall')

            # ============== CELEBRATE ==============
            elif m in [px + 'celebrate', px + 'celeb']:
                self._apply_to_players(activity_players, n, 'celebrate')

            # ============== FLY ==============
            elif m in [px + 'fly']:
                self._apply_to_players(activity_players, n, 'fly')

            # ============== GOD MODE ==============
            elif m in [px + 'gm', px + 'godmode']:
                self._apply_to_players(activity_players, n, 'godmode')

            # ============== DEFAULT BOMB ==============
            elif m in [px + 'd_bomb', px + 'default_bomb']:
                self._handle_bomb_command(activity_players, n)

            # ============== BOMB COUNT ==============
            elif m in [px + 'd_bomb_count', px + 'default_bomb_count', px + 'dbc']:
                self._handle_bomb_count(activity_players, n)

            # ============== CREDITS ==============
            elif m in [px + 'credits']:
                bs.chatmessage('🍚 created by Nazz 🍚')
                bs.chatmessage('🍚 Nazz are past/present/future 🍚')
                bs.chatmessage('🍚 everything is Nazz 🍚')

            # ============== HELP PAGES ==============
            else:
                # اگر دستور ناشناخته بود
                pass

        except Exception as e:
            print(f"Error handling command: {e}")

    def _handle_help(self, n: list[str]):
        """مدیریت دستور help"""
        if not n:
            bs.chatmessage('===========================================')
            bs.chatmessage(f' {px}help 1 - for page 1 | simple commands')
            bs.chatmessage(f' {px}help 2 - for page 2 | all or number of list cmds')
            bs.chatmessage(f' {px}help 3 - for page 3 | Other useful cmds')
            bs.chatmessage('===========================================')
        elif n[0] == '1':
            bs.chatmessage('============================')
            bs.chatmessage(f' {px}help 1 page 1 |')
            bs.chatmessage(f' {px}help 1 page 2 |')
            bs.chatmessage('============================')
            if len(n) > 2 and n[1] in ['page', 'Page']:
                if n[2] == '1':
                    bs.chatmessage('============== Help 1, Page 1 ==============')
                    bs.chatmessage(f' your command prefix is or all commands starts with - {px}')
                    bs.chatmessage(f' {px}list or {px}l --   to see ids of players and execute commands')
                    bs.chatmessage(f' {px}uniqeid or {px}id --   to see accountid/uniqeid of player')
                    bs.chatmessage(f' {px}quit or {px}restart  --  to restart the game')
                    bs.chatmessage(f' {px}mute/unmute  --  to mute chat for everyone in your game')
                elif n[2] == '2':
                    bs.chatmessage('============== Help 1, Page 2 ==============')
                    bs.chatmessage(f' {px}pause  --  to pause everyone in your game')
                    bs.chatmessage(f' {px}nv or {px}night  --  to make night in your game')
                    bs.chatmessage(f' {px}dv or {px}day  --  to make day in your game')
                    bs.chatmessage(f' {px}camera_mode  --  to rotate camera ,repeat to off')
                    bs.chatmessage('===========================================')
        elif n[0] == '2':
            bs.chatmessage('============================')
            bs.chatmessage(f' {px}help 2 page 1 |')
            bs.chatmessage(f' {px}help 2 page 2 |')
            bs.chatmessage(f' {px}help 2 page 3 |')
            bs.chatmessage('============================')
            if len(n) > 2 and n[1] in ['page', 'Page']:
                if n[2] == '1':
                    bs.chatmessage('============== Help 2 Page 1 ==============')
                    bs.chatmessage(f' {px}kill all or {px}kill number of list | kills the player')
                    bs.chatmessage(f' {px}heal all or {px}heal number of list | heals the players')
                    bs.chatmessage(f' {px}freeze all or {px}freeze number of list | freeze the player')
                    bs.chatmessage(f' {px}unfreeze/thaw all or {px}unfreeze/thaw number of list | unfreeze the player')
                    bs.chatmessage(f' {px}gloves all or {px}gloves number of list | give gloves to player')
                    bs.chatmessage('============================')
                elif n[2] == '2':
                    bs.chatmessage('============== Help 2 Page 2 ==============')
                    bs.chatmessage(f' {px}shield all or {px}shield number of list | give shield the player')
                    bs.chatmessage(f' {px}fall all or {px}fall number of list | teleport in down and fall up the player')
                    bs.chatmessage(f' {px}curse all or {px}curse number of list | curse the player')
                    bs.chatmessage(f' {px}creepy all or {px}creepy number of list | make creepy actor of player')
                    bs.chatmessage(f' {px}inv all or {px}inv number of list | makes invisible player')
                    bs.chatmessage(f' {px}celebrate all or {px}celebrate number of list | celebrate action to the player')
                    bs.chatmessage('============================')
                elif n[2] == '3':
                    bs.chatmessage('============== Help 2 Page 3 ==============')
                    bs.chatmessage(f' {px}gm all or {px}gm number of list | give bs gods like powers to player')
                    bs.chatmessage(f' {px}sp all or {px}sp number of list | give superrrrrrr damages when punch to player')
                    bs.chatmessage(f' {px}sleep all or {px}sleep number of list | sleep up the player')
                    bs.chatmessage(f' {px}fly all or {px}fly number of list | fly up the player ')
                    bs.chatmessage(f' {px}hug number of list | hugup the player')
                    bs.chatmessage('============================')
        elif n[0] == '3':
            bs.chatmessage('============================')
            bs.chatmessage(f" {px}d_bomb bombType | changes default bomb | do {px}d_bomb help for bomb names ")
            bs.chatmessage(f' {px}dbc (number of bombs) | changes default count of player')
            bs.chatmessage('============================')

    def _apply_to_players(self, activity_players: list, n: list[str], action: str):
        """اعمال اکشن به بازیکنان"""
        try:
            session = bs.get_foreground_host_session()
            if session is None:
                return

            session_players = session.sessionplayers

            if not n:
                bs.chatmessage(f'Use: {px}{action} all or {px}{action} number of list')
                return

            # اگر تعداد بازیکنان کمتر از 1 بود
            if not activity_players:
                bs.chatmessage('No players found')
                return

            if n[0] == 'all':
                for player in activity_players:
                    self._apply_action(player, action)
                bs.chatmessage(f'{action} applied to all')
            else:
                try:
                    index = int(n[0])
                    if 0 <= index < len(activity_players):
                        is_name = session_players[index].getname() if index < len(session_players) else f"Player {index}"
                        self._apply_action(activity_players[index], action)
                        bs.chatmessage(f'{action} applied to {is_name}')
                    else:
                        bs.chatmessage('Player index out of range')
                except ValueError:
                    bs.chatmessage('Please use a valid number')
                except:
                    bs.chatmessage('Could not find player')

        except Exception as e:
            print(f"Error in _apply_to_players: {e}")

    def _apply_action(self, player, action: str):
        """اعمال اکشن خاص به یک بازیکن"""
        try:
            if not player or not hasattr(player, 'actor') or not player.actor:
                return

            actor = player.actor
            if not hasattr(actor, 'node') or not actor.node:
                return

            node = actor.node

            if action == 'invisible':
                if node.torso_mesh is not None:
                    node.head_mesh = None
                    node.torso_mesh = None
                    node.upper_arm_mesh = None
                    node.forearm_mesh = None
                    node.pelvis_mesh = None
                    node.hand_mesh = None
                    node.toes_mesh = None
                    node.upper_leg_mesh = None
                    node.lower_leg_mesh = None
                    node.style = 'cyborg'

            elif action == 'headless':
                if node.head_mesh is not None:
                    node.head_mesh = None
                    node.style = 'cyborg'

            elif action == 'creepy':
                node.head_mesh = None
                node.handlemessage(bs.PowerupMessage(poweruptype='punch'))
                node.handlemessage(bs.PowerupMessage(poweruptype='shield'))

            elif action == 'kill':
                node.handlemessage(bs.DieMessage())

            elif action == 'heal':
                node.handlemessage(bs.PowerupMessage(poweruptype='health'))

            elif action == 'curse':
                node.handlemessage(bs.PowerupMessage(poweruptype='curse'))

            elif action == 'sleep':
                node.handlemessage('knockout', 8000)

            elif action == 'superpunch':
                if actor._punch_power_scale != 15:
                    actor._punch_power_scale = 15
                    actor._punch_cooldown = 0
                else:
                    actor._punch_power_scale = 1.2
                    actor._punch_cooldown = 400

            elif action == 'gloves':
                node.handlemessage(bs.PowerupMessage(poweruptype='punch'))

            elif action == 'shield':
                node.handlemessage(bs.PowerupMessage(poweruptype='shield'))

            elif action == 'freeze':
                node.handlemessage(bs.FreezeMessage())

            elif action == 'unfreeze':
                node.handlemessage(bs.ThawMessage())

            elif action == 'fall':
                node.handlemessage(bs.StandMessage())

            elif action == 'celebrate':
                node.handlemessage(bs.CelebrateMessage())

            elif action == 'fly':
                node.fly = not node.fly

            elif action == 'godmode':
                if not node.hockey:
                    node.hockey = True
                    node.invincible = True
                    actor._punch_power_scale = 7
                else:
                    node.hockey = False
                    node.invincible = False
                    actor._punch_power_scale = 1.2

        except Exception as e:
            print(f"Error in _apply_action: {e}")

    def _handle_bomb_command(self, activity_players: list, n: list[str]):
        """مدیریت دستور bomb"""
        if not n:
            bs.chatmessage(
                f'Use: {px}d_bomb/default_bomb all or {px}d_bomb number of list ,type {px}d_bomb help for help')
            return

        if n[0] == 'help':
            bs.chatmessage("bombtypes - ['ice', 'impact', 'land_mine', 'normal', 'sticky','tnt']")
            return

        bomb_types = ['ice', 'impact', 'land_mine', 'normal', 'sticky', 'tnt']
        if n[0] in bomb_types:
            for player in activity_players:
                if hasattr(player, 'actor') and player.actor:
                    player.actor.bomb_type = n[0]
            bs.chatmessage(f'default bomb type - {n[0]} now')
        else:
            bs.chatmessage(f'unknown bombtype , type {px}d_bomb help for help')

    def _handle_bomb_count(self, activity_players: list, n: list[str]):
        """مدیریت دستور bomb count"""
        if not n:
            bs.chatmessage(
                f'Use: {px}d_bomb_count/default_bomb/dbc all or {px}d_bomb_count/default_bomb_count/dbc number of list')
            return

        try:
            count = int(n[0])
            for player in activity_players:
                if hasattr(player, 'actor') and player.actor:
                    player.actor.set_bomb_count(count)
            bs.chatmessage(f'default bomb count is {count} now')
        except ValueError:
            bs.chatmessage('Must use number to use')


# ==================== کلاس پنجره منوی اصلی ====================
class NewMainMenuWindow(mainmenu.MainMenuWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Display chat icon
        bui.set_party_icon_always_visible(True)


# ==================== تابع پردازش دستورات ====================
_command_handler = ChatCommands()


def process_commands():
    """پردازش دستورات چت"""
    try:
        _command_handler.process_cmd()
    except Exception as e:
        print(f"Error in process_commands: {e}")


# ==================== پلاگین اصلی ====================
# ba_meta export babase.Plugin
class ChatCommandPlugin(babase.Plugin):
    """پلاگین دستورات چت"""

    def __init__(self):
        # تایمر برای بررسی دستورات
        self._timer = bs.AppTimer(0.3, process_commands, repeat=True)
        print("✅ Chat Command Plugin Loaded!")
        print(f"📝 Type {px}help for commands list")

    def on_app_running(self):
        # جایگزینی کلاس منوی اصلی
        mainmenu.MainMenuWindow = NewMainMenuWindow
        print(f"💡 Chat commands ready! Prefix: {px}")

    def has_settings_ui(self):
        return False