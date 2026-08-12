# ba_meta require api 9
#کص مادر هرکي به هر نحوي از اين کد ها استفاده کنه و به اسم خودش ثبت کنه
from babase import Plugin
from bauiv1 import (
    get_special_widget as gsw,
    containerwidget as cw,
    screenmessage as push,
    checkboxwidget as chk,
    scrollwidget as sw,
    buttonwidget as bw,
    SpecialChar as sc,
    textwidget as tw,
    gettexture as gt,
    apptimer as teck,
    getsound as gs,
    UIScale as uis,
    charstr as cs,
    app as APP,
    CallPartial,
    CallStrict
)
from bascenev1 import (
    get_chat_messages as GCM,
    chatmessage as CM,
    get_game_roster as GGR
)
from _babase import get_string_width as strw
from datetime import datetime as DT
from bauiv1lib import party

DEFAULT_SWEARS = [
    "مادر",
    "کاييدم",
    "ک3 ننت",
    "ننت",
    "مادر چنده",
    "خرومزاده",
    " Mj",
    "مامیت ",
    "مادرت ",
    "مدرت ",
    "بیناموس",
    "بیناموص",
    "خارتو ",
    "کاییدم ",
    "گییدم ",
    "حرمزاده ",
    "حرمزده ",
    "هرومزاده ",
    "چنده ",
    "مادرچنده ",
    "تحمسگ ",
    "تخمسگ ",
    "ک۳خارت",
    "گصخارت"
]

class SwearOptionsPanel:
    def __init__(s, source):
        w = s.w = AR.cw(
            source=source,
            size=(350, 290),
            ps=AR.UIS() * 0.8
        )
        
        tw(
            parent=w,
            text='SWEAR OPTIONS',
            scale=1.5,
            h_align='center',
            position=(150, 260),
            color=(1, 0.3, 0.3)
        )
        
        buttons = [
            ('Add New Swear', 'AddSwear', (35, 200)),
            ('Remove Swear', 'RemoveSwear', (190, 200)),
            ('View All Swears', 'SwearList', (35, 80)),
            ('Load Default Swears', 'load_default_swears', (190,140)),
            ('Clear All Swears', 'clear_all_swears', (35, 140)),
            ('Settings', 'Settings', (190, 80))
        ]
        tw(
            parent=w,
            text=f'Total Swear Words: {len(var("swears") or {})}',
            scale=0.8,
            position=(150, 40),
            h_align='center',
            color=(0.8, 0.8, 1)
        )

        tw(
            parent=w,
            text='https://t.me/SinglMod',
            scale=0.8,
            h_align='center',
            position=(150, 10),
            color=(0, 0.5, 0.3)
        )
            
        mem = globals()
        for label, action, pos in buttons:
            if action in ['load_default_swears', 'clear_all_swears']:
                on_activate = getattr(s, action)
            else:
                on_activate = CallPartial(mem[action], w)
            
            s.create_button(
                label=label,
                parent=w,
                size=(130, 45),
                position=pos,
                on_activate_call=on_activate,
                color=(0.3, 0.3, 0.5)
            )
        
        AR.swish()
    
    def create_button(s, **kwargs):
        button_color = kwargs.pop('color', (0.25, 0.25, 0.35))
        return bw(
            **kwargs,
            color=button_color,
            enable_sound=True,
            button_type='square'
        )
    
    def load_default_swears(s):
        swears_dict = {}
        swears_lc_dict = {}
        
        for swear in DEFAULT_SWEARS:
            swears_dict[swear] = True
            swears_lc_dict[swear.lower()] = True
        
        var('swears', swears_dict)
        var('swears_lc', swears_lc_dict)
        
        push('Default swear words loaded!', color=(0, 1, 0))
        gs('dingSmallHigh').play()
    
    def clear_all_swears(s):
        var('swears', {})
        var('swears_lc', {})
        push('All swear words cleared!', color=(1, 0.5, 0))
        gs('laser').play()

