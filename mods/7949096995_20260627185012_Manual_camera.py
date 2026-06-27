# ba_meta require api 7

###################
# Credits - Droopy#3730. #
###################

# Don't edit  . 


from __future__ import annotations
import _ba
import ba
from bastd.ui.mainmenu import MainMenuWindow


class Manual_camera_window:
    def __init__(self):
            self._root_widget = ba.containerwidget(
                               on_outside_click_call=None,
                               size=(0,0))
            button_size = (50,50)
            self._xminus = ba.buttonwidget(parent=self._root_widget,
                              size=button_size,
                              label=ba.charstr(ba.SpecialChar.LEFT_ARROW),
                              button_type='square',
                              autoselect=True,
                              position=(429, 60),
                              on_activate_call=ba.Call(self._change_camera_position, 'x-'))
            self._xplus = ba.buttonwidget(parent=self._root_widget,
                              size=button_size,
                              label=ba.charstr(ba.SpecialChar.RIGHT_ARROW),
                              button_type='square',
                              autoselect=True,
                              position=(538, 60),
                              on_activate_call=ba.Call(self._change_camera_position, 'x'))
            self._yplus = ba.buttonwidget(parent=self._root_widget,
                              size=button_size,
                              label=ba.charstr(ba.SpecialChar.UP_ARROW),
                              button_type='square',
                              autoselect=True,
                              position=(482, 120),
                              on_activate_call=ba.Call(self._change_camera_position, 'y'))
            self._yminus = ba.buttonwidget(parent=self._root_widget,
                              size=button_size,
                              label=ba.charstr(ba.SpecialChar.DOWN_ARROW),
                              button_type='square',
                              autoselect=True,
                              position=(482, 2),
                              on_activate_call=ba.Call(self._change_camera_position, 'y-'))
            self.inwards = ba.buttonwidget(parent=self._root_widget,
                              size=(100,30),
                              label='Zoom +',
                              button_type='square',
                              autoselect=True,
                              position=(-550, -60),
                              on_activate_call=ba.Call(self._change_camera_position, 'z-'))
            self._outwards = ba.buttonwidget(parent=self._root_widget,
                              size=(100,30),
                              label='Zoom -',
                              button_type='square',
                              autoselect=True,
                              position=(-550, -100),
                              on_activate_call=ba.Call(self._change_camera_position, 'z'))
            self.target_xminus = ba.buttonwidget(parent=self._root_widget,
                              size=button_size,
                              label=ba.charstr(ba.SpecialChar.LEFT_ARROW),
                              button_type='square',
                              autoselect=True,
                              position=(-538, 60),
                              on_activate_call=ba.Call(self._change_camera_target, 'x-'))
            self.target_xplus = ba.buttonwidget(parent=self._root_widget,
                              size=button_size,
                              label=ba.charstr(ba.SpecialChar.RIGHT_ARROW),
                              button_type='square',
                              autoselect=True,
                              position=(-429, 60),
                              on_activate_call=ba.Call(self._change_camera_target, 'x'))
            self.target_yplus = ba.buttonwidget(parent=self._root_widget,
                              size=button_size,
                              label=ba.charstr(ba.SpecialChar.UP_ARROW),
                              button_type='square',
                              autoselect=True,
                              position=(-482, 120),
                              on_activate_call=ba.Call(self._change_camera_target, 'y'))
            self.target_yminus = ba.buttonwidget(parent=self._root_widget,
                              size=button_size,
                              label=ba.charstr(ba.SpecialChar.DOWN_ARROW),
                              button_type='square',
                              autoselect=True,
                              position=(-482, 2),
                              on_activate_call=ba.Call(self._change_camera_target, 'y-'))                 
            self._step_text = ba.textwidget(parent=self._root_widget,
                                         scale=0.85,
                                         color=(1,1,1),
                                         text='Step:',
                                         size=(0, 0),
                                         position=(450, -38),
                                         h_align='center',
                                         v_align='center')
            self._text_field = ba.textwidget(
                                 parent=self._root_widget,
                                 editable=True,
                                 size=(100, 40),
                                 position=(480, -55),
                                 text='',
                                 maxwidth=120,
                                 flatness=1.0,
                                 autoselect=True,
                                 v_align='center',
                                 corner_scale=0.7)
            self._reset = ba.buttonwidget(parent=self._root_widget,
                              size=(50,30),
                              label='Reset',
                              button_type='square',
                              autoselect=True,
                              position=(450, -100),
                              on_activate_call=ba.Call(self._change_camera_position, 'reset'))
            self._done = ba.buttonwidget(parent=self._root_widget,
                              size=(50,30),
                              label='Done',
                              button_type='square',
                              autoselect=True,
                              position=(520, -100),
                              on_activate_call=self._close)
            ba.containerwidget(edit=self._root_widget,
                           cancel_button=self._done)
    def _close(self):
        ba.containerwidget(edit=self._root_widget,
                           transition=('out_scale'))
        MainMenuWindow()                   

    def _change_camera_position(self, direction):
        camera = _ba.get_camera_position()
        x = camera[0]
        y = camera[1]
        z = camera[2]
        
        try:
            increment = float(ba.textwidget(query=self._text_field))
        except:
            increment = 1

        if direction == 'x':
            x += increment
        elif direction == 'x-':
            x -= increment
        elif direction == 'y':
            y += increment
        elif direction == 'y-':
            y -= increment
        elif direction == 'z':
            z += increment
        elif direction == 'z-':
            z -= increment
        elif direction == 'reset':
            _ba.set_camera_manual(False)
            return
            
        _ba.set_camera_manual(True)
        _ba.set_camera_position(x, y, z)  
        
    def _change_camera_target(self, direction):
        camera = _ba.get_camera_target()
        x = camera[0]
        y = camera[1]
        z = camera[2]
        
        try:
            increment = float(ba.textwidget(query=self._text_field))
        except:
            increment = 1

        if direction == 'x':
            x += increment
        elif direction == 'x-':
            x -= increment
        elif direction == 'y':
            y += increment
        elif direction == 'y-':
            y -= increment
            
        _ba.set_camera_manual(True)
        _ba.set_camera_target(x, y, z)

