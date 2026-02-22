# ba_meta require api 9
# ba_meta name BsRush Stars with Shields Advanced
# ba_meta description Stars with shields, trails, pulses and mini explosions
# Made by Taha

import bascenev1 as bs
import babase
import random
import math

_original_handlemessage = None
_original_init = None

class StarWithShield:
    def __init__(self, node, shield):
        self.node = node
        self.shield = shield
        self.offset_angle = 0
        self.radius = 1.2
        self.last_pos = None
        self.pulse_timer = 0
        self.explosion_timer = random.randint(30, 90)

class RotatingStarsEffect:
    def __init__(self, spaz):
        self.spaz = spaz
        self.node = spaz.node
        self.active = True
        self.timer = None
        self.stars = []
        self.angle = 0
        
    def start(self):
        try:
            activity = bs.get_foreground_host_activity()
            if activity:
                with activity.context:
                    self.create_stars()
            else:
                bs.timer(0.5, self.start)
        except Exception:
            pass
    
    def create_star_with_shield(self, offset_angle):
        """ساخت یک ستاره با شیلد مخصوص خودش"""
        try:
            pos = self.node.position
            
            # ایجاد فلش (ستاره)
            flash = bs.newnode("flash",
                owner=self.node,
                attrs={
                    'position': pos,
                    'size': 0.3,
                    'color': (1, 1, 1)
                })
            
            # انیمیشن رنگ RGB
            bs.animate_array(flash, 'color', 3, {
                0: (random.choice([1, 2, 3, 4, 5]), 
                    random.choice([1, 2, 3, 4, 5]), 
                    random.choice([1, 2, 3, 4, 5])),
                0.2: (2, 0, 2),
                0.4: (2, 2, 0),
                0.6: (0, 2, 0),
                0.8: (0, 2, 2)
            }, loop=True)
            
            # پالس نوری (تغییر سایز)
            bs.animate(flash, 'size', {
                0: 0.3,
                0.5: 0.4,
                1.0: 0.3
            }, loop=True)
            
            # ایجاد شیلد
            shield = bs.newnode("shield",
                owner=self.node,
                attrs={
                    'color': (1, 1, 1),
                    'position': pos,
                    'radius': 0.35,
                    'opacity': 0.25
                })
            
            # انیمیشن رنگ شیلد
            bs.animate_array(shield, 'color', 3, {
                0: (2, 0, 2),
                0.2: (2, 2, 0),
                0.4: (0, 2, 0),
                0.6: (0, 2, 2),
                0.8: (2, 0, 2)
            }, loop=True)
            
            star = StarWithShield(flash, shield)
            star.offset_angle = offset_angle
            star.last_pos = pos
            self.stars.append(star)
            
        except Exception:
            pass
    
    def create_trail(self, star, old_pos, new_pos):
        """ایجاد دنباله نور"""
        try:
            steps = 5
            for i in range(steps):
                t = i / steps
                x = old_pos[0] + (new_pos[0] - old_pos[0]) * t
                y = old_pos[1] + (new_pos[1] - old_pos[1]) * t
                z = old_pos[2] + (new_pos[2] - old_pos[2]) * t
                
                # نور دنباله
                trail_light = bs.newnode('light',
                    owner=self.node,
                    attrs={
                        'position': (x, y, z),
                        'color': (0.8, 0, 0.8),  # نور کمتر
                        'radius': 0.1,
                        'intensity': 0.15  # نور کمتر
                    })
                bs.timer(0.1 * (steps - i), trail_light.delete)
                
                # ذرات ریز دنباله
                if i % 2 == 0:
                    bs.emitfx(
                        position=(x, y, z),
                        velocity=(0, 0.2, 0),
                        count=1,
                        scale=0.1,
                        spread=0.05,
                        chunk_type='spark'
                    )
        except:
            pass
    
    def create_mini_explosion(self, pos):
        """ایجاد انفجار کوچک"""
        try:
            # نور انفجار
            explosion_light = bs.newnode('light',
                owner=self.node,
                attrs={
                    'position': pos,
                    'color': (1, 1, 0),
                    'radius': 0.4,
                    'intensity': 0.5
                })
            bs.animate(explosion_light, 'intensity', {0: 0.5, 0.1: 0.2, 0.2: 0.0})
            bs.timer(0.3, explosion_light.delete)
            
            # ذرات انفجار
            for _ in range(5):
                bs.emitfx(
                    position=pos,
                    velocity=(random.uniform(-1, 1), 
                             random.uniform(0.5, 2), 
                             random.uniform(-1, 1)),
                    count=3,
                    scale=0.2,
                    spread=0.2,
                    chunk_type='spark'
                )
                
            # صدای انفجار کوچک
            bs.getsound('click01').play(0.3)
            
        except:
            pass
    
    def create_particles(self, pos):
        """ایجاد ذرات ریز دور ستاره"""
        try:
            for _ in range(2):
                angle = random.uniform(0, 2 * math.pi)
                rad = math.radians(random.uniform(0, 360))
                
                x = pos[0] + math.cos(angle) * 0.2
                z = pos[2] + math.sin(angle) * 0.2
                
                bs.emitfx(
                    position=(x, pos[1] + 0.1, z),
                    velocity=(math.cos(angle) * 0.5, 
                             random.uniform(0.1, 0.3), 
                             math.sin(angle) * 0.5),
                    count=1,
                    scale=0.1,
                    spread=0.03,
                    chunk_type='spark'
                )
        except:
            pass
    
    def create_stars(self):
        """ساخت ۳ ستاره"""
        self.create_star_with_shield(0)      # ستاره اول
        self.create_star_with_shield(120)    # ستاره دوم
        self.create_star_with_shield(240)    # ستاره سوم
        
        if self.active:
            self.timer = bs.timer(0.05, self.update_rotation)
    
    def update_rotation(self):
        if not self.node or not self.node.exists() or not self.active:
            return
        
        try:
            pos = self.node.position
            self.angle += 3
            current_time = bs.time()
            
            for star in self.stars:
                if star.node and star.node.exists():
                    current_angle = math.radians(self.angle + star.offset_angle)
                    
                    x = pos[0] + math.cos(current_angle) * star.radius
                    z = pos[2] + math.sin(current_angle) * star.radius
                    y = pos[1] + 0.4
                    
                    new_pos = (x, y, z)
                    old_pos = star.node.position
                    
                    # دنباله نور
                    if star.last_pos:
                        self.create_trail(star, star.last_pos, new_pos)
                    
                    star.node.position = new_pos
                    star.last_pos = new_pos
                    
                    if star.shield and star.shield.exists():
                        star.shield.position = new_pos
                    
                    # ذرات ریز دور ستاره
                    if random.random() < 0.3:
                        self.create_particles(new_pos)
                    
                    # پالس نوری اضافی
                    if random.random() < 0.1:
                        pulse_light = bs.newnode('light',
                            owner=self.node,
                            attrs={
                                'position': new_pos,
                                'color': (1, 0, 1),
                                'radius': 0.25,
                                'intensity': 0.3
                            })
                        bs.timer(0.1, pulse_light.delete)
                    
                    # انفجار کوچک
                    star.explosion_timer -= 1
                    if star.explosion_timer <= 0:
                        self.create_mini_explosion(new_pos)
                        star.explosion_timer = random.randint(60, 120)
                        
        except Exception:
            pass
        
        if self.active:
            self.timer = bs.timer(0.05, self.update_rotation)
    
    def stop(self):
        self.active = False
        for star in self.stars:
            if star.node and star.node.exists():
                star.node.delete()
            if star.shield and star.shield.exists():
                star.shield.delete()
        self.stars.clear()
        if self.timer:
            self.timer = None