class WhiteListOptionsPanel:
    def __init__(s, source):
        w = s.w = AR.cw(
            source=source,
            size=(350, 290),
            ps=AR.UIS() * 0.8
        )
        tw(
            parent=w,
            text='WHITE LIST OPTIONS',
            scale=1.2,
            h_align='center',
            position=(150, 260),
            color=(0.3, 1, 0.3)
        )
        buttons = [
            ('Add to White List', 'AddWhiteList', (35, 210)),
            ('Remove from White List', 'RemoveWhiteList', (190, 210)),
            ('View White List', 'WhiteListView', (190, 150)),
            ('Clear White List', 'clear_white_list', (35, 150))
        ]
        s.white_list_toggle = chk(
            parent=w,
            text='White List Enabled',
            size=(200, 30),
            position=(50, 100),
            value=var('white_list_enabled'),
            on_value_change_call=CallPartial(var, 'white_list_enabled'),
            color=(0, 1, 0.6)
        )
        tw(
            parent=w,
            text=f'Names in White List: {len(var("white_list") or {})}',
            scale=0.8,
            position=(150, 50),
            h_align='center',
            color=(0.8, 1, 0.8)
        )
        
        mem = globals()
        for label, action, pos in buttons:
            if action == 'clear_white_list':
                on_activate = s.clear_white_list
            else:
                on_activate = CallPartial(mem[action], w)
            
            s.create_button(
                label=label,
                parent=w,
                size=(130, 45),
                position=pos,
                on_activate_call=on_activate,
                color=(0.3, 0.3, 0.5)
            )
        
        AR.swish()
    
    def create_button(s, **kwargs):
        button_color = kwargs.pop('color', (0.25, 0.25, 0.35))
        return bw(
            **kwargs,
            color=button_color,
            enable_sound=True,
            button_type='square'
        )
    
    def clear_white_list(s):
        var('white_list', {})
        var('white_list_lc', {})
        push('White list cleared!', color=(0.5, 1, 0.5))
        gs('laser').play()

class AddSwear:
    def __init__(s, t):
        w = AR.cw(
            source=t,
            size=(400, 200),
            ps=AR.UIS() * 0.8
        )
        
        tw(
            parent=w,
            text='ADD NEW SWEAR WORD',
            scale=1.2,
            h_align='center',
            position=(175, 165),
            color=(1, 0.5, 0.5)
        )
        
        tw(
            parent=w,
            text='Enter the swear word to detect:',
            scale=0.7,
            position=(30, 120),
            color=(0.9, 0.9, 0.9)
        )
        input_container = cw(
            parent=w,
            size=(300, 35),
            position=(50, 85),
            color=(0.2, 0.2, 0.2)
        )
        
        s.swear_input = tw(
            parent=input_container,
            maxwidth=300,
            size=(300, 35),
            editable=True,
            v_align='center',
            h_align='center',
            color=(1, 1, 1),
            position=(0, 0),
            allow_clear_button=False
        )
        
        s.create_button(
            parent=w,
            label='Add',
            size=(100, 40),
            position=(150, 30),
            on_activate_call=CallStrict(s._add),
            color=(0.8, 0.2, 0.2)
        )
        
        AR.swish()
    
    def create_button(s, **kwargs):
        button_color = kwargs.pop('color', (0.25, 0.25, 0.35))
        return bw(
            **kwargs,
            color=button_color,
            enable_sound=True,
            button_type='square'
        )
    
    def _add(s):
        swear = tw(query=s.swear_input).strip().replace('\n', ' ')
        
        if not swear:
            AR.err('Enter a swear word!')
            return
        
        l = var('swears') or {}
        lc = var('swears_lc') or {}
        
        if swear.lower() in lc:
            AR.err('This swear word already exists!')
            return
        
        l.update({swear: True})
        lc.update({swear.lower(): True})
        
        var('swears', l)
        var('swears_lc', lc)
        
        tw(s.swear_input, text='')
        AR.ok()