def my_refresh_in_game(
        self, positions: List[Tuple[float, float,
                                    float]]) -> Tuple[float, float, float]:
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-statements
        custom_menu_entries: List[Dict[str, Any]] = []
        session = _ba.get_foreground_host_session()
        camera_button = ba.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(290, 105),
            size=(70, 50),
            button_type='square',
            label='Manual\nCamera',
            text_scale=1.5,
            on_activate_call=self._manual_camera)    
        if session is not None:
            try:
                custom_menu_entries = session.get_custom_menu_entries()
                for cme in custom_menu_entries:
                    if (not isinstance(cme, dict) or 'label' not in cme
                            or not isinstance(cme['label'], (str, ba.Lstr))
                            or 'call' not in cme or not callable(cme['call'])):
                        raise ValueError('invalid custom menu entry: ' +
                                         str(cme))
            except Exception:
                custom_menu_entries = []
                ba.print_exception(
                    f'Error getting custom menu entries for {session}')
        self._width = 250.0
        self._height = 250.0 if self._input_player else 180.0
        if (self._is_demo or self._is_arcade) and self._input_player:
            self._height -= 40
        if not self._have_settings_button:
            self._height -= 50
        if self._connected_to_remote_player:
            # In this case we have a leave *and* a disconnect button.
            self._height += 50
        self._height += 50 * (len(custom_menu_entries))
        uiscale = ba.app.ui.uiscale
        ba.containerwidget(
            edit=self._root_widget,
            size=(self._width, self._height),
            scale=(2.15 if uiscale is ba.UIScale.SMALL else
                   1.6 if uiscale is ba.UIScale.MEDIUM else 1.0))
        h = 125.0
        v = (self._height - 80.0 if self._input_player else self._height - 60)
        h_offset = 0
        d_h_offset = 0
        v_offset = -50
        for _i in range(6 + len(custom_menu_entries)):
            positions.append((h, v, 1.0))
            v += v_offset
            h += h_offset
            h_offset += d_h_offset
        self._start_button = None
        ba.app.pause()

        # Player name if applicable.
        if self._input_player:
            player_name = self._input_player.getname()
            h, v, scale = positions[self._p_index]
            v += 35
            ba.textwidget(parent=self._root_widget,
                          position=(h - self._button_width / 2, v),
                          size=(self._button_width, self._button_height),
                          color=(1, 1, 1, 0.5),
                          scale=0.7,
                          h_align='center',
                          text=ba.Lstr(value=player_name))
        else:
            player_name = ''
        h, v, scale = positions[self._p_index]
        self._p_index += 1
        btn = ba.buttonwidget(parent=self._root_widget,
                              position=(h - self._button_width / 2, v),
                              size=(self._button_width, self._button_height),
                              scale=scale,
                              label=ba.Lstr(resource=self._r + '.resumeText'),
                              autoselect=self._use_autoselect,
                              on_activate_call=self._resume)
        ba.containerwidget(edit=self._root_widget, cancel_button=btn)

        # Add any custom options defined by the current game.
        for entry in custom_menu_entries:
            h, v, scale = positions[self._p_index]
            self._p_index += 1

            # Ask the entry whether we should resume when we call
            # it (defaults to true).
            resume = bool(entry.get('resume_on_call', True))

            if resume:
                call = ba.Call(self._resume_and_call, entry['call'])
            else:
                call = ba.Call(entry['call'], ba.WeakCall(self._resume))

            ba.buttonwidget(parent=self._root_widget,
                            position=(h - self._button_width / 2, v),
                            size=(self._button_width, self._button_height),
                            scale=scale,
                            on_activate_call=call,
                            label=entry['label'],
                            autoselect=self._use_autoselect)
        # Add a 'leave' button if the menu-owner has a player.
        if ((self._input_player or self._connected_to_remote_player)
                and not (self._is_demo or self._is_arcade)):
            h, v, scale = positions[self._p_index]
            self._p_index += 1
            btn = ba.buttonwidget(parent=self._root_widget,
                                  position=(h - self._button_width / 2, v),
                                  size=(self._button_width,
                                        self._button_height),
                                  scale=scale,
                                  on_activate_call=self._leave,
                                  label='',
                                  autoselect=self._use_autoselect)

            if (player_name != '' and player_name[0] != '<'
                    and player_name[-1] != '>'):
                txt = ba.Lstr(resource=self._r + '.justPlayerText',
                              subs=[('${NAME}', player_name)])
            else:
                txt = ba.Lstr(value=player_name)
            ba.textwidget(parent=self._root_widget,
                          position=(h, v + self._button_height *
                                    (0.64 if player_name != '' else 0.5)),
                          size=(0, 0),
                          text=ba.Lstr(resource=self._r + '.leaveGameText'),
                          scale=(0.83 if player_name != '' else 1.0),
                          color=(0.75, 1.0, 0.7),
                          h_align='center',
                          v_align='center',
                          draw_controller=btn,
                          maxwidth=self._button_width * 0.9)
            ba.textwidget(parent=self._root_widget,
                          position=(h, v + self._button_height * 0.27),
                          size=(0, 0),
                          text=txt,
                          color=(0.75, 1.0, 0.7),
                          h_align='center',
                          v_align='center',
                          draw_controller=btn,
                          scale=0.45,
                          maxwidth=self._button_width * 0.9)
        return h, v, scale
        
def _manual_camera(self):
    ba.containerwidget(edit=self._root_widget, transition='out_scale')
    Manual_camera_window() 
        
# ba_meta export plugin                    
class ByDroopy(ba.Plugin):
    def __init__(self):
        MainMenuWindow._refresh_in_game = my_refresh_in_game  
        MainMenuWindow._manual_camera = _manual_camera
      
