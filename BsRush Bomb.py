# ba_meta require api 9

import babase
import bascenev1 as bs
import random


class PluginSettings:
    ENABLED = True
    BOMB_AURA_ENABLED = True
    EXPLOSION_EFFECTS_ENABLED = True
    SPARK_EFFECT_ENABLED = True


def overload_aura(position):
    try:
        bs.emitfx(
            position=position,
            velocity=(0, 3, 0),
            count=120,
            scale=2.0,
            spread=0.2,
            chunk_type='spark'
        )
        
        bs.emitfx(
            position=position,
            velocity=(0, 3, 0),
            count=120,
            scale=1.0,
            spread=0.2,
            chunk_type='metal'
        )
        
        bs.emitfx(
            position=position,
            velocity=(0, 3, 0),
            count=120,
            scale=1.0,
            spread=0.2,
            chunk_type='ice'
        )

        color = random.choice([
            (1, 0, 0), (0, 1, 0), (0, 0, 1),
            (1, 1, 0), (0, 1, 1), (1, 0, 1)
        ])

        light = bs.newnode('light',
            attrs={
                'position': position,
                'color': color,
                'radius': 0.3,
                'intensity': 0.8,
                'volume_intensity_scale': 1.0
            })
        
        bs.timer(1.0, light.delete)
        
    except Exception:
        pass


def spark_effect(position):
    try:
        bs.emitfx(
            position=position,
            velocity=(0, 3, 0),
            count=20,
            scale=2.0,
            spread=0.2,
            chunk_type='spark'
        )
        
        bs.emitfx(
            position=position,
            velocity=(random.uniform(-2, 2), random.uniform(2, 5), random.uniform(-2, 2)),
            count=15,
            scale=1.5,
            spread=0.3,
            chunk_type='spark'
        )
        
        bs.emitfx(
            position=position,
            velocity=(random.uniform(-1, 1), random.uniform(1, 3), random.uniform(-1, 1)),
            count=10,
            scale=1.0,
            spread=0.1,
            chunk_type='spark'
        )

        spark_light = bs.newnode('light',
            attrs={
                'position': position,
                'color': (1, 0.8, 0.2),
                'radius': 0.4,
                'intensity': 0.6,
            })
        
        bs.animate(spark_light, 'intensity', {0: 0.6, 0.5: 0})
        bs.timer(0.6, spark_light.delete)
        
    except Exception:
        pass


def new_bomb_init(original_init):
    def wrapped_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        
        if hasattr(self, 'node') and self.node:
            change_bomb_color(self.node)
        
        if PluginSettings.BOMB_AURA_ENABLED:
            setup_bomb_aura(self)
        
        if PluginSettings.SPARK_EFFECT_ENABLED:
            setup_bomb_spark(self)
    
    return wrapped_init


def change_bomb_color(bomb_node):
    try:
        bomb_colors = [
            (1, 0.2, 0.2),
            (0.2, 1, 0.2),
            (0.2, 0.2, 1),
            (1, 1, 0.2),
            (1, 0.2, 1),
            (0.2, 1, 1),
            (1, 0.5, 0.2),
            (0.5, 0.2, 1),
        ]
        
        new_color = random.choice(bomb_colors)
        bomb_node.color = new_color
        
        bomb_light = bs.newnode('light',
            attrs={
                'position': bomb_node.position,
                'color': new_color,
                'radius': 0.5,
                'intensity': 0.3,
            })
        
        def update_light():
            if bomb_light.exists() and bomb_node.exists():
                bomb_light.position = bomb_node.position
            else:
                bomb_timer = None
        
        bomb_timer = bs.Timer(0.1, update_light, repeat=True)
        
        def cleanup_light():
            if bomb_light.exists():
                bomb_light.delete()
            if bomb_timer:
                bomb_timer = None
        
        bs.timer(10.0, cleanup_light)
        
    except Exception:
        pass


def setup_bomb_aura(bomb_instance):
    try:
        def add_aura():
            try:
                if not hasattr(bomb_instance, 'node') or not bomb_instance.node:
                    return
                
                position = bomb_instance.node.position
                overload_aura(position)
                
            except Exception:
                pass
        
        bs.timer(0.1, lambda: bs.timer(0.3, add_aura, repeat=True))
        
    except Exception:
        pass


def setup_bomb_spark(bomb_instance):
    try:
        def add_spark():
            try:
                if not hasattr(bomb_instance, 'node') or not bomb_instance.node:
                    return
                
                position = bomb_instance.node.position
                spark_effect(position)
                
            except Exception:
                pass
        
        bs.timer(0.2, lambda: bs.timer(0.5, add_spark, repeat=True))
        
    except Exception:
        pass


