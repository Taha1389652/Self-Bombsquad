#کص مادر کسي که کد ها رو تيير بده يا کپي کنه((هر نوع استفاده))
from babase import (
    clipboard_is_supported as CIS,
    clipboard_get_text as CGT,
    clipboard_has_text as CHT,
    Plugin
)
from bauiv1 import (
    get_special_widget as gsw,
    containerwidget as cw,
    screenmessage as push,
    checkboxwidget as chk,
    scrollwidget as sw,
    buttonwidget as bw,
    SpecialChar as sc,
    textwidget as tw,
    checkboxwidget as cb,
    gettexture as gt,
    apptimer as teck,
    getsound as gs,
    UIScale as uis,
    charstr as cs,
    app as APP
)
from bascenev1 import (
    get_chat_messages as GCM,
    chatmessage as CM
)
from datetime import datetime as DT
import bauiv1lib.party as party

class SpamSystem:
    def __init__(s, source):
        w = s.w = NemSpamer.cw(
            source=source,
            size=(350, 290),
            ps=NemSpamer.UIS() * 0.8
        )
        tw(
            parent=w,
            text='اسپم',
            scale=1.2,
            h_align='center',
            position=(155, 265),
            color=(1, 0.5, 0)
        )
        tw(
            parent=w,
            text='پیام :',
            position=(15, 200),
            color=(0.8, 0.8, 0.8)
        )
        
        s.message_widget = tw(
            parent=w,
            size=(280, 35),
            editable=True,
            text='',
            position=(15, 170),
            color=(0.9, 0.9, 0.9),
            allow_clear_button=True
        )
        tw(
            parent=w,
            text='تعداد:',
            position=(15, 130),
            color=(0.8, 0.8, 0.8)
        )
        
        s.count_widget = tw(
            parent=w,
            size=(100, 35),
            editable=True,
            text='5',
            position=(20, 100),
            color=(0.9, 0.9, 0.9),
            allow_clear_button=True
        )
        tw(
            parent=w,
            text='ثانیه:',
            position=(150, 130),
            color=(0.8, 0.8, 0.8)
        )
        
        s.delay_widget = tw(
            parent=w,
            size=(100, 35),
            editable=True,
            text='2.0',
            position=(150, 100),
            color=(0.9, 0.9, 0.9),
            allow_clear_button=True
        )
        tw(
            parent=w,
            scale=0.9,
            position=(20, 70),
            text='@Bombsquad002',
            maxwidth=310,
            color=(0.6, 0.3, 0.6)
        )
        s.start_btn = NemSpamer.bw(
            parent=w,
            label='شروع',
            size=(120, 40),
            position=(40, 10),
            color=(0, 0.5, 0),
            on_activate_call=lambda: s.start_spam()
        )
        
        NemSpamer.bw(
            parent=w,
            label='پایان',
            size=(120, 40),
            position=(190, 10),
            color=(0.5, 0, 0),
            on_activate_call=lambda: s.stop_spam()
        )
        
        s.spam_active = False
        s.spam_timers = []
        s.message_counter = 0
        NemSpamer.swish()
    
    def start_spam(s):
        if s.spam_active:
            push('Spam already running!', color=(1, 0.6, 0))
            return
        
        message = tw(query=s.message_widget).strip()
        if not message:
            NemSpamer.err('Enter spam message!')
            return
        
        try:
            count = int(tw(query=s.count_widget))
            delay = float(tw(query=s.delay_widget))
        except:
            NemSpamer.err('Invalid count/delay!')
            return
        
        s.spam_active = True
        s.message_counter = 0
        try:
            bw(
                s.start_btn,
                color=(0, 0.3, 0),
                textcolor=(0.7, 1, 0.7)
            )
        except:
            pass
        
        push(f'Starting spam: {count} times', color=(0, 1, 0))
        push('Anti-Spam system is active', color=(0, 0.8, 0))
        s.spam_timers = []
        
        for i in range(count):
            def make_spam_task(idx, msg):
                return lambda: s.send_spam_message(msg, idx)
            
            timer = teck(i * delay, make_spam_task(i, message))
            s.spam_timers.append(timer)
        auto_stop_timer = teck(count * delay, lambda: s.stop_spam())
        s.spam_timers.append(auto_stop_timer)
    
    def send_spam_message(s, message, index):
        if not s.spam_active:
            return
        s.message_counter += 1
        number = s.message_counter
        final_message = f"{number}.{message}"
        
        CM(final_message)
        gs('dingSmall').play()
        if s.message_counter == 1:
            push(f'Message {number} ', color=(0, 0.8, 0.8))
    
    def stop_spam(s):
        if not s.spam_active:
            return
        
        s.spam_active = False
        try:
            bw(
                s.start_btn,
                color=(0, 0.5, 0),
                textcolor=(1, 1, 1)
            )
        except:
            pass
        for timer in s.spam_timers:
            try:
                timer.cancel()
            except:
                pass
        
        s.spam_timers.clear()
        s.message_counter = 0
        push('Spam stopped!', color=(1, 0.5, 0))
        gs('shieldDown').play()

