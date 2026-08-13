# ba_meta require api 7
import ba , _ba 


#####################

khas1 = "Amirhoshein"
khas2 = None
khas3 = None
khas4 = None

#####################



_ba.chatmessage("#‌# mode by @bombmod in (rubika)")
nameof = {} ; to = [True] ; names = [khas1,khas2,khas3,khas4] ; noch=[] ; spam=[""]
try : a = eval(open("chatyad",'rb').read())
except: a = {}
def yad_begir():
    try:
        msg=_ba.get_chat_messages()
        msg1=msg[len(msg)-1]
        msg2=msg1.split(": ")
        msg1=""
        for i in msg2[1:]:
            msg1 += i + ": "
        msg1 = msg1[:-2]
    except:pass
    _ba.set_party_icon_always_visible(True)
    
    if to[0]:
        names.append(msg2[0])
        to[0] = False
    elif '##' in msg1 and msg2[0] in names:
        for i in range(3):
            msg1 = msg1.replace(" ## ",'##').replace(" ##","##").replace("## ",'##')
        msg1 = msg1.split("##")
        hmm = True
        if msg1[0] in list(a):
            if a[msg1[0]] == msg1[-1]:
                hmm = False
        if hmm: 
            a[msg1[0]] = msg1[-1]
            open("chatyad",'wb').write(bytes(str(a),'utf-8'))
            ba.screenmessage("✅",color=(0,1,0))
        spam[0] = ""
    elif "##" in msg1:
        if not msg1 in noch:
            ba.screenmessage("❌",color=(1,0,0))
            noch.append(msg1)
        spam[0] = ""
    elif msg1 in list(a):
        if not a[msg1] == "خالی" and not spam[0] == msg2[0] + msg1:
            if msg1 == a[msg1]:
                spam[0] = msg2[0] + msg1
                _ba.chatmessage(str(a[msg1]).replace("#اسم",msg2[0]))
            else:
                spam[0] = ""
                _ba.chatmessage(str(a[msg1]).replace("#اسم",msg2[0]))
        elif a[msg1] == "خالی":
        	spam[0] = ""
    else:
    	spam[0] = ""

# ba_meta export plugin
class yad_begir_bego(ba.Plugin):
    def on_app_running(self) -> None:
    	ba.timer(0.1, yad_begir, True)