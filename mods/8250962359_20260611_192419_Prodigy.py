from babase import Plugin
from bauiv1 import buttonwidget as bw, gettexture as gt, Call
from bascenev1 import chatmessage as CM
from bauiv1lib import party
import random

# ba_meta require api 9
# ba_meta export plugin
class OneButtonSender(Plugin):

    def __init__(s):
        o = party.PartyWindow.__init__

        def e(s,*a,**k):
            r = o(s,*a,**k)
            # دکمه کوچک، پایین سمت چپ
            s.my_button = AR.bw(
                icon=gt('achievementOutline'),
                position=(10, 10),  # پایین سمت چپ
                parent=s._root_widget,
                iconscale=0.5,
                size=(60,25),
                label='ارسال 1'
            )
            # هر بار کلیک فقط یک "1" بفرستد
            bw(s.my_button, on_activate_call=Call(lambda: CM("1")()))
            return r

        party.PartyWindow.__init__ = e

class AR:
    @classmethod
    def bw(c,**k):
        r = random.random()
        g = random.random()
        b = random.random()
        return bw(
            **k,
            textcolor=(1,1,1),
            enable_sound=False,
            button_type='square',
            color=(r*0.7+0.3, g*0.7+0.3, b*0.7+0.3)
        )