class RemoveSwear:
    def __init__(s, t):
        i = len(var('swears') or {})
        if not i:
            AR.err('Add some swear words first!')
            return
            
        w = AR.cw(
            source=t,
            size=(400, 290),
            ps=AR.UIS() * 0.8
        )
        
        tw(
            parent=w,
            text='REMOVE SWEAR WORD',
            scale=1.2,
            h_align='center',
            position=(175, 250),
            color=(1, 0.5, 0.5)
        )
        
        a = sw(
            parent=w,
            size=(360, 150),
            position=(20, 80)
        )
        
        s.c = cw(
            parent=a,
            size=(360, i * 40),
            background=False
        )
        
        s.create_button(
            parent=w,
            label='REMOVE SELECTED',
            size=(150, 40),
            position=(125, 30),
            on_activate_call=CallStrict(s._remove),
            color=(0.8, 0.2, 0.2)
        )
        
        s.kids = []
        s.selected = None
        s.refresh()
        AR.swish()
    
    def create_button(s, **kwargs):
        button_color = kwargs.pop('color', (0.25, 0.25, 0.35))
        return bw(
            **kwargs,
            color=button_color,
            enable_sound=True,
            button_type='square'
        )
    
    def _remove(s):
        if s.selected is None:
            AR.err('Select a swear word!')
            return
            
        l = var('swears') or {}
        lc = var('swears_lc') or {}
        
        swear_key = list(l)[s.selected]
        
        l.pop(swear_key)
        lc.pop(swear_key.lower())
        
        var('swears', l)
        var('swears_lc', lc)
        
        s.selected = None
        s.refresh()
        AR.bye()
    
    def refresh(s):
        [k.delete() for k in s.kids]
        s.kids.clear()
        
        l = var('swears') or {}
        swears_list = list(l)
        count = len(swears_list)
        
        for i in range(count):
            swear = swears_list[i]
            widget = tw(
                text=f"{i + 1}. {swear}",
                parent=s.c,
                size=(360, 40),
                selectable=True,
                click_activate=True,
                h_align='center',
                v_align='center',
                position=(0, (40 * count) - 40 * (i + 1)),
                on_activate_call=CallPartial(s.highlight, i),
                color=(0.8, 0.8, 0.8)
            )
            s.kids.append(widget)
        
        cw(s.c, size=(360, count * 40))
    
    def highlight(s, i):
        [tw(t, color=(0.8, 0.8, 0.8)) for t in s.kids]
        tw(s.kids[i], color=(1, 0.5, 0.5))
        s.selected = i

class AddWhiteList:
    def __init__(s, t):
        w = AR.cw(
            source=t,
            size=(400, 200),
            ps=AR.UIS() * 0.8
        )
        
        tw(
            parent=w,
            text='ADD TO WHITE LIST',
            scale=1.3,
            h_align='center',
            position=(175, 165),
            color=(0.5, 1, 0.5)
        )
        
        tw(
            parent=w,
            text='Enter silent name:',
            scale=0.7,
            position=(20, 120),
            color=(0.9, 0.9, 0.9)
        )
        input_container = cw(
            parent=w,
            size=(300, 35),
            position=(50, 85),
            color=(0.2, 0.2, 0.2)
        )
        
        s.name_input = tw(
            parent=input_container,
            maxwidth=300,
            size=(300, 35),
            editable=True,
            v_align='center',
            h_align='center',
            color=(1, 1, 1),
            position=(0, 0),
            allow_clear_button=False
        )
        
        s.create_button(
            parent=w,
            label='Add',
            size=(100, 40),
            position=(150, 30),
            on_activate_call=CallStrict(s._add),
            color=(0.2, 0.8, 0.2)
        )
        
        AR.swish()
    
    def create_button(s, **kwargs):
        button_color = kwargs.pop('color', (0.25, 0.25, 0.35))
        return bw(
            **kwargs,
            color=button_color,
            enable_sound=True,
            button_type='square'
        )
    
    def _add(s):
        name = tw(query=s.name_input).strip().replace('\n', ' ')
        
        if not name:
            AR.err('Enter a name!')
            return
        
        l = var('white_list') or {}
        lc = var('white_list_lc') or {}
        
        if name.lower() in lc:
            AR.err('This name already in white list!')
            return
        
        l.update({name: True})
        lc.update({name.lower(): True})
        
        var('white_list', l)
        var('white_list_lc', lc)
        
        tw(s.name_input, text='')
        AR.ok()

