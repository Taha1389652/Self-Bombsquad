# ba_meta require api 9
import babase
import bascenev1 as bs
from bascenev1lib.actor import spaz
from bascenev1lib.actor.bomb import Blast
import weakref
from typing import Any

_original_on_jump_press = spaz.Spaz.on_jump_press
_original_on_punch_press = spaz.Spaz.on_punch_press
_original_on_pickup_press = spaz.Spaz.on_pickup_press
_original_on_bomb_press = spaz.Spaz.on_bomb_press
_original_handlemessage = spaz.Spaz.handlemessage

TACTICS_CONFIG = {
    'BOXING_GLOVES': 'UUUUD', # مثال تغییر: 'UUUDR'
    'AURA': 'UUUUL',
    'TELEPORT': 'LLLLD',
    'AIR_DASH': 'LU',
    'BACKFLIP': 'LD'
}

def _create_real_explosion(spaz_node, blast_type='normal'):
    if not spaz_node.node.exists(): return
    
    p = spaz_node.node.position

    spaz_node.node.invincible = True
    
    
    def _remove_inv():
        if spaz_node.node and spaz_node.node.exists():
            spaz_node.node.invincible = False
            
    bs.timer(0.2, _remove_inv)
    
    try:
        sp = spaz_node.getplayer(bs.Player, False)
    except Exception:
        sp = None
        
    # ایجاد انفجار
    Blast(
        position=p,
        velocity=(0, 0, 0),
        blast_radius=3.0 if blast_type == 'tnt' else 2.0,
        blast_type=blast_type,
        source_player=sp
    ).autoretain()


def _do_boxing_gloves(self) -> bool:
    t = bs.time() 
    if not hasattr(self, '_last_glove_time'): self._last_glove_time = -999.0
    
    if t - self._last_glove_time >= 5.0:
        if not self.node.exists(): return False
        self.equip_boxing_gloves()
        
        _create_real_explosion(self, blast_type='normal')
        
        self._last_glove_time = t
        return True
    return False

def _do_teleport(self) -> bool:
    t = bs.time() 
    if not hasattr(self, '_last_teleport_time'): self._last_teleport_time = -999.0
    
    if t - self._last_teleport_time >= 1.0:
        if not self.node.exists(): return False
        p = self.node.position
        dx = self.node.move_left_right
        dz = -self.node.move_up_down
        
        bs.emitfx(position=p, count=15, scale=0.4, spread=0.3, chunk_type='spark')
        
        if abs(dx) < 0.1 and abs(dz) < 0.1:
            new_p = (p[0], p[1] + 0.2, p[2])
        else:
            new_p = (p[0] + (dx * 2.0), p[1] + 0.2, p[2] + (dz * 2.0))
            
        self.node.handlemessage('stand', new_p[0], new_p[1], new_p[2], 0)
        
        bs.emitfx(position=new_p, count=15, scale=0.4, spread=0.3, chunk_type='spark')
        bs.getsound('shieldDown').play(position=new_p, volume=1.0)
        
        self._last_teleport_time = t
        return True
    return False

def _do_aura(self) -> bool:
    t = bs.time() 
    if not hasattr(self, '_last_aura_time'): self._last_aura_time = -999.0
    
    if t - self._last_aura_time >= 30.0:
        if not self.node.exists(): return False
        
        _create_real_explosion(self, blast_type='tnt')
        
        if hasattr(self, 'custom_aura_shield') and self.custom_aura_shield:
            self.custom_aura_shield.delete()
            
        self.custom_aura_shield = bs.newnode('shield', owner=self.node, attrs={
            'color': (1.0, 1.0, 0.0), 
            'radius': 1.1
        })
        self.node.connectattr('position_center', self.custom_aura_shield, 'position')
        
        if not hasattr(self, '_original_punch_power'):
            self._original_punch_power = self._punch_power_scale
        self._punch_power_scale = self._original_punch_power * 2.0
        
        if not hasattr(self, '_original_hitpoints_max'):
            self._original_hitpoints_max = self.hitpoints_max
        self.hitpoints_max = int(self._original_hitpoints_max * 5.0)
        self.hitpoints = int(self.hitpoints * 5.0)
        
        weak_self_sparks = weakref.ref(self)
        def _aura_sparks():
            s = weak_self_sparks()
            if s and s.node and s.node.exists():
                pos = s.node.position
                bs.emitfx(position=(pos[0], pos[1]-0.5, pos[2]), count=8, scale=0.4, spread=0.2, chunk_type='spark')
                
        self._aura_timer = bs.Timer(0.15, _aura_sparks, repeat=True)
        
        weak_self = weakref.ref(self)
        def _stop_aura():
            s = weak_self()
            if s and s.node and s.node.exists():
                if hasattr(s, 'custom_aura_shield') and s.custom_aura_shield:
                    s.custom_aura_shield.delete()
                if hasattr(s, '_original_punch_power'):
                    s._punch_power_scale = s._original_punch_power
                if hasattr(s, '_original_hitpoints_max'):
                    s.hitpoints_max = s._original_hitpoints_max
                    s.hitpoints = int(min(s.hitpoints / 5.0, s.hitpoints_max))
                s._aura_timer = None

        bs.Timer(30.0, _stop_aura)
        self._last_aura_time = t
        return True
    return False

