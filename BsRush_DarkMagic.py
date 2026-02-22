# ba_meta require api 9
# ba_meta name BsRush Effect Made By Taha / BsRush
# ba_meta description Dark magic effect for players

import bascenev1 as bs
import babase
import random
from bascenev1lib.actor.spazfactory import SpazFactory

_original_spaz_handlemessage = None
_original_spaz_init = None

class DarkMagicEffect:
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

def new_spaz_init(self, *args, **kwargs):
    global _original_spaz_init
    if _original_spaz_init:
        _original_spaz_init(self, *args, **kwargs)
    
    def add_effect():
        try:
            effect = DarkMagicEffect(self)
            effect.start()
            self._darkmagic_effect = effect
        except Exception:
            pass
    
    bs.timer(0.1, add_effect)

def new_handlemessage(self, msg):
    global _original_spaz_handlemessage
    if isinstance(msg, bs.DieMessage):
        if hasattr(self, '_darkmagic_effect'):
            try:
                self._darkmagic_effect.stop()
            except:
                pass
            delattr(self, '_darkmagic_effect')
    
    if _original_spaz_handlemessage:
        return _original_spaz_handlemessage(self, msg)
    return True

# ba_meta export babase.Plugin
class DarkMagicPlugin(babase.Plugin):
    def on_app_running(self):
        global _original_spaz_handlemessage, _original_spaz_init
        
        try:
            from bascenev1lib.actor.playerspaz import PlayerSpaz
            from bascenev1lib.actor.spaz import Spaz
            
            _original_spaz_init = PlayerSpaz.__init__
            _original_spaz_handlemessage = Spaz.handlemessage
            
            PlayerSpaz.__init__ = new_spaz_init
            Spaz.handlemessage = new_handlemessage
            
            bs.timer(5.0, lambda: bs.broadcastmessage("🌑 Dark Magic Activated!", color=(0.5, 0.0, 1.0)))
            
        except Exception as e:
            print(f"Error loading Dark Magic: {e}")