class RemoveWhiteList:
    def __init__(s, t):
        i = len(var('white_list') or {})
        if not i:
            AR.err('White list is empty!')
            return
            
        w = AR.cw(
            source=t,
            size=(400, 290),
            ps=AR.UIS() * 0.8
        )
        
        tw(
            parent=w,
            text='REMOVE WHITE LIST',
            scale=1.3,
            h_align='center',
            position=(200, 250),
            color=(0.5, 1, 0.5)
        )
        
        a = sw(
            parent=w,
            size=(360, 150),
            position=(20, 80)
        )
        
        s.c = cw(
            parent=a,
            size=(360, i * 40),
            background=False
        )
        
        s.create_button(
            parent=w,
            label='REMOVE SELECTED',
            size=(150, 40),
            position=(125, 30),
            on_activate_call=CallStrict(s._remove),
            color=(0.2, 0.8, 0.2)
        )
        
        s.kids = []
        s.selected = None
        s.refresh()
        AR.swish()
    
    def create_button(s, **kwargs):
        button_color = kwargs.pop('color', (0.25, 0.25, 0.35))
        return bw(
            **kwargs,
            color=button_color,
            enable_sound=True,
            button_type='square'
        )
    
    def _remove(s):
        if s.selected is None:
            AR.err('Select a name!')
            return
            
        l = var('white_list') or {}
        lc = var('white_list_lc') or {}
        
        name_key = list(l)[s.selected]
        
        l.pop(name_key)
        lc.pop(name_key.lower())
        
        var('white_list', l)
        var('white_list_lc', lc)
        
        s.selected = None
        s.refresh()
        AR.bye()
    
    def refresh(s):
        [k.delete() for k in s.kids]
        s.kids.clear()
        
        l = var('white_list') or {}
        names_list = list(l)
        count = len(names_list)
        
        for i in range(count):
            name = names_list[i]
            widget = tw(
                text=f"{i + 1}. {name}",
                parent=s.c,
                size=(360, 40),
                selectable=True,
                click_activate=True,
                h_align='center',
                v_align='center',
                position=(0, (40 * count) - 40 * (i + 1)),
                on_activate_call=CallPartial(s.highlight, i),
                color=(0.8, 0.8, 0.8)
            )
            s.kids.append(widget)
        
        cw(s.c, size=(360, count * 40))
    
    def highlight(s, i):
        [tw(t, color=(0.8, 0.8, 0.8)) for t in s.kids]
        tw(s.kids[i], color=(0.5, 1, 0.5))
        s.selected = i

class Settings:
    def __init__(s, t):
        w = AR.cw(
            source=t,
            size=(400, 290),
            ps=AR.UIS() * 0.8
        )
        
        tw(
            parent=w,
            text='SETTINGS',
            scale=1.5,
            h_align='center',
            position=(175, 260),
            color=(0.3, 0.6, 1)
        )
        
        options = [
            ('Notify on report', 'notify'),
            ('Play sound on report', 'sound'),
        ]
        
        for i, (label, config_key) in enumerate(options):
            chk(
                text=label,
                parent=w,
                size=(350, 35),
                color=(1, 1, 1),
                value=var(config_key),
                position=(25, 180 - 50 * i),
                textcolor=(0.2, 0.2, 0.3),
                text_scale=0.9,
                on_value_change_call=CallPartial(var, config_key)
            )
        
        s.create_button(
            parent=w,
            label='SAVE & CLOSE',
            size=(150, 40),
            position=(125, 40),
            on_activate_call=CallPartial(cw, w, transition='out_scale'),
            color=(0.3, 0.5, 0.7)
        )
        
        AR.swish()
    
    def create_button(s, **kwargs):
        button_color = kwargs.pop('color', (0.25, 0.25, 0.35))
        return bw(
            **kwargs,
            color=button_color,
            enable_sound=True,
            button_type='square'
        )

