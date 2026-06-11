# ba_meta require api 9

from __future__ import annotations
from typing import TYPE_CHECKING
import babase as ba
import bascenev1 as bs
import bauiv1 as bui

if TYPE_CHECKING:
    from typing import Dict, List, Callable, Tuple, Any

try:
    from babase._profile import get_player_profile_colors
except ImportError:
    try:
        from bascenev1 import get_player_profile_colors
    except ImportError:

        def get_player_profile_colors(profilename: str = None, profiles: dict = None) -> Tuple[tuple, tuple]:
            return ((0.5, 0.5, 0.5), (0.8, 0.8, 0.8))

try:
    from babase._error import print_exception
except ImportError:
    import traceback
    def print_exception(msg):
        print(msg)
        traceback.print_exc()


def __init__(self, vpos: float, sessionplayer: bs.SessionPlayer, lobby: bs.Lobby) -> None:
    self._markers = ['"', "'", "^", "%", ";", "`"]
    self._glowing = {}
    self.__init___glowing(vpos, sessionplayer, lobby)


def get_glowing(self) -> Dict[str, List[float, float, int, int]]:
    for profile_name in self._profilenames:
        for m in self._markers:
            if m in profile_name:
                s = profile_name.split(',')
                if len(s) > 3:
                    if s[0] != m:
                        s = [m, s[0].replace(m, '')] + s[1:]
                    result = []
                    for i, c in enumerate(s[1:5]):
                        try:
                            result.append(min(20, max(float(c), -20)) if i in range(2) else int(c))
                        except ValueError:
                            break
                    if len(result) == 4:
                        self._glowing[m] = result
    return self._glowing


def update_from_profile(self) -> None:
    self._profilename = self._profilenames[self._profileindex]
    self.get_glowing()
    if self._profilename and self._profilename[0] in self._glowing:
        m = self._profilename[0]
        character = self._profiles[self._profilename]['character']
        spaz_appearances = None
        if hasattr(ba.app, 'classic') and ba.app.classic:
            spaz_appearances = ba.app.classic.spaz_appearances
        if character not in self._character_names and spaz_appearances and character in spaz_appearances:
            self._character_names.append(character)
        self._character_index = self._character_names.index(character)
        color_multiple = self._glowing[m][0]
        highlight_multiple = self._glowing[m][1]
        self._color, self._highlight = get_player_profile_colors(self._profilename, profiles=self._profiles)
        if not (self._glowing[m][2] > 0):
            self._color = tuple([i * color_multiple for i in list(self._color)])
        else:
            self._color = list(self._color)
            if self._color:
                val = max(self._color)
                for i, c in enumerate(self._color):
                    if c == val:
                        self._color[i] *= color_multiple
            self._color = tuple(self._color)
        if not (self._glowing[m][3] > 0):
            self._highlight = tuple([i * highlight_multiple for i in list(self._highlight)])
        else:
            self._highlight = list(self._highlight)
            if self._highlight:
                val = max(self._highlight)
                for i, c in enumerate(self._highlight):
                    if c == val:
                        self._highlight[i] *= highlight_multiple
            self._highlight = tuple(self._highlight)
        self._update_icon()
        self._update_text()
    else:
        self.update_from_profile_glowing()


def _getname(self, full: bool = False) -> str:
    name_raw = name = self._profilenames[self._profileindex]
    if name and name[0] in self._glowing:
        name = name[1:]
        clamp = False
        if full:
            try:
                if self._profiles[name_raw].get('global', False):
                    icon = (self._profiles[name_raw]['icon'] if 'icon' in self._profiles[name_raw] else ba.charstr(ba.SpecialChar.LOGO))
                    name = icon + name
            except Exception:
                print_exception('Error applying global icon.')
        else:
            clamp = True
        if clamp and len(name) > 10:
            name = name[:10] + '...'
        return name
    return self._getname_glowing(full)


def i_was_imported() -> bool:
    result = bool(getattr(ba.app, '_glowing_enabled', False))
    setattr(ba.app, '_glowing_enabled', True)
    return result


def redefine(methods: Dict[str, Callable]) -> None:
    for attr, obj in methods.items():
        chooser_class = None
        if hasattr(bs, 'Chooser'):
            chooser_class = bs.Chooser
        elif hasattr(ba, '_lobby') and hasattr(ba._lobby, 'Chooser'):
            chooser_class = ba._lobby.Chooser
        
        if chooser_class and hasattr(chooser_class, attr) and not hasattr(chooser_class, attr + '_glowing'):
            setattr(chooser_class, attr + '_glowing', getattr(chooser_class, attr))
        if chooser_class:
            setattr(chooser_class, attr, obj)


def main() -> None:
    if i_was_imported():
        return
    redefine({'__init__': __init__, 'get_glowing': get_glowing, 'update_from_profile': update_from_profile, '_getname': _getname})


# ba_meta export babase.Plugin
class BsRush(ba.Plugin):
    def __init__(self) -> None:
        main()