def new_init(self, *args, **kwargs):
    if _original_init:
        _original_init(self, *args, **kwargs)
    
    def add_effect():
        try:
            effect = RotatingStarsEffect(self)
            effect.start()
            self._stars_effect = effect
        except Exception:
            pass
    
    bs.timer(0.1, add_effect)

def new_handlemessage(self, msg):
    if isinstance(msg, bs.DieMessage):
        if hasattr(self, '_stars_effect'):
            try:
                self._stars_effect.stop()
            except:
                pass
            delattr(self, '_stars_effect')
    
    if _original_handlemessage:
        return _original_handlemessage(self, msg)
    return True

# ba_meta export babase.Plugin
class StarsAdvancedPlugin(babase.Plugin):
    def on_app_running(self):
        global _original_handlemessage, _original_init
        
        try:
            from bascenev1lib.actor.playerspaz import PlayerSpaz
            from bascenev1lib.actor.spaz import Spaz
            
            _original_init = PlayerSpaz.__init__
            _original_handlemessage = Spaz.handlemessage
            
            PlayerSpaz.__init__ = new_init
            Spaz.handlemessage = new_handlemessage
            
            bs.timer(5.0, lambda: bs.broadcastmessage("✨ Advanced Stars Effect Activated!", color=(1, 0, 1)))
            print("✅ Advanced Stars Effect loaded!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