class SwearList:
    def __init__(s, t):
        swears = var('swears') or {}
        count = len(swears)
        
        if not count:
            AR.err('No swear words added!')
            return
            
        w = AR.cw(
            source=t,
            size=(400, 290),
            ps=AR.UIS() * 0.8
        )
        
        tw(
            parent=w,
            text='SWEAR LIST',
            scale=1.5,
            h_align='center',
            position=(175,260),
            color=(1, 0.5, 0.5)
        )
        
        scroll_area = sw(
            parent=w,
            size=(360, 170),
            position=(20, 70)
        )
        
        s.container = cw(
            parent=scroll_area,
            size=(360, count * 40),
            background=False,
        )
        
        s.swear_widgets = []
        s.refresh()
        
        s.create_button(
            parent=w,
            label='CLOSE',
            size=(100, 40),
            position=(150, 20),
            on_activate_call=CallPartial(cw, w, transition='out_scale'),
            color=(0.4, 0.4, 0.6)
        )
        
        AR.swish()
    
    def create_button(s, **kwargs):
        button_color = kwargs.pop('color', (0.25, 0.25, 0.35))
        return bw(
            **kwargs,
            color=button_color,
            enable_sound=True,
            button_type='square'
        )
    
    def refresh(s):
        [w.delete() for w in s.swear_widgets]
        s.swear_widgets.clear()
        
        swears = var('swears') or {}
        swear_list = list(swears.keys())
        count = len(swear_list)
        
        for i, swear in enumerate(swear_list):
            widget = tw(
                text=f"{i + 1:02d}. {swear}",
                parent=s.container,
                size=(360, 40),
                selectable=True,
                click_activate=True,
                h_align='center',
                v_align='center',
                position=(0, (40 * count) - 40 * (i + 1)),
                color=(0.8, 0.8, 0.8)
            )
            s.swear_widgets.append(widget)
        
        cw(s.container, size=(360, count * 40))

class WhiteListView:
    def __init__(s, t):
        white_list = var('white_list') or {}
        count = len(white_list)
        
        if not count:
            AR.err('White list is empty!')
            return
            
        w = AR.cw(
            source=t,
            size=(400,290),
            ps=AR.UIS() * 0.8
        )
        
        tw(
            parent=w,
            text='WHITE LIST',
            scale=1.5,
            h_align='center',
            position=(175, 260),
            color=(0.5, 1, 0.5)
        )
        
        
        scroll_area = sw(
            parent=w,
            size=(360, 190),
            position=(20, 70)
        )
        
        s.container = cw(
            parent=scroll_area,
            size=(360, count * 40),
            background=True,
        )
        
        s.name_widgets = []
        s.refresh()
        
        s.create_button(
            parent=w,
            label='CLOSE',
            size=(100, 40),
            position=(150, 20),
            on_activate_call=CallPartial(cw, w, transition='out_scale'),
            color=(0.4, 0.4, 0.6)
        )
        
        AR.swish()
    
    def create_button(s, **kwargs):
        button_color = kwargs.pop('color', (0.25, 0.25, 0.35))
        return bw(
            **kwargs,
            color=button_color,
            enable_sound=True,
            button_type='square'
        )
    
    def refresh(s):
        [w.delete() for w in s.name_widgets]
        s.name_widgets.clear()
        
        white_list = var('white_list') or {}
        names_list = list(white_list.keys())
        count = len(names_list)
        
        for i, name in enumerate(names_list):
            widget = tw(
                text=f"{i + 1:02d}. {name}",
                parent=s.container,
                size=(360, 40),
                selectable=True,
                click_activate=True,
                h_align='center',
                v_align='center',
                position=(0, (40 * count) - 40 * (i + 1)),
                color=(0.8, 0.8, 0.8)
            )
            s.name_widgets.append(widget)
        
        cw(s.container, size=(360, count * 40))