class NemSpamer:
    @classmethod
    def UIS(c=0):
        i = APP.ui_v1.uiscale
        return [1.5, 1.1, 0.8][0 if i == uis.SMALL else 1 if i == uis.MEDIUM else 2]
    
    @classmethod
    def bw(c, **k):
        if 'color' in k:
            btn_color = k['color']
            del k['color']
            return bw(
                **k,
                textcolor=(1, 1, 1),
                enable_sound=False,
                button_type='square',
                color=btn_color
            )
        else:
            return bw(
                **k,
                textcolor=(1, 1, 1),
                enable_sound=False,
                button_type='square',
                color=(0, 0, 0)
            )
    
    @classmethod
    def cw(c, source, ps=0, **k):
        o = source.get_screen_space_center() if source else None
        r = cw(
            **k,
            scale=c.UIS() + ps,
            transition='in_scale',
            color=(0, 0, 0),
            parent=gsw('overlay_stack'),
            scale_origin_stack_offset=o
        )
        cw(r, on_outside_click_call=lambda: c.swish(t=r))
        return r
    
    @staticmethod
    def swish(t=None):
        gs('swish').play()
        if t:
            try:
                cw(t, transition='out_scale')
            except:
                pass
    
    @staticmethod
    def err(t):
        gs('block').play()
        push(t, color=(1, 1, 0))
    
    @staticmethod
    def ok():
        gs('dingSmallHigh').play()
        push('Okay!', color=(0, 1, 0))
    
    def __init__(s, source=None) -> None:
        w = s.w = s.cw(
            source=source,
            size=(260, 250),
        )
        [tw(
            scale=2,
            parent=w,
            text='Nem',
            h_align='center',
            position=(110 - i * 3, 205 - i * 3),
            color=[(1, 0.5, 0), (0.8, 0.4, 0)][i]
        ) for i in [1, 0]]
        
        [tw(
            scale=1,
            parent=w,
            text='SPAMER',
            h_align='center',
            position=(150 - i * 2, 175 - i * 2),
            color=[(0, 1, 1), (0, 0.8, 0.8)][i]
        ) for i in [1, 0]]
        s.spam_btn = NemSpamer.bw(
            label='SPAM',
            parent=w,
            size=(200, 65),
            position=(30, 80),
            icon=gt('spinner0'),
            color=(0.2, 0.2, 0.6),
            on_activate_call=lambda: SpamSystem(s.spam_btn)
        )
        tw(
            parent=w,
            scale=0.9,
            position=(110, 10),
            h_align='center',
            text='This mod is free',
            color=(0.6, 0.6,0)
        )
        
        NemSpamer.swish()

# ba_meta require api 9
# ba_meta export babase.Plugin
class NemSpamerPlugin(Plugin):
    def __init__(s):
        original_init = party.PartyWindow.__init__
        
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            button = NemSpamer.bw(
                icon=gt('spinner'),
                position=(self._width - 490, self._height - 210),
                parent=self._root_widget,
                iconscale=1.2,
                size=(20, 20),
                label=''
            )
            bw(button, on_activate_call=lambda: NemSpamer(source=button))
            clock_button = NemSpamer.bw(
                icon=gt('cuteSpaz'),
                position=(self._width - 160, self._height - 590),
                parent=self._root_widget,
                iconscale=0.5,
                size=(90, 30),
                label=DT.now().strftime("%H:%M"),
                color=(0.9, 0.5, 0.0),
                on_activate_call=lambda: s.send_time_to_chat()
            )
            s.clock_button = clock_button
            s.update_clock_button()
        
        party.PartyWindow.__init__ = new_init
    
    def update_clock_button(s):
        try:
            if hasattr(s, 'clock_button'):
                current_time = DT.now().strftime("%H:%M")
                bw(s.clock_button, label=current_time)
                teck(10, lambda: s.update_clock_button())
        except:
            pass
    
    def send_time_to_chat(s):
        current_time = DT.now().strftime("NemMod:%H:%M")
        CM(current_time)
        gs('dingSmallHigh').play()
        push('Time sent to chat!', color=(0, 1, 1))
