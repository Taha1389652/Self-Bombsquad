# ba_meta require api 9
# ba_meta name Star Trail
# ba_meta description Stars follow behind the player!

import babase
import bascenev1 as bs
import random
import math

# ============================================
# کلاس افکت ستاره‌ای
# ============================================
class StarTrailEffect:
    def __init__(self, spaz):
        self.spaz = spaz
        self.node = spaz.node
        self.active = True
        self.timer = None
        self.last_pos = None
        
    def start(self):
        """شروع افکت"""
        try:
            activity = bs.get_foreground_host_activity()
            if activity:
                with activity.context:
                    self.create_trail()
            else:
                bs.timer(0.5, self.start)
        except Exception:
            pass
    
    def create_trail(self):
        """ایجاد دنباله ستاره‌ای"""
        if not self.node or not self.node.exists() or not self.active:
            self.timer = None
            return
        
        try:
            pos = self.node.position
            
            # اگر موقعیت قبلی داریم، بینش خط بکش
            if self.last_pos:
                steps = 5
                for i in range(steps):
                    t = i / steps
                    x = self.last_pos[0] + (pos[0] - self.last_pos[0]) * t
                    y = self.last_pos[1] + (pos[1] - self.last_pos[1]) * t
                    z = self.last_pos[2] + (pos[2] - self.last_pos[2]) * t
                    
                    # ایجاد ستاره در این نقطه
                    self._create_star((x, y, z))
            
            self.last_pos = pos
            
        except Exception:
            pass
        
        # ادامه تایمر
        if self.active:
            self.timer = bs.timer(0.08, self.create_trail)
    
    def _create_star(self, pos):
        """ایجاد یک ستاره"""
        try:
            # رنگ تصادفی
            color = (
                random.uniform(0.5, 1.0),
                random.uniform(0.5, 1.0),
                random.uniform(0.5, 1.0)
            )
            
            # اندازه تصادفی
            size = random.uniform(0.1, 0.3)
            
            # ایجاد فلش (ستاره)
            flash = bs.newnode("flash",
                attrs={
                    'position': pos,
                    'size': size,
                    'color': color
                })
            
            # محو شدن تدریجی
            bs.animate(flash, 'size', {
                0: size,
                0.3: size * 0.5,
                0.6: 0
            })
            
            bs.animate(flash, 'opacity', {
                0: 1.0,
                0.3: 0.5,
                0.6: 0
            })
            
            # حذف بعد از ۰.۶ ثانیه
            bs.timer(0.7, flash.delete)
            
            # گاهی ذرات اضافی
            if random.random() < 0.3:
                bs.emitfx(
                    position=pos,
                    velocity=(
                        random.uniform(-0.5, 0.5),
                        random.uniform(0.5, 1.5),
                        random.uniform(-0.5, 0.5)
                    ),
                    count=2,
                    scale=0.1,
                    spread=0.1,
                    chunk_type='spark'
                )
                
        except Exception:
            pass
    
    def stop(self):
        """توقف افکت"""
        self.active = False
        if self.timer:
            self.timer = None


# ============================================
# پچ کردن کلاس PlayerSpaz
# ============================================
_original_init = None
_original_handlemessage = None

def new_spaz_init(self, *args, **kwargs):
    """اضافه کردن افکت به اسپاز"""
    global _original_init
    
    if _original_init:
        _original_init(self, *args, **kwargs)
    
    # اضافه کردن افکت بعد از ۰.۱ ثانیه
    def add_effect():
        try:
            effect = StarTrailEffect(self)
            effect.start()
            self._star_trail = effect
        except Exception:
            pass
    
    bs.timer(0.1, add_effect)

def new_handlemessage(self, msg):
    """پاک کردن افکت هنگام مرگ"""
    global _original_handlemessage
    
    if isinstance(msg, bs.DieMessage):
        if hasattr(self, '_star_trail'):
            try:
                self._star_trail.stop()
            except:
                pass
            delattr(self, '_star_trail')
    
    if _original_handlemessage:
        return _original_handlemessage(self, msg)
    return True


# ============================================
# پلاگین اصلی
# ============================================
# ba_meta export babase.Plugin
class StarTrailPlugin(babase.Plugin):
    def on_app_running(self):
        global _original_init, _original_handlemessage
        
        try:
            from bascenev1lib.actor.playerspaz import PlayerSpaz
            from bascenev1lib.actor.spaz import Spaz
            
            # ذخیره توابع اصلی
            _original_init = PlayerSpaz.__init__
            _original_handlemessage = Spaz.handlemessage
            
            # جایگزینی با توابع جدید
            PlayerSpaz.__init__ = new_spaz_init
            Spaz.handlemessage = new_handlemessage
            
            # پیام فعال‌سازی
            bs.timer(3.0, lambda: bs.broadcastmessage(
                "✨ Star Trail Activated!", 
                color=(0.5, 0.8, 1.0)
            ))
            
            print("✅ Star Trail Plugin loaded!")
            
        except Exception as e:
            print(f"❌ Error loading Star Trail: {e}")