class AR:
    @classmethod
    def UIS(c=0):
        i = APP.ui_v1.uiscale
        return [1.5, 1.1, 0.8][0 if i == uis.SMALL else 1 if i == uis.MEDIUM else 2]
    
    @classmethod
    def create_button(c, **k):
        kwargs = dict(k)
        button_color = kwargs.pop('color', (0.25, 0.25, 0.35))
        return bw(
            **kwargs,
            color=button_color,
            enable_sound=True,
            button_type='square'
        )
    
    @classmethod
    def cw(c, source, ps=0, **k):
        o = source.get_screen_space_center() if source else None
        r = cw(
            **k,
            scale=c.UIS() + ps,
            transition='in_scale',
            color=(0.15, 0.15, 0.25),
            parent=gsw('overlay_stack'),
            scale_origin_stack_offset=o
        )
        cw(r, on_outside_click_call=CallPartial(c.swish, t=r))
        return r
    
    swish = lambda c=0, t=0: (gs('swish').play(), cw(t, transition='out_scale') if t else t)
    err = lambda t: (gs('error').play() if hasattr(gs, 'error') else gs('block').play(), push(t, color=(1, 0.5, 0)))
    ok = lambda: (gs('dingSmallHigh').play(), push('Success!', color=(0, 1, 0)))
    bye = lambda: (gs('laser').play(), push('Done!', color=(0, 1, 0)))
    
    def __init__(s, source=None) -> None:
        w = s.w = s.cw(
            source=source,
            size=(300, 400),
        )
        title_bar = cw(
            parent=w,
            size=(280, 50),
            position=(17, 350),
            color=(00, 0.3, 0.3)
        )
        tw(
            parent=title_bar,
            text='SinglMod',
            scale=1.3,
            h_align='center',
            position=(115, 15),
            color=(1, 1, 1)
        )
        s.update_status_indicator(w)
        buttons_container = cw(
            parent=w,
            size=(280, 200),
            position=(10, 90),
            color=(0.0, 0.2, 0.3)
        )
        main_buttons = [
            ('SWEAR OPTIONS', SwearOptionsPanel, (140, 145), (1, 0.3, 0.3)),
            ('WHITE LIST OPTIONS', WhiteListOptionsPanel, (140, 85), (0.3, 1, 0.3)),
            ('SETTINGS', Settings, (140,25), (0.3, 0.6, 1))
        ]
        
        for label, panel_class, pos, color in main_buttons:
            s.create_button(
                label=label,
                parent=buttons_container,
                size=(240, 50),
                position=(25, pos[1]),
                on_activate_call=CallPartial(panel_class, w),
                color=color
            )
        s.update_stats_display(w)
        current_state = var('enabled')
        s.toggle_button = s.create_button(
            parent=w,
            label='ON' if current_state else 'OFF',
            size=(100, 35),
            position=(105, 10),
            on_activate_call=CallStrict(s.toggle_system),
            color=(0, 0.7, 0) if current_state else (0.7, 0, 0) 
        )

        AR.swish()
    
    def update_status_indicator(s, w):
        status_color = (0, 0.7, 0) if var('enabled') else (0.7, 0, 0)
        status_text = 'ACTIVE' if var('enabled') else 'INACTIVE'
        
        if hasattr(s, 'status_indicator'):
            s.status_indicator.delete()
        
    def update_stats_display(s, w):
        stats_text = f'Swears: {len(var("swears") or {})} | WhiteList: {len(var("white_list") or {})}'
        if hasattr(s, 'stats_display'):
            s.stats_display.delete()
        
        s.stats_display = tw(
            parent=w,
            text=stats_text,
            scale=0.9,
            h_align='center',
            position=(130, 305),
            color=(0.7, 0.7, 0.9)
        )
    
    def toggle_system(s):
        current_state = var('enabled')
        new_state = not current_state
        var('enabled', new_state)
        bw(
            s.toggle_button,
            label='ON' if new_state else 'OFF',
            color=(0, 0.7, 0) if new_state else (0.7, 0, 0) 
        )
        
        s.update_status_indicator(s.w)
        if new_state:
            push("System ENABLED", color=(0, 1, 0))
            gs('dingSmallHigh').play()
        else:
            push("System DISABLED", color=(1, 0.5, 0))
            gs('laser').play()

