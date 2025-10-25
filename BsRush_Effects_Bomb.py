# ba_meta require api 9

from __future__ import annotations
import babase
import bascenev1 as bs
from random import choice
import random

# ba_meta export plugin
class Plugin(babase.Plugin):

    def __init__(self):
        from bascenev1lib.actor import bomb
        bomb.Bomb.__init__ = self.new_bomb_init(bomb.Bomb.__init__)

    def new_bomb_init(self, original_init):
        def wrapped_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            Plugin.add_bomb_effects(self)
        return wrapped_init

    @staticmethod
    def add_bomb_effects(bomb_instance):
        if not bomb_instance.node:
            return

        bomb_type = getattr(bomb_instance, 'bomb_type', 'normal')
        display_name = Plugin.get_bomb_display_name(bomb_type)

        shield_radius = 1.2 if bomb_type == 'tnt' else 0.8

        shield = bs.newnode("shield", attrs={
            'color': (1, 1, 1),
            'position': bomb_instance.node.position,
            'radius': shield_radius
        })

        shield_colors = Plugin.get_bomb_shield_color(bomb_type)
        bs.animate_array(shield, 'color', 3, shield_colors, loop=True)

        bomb_instance.node.connectattr('position', shield, 'position')

        text_node = bs.newnode('text', attrs={
            'text': f'\ue00c{display_name}\ue00c',
            'in_world': True,
            'shadow': 2.5,  
            'flatness': 1.0,
            'color': (1, 1, 1),
            'scale': 0.012,
            'h_align': 'center'
        })

        text_math = bs.newnode('math', attrs={
            'input1': (0, 0.8, 0),
            'operation': 'add'
        })

        bomb_instance.node.connectattr('position', text_math, 'input2')
        text_math.connectattr('output', text_node, 'position')

        text_colors = Plugin.get_bomb_text_color(bomb_type)
        bs.animate_array(text_node, 'color', 3, text_colors, loop=True)

        bomb_instance.glow_shield = shield
        bomb_instance.glow_text = text_node
        bomb_instance.glow_text_math = text_math

        def create_boom_animation():

            boom_text = bs.newnode('text', attrs={
                'text': 'BOOM!',
                'in_world': True,
                'shadow': 2.0,  
                'flatness': 1.0,
                'color': (1, 0, 0),
                'scale': 0.02,
                'h_align': 'center',
                'v_align': 'center'
            })

            boom_math = bs.newnode('math', attrs={
                'input1': (0, 2, 0),
                'operation': 'add'
            })

            bomb_instance.node.connectattr('position', boom_math, 'input2')
            boom_math.connectattr('output', boom_text, 'position')

            bs.animate(boom_text, 'scale', {
                0: 0.01,
                0.2: 0.05,
                0.4: 0.04,
                0.6: 0.03,
                1.0: 0.0
            })

            bs.animate_array(boom_text, 'color', 3, {
                0: (1, 0, 0),
                0.3: (1, 1, 0),
                0.6: (1, 0.5, 0),
                1.0: (1, 0, 0)
            })

            if hasattr(bomb_instance, 'glow_shield') and bomb_instance.glow_shield.exists():

                final_radius = 4.0 if bomb_type == 'tnt' else 3.0
                
                bs.animate(bomb_instance.glow_shield, 'radius', {
                    0: shield_radius,
                    0.2: final_radius,
                    0.4: final_radius * 0.8,
                    0.6: final_radius * 0.5,
                    0.8: final_radius * 0.3,
                    1.0: 0.0
                })

                explosion_colors = Plugin.get_explosion_colors(bomb_type)
                bs.animate_array(bomb_instance.glow_shield, 'color', 3, explosion_colors)

            def cleanup_boom():
                if boom_text.exists():
                    boom_text.delete()
                if boom_math.exists():
                    boom_math.delete()

            bs.timer(1.0, cleanup_boom)

        def clean_up_effects():
            for attr in ['glow_shield', 'glow_text', 'glow_text_math']:
                node = getattr(bomb_instance, attr, None)
                if node and node.exists():
                    node.delete()

        original_handle_message = bomb_instance.handlemessage

        def new_handle_message(msg):
            if isinstance(msg, bs.DieMessage):

                create_boom_animation()

                bs.timer(0.1, clean_up_effects)
            return original_handle_message(msg)

        bomb_instance.handlemessage = new_handle_message

        def on_bomb_death():
            create_boom_animation()
            bs.timer(0.1, clean_up_effects)

        bomb_instance.node.add_death_action(bs.Call(on_bomb_death))

    @staticmethod
    def get_explosion_colors(bomb_type: str) -> dict:
        colors = {
            'normal': {
                0: (1, 0, 0),
                0.2: (1, 0.5, 0),
                0.4: (1, 1, 0),
                0.6: (0.5, 1, 0),
                0.8: (0, 1, 0),
                1.0: (0, 0.5, 0)
            },
            'ice': {
                0: (0.3, 0.7, 1.0),
                0.2: (0.5, 0.8, 1.0),
                0.4: (0.7, 0.9, 1.0),
                0.6: (0.5, 0.8, 1.0),
                0.8: (0.3, 0.7, 1.0),
                1.0: (0.1, 0.5, 1.0)
            },
            'tnt': {
                0: (1, 0, 0),
                0.2: (1, 0.3, 0),
                0.4: (1, 0.6, 0),
                0.6: (1, 0.3, 0),
                0.8: (1, 0, 0),
                1.0: (0.8, 0, 0)
            },
            'sticky': {
                0: (0, 1, 0),
                0.2: (0.3, 1, 0),
                0.4: (0.6, 1, 0),
                0.6: (0.3, 1, 0),
                0.8: (0, 1, 0),
                1.0: (0, 0.8, 0)
            },
            'impact': {
                0: (1, 0, 1),
                0.2: (1, 0.3, 1),
                0.4: (1, 0.6, 1),
                0.6: (1, 0.3, 1),
                0.8: (1, 0, 1),
                1.0: (0.8, 0, 0.8)
            }
        }
        return colors.get(bomb_type, colors['normal'])

    @staticmethod
    def get_bomb_shield_color(bomb_type: str) -> dict:
        colors = {
            'normal': {
                0: (1, 0, 0),
                0.2: (1, 1, 0),
                0.4: (0, 1, 0),
                0.6: (0, 1, 1),
                0.8: (1, 0, 1),
            },
            'ice': {
                0: (0.5, 0.8, 1.0),
                0.2: (0.7, 0.9, 1.0),
                0.4: (0.3, 0.7, 1.0),
                0.6: (0.5, 0.8, 1.0),
                0.8: (0.7, 0.9, 1.0),
            },
            'tnt': {
                0: (1, 0.2, 0.2),
                0.2: (1, 0.5, 0.2),
                0.4: (1, 0.8, 0.2),
                0.6: (1, 0.5, 0.2),
                0.8: (1, 0.2, 0.2),
            },
            'sticky': {
                0: (0, 1, 0),
                0.2: (0.5, 1, 0),
                0.4: (0, 1, 0.5),
                0.6: (0, 1, 1),
                0.8: (0, 1, 0),
            },
            'impact': {
                0: (1, 0, 1),
                0.2: (1, 0.5, 1),
                0.4: (0.5, 0, 1),
                0.6: (1, 0.5, 1),
                0.8: (1, 0, 1),
            }
        }
        return colors.get(bomb_type, colors['normal'])

    @staticmethod
    def get_bomb_text_color(bomb_type: str) -> dict:
        colors = {
            'normal': {
                0: (1, 0, 0),
                0.2: (1, 1, 0),
                0.4: (0, 1, 0),
                0.6: (0, 1, 1),
                0.8: (1, 0, 1),
            },
            'ice': {
                0: (0.3, 0.7, 1.0),
                0.2: (0.5, 0.8, 1.0),
                0.4: (0.7, 0.9, 1.0),
                0.6: (0.5, 0.8, 1.0),
                0.8: (0.3, 0.7, 1.0),
            },
            'tnt': {
                0: (1, 0, 0),
                0.2: (1, 0.3, 0),
                0.4: (1, 0.6, 0),
                0.6: (1, 0.3, 0),
                0.8: (1, 0, 0),
            },
            'sticky': {
                0: (0, 1, 0),
                0.2: (0.3, 1, 0),
                0.4: (0.6, 1, 0),
                0.6: (0.3, 1, 0),
                0.8: (0, 1, 0),
            },
            'impact': {
                0: (1, 0, 1),
                0.2: (1, 0.3, 1),
                0.4: (0.5, 0, 1),
                0.6: (1, 0.3, 1),
                0.8: (1, 0, 1),
            }
        }
        return colors.get(bomb_type, colors['normal'])

    @staticmethod
    def get_bomb_display_name(bomb_type: str) -> str:
        names = {
            'normal': 'BOMB',
            'sticky': 'STICK BOMB',
            'ice': 'ICE BOMB',
            'impact': 'IMPACT BOMB',
            'land_mine': 'MINE',
            'tnt': 'TNT',
            'curse': 'CURSE BOMB',
        }
        return names.get(bomb_type, bomb_type.upper())