def new_blast_init(original_init):
    def wrapped_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        
        if PluginSettings.EXPLOSION_EFFECTS_ENABLED:
            add_explosion_effects(self, kwargs)
    
    return wrapped_init


def add_explosion_effects(blast_instance, kwargs):
    try:
        position = kwargs.get('position', (0, 1, 0))
        blast_type = kwargs.get('blast_type', 'normal')
        
        add_colored_scorch(position, blast_type)
        
        if random.random() < 0.7:
            add_light_flash(position, blast_type)
            
        add_boom_text_effect(position)
            
        if PluginSettings.SPARK_EFFECT_ENABLED:
            spark_effect(position)
            
    except Exception:
        pass


def add_colored_scorch(position, blast_type):
    try:
        scorch_radius = 2.0
        if blast_type == 'tnt':
            scorch_radius = 2.5
        elif blast_type == 'ice':
            scorch_radius = 1.8
        elif blast_type == 'impact':
            scorch_radius = 2.2
        elif blast_type == 'land_mine':
            scorch_radius = 2.3
        elif blast_type == 'sticky':
            scorch_radius = 1.9
        elif blast_type == 'curse':
            scorch_radius = 2.4
        
        scorch = bs.newnode('scorch', attrs={
            'position': position,
            'size': scorch_radius * 0.5,
            'big': (blast_type == 'tnt'),
        })
        
        color = get_blast_color(blast_type)
        scorch.color = babase.safecolor(color)
        
        bs.animate(scorch, 'presence', {3.0: 1, 8.0: 0})
        bs.timer(8.0, scorch.delete)
        
    except Exception:
        pass


def add_light_flash(position, blast_type):
    try:
        color = get_blast_color(blast_type)
        
        light = bs.newnode('light', attrs={
            'position': position,
            'color': color,
            'radius': 2.5,
            'intensity': 0.6
        })
        
        bs.animate(light, 'intensity', {
            0: 0.6,
            0.1: 0.3,
            0.2: 0
        })
        
        bs.timer(0.3, light.delete)
        
    except Exception:
        pass


def add_boom_text_effect(position):
    try:
        boom_text = "Boom!"
        
        text = bs.newnode('text', attrs={
            'text': boom_text,
            'in_world': True,
            'shadow': 0.2,
            'flatness': 1.0,
            'h_align': 'center',
            'v_align': 'center',
            'scale': 0.04,
            'color': (1, 0.7, 0.1)
        })
        
        text_pos = (position[0], position[1] + 0.3, position[2])
        text.position = text_pos
        
        bs.animate(text, 'opacity', {
            0: 0,
            0.1: 0.9,
            1.0: 0.9,
            2.0: 0
        })
        
        bs.animate_array(text, 'position', 3, {
            0: text_pos,
            2.0: (text_pos[0], text_pos[1] + 0.8, text_pos[2])
        })
        
        bs.timer(2.5, text.delete)
        
    except Exception:
        pass


def get_blast_color(blast_type):
    color_map = {
        'normal': (1.0, 0.3, 0.1),
        'tnt': (1.0, 0.1, 0.1),
        'ice': (0.3, 0.7, 1.0),
        'impact': (0.8, 0.6, 0.1),
        'land_mine': (0.9, 0.2, 0.8),
        'sticky': (0.2, 0.8, 0.2),
        'curse': (0.4, 0.1, 0.4),
        'blast_mini': (1.0, 0.5, 0.0),
    }
    return color_map.get(blast_type, (1.0, 0.5, 0.0))


# ba_meta export babase.Plugin
class UltimateBombEffectsPlugin(babase.Plugin):
    def __init__(self):
        self._apply_patches()
        
    def _apply_patches(self):
        try:
            from bascenev1lib.actor import bomb
            
            self.original_bomb_init = bomb.Bomb.__init__
            self.original_blast_init = bomb.Blast.__init__
            
            bomb.Bomb.__init__ = new_bomb_init(self.original_bomb_init)
            bomb.Blast.__init__ = new_blast_init(self.original_blast_init)
            
        except Exception:
            pass
    
    def on_app_launch(self):
        pass
    
    def on_app_shutdown(self):
        try:
            from bascenev1lib.actor import bomb
            bomb.Bomb.__init__ = self.original_bomb_init
            bomb.Blast.__init__ = self.original_blast_init
        except Exception:
            pass