pr = 'sr_'
def var(s, v=None):
    c = APP.config
    s = pr + s
    if v is None:
        return c.get(s, v)
    c[s] = v
    c.commit()

def reset_conf():
    cfg = APP.config
    for key in list(cfg.keys()):
        if key.startswith(pr):
            cfg.pop(key)
    cfg.commit()

default_configs = {
    'enabled': True,
    'notify': True,
    'sound': True,
    'case_sensitive': False,
    'white_list_enabled': True,
    'swears': {},
    'swears_lc': {},
    'white_list': {},
    'white_list_lc': {}
}

for key, default_value in default_configs.items():
    if var(key) is None:
        var(key, default_value)

if not var('swears'):
    swears_dict = {}
    swears_lc_dict = {}
    
    for swear in DEFAULT_SWEARS:
        swears_dict[swear] = True
        swears_lc_dict[swear.lower()] = True
    
    var('swears', swears_dict)
    var('swears_lc', swears_lc_dict)

def get_client_id_from_name(player_name):
    try:
        game_roster = GGR()
        for entry in game_roster:
            if 'client_id' in entry and 'players' in entry:
                client_id = entry['client_id']
                for player in entry['players']:
                    if 'name' in player:
                        if player['name'] == player_name:
                            return client_id
                    if 'name_full' in player:
                        if player_name in player['name_full']:
                            return client_id
    except:
        pass
    return None

def is_in_white_list(name):
    if not var('white_list_enabled'):
        return False
    
    white_list = var('white_list_lc') or {}
    return name.lower() in white_list

# ba_meta export babase.Plugin
class SinglReporter(Plugin):
    
    def __init__(s):
        original_party_init = party.PartyWindow.__init__
        
        def new_party_init(self, *args, **kwargs):
            result = original_party_init(self, *args, **kwargs)
            btn = AR.create_button(
                icon=gt('agentIcon'),
                position=(self._width - 500, self._height - 170),
                parent=self._root_widget,
                iconscale=1.2,
                size=(35, 35),
                label='',
                color=(0.3, 0.5, 0.7)
            )
            def activate_ar():
                AR(source=btn)
            bw(btn, on_activate_call=CallStrict(activate_ar))
            
            return result
        
        party.PartyWindow.__init__ = new_party_init
        
        s.messages = []
        s.last_reported = {}
        teck(3, s.check_chat)
    
    def check_chat(s):
        if not var('enabled'):
            teck(2, s.check_chat)
            return
            
        chat_messages = GCM()
        teck(0.5, s.check_chat)
        
        if chat_messages == s.messages:
            return
            
        s.messages = chat_messages
        
        if not chat_messages:
            return
            
        latest_message = chat_messages[-1]
        
        if not latest_message:
            return
        try:
            if ': ' in latest_message:
                sender, message = latest_message.split(': ', 1)
            else:
                return
        except:
            return
        v2_logo = cs(sc.V2_LOGO)
        clean_sender = sender.replace(v2_logo, '').strip()
        if is_in_white_list(clean_sender):
            return
        client_id = get_client_id_from_name(clean_sender)
        
        if not client_id:
            client_id = get_client_id_from_name(sender)
            
        if not client_id:
            return
        if var('case_sensitive'):
            swears_dict = var('swears') or {}
        else:
            swears_dict = var('swears_lc') or {}
            message = message.lower()
        found_swear = False
        
        for swear in swears_dict:
            check_swear = swear if var('case_sensitive') else swear.lower()
            if check_swear in message:
                found_swear = True
                break
        if found_swear:
            current_time = DT.now()
            if clean_sender in s.last_reported:
                time_diff = (current_time - s.last_reported[clean_sender]).total_seconds()
                if time_diff < 30:
                    return
            report_command = f'%rep {client_id}'
            CM(report_command)
            s.last_reported[clean_sender] = current_time
            if var('notify'):
                push(f"Report: %rep {client_id}", color=(1, 0.5, 0))
            if var('sound'):
                gs('dingSmallHigh').play()
    
    def on_app_running(self):
        push("Singl Reporter v1.0", color=(0, 1, 0.5))