def _do_air_dash(self) -> bool:
    t = bs.time() 
    if not hasattr(self, '_custom_last_dash_time'): self._custom_last_dash_time = -999.0
    
    if t - self._custom_last_dash_time >= 0.0001:
        if not self.node.exists(): return False
        p = self.node.position
        dx = self.node.move_left_right
        dz = -self.node.move_up_down
        
        if abs(dx) > 0.1 or abs(dz) > 0.1:
            force_x = dx * 36
            force_z = dz * 36
            force_y = 4 
            
            self.node.handlemessage("impulse", p[0], p[1] + 0.5, p[2], 0, 0, 0, 200, 50, 0, 0, force_x, force_y, force_z)
            
            bs.emitfx(position=p, count=50, scale=2.0, spread=0.5, chunk_type='sweat')
            bs.getsound('swish').play(position=p, volume=1.0)
            
            self._custom_last_dash_time = t
            return True
    return False

def _do_backflip(self) -> bool:
    t = bs.time() 
    if not hasattr(self, '_last_backflip_time'): self._last_backflip_time = -999.0
    
    if t - self._last_backflip_time >= 0.01:
        if not self.node.exists(): return False
        p = self.node.position
        v = self.node.velocity
        
        self.node.handlemessage("impulse", p[0], p[1]+3.5, p[2], v[0], v[1], v[2], 50*self.node.run, 10*self.node.run, 0, 0, v[0], v[1], v[2])
        self.node.handlemessage("impulse", p[0], p[1]+3.6, p[2], v[0], v[1], v[2], 50*self.node.run, 10*self.node.run, 0, 0, v[0], v[1], v[2])
        self.node.handlemessage('impulse', p[0], p[1]+0.001, p[2], 0, 0.2, 0, 200, 200, 0, 0, 0, 5, 0)
        
        bs.emitfx(position=p, count=15, scale=1.2, spread=0.4, chunk_type='sweat')
        bs.emitfx(position=p, count=15, scale=1.0, spread=0.3, chunk_type='rock')
        
        self._last_backflip_time = t
        return True
    return False

def _handle_press_events(self, key: str) -> bool:
    if not self.node or not self.node.exists(): return False
    
    t = bs.time() 
    if not hasattr(self, '_combo_buffer'):
        self._combo_buffer = ""
        self._last_input_time = -999.0
        
    if t - self._last_input_time > 0.2:
        self._combo_buffer = ""
        
    self._combo_buffer += key
    self._last_input_time = t
    
    sorted_tactics = sorted(TACTICS_CONFIG.items(), key=lambda item: len(item[1]), reverse=True)
    
    for power_name, combo_string in sorted_tactics:
        if self._combo_buffer.endswith(combo_string):
            power_triggered = False
            
            if power_name == 'BOXING_GLOVES': power_triggered = _do_boxing_gloves(self)
            elif power_name == 'AURA': power_triggered = _do_aura(self)
            elif power_name == 'TELEPORT': power_triggered = _do_teleport(self)
            elif power_name == 'AIR_DASH': power_triggered = _do_air_dash(self)
            elif power_name == 'BACKFLIP':
                if abs(self.node.move_up_down) >= 0.01 or abs(self.node.move_left_right) >= 0.01:
                    power_triggered = _do_backflip(self)
            
            if power_triggered:
                self._combo_buffer = ""
                return True
                
    return False



def my_new_handlemessage(self, msg: Any) -> Any:
    
    return _original_handlemessage(self, msg)

def my_new_on_punch_press(self) -> None:
    _original_on_punch_press(self)
    _handle_press_events(self, 'L')

def my_new_on_pickup_press(self) -> None:
    _original_on_pickup_press(self)
    _handle_press_events(self, 'U')

def my_new_on_bomb_press(self) -> None:
    _original_on_bomb_press(self)
    _handle_press_events(self, 'R')

def my_new_on_jump_press(self) -> None:
    _original_on_jump_press(self)
    if not self.node or not self.node.exists(): return
    
    if _handle_press_events(self, 'D'):
        self._custom_jump_count = 2
        return

    t = bs.time() 
    if not hasattr(self, '_custom_last_jump_time'):
        self._custom_last_jump_time = -999.0
        self._custom_jump_count = 0
        
    time_since_last_jump = t - self._custom_last_jump_time
    p = self.node.position
    
    if time_since_last_jump < 0.1 and self._custom_jump_count == 1:
        self.node.handlemessage("impulse", p[0], p[1]+3.5, p[2], 0, 0, 0, 50, 10, 0, 0, 0, 5, 0)
        self.node.handlemessage("impulse", p[0], p[1]+3.6, p[2], 0, 0, 0, 50, 10, 0, 0, 0, 5, 0)
        self.node.handlemessage('impulse', p[0], p[1]+0.001, p[2], 0, 0.2, 0, 200, 200, 0, 0, 0, 5, 0)
        
        bs.emitfx(position=p, count=10, scale=0.5, spread=0.2, chunk_type='spark')
        self._custom_jump_count = 2 
        
    elif time_since_last_jump >= 0.1:
        self._custom_jump_count = 1
        
    self._custom_last_jump_time = t

# ba_meta export babase.Plugin
class TysonGokuMod(babase.Plugin):
    def on_app_running(self) -> None:
        spaz.Spaz.on_jump_press = my_new_on_jump_press
        spaz.Spaz.on_punch_press = my_new_on_punch_press
        spaz.Spaz.on_pickup_press = my_new_on_pickup_press
        spaz.Spaz.on_bomb_press = my_new_on_bomb_press
        spaz.Spaz.handlemessage = my_new_handlemessage