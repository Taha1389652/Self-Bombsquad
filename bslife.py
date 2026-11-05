# ba_meta require api 9
# BSLIFE Ally Manager — Finder-style UI edition
# Logic/API: BSLIFE Ally Manager v9  |  Look & animations: Finder-style
# mod is Free

from __future__ import annotations

import babase
import bauiv1 as bui
import bascenev1 as bs
from bauiv1lib import party

import urllib.request
import urllib.error
import http.cookiejar
import ssl
import json
import os
import threading
import time
from random import uniform

# ═══════════════════════════════════════════════════════════════
# SETTINGS / PALETTE (Finder palette)
# ═══════════════════════════════════════════════════════════════

BASE_URL = "https://bslife.ir"
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".bslife_ally")
os.makedirs(DATA_DIR, exist_ok=True)
SESSION_FILE = os.path.join(DATA_DIR, "session.json")
LOG_FILE = os.path.join(DATA_DIR, "bslife_debug.log")

C1 = (0, 0.3, 0.3)      # window background
C2 = (0, 0.55, 0.55)    # buttons / separators
C3 = (0, 0.7, 0.7)      # secondary text
C4 = (0, 1, 1)          # primary text
C5 = (1, 1, 0)          # highlight / warning
DNG = (0.5, 0.12, 0.12)  # danger button
DNGT = (1, 0.7, 0.7)
GRN = (0.4, 1, 0.6)
RED = (1, 0.4, 0.4)
NOSEL = "__not_set__"

Call = getattr(bui, 'CallPartial', bui.Call)
gt = bui.gettexture

# ═══════════════════════════════════════════════════════════════
# LANGUAGE   key: (fa, en)
# ═══════════════════════════════════════════════════════════════

T = {
    "login": ("ورود", "Login"), "logout": ("خروج", "Logout"),
    "cancel": ("انصراف", "Cancel"), "overview": ("مرور کلی", "Overview"),
    "members": ("اعضا", "Members"), "requests": ("درخواست‌ها", "Requests"),
    "vault": ("خزانه", "Vault"), "settings": ("تنظیمات", "Settings"),
    "ranking": ("رنکینگ", "Ranking"), "chat": ("چت", "Chat"),
    "news": ("اخبار", "News"), "manage": ("مدیریت", "Manage"),
    "title": ("عنوان", "Title"), "color": ("رنگ", "Color"),
    "apply_title": ("اعمال عنوان", "Apply Title"), "role": ("نقش", "Role"),
    "change_role": ("تغییر نقش", "Change Role"), "mute": ("سکوت", "Mute"),
    "unmute": ("رفع سکوت", "Unmute"), "kick": ("اخراج", "Kick"),
    "leader": ("لیدر", "Leader"), "general": ("جنرال", "General"),
    "spy": ("جاسوس", "Spy"), "member": ("عضو", "Member"),
    "deposit": ("واریز", "Deposit"), "split": ("تقسیم خزانه", "Split Vault"),
    "capacity": ("ظرفیت", "Capacity"), "buy_1": ("خرید +۱", "Buy +1"),
    "new": ("جدید", "New"), "accepted": ("تایید شده", "Accepted"),
    "rejected": ("رد شده", "Rejected"), "yes": ("قبول", "YES"), "no": ("رد", "NO"),
    "ready": ("آماده", "Ready"), "loading": ("در حال لود...", "Loading..."),
    "session_expired": ("سشن منقضی شده", "Session expired"),
    "not_ranked": ("هنوز رتبه‌بندی نشده", "Not ranked yet"),
    "alliance_name": ("نام اتحاد", "Alliance Name"),
    "your_role": ("نقش شما", "Your Role"),
    "members_count": ("تعداد اعضا", "Members Count"), "coins": ("سکه", "Coins"),
    "message": ("پیام...", "Message..."), "send": ("ارسال", "Send"),
    "error_fill": ("لطفا هر دو فیلد را پر کنید!", "Please fill both fields!"),
    "logging_in": ("در حال ورود...", "Logging in..."),
    "success_loading": ("موفق! در حال لود...", "Success! Loading..."),
    "error": ("خطا", "Error"), "hub_title": ("مرکز اتحادها", "Alliance Hub"),
    "not_in_ally": ("شما عضو هیچ اتحادی نیستید.", "You are not in an alliance."),
    "create_ally": ("ساخت اتحاد", "Create Ally"),
    "join_ally": ("پیوستن به اتحاد", "Join Ally"),
    "search": ("جستجو...", "Search..."), "cost": ("هزینه", "Cost"),
    "user": ("کاربر", "User"), "no_ally": ("بدون اتحاد", "No Ally"),
    "request_sent": ("درخواست ارسال شد", "Request sent"),
    "join_fail": ("شما شرایط لازم برای ورود را ندارید", "You don't meet the requirements"),
    "ok": ("باشه", "OK"), "request_btn": ("درخواست", "Request"),
    "join_btn": ("عضویت", "Join"), "confirm": ("تایید", "Confirm"),
    "success": ("موفق", "Success"), "fail": ("ناموفق", "Failed"),
    "enter_amount": ("مقدار را وارد کنید", "Enter amount"),
    "equal_all": ("مساوی بین همه", "Equal: All"),
    "equal_ranking": ("مساوی بین ۲۰ برتر", "Equal: Top 20"),
    "ranking_points": ("متناسب با امتیاز", "By points"),
    "remove_role": ("حذف نقش", "Remove role"),
    "create_fail": ("خطا در ساخت اتحاد", "Create failed"),
    "already_in_ally": ("شما در اتحاد دیگری هستید", "Already in another ally"),
    "not_enough_coins": ("سکه کافی نیست", "Not enough coins"),
    "select_type": ("نوع را انتخاب کنید", "Select type"),
    "select_role": ("نقش را انتخاب کنید", "Select role"),
    "vault_split_ok": ("خزانه تقسیم شد", "Vault split successful"),
    "deposit_ok": ("واریز موفق", "Deposit successful"),
    "role_changed": ("نقش تغییر کرد", "Role changed"),
    "leave_ally": ("خروج از اتحاد", "Leave Ally"),
    "leave_confirm": ("آیا مطمئنید می‌خواهید از اتحاد خارج شوید؟", "Are you sure you want to leave the ally?"),
    "vault_news": ("تاریخچه خزانه", "Vault History"),
    "vault_shares": ("لیست سهام", "Vault Shares"), "history": ("تاریخچه", "History"),
    "more": ("بیشتر", "More"), "no_news": ("خبری وجود ندارد", "No news available"),
    "gkick": ("حذف مجاز جنرال", "General Kick Limit"),
    "spynet": ("بودجه Spynet", "Spynet Budget"),
    "tag_status": ("وضعیت تگ", "Tag Status"), "tag_active": ("فعال", "Active"),
    "tag_inactive": ("غیرفعال", "Inactive"),
    "sale_price": ("فروش اتحاد", "Ally Sale Price"),
    "enrol_settings": ("تنظیمات عضوگیری", "Enrolment Settings"),
    "mode_direct": ("مستقیم", "Direct"), "mode_request": ("درخواستی", "Request"),
    "mode_closed": ("بسته", "Closed"), "min_coin": ("حداقل سکه", "Min Coins"),
    "req_top": ("رتبه تاپ", "Required Top"), "min_score": ("حداقل امتیاز", "Min Score"),
    "saved": ("ذخیره شد", "Saved"),
    "order_rank": ("رتبه", "Rank"), "order_new": ("جدیدترین", "Newest"),
    "order_old": ("قدیمی‌ترین", "Oldest"), "order_count": ("بیشترین عضو", "Most Members"),
    # extra
    "set": ("تنظیم", "Set"), "change": ("تغییر", "Change"), "toggle": ("تغییر وضعیت", "Toggle"),
    "mode": ("حالت ورود", "Join Mode"), "bot_link": ("اتصال به ربات تلگرام", "Telegram Bot Link"),
    "required": ("اجباری", "Required"), "off": ("خاموش", "Off"),
    "not_set": ("تنظیم نشده", "Not set"), "needed": ("شرایط مورد نیاز", "Requirements"),
    "req_rejected": ("درخواست شما قبلا رد شده است.", "Your request was already rejected."),
    "req_pending": ("درخواست شما در انتظار بررسی است.", "Your request is pending review."),
    "already_left": ("شما اخیرا از این اتحاد خارج شده اید. 24 ساعت صبر کنید.", "You recently left this ally. Wait 24 hours."),
    "enter_name": ("نام را وارد کنید", "Enter a name"),
    "too_many": ("ظرفیت نقش پر است", "Role capacity is full"),
    "no_bot": ("اکانت به بات متصل نیست", "Account is not linked to the bot"),
    "no_ranking": ("اطلاعات رنکینگ موجود نیست", "No ranking info"),
    "invalid": ("مقدار نامعتبر", "Invalid value"),
    "min100": ("حداقل مقدار ۱۰۰ است", "Minimum is 100"),
    "net_error": ("خطای شبکه", "Network error"),
    "kick_confirm": ("این عضو اخراج شود؟", "Kick this member?"),
    "empty": ("خالی", "Empty"),
}


def _fa():
    try:
        return bui.app.lang.language in ("Persian", "fa", "Farsi")
    except Exception:
        return False


def L(key):
    v = T.get(key)
    if not v:
        return key
    return v[0] if _fa() else v[1]


def log(msg):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    except Exception:
        pass


def fmt(n):
    try:
        return f"{int(n):,}"
    except Exception:
        return str(n)


def role_name(rid):
    return L({1: "leader", 2: "general", 3: "spy"}.get(rid, "member"))


def role_color(rid):
    return {1: C5, 2: C4, 3: (0.8, 0.6, 1)}.get(rid, C3)


# ═══════════════════════════════════════════════════════════════
# API CLIENT (unchanged logic)
# ═══════════════════════════════════════════════════════════════

class BslifeAPI:
    def __init__(self):
        self.jar = http.cookiejar.CookieJar()
        try:
            ctx = ssl.create_default_context()
        except Exception:
            try:
                ctx = ssl._create_unverified_context()
            except Exception:
                ctx = None
        handlers = [urllib.request.HTTPCookieProcessor(self.jar)]
        try:
            handlers.append(urllib.request.HTTPSHandler(context=ctx))
        except Exception:
            pass
        self.opener = urllib.request.build_opener(*handlers)
        self.headers = {"User-Agent": "BombSquad/1.7.x (Modded Ally Manager)",
                        "Accept": "application/json", "Content-Type": "application/json"}
        self.user = None
        self.ally = None
        self.roleid = None
        self.memberid = None
        self._load_cookies()

    def _load_cookies(self):
        if not os.path.exists(SESSION_FILE):
            return
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k, v in data.get("cookies", {}).items():
                c = http.cookiejar.Cookie(
                    version=0, name=k, value=v, port=None, port_specified=False,
                    domain="bslife.ir", domain_specified=True, domain_initial_dot=False,
                    path="/", path_specified=True, secure=True,
                    expires=None, discard=True, comment=None, comment_url=None,
                    rest={"HttpOnly": None}, rfc2109=False)
                self.jar.set_cookie(c)
            self.user = data.get("user")
            log(f"Loaded session for: {self.user}")
        except Exception as e:
            log(f"Load cookies failed: {e}")

    def _save_cookies(self):
        data = {"cookies": {c.name: c.value for c in self.jar}, "user": self.user}
        try:
            with open(SESSION_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            log(f"Save cookies failed: {e}")

    def post(self, path, payload):
        url = BASE_URL + path
        try:
            data = json.dumps(payload).encode("utf-8")
            cookies = self.jar._cookies
            cookie_str = "".join(f"{n}={cookies[d][p][n].value}; "
                                 for d in cookies for p in cookies[d] for n in cookies[d][p])
            headers = self.headers.copy()
            if cookie_str:
                headers["Cookie"] = cookie_str
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with self.opener.open(req, timeout=20) as resp:
                result = resp.read().decode("utf-8", errors="replace").strip()
                self._save_cookies()
                return result
        except urllib.error.HTTPError as e:
            return f"__HTTPERROR__:{e.code}"
        except Exception as e:
            return f"__ERROR__:{e}"

    def post_json(self, path, payload):
        t = self.post(path, payload)
        if t in ("3", "", "-1"):
            return t
        if t.startswith("__"):
            return {"error": t}
        try:
            return json.loads(t)
        except Exception:
            return t

    def login(self, name, otp):
        r = self.post("/Head.php", {"fu": "login", "n": name, "p": otp})
        if r == "1":
            self.user = name
            self._save_cookies()
            return True, L("success_loading")
        return False, {"0": "Wrong Username/OTP", "ban": "Blocked", "banned": "Banned",
                       "-1": "Server Error"}.get(r, "Unknown Error")

    def whoami(self):
        r = self.post("/Head.php", {"fu": "load"})
        if r in ("3", ""):
            log("Session expired, trying to recover...")
            r = self.post("/Head.php", {"fu": "load"})
        return None if r in ("3", "") else r

    def logout(self):
        try:
            self.post("/Head.php", {"fu": "account_logout"})
        except Exception:
            pass
        self.jar.clear()
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
        self.user = self.ally = self.roleid = self.memberid = None

    def ally_status(self): return self.post_json("/post/Ally.php", {"fu": "status"})
    def ally_members(self): return self.post_json("/post/Ally.php", {"fu": "members"})
    def ally_leave(self): return self.post("/post/Ally.php", {"fu": "leave_ally"})
    def ally_requests(self, rtype="new"): return self.post_json("/post/Ally.php", {"fu": "get_requests", "type": rtype, "offset": None})
    def ally_handle_request(self, req_id, mode): return self.post("/post/Ally.php", {"fu": "handle_request", "request": req_id, "mode": mode})
    def ally_change_role(self, member_id, roleid): return self.post("/post/Ally.php", {"fu": "change_role", "id": member_id, "roleid": roleid})
    def ally_change_title(self, member_id, title, color): return self.post("/post/Ally.php", {"fu": "change_title", "id": member_id, "title": title, "color": color})
    def ally_mute(self, target, typ): return self.post("/post/Ally.php", {"fu": "mute_unmute", "target": target, "type": typ})
    def ally_kick(self, member_id): return self.post("/post/Ally.php", {"fu": "delete_member", "id": member_id})
    def ally_settings(self): return self.post_json("/post/Ally.php", {"fu": "settings"})
    def ally_save_setting(self, key, val): return self.post_json("/post/Ally.php", {"fu": "settings", "key": key, "val": val})
    def ally_capacity(self): return self.post("/post/Ally.php", {"fu": "capacity"})
    def ally_chat_history(self, offset=None): return self.post_json("/post/Ally.php", {"fu": "chat_history", "offset": offset})
    def ally_chat_send(self, text): return self.post("/post/Ally.php", {"fu": "chat_send", "chat": text})
    def ally_ranking(self, date=None): return self.post_json("/post/Ally.php", {"fu": "ranking_info", "date": date})
    def ally_vault_status(self): return self.post_json("/post/Ally.php", {"fu": "vault_status"})
    def ally_vault_add(self, amount): return self.post("/post/Ally.php", {"fu": "vault_add", "amount": amount})
    def ally_vault_clear(self, typ): return self.post("/post/Ally.php", {"fu": "vault_clear", "type": typ})
    def ally_vault_news(self, offset=None): return self.post_json("/post/Ally.php", {"fu": "vault_news", "offset": offset})
    def ally_vault_shares(self, trans_id): return self.post_json("/post/Ally.php", {"fu": "vault_shares", "id": trans_id})
    def ally_enrol(self): return self.post_json("/post/Ally.php", {"fu": "enrol_settings"})
    def ally_set_enrol(self, key, val): return self.post_json("/post/Ally.php", {"fu": "enrol_settings", "key": key, "val": val})
    def ally_news(self, offset=None): return self.post_json("/post/Ally.php", {"fu": "news", "offset": offset})
    def create_status(self): return self.post_json("/post/AllyCreate.php", {"fu": "status"})
    def create_ally(self, name, confirm=0): return self.post_json("/post/AllyCreate.php", {"fu": "create", "name": name, "confirm": confirm})
    def list_allies(self, search="", order="rank"): return self.post_json("/post/AllyList.php", {"fu": "get_allys", "offset": None, "order": order, "search": search, "filter": "[]"})
    def join_ally(self, ally_id): return self.post("/post/AllyList.php", {"fu": "join_ally", "ally": ally_id})


class Network:
    @classmethod
    def fetch(cls, api, method_name, args=(), callback=None):
        def worker():
            try:
                result = getattr(api, method_name)(*args)
            except Exception as e:
                result = {"error": str(e)}
            if callback:
                try:
                    bui.pushcall(Call(callback, result), from_other_thread=True)
                except Exception as e:
                    log(f"Pushcall error: {e}")
        threading.Thread(target=worker, daemon=True).start()


# ═══════════════════════════════════════════════════════════════
# FINDER-STYLE UI KIT
# ═══════════════════════════════════════════════════════════════

def uis():
    s = bui.app.ui_v1.uiscale
    return 1.35 if s is babase.UIScale.SMALL else 1.15 if s is babase.UIScale.MEDIUM else 1.0


def snd(name):
    s = bui.getsound(name)
    s.play()
    bui.apptimer(uniform(0.14, 0.18), s.stop)
    return s


def ding(i=1, j=1):
    a = ['Small', '']
    snd('ding' + a[i])
    bui.apptimer(0.1, bui.getsound('ding' + a[j]).play)


def TIP(t):
    bui.screenmessage(t, C3)


def BTW(t):
    bui.screenmessage(t, C5)
    bui.getsound('block').play()


def tw(parent, pos, text, col=C4, scale=1.0, h='left', v='center', maxw=None, **k):
    kw = dict(parent=parent, position=pos, text='' if text is None else str(text),
              color=col, scale=scale, h_align=h, v_align=v)
    if maxw:
        kw['maxwidth'] = maxw
    kw.update(k)
    return bui.textwidget(**kw)


def btn(parent, pos, size, label, call, col=C2, tcol=C4, ts=None):
    def go():
        snd('dingSmall')
        call()
    kw = dict(parent=parent, position=pos, size=size, label=label, color=col,
              textcolor=tcol, texture=gt('white'), enable_sound=False, on_activate_call=go)
    if ts:
        kw['text_scale'] = ts
    return bui.buttonwidget(**kw)


def sep(parent, pos, w):
    return bui.imagewidget(parent=parent, size=(w, 1), position=pos, texture=gt('white'), color=C2)


def panel(parent, pos, size):
    return bui.imagewidget(parent=parent, position=pos, size=size, texture=gt('scrollWidget'),
                           mesh_transparent=bui.getmesh('softEdgeOutside'), opacity=0.4)


def inp(parent, pos, size, text='', maxc=None, desc='', h='left'):
    bui.imagewidget(parent=parent, position=pos, size=size, texture=gt('white'), color=(0, 0.4, 0.4))
    kw = dict(parent=parent, position=(pos[0] + 6, pos[1]), size=(size[0] - 12, size[1]),
              text='' if text is None else str(text), color=C4, editable=True, h_align=h,
              v_align='center', allow_clear_button=False, shadow=0, flatness=1, description=desc)
    if maxc:
        kw['max_chars'] = maxc
    return bui.textwidget(**kw)


def listbox(parent, pos, size, n, rh):
    H = max(n * rh, size[1] - 10)
    sc = bui.scrollwidget(parent=parent, position=pos, size=size, border_opacity=0.4)
    ct = bui.containerwidget(parent=sc, size=(size[0] - 6, H), background=False)
    return sc, ct, H


class Win:
    """Finder-style window: soft shadow, flat teal body, scale-in, sounds."""

    def __init__(self, size, src=None, on_close=None, outside=True):
        self.size = size
        self.closed = False
        self._cb = on_close
        w, h = size
        kw = dict(parent=bui.get_special_widget('overlay_stack'), background=False,
                  transition='in_scale', size=size, scale=uis())
        if outside:
            kw['on_outside_click_call'] = self.close
        if src is not None:
            try:
                kw['scale_origin_stack_offset'] = src.get_screen_space_center()
            except Exception:
                pass
        try:
            self.p = bui.containerwidget(**kw)
        except TypeError:
            kw.pop('scale_origin_stack_offset', None)
            self.p = bui.containerwidget(**kw)
        bui.imagewidget(parent=self.p, texture=gt('softRect'), size=(w * 1.2, h * 1.2),
                        position=(-w * 0.1, -h * 0.1), opacity=0.55, color=(0, 0, 0))
        bui.imagewidget(parent=self.p, size=size, texture=gt('white'), color=C1)
        bui.scrollwidget(parent=self.p, size=size, border_opacity=0)
        self.s1 = snd('powerup01')

    def alive(self):
        return (not self.closed) and self.p.exists()

    def close(self):
        if self.closed:
            return
        self.closed = True
        try:
            self.s1.stop()
        except Exception:
            pass
        try:
            bui.containerwidget(edit=self.p, transition='out_scale')
        except Exception:
            pass
        l = snd('laser')

        def f():
            if self.p.exists():
                bui.apptimer(0.01, f)
            else:
                l.stop()
        f()
        if self._cb:
            try:
                self._cb()
            except Exception as e:
                log(f"on_close error: {e}")


# ═══════════════════════════════════════════════════════════════
# POPUPS
# ═══════════════════════════════════════════════════════════════

class Msg:
    def __init__(self, title, text, kind="info", on_ok=None):
        self._on_ok = on_ok
        self.w = Win((380, 230), on_close=self._fin)
        p = self.w.p
        col = GRN if kind == "success" else RED if kind == "error" else C5
        tw(p, (190, 197), title, col, 1.0, 'center', maxw=350)
        sep(p, (17, 172), 346)
        tw(p, (190, 112), text, C3, 0.75, 'center', maxw=350)
        btn(p, (140, 15), (100, 34), L("ok"), self.w.close)

    def _fin(self):
        if self._on_ok:
            bui.apptimer(0.25, self._on_ok)


class Confirm:
    def __init__(self, title, text, on_yes, danger=True):
        self._yes = on_yes
        self.w = Win((380, 190))
        p = self.w.p
        tw(p, (190, 158), title, RED if danger else C4, 1.0, 'center', maxw=350)
        sep(p, (17, 136), 346)
        tw(p, (190, 94), text, C3, 0.8, 'center', maxw=340)
        btn(p, (30, 15), (155, 34), L("yes"), self._ok, C2)
        btn(p, (195, 15), (155, 34), L("no"), self.w.close, DNG, DNGT)

    def _ok(self):
        self.w.close()
        bui.apptimer(0.2, self._yes)


class NumberInput:
    def __init__(self, title, initial, on_submit):
        self._on_submit = on_submit
        self.w = Win((340, 190))
        p = self.w.p
        tw(p, (170, 158), title, C4, 1.0, 'center', maxw=310)
        sep(p, (17, 138), 306)
        self.inp = inp(p, (50, 84), (240, 36), initial if initial is not None else '', h='center')
        btn(p, (30, 18), (135, 36), L("confirm"), self._ok)
        btn(p, (175, 18), (135, 36), L("cancel"), self.w.close, DNG, DNGT)

    def _ok(self):
        txt = bui.textwidget(query=self.inp).strip()
        if txt == "":
            val = None
        else:
            try:
                val = int(txt)
            except Exception:
                BTW(L("invalid"))
                return
        self.w.close()
        bui.apptimer(0.2, Call(self._on_submit, val))


class Choice:
    def __init__(self, title, sub, options, on_pick):
        self._pickcb = on_pick
        n = len(options)
        h = 136 + 44 * n
        self.w = Win((380, h))
        p = self.w.p
        self.sel = NOSEL
        self.btns = []
        tw(p, (190, h - 30), title, C4, 1.0, 'center', maxw=350)
        tw(p, (190, h - 56), sub, C3, 0.8, 'center', maxw=350)
        sep(p, (17, h - 72), 346)
        for i, (lab, val) in enumerate(options):
            b = btn(p, (30, 14 + 44 * (n - i)), (320, 36), lab, Call(self._pick, val))
            self.btns.append((b, val))
        btn(p, (30, 14), (155, 34), L("confirm"), self._ok)
        btn(p, (195, 14), (155, 34), L("cancel"), self.w.close, DNG, DNGT)

    def _pick(self, v):
        self.sel = v
        for b, vv in self.btns:
            try:
                bui.buttonwidget(edit=b, color=C3 if vv == v else C2)
            except Exception:
                pass

    def _ok(self):
        if self.sel is NOSEL or self.sel == NOSEL:
            return
        v = self.sel
        self.w.close()
        bui.apptimer(0.2, Call(self._pickcb, v))


# ═══════════════════════════════════════════════════════════════
# MEMBER WINDOW
# ═══════════════════════════════════════════════════════════════

class MemberWin:
    COLORS = [("white", (1, 1, 1)), ("red", (1, 0.3, 0.3)), ("blue", (0.3, 0.6, 1)),
              ("green", (0.3, 1, 0.3)), ("yellow", (1, 1, 0.2)), ("orange", (1, 0.6, 0.2))]

    def __init__(self, api, member, on_refresh, src=None):
        self.api, self.m, self.on_refresh = api, member, on_refresh
        self.color = "white"
        self.sw = {}
        self.w = Win((340, 340), src=src)
        p = self.w.p
        name = member.get("name", "?")
        tw(p, (170, 312), f"{L('manage')}: {name}", C4, 1.0, 'center', maxw=310)
        sep(p, (17, 294), 306)

        tw(p, (19, 266), L('title'), C3, 0.8)
        self.inp_title = inp(p, (90, 250), (230, 32), (member.get("title") or {}).get("t", ""))

        tw(p, (19, 222), L('color'), C3, 0.8)
        for i, (nm, rgb) in enumerate(self.COLORS):
            self.sw[nm] = btn(p, (90 + i * 38, 209), (34, 26), '*' if nm == "white" else '',
                              Call(self._pick, nm), rgb, (0, 0, 0))
        btn(p, (19, 158), (302, 36), L('apply_title'), self._apply)
        sep(p, (17, 144), 306)
        btn(p, (19, 100), (302, 36), L('change_role'), self._role)
        muted = member.get("muted")
        btn(p, (19, 50), (147, 36), L("unmute") if muted else L("mute"), self._mute)
        btn(p, (174, 50), (147, 36), L("kick"), self._kick, DNG, DNGT)

    def _pick(self, nm):
        self.color = nm
        for k, b in self.sw.items():
            try:
                bui.buttonwidget(edit=b, label='*' if k == nm else '')
            except Exception:
                pass

    def _apply(self):
        title = bui.textwidget(query=self.inp_title).strip()

        def cb(r):
            TIP(L("saved"))
            ding(0, 1)
            self.w.close()
            self.on_refresh()
        Network.fetch(self.api, "ally_change_title", (self.m["id"], title, self.color), callback=cb)

    def _role(self):
        def picked(role):
            def cb(r):
                if r == "1":
                    TIP(L("role_changed"))
                    ding(0, 1)
                    self.w.close()
                    self.on_refresh()
                else:
                    BTW({"too_many": L("too_many"), "no_bot": L("no_bot")}.get(r, L("fail")))
            Network.fetch(self.api, "ally_change_role", (self.m["id"], role), callback=cb)
        Choice(L("select_role"), self.m.get("name", ""),
               [(L("general"), 2), (L("spy"), 3), (L("remove_role"), None)], picked)

    def _mute(self):
        typ = "unmute" if self.m.get("muted") else "mute"

        def cb(r):
            self.w.close()
            self.on_refresh()
        Network.fetch(self.api, "ally_mute", (self.m.get("name"), typ), callback=cb)

    def _kick(self):
        def do():
            def cb(r):
                self.w.close()
                self.on_refresh()
            Network.fetch(self.api, "ally_kick", (self.m["id"],), callback=cb)
        Confirm(L("kick"), f"{self.m.get('name', '?')}\n{L('kick_confirm')}", do)


# ═══════════════════════════════════════════════════════════════
# LOGIN WINDOW
# ═══════════════════════════════════════════════════════════════

class LoginWin:
    def __init__(self, api, on_success, src=None):
        global _cur
        self.api, self.on_success = api, on_success
        self._loading = None
        self._angle = 0
        self._busy = False
        self.w = Win((460, 330), src=src, on_close=lambda: _clear(self))
        _cur = self
        p = self.w.p
        tw(p, (19, 300), u"\ue010 BSLIFE Ally", C4, 1.0)
        tw(p, (19, 274), "Manage your alliance from inside BombSquad" if not _fa()
           else "مدیریت اتحاد از داخل بازی بمب اسکواد", C3, 0.8, maxw=420)
        sep(p, (17, 260), 426)
        tw(p, (19, 228), "• In BombSquad chat, type: login\n• Or message @BslifeBot: login" if not _fa()
           else "• در چت بازی تایپ کنید: login\n• یا در بات @BslifeBot: login", C3, 0.75, maxw=420)
        sep(p, (17, 196), 426)
        tw(p, (19, 170), "Username" if not _fa() else "اسم خاص", C4)
        self.inp_user = inp(p, (150, 154), (290, 34), '', 30)
        tw(p, (19, 120), "OTP" if not _fa() else "کد لاگین", C4)
        self.inp_otp = inp(p, (150, 104), (290, 34), '', 8)
        self.status = tw(p, (230, 78), '', C3, 0.8, 'center', maxw=420)
        btn(p, (80, 20), (140, 40), L("login"), self.do_login)
        btn(p, (240, 20), (140, 40), L("cancel"), self.w.close, DNG, DNGT)

    def alive(self):
        return self.w.alive()

    def set_status(self, text, col=C3):
        try:
            bui.textwidget(edit=self.status, text=text, color=col)
        except Exception:
            pass

    def do_login(self):
        if self._busy:
            return
        name = bui.textwidget(query=self.inp_user).strip()
        otp = bui.textwidget(query=self.inp_otp).strip()
        if not name or not otp:
            BTW(L("error_fill"))
            self.set_status(L("error_fill"), C5)
            return
        self._busy = True
        self.set_status(L("logging_in"), C3)
        ding(1, 0)
        self._loading = tw(self.w.p, (230, 78), u"\ue00c", C4, 1.6, 'center')

        def tick():
            if not self._busy or self._loading is None or not self.w.alive():
                return
            self._angle = (self._angle + 30) % 360
            try:
                bui.textwidget(edit=self._loading, rotate=self._angle)
            except Exception:
                pass
            bui.apptimer(0.05, tick)
        bui.apptimer(0.05, tick)

        def worker():
            ok, msg = self.api.login(name, otp)
            bui.pushcall(Call(self._done, ok, msg), from_other_thread=True)
        threading.Thread(target=worker, daemon=True).start()

    def _done(self, ok, msg):
        self._busy = False
        if self._loading is not None:
            try:
                self._loading.delete()
            except Exception:
                pass
            self._loading = None
        if not self.w.alive():
            return
        if ok:
            self.set_status(L("success_loading"), GRN)
            ding(0, 1)
            bui.apptimer(0.5, self._next)
        else:
            self.set_status(f"{L('error')}: {msg}", RED)
            BTW(f"{L('error')}: {msg}")

    def _next(self):
        self.w.close()
        bui.apptimer(0.3, self.on_success)


# ═══════════════════════════════════════════════════════════════
# MAIN WINDOW
# ═══════════════════════════════════════════════════════════════

CW, CH = 378, 310


class MainWin:
    TABS = ["overview", "members", "requests", "vault", "settings", "ranking", "news", "chat"]

    def __init__(self, api, src=None):
        global _cur
        self.api = api
        self.tab = "overview"
        self.tabs = {}
        self._req = "new"
        self._closing = False
        self._chat_token = 0
        self._chat_sig = None
        self.news_items = []
        self.c = None
        self.w = Win((520, 400), src=src, on_close=lambda: _clear(self))
        _cur = self
        p = self.w.p

        self.head = tw(p, (19, 375), u"\ue010 BSLIFE Ally", C4, 1.0, maxw=370)
        self.sub = tw(p, (19, 355), f"{L('user')}: ...", C3, 0.8, maxw=370)
        btn(p, (415, 358), (90, 30), L("logout"), self._logout, DNG, DNGT)
        sep(p, (17, 344), 486)

        panel(p, (10, 22), (108, 318))
        panel(p, (124, 22), (386, 318))
        self.status_line = tw(p, (260, 10), '', C3, 0.7, 'center', maxw=480)

        self._sidebar()
        self._new_content()
        self.refresh()

    # ── helpers ──
    def alive(self):
        return self.w.alive() and not self._closing

    def live(self, c):
        return self.alive() and c is not None and c.exists()

    def set_status(self, text, col=C3):
        try:
            bui.textwidget(edit=self.status_line, text=text, color=col)
        except Exception:
            pass

    def _new_content(self):
        if self.c is not None:
            try:
                self.c.delete()
            except Exception:
                pass
        self.c = bui.containerwidget(parent=self.w.p, position=(128, 26), size=(CW, CH), background=False)

    def _reload(self):
        if self.alive():
            self._new_content()
            self._render()

    def _logout(self):
        self._closing = True
        self.api.logout()
        self.w.close()
        bui.apptimer(0.3, lambda: LoginWin(self.api, _route))

    # ── sidebar ──
    def _sidebar(self):
        for b in self.tabs.values():
            try:
                b.delete()
            except Exception:
                pass
        self.tabs = {}
        y = 296
        for key in self.TABS:
            if key in ("requests", "settings") and self.api.roleid not in (1, 2):
                continue
            self.tabs[key] = btn(self.w.p, (16, y), (96, 30), L(key), Call(self.switch_tab, key), C2, C4, 0.8)
            y -= 38
        self._hl()

    def _hl(self):
        for k, b in self.tabs.items():
            try:
                sel = k == self.tab
                bui.buttonwidget(edit=b, color=C3 if sel else C2, textcolor=(1, 1, 1) if sel else C4)
            except Exception:
                pass

    def switch_tab(self, key):
        if not self.alive():
            return
        self.tab = key
        self._chat_token += 1
        self._hl()
        self._new_content()
        self._render()

    # ── status / header ──
    def refresh(self):
        self.set_status(L("loading"), C3)
        Network.fetch(self.api, "ally_status", callback=self._on_status)

    def _on_status(self, st):
        if not self.alive():
            return
        if isinstance(st, dict) and "error" in st:
            self.set_status(L("net_error"), RED)
            return
        if st in ("3", "0", "", None):
            self.set_status(L("session_expired"), C5)

            def check(who):
                if who:
                    self.refresh()
                else:
                    self.set_status(L("session_expired"), RED)
                    self._logout()
            Network.fetch(self.api, "whoami", callback=check)
            return
        if not isinstance(st, dict):
            self.w.close()
            bui.apptimer(0.3, lambda: HubWin(self.api))
            return
        self.api.ally = st.get("name")
        self.api.roleid = st.get("roleid")
        self.api.memberid = st.get("memberid")
        try:
            bui.textwidget(edit=self.head, text=u"\ue010 " + f"{st.get('name') or L('no_ally')} ({role_name(st.get('roleid'))})")
            bui.textwidget(edit=self.sub, text=f"{L('user')}: {self.api.user or '?'}")
        except Exception:
            pass
        self.set_status(L("ready"), GRN)
        self._sidebar()
        self._new_content()
        self._render()

    def _render(self):
        if not self.alive():
            return
        h = getattr(self, "t_" + self.tab, None)
        if h:
            try:
                h()
            except Exception as e:
                log(f"Render EXCEPTION {self.tab}: {e}")

    def _empty(self, c, text=None):
        tw(c, (CW / 2, CH / 2), text or L("empty"), C3, 0.9, 'center')

    # ── overview ──
    def t_overview(self):
        c = self.c

        def cb(st):
            if not self.live(c) or not isinstance(st, dict):
                return
            tw(c, (CW / 2, 285), L("overview"), C4, 1.0, 'center')
            sep(c, (10, 266), CW - 20)
            rid = st.get("roleid")
            rows = [(L("alliance_name"), st.get("name"), C4),
                    (L("your_role"), role_name(rid), role_color(rid)),
                    (L("members_count"), st.get("count", "?"), C4)]
            y = 232
            for lab, val, col in rows:
                tw(c, (14, y), lab, C3, 0.8, maxw=140)
                tw(c, (160, y), val, col, 0.9, maxw=205)
                sep(c, (10, y - 22), CW - 20)
                y -= 46
            if self.api.roleid != 1:
                btn(c, (116, 30), (146, 36), L("leave_ally"), self._leave, DNG, DNGT)
        Network.fetch(self.api, "ally_status", callback=cb)

    def _leave(self):
        def do():
            def cb(r):
                if r == "1":
                    self.w.close()
                    bui.apptimer(0.5, _route)
                else:
                    BTW(L("fail"))
            Network.fetch(self.api, "ally_leave", callback=cb)
        Confirm(L("leave_ally"), L("leave_confirm"), do)

    # ── members ──
    def t_members(self):
        c = self.c

        def cb(ms):
            if not self.live(c):
                return
            if not isinstance(ms, list):
                if ms in ("3", "", "-1"):
                    self._on_status("3")
                return
            if not ms:
                return self._empty(c)
            RH = 30
            sc, ct, H = listbox(c, (6, 6), (CW - 12, CH - 12), len(ms), RH)
            for i, m in enumerate(ms):
                y = H - RH * (i + 1)
                is_me = m.get("id") == self.api.memberid
                can = self.api.roleid in (1, 2) and not is_me
                tw(ct, (8, y + 15), role_name(m.get("roleid")), role_color(m.get("roleid")), 0.75, maxw=70)
                kw = dict(parent=ct, size=(250, RH), position=(80, y), text=m.get("name", "?"),
                          color=C5 if is_me else C3, v_align='center', maxwidth=240,
                          selectable=can, click_activate=can)
                if can:
                    kw["on_activate_call"] = Call(self._open_member, m)
                bui.textwidget(**kw)
        Network.fetch(self.api, "ally_members", callback=cb)

    def _open_member(self, m):
        snd('dingSmall')
        MemberWin(self.api, m, self._reload)

    # ── requests ──
    def t_requests(self):
        c = self.c
        for i, key in enumerate(["new", "accepted", "rejected"]):
            btn(c, (6 + i * 124, 278), (118, 28), L(key), Call(self._set_req, key),
                C3 if key == self._req else C2, (1, 1, 1) if key == self._req else C4, 0.8)

        def cb(reqs):
            if not self.live(c) or not isinstance(reqs, list):
                return
            if not reqs:
                return self._empty(c)
            RH = 32
            sc, ct, H = listbox(c, (6, 6), (CW - 12, 262), len(reqs), RH)
            for i, r in enumerate(reqs):
                y = H - RH * (i + 1)
                tw(ct, (8, y + 16), r.get("name", "?"), C3, 0.85, maxw=210)
                if self._req == "new":
                    btn(ct, (230, y + 4), (56, 24), L("yes"), Call(self._handle, r, "accept"), C2, GRN, 0.7)
                    btn(ct, (292, y + 4), (56, 24), L("no"), Call(self._handle, r, "reject"), DNG, DNGT, 0.7)
        Network.fetch(self.api, "ally_requests", (self._req,), callback=cb)

    def _set_req(self, key):
        self._req = key
        self._reload()

    def _handle(self, r, mode):
        def cb(res):
            self._reload()
        Network.fetch(self.api, "ally_handle_request", (r.get("id"), mode), callback=cb)

    # ── vault ──
    def t_vault(self):
        c = self.c

        def cb(v):
            if not self.live(c) or not isinstance(v, dict):
                return
            tw(c, (CW / 2, 265), L("vault"), C4, 1.0, 'center')
            sep(c, (10, 246), CW - 20)
            tw(c, (CW / 2, 195), f"{fmt(v.get('coin', 0))}", C5, 2.0, 'center')
            tw(c, (CW / 2, 150), L("coins"), C3, 0.9, 'center')
            sep(c, (10, 125), CW - 20)
            btn(c, (10, 60), (112, 38), L("deposit"), self._deposit)
            btn(c, (133, 60), (112, 38), L("history"), self._history)
            if self.api.roleid in (1, 2):
                btn(c, (256, 60), (112, 38), L("split"), self._split)
        Network.fetch(self.api, "ally_vault_status", callback=cb)

    def _deposit(self):
        def go(amount):
            if amount is None or amount < 100:
                BTW(L("min100"))
                return

            def cb(r):
                if r == "1":
                    TIP(L("deposit_ok"))
                    ding(0, 1)
                    if self.tab == "vault":
                        self._reload()
                else:
                    BTW(L("not_enough_coins") if r == "coin_not_enough" else L("fail"))
            Network.fetch(self.api, "ally_vault_add", (amount,), callback=cb)
        NumberInput(L("enter_amount"), "", go)

    def _split(self):
        def go(typ):
            def cb(r):
                if r == "1":
                    TIP(L("vault_split_ok"))
                    ding(0, 1)
                    if self.tab == "vault":
                        self._reload()
                else:
                    BTW({"coin_not_enough": L("not_enough_coins"), "no_ranking_info": L("no_ranking")}.get(r, L("fail")))
            Network.fetch(self.api, "ally_vault_clear", (typ,), callback=cb)
        Choice(L("split"), L("select_type"),
               [(L("equal_all"), "equal_all"), (L("equal_ranking"), "equal_ranking"),
                (L("ranking_points"), "ranking_points")], go)

    def _history(self):
        w = Win((460, 370))
        p = w.p
        tw(p, (230, 342), L("vault_news"), C4, 1.0, 'center')
        sep(p, (17, 324), 426)
        hold = bui.containerwidget(parent=p, position=(0, 0), size=(460, 320), background=False)
        tw(hold, (230, 160), L("loading"), C3, 0.8, 'center')

        def cb(news):
            if not w.alive() or not hold.exists() or not isinstance(news, list):
                return
            for ch in hold.get_children():
                ch.delete()
            if not news:
                tw(hold, (230, 160), L("empty"), C3, 0.9, 'center')
                return
            RH = 34
            sc, ct, H = listbox(hold, (17, 18), (426, 296), len(news), RH)
            for i, n in enumerate(news):
                y = H - RH * (i + 1)
                tw(ct, (6, y + 17), n.get("text", ""), C3, 0.75, maxw=300)
                if n.get("is_parent"):
                    btn(ct, (320, y + 4), (92, 26), L("vault_shares"), Call(self._shares, n.get("id")), C2, C4, 0.6)
        Network.fetch(self.api, "ally_vault_news", (None,), callback=cb)

    def _shares(self, trans_id):
        w = Win((340, 360))
        p = w.p
        tw(p, (170, 332), L("vault_shares"), C4, 1.0, 'center')
        sep(p, (17, 314), 306)
        hold = bui.containerwidget(parent=p, position=(0, 0), size=(340, 310), background=False)

        def cb(shares):
            if not w.alive() or not hold.exists() or not isinstance(shares, list):
                return
            if not shares:
                tw(hold, (170, 150), L("empty"), C3, 0.9, 'center')
                return
            RH = 28
            sc, ct, H = listbox(hold, (17, 18), (306, 286), len(shares), RH)
            for i, s in enumerate(shares):
                y = H - RH * (i + 1)
                tw(ct, (6, y + 14), s.get("name", "?"), C3, 0.8, maxw=170)
                tw(ct, (292, y + 14), fmt(s.get("val", 0)), C5, 0.8, 'right')
        Network.fetch(self.api, "ally_vault_shares", (trans_id,), callback=cb)

    # ── settings ──
    def t_settings(self):
        c = self.c

        def cb_s(st):
            if not self.live(c):
                return

            def cb_e(en):
                if not self.live(c) or not isinstance(st, dict) or not isinstance(en, dict):
                    return
                mode_txt = {None: L("mode_direct"), 1: L("mode_request"), -1: L("mode_closed")}.get(en.get("request"), "?")
                tag_on = st.get("taghide") is None
                price = fmt(st.get("price")) if st.get("price") else L("not_set")

                def num(title, key, cur, enrol):
                    return lambda: NumberInput(title, cur, lambda v: self._save(key, v, enrol))

                rows = [
                    ("row", L("capacity"), st.get("capacity", "?"), C4, L("buy_1"), self._buy_cap),
                    ("row", L("gkick"), st.get("gkick", 1), C4, L("set"), num(L("gkick"), "gkick", st.get("gkick", 1), False)),
                    ("row", L("spynet"), fmt(st.get("spynet", 0)), C4, L("set"), num(L("spynet"), "spynet", st.get("spynet", 0), False)),
                    ("row", L("tag_status"), L("tag_active") if tag_on else L("tag_inactive"), GRN if tag_on else RED, None, None),
                    ("row", L("sale_price"), price, C4, L("set"), num(L("sale_price"), "price", st.get("price"), False)),
                    ("hdr", L("enrol_settings")),
                    ("row", L("mode"), mode_txt, C4, L("change"), self._join_mode),
                    ("row", L("min_coin"), en.get("coin", "-"), C4, L("set"), num(L("min_coin"), "coin", en.get("coin"), True)),
                    ("row", L("req_top"), en.get("top", "-"), C4, L("set"), num(L("req_top"), "top", en.get("top"), True)),
                    ("row", L("min_score"), en.get("score", "-"), C4, L("set"), num(L("min_score"), "score", en.get("score"), True)),
                    ("row", L("bot_link"), L("required") if en.get("bot") == 1 else L("off"), C4, L("toggle"),
                     Call(self._toggle_bot, en.get("bot"))),
                ]
                RH = 42
                sc, ct, H = listbox(c, (6, 6), (CW - 12, CH - 12), len(rows), RH)
                for i, r in enumerate(rows):
                    y = H - RH * (i + 1)
                    if r[0] == "hdr":
                        tw(ct, (CW / 2 - 6, y + 21), r[1], C5, 0.9, 'center', maxw=330)
                        continue
                    _, lab, val, vcol, bl, bc = r
                    tw(ct, (8, y + 21), lab, C3, 0.75, maxw=150)
                    tw(ct, (162, y + 21), val, vcol, 0.8, maxw=100)
                    if bl:
                        btn(ct, (268, y + 7), (86, 28), bl, bc, C2, C4, 0.7)
                    sep(ct, (6, y), CW - 24)
            Network.fetch(self.api, "ally_enrol", callback=cb_e)
        Network.fetch(self.api, "ally_settings", callback=cb_s)

    def _save(self, key, val, enrol):
        def cb(r):
            if isinstance(r, dict) and "err" in r:
                BTW(str(r["err"]))
            else:
                TIP(L("saved"))
                ding(0, 1)
                if self.tab == "settings":
                    self._reload()
        Network.fetch(self.api, "ally_set_enrol" if enrol else "ally_save_setting", (key, val), callback=cb)

    def _buy_cap(self):
        def cb(r):
            if r == "1":
                TIP(L("success"))
                ding(0, 1)
            else:
                BTW(L("fail"))
            if self.tab == "settings":
                self._reload()
        Network.fetch(self.api, "ally_capacity", callback=cb)

    def _join_mode(self):
        Choice(L("mode"), "",
               [(L("mode_direct"), None), (L("mode_request"), 1), (L("mode_closed"), -1)],
               lambda v: self._save("request", v, True))

    def _toggle_bot(self, current):
        self._save("bot", None if current == 1 else 1, True)

    # ── ranking ──
    def t_ranking(self):
        c = self.c

        def cb(r):
            if not self.live(c) or not isinstance(r, dict):
                return
            tw(c, (CW / 2, 288), L("ranking"), C4, 1.0, 'center')
            if not r.get("rank"):
                tw(c, (CW / 2, 160), L("not_ranked"), C3, 0.9, 'center')
                return
            tw(c, (CW / 2, 252), f"#{r.get('rank')}  |  {float(r.get('score', 0)):.2f} pts", C5, 1.1, 'center')
            sep(c, (10, 232), CW - 20)
            eff = [m for m in (r.get("m_data") or {}).values() if m.get("c") == 1]
            if not eff:
                return
            RH = 26
            sc, ct, H = listbox(c, (6, 6), (CW - 12, 218), len(eff), RH)
            for i, m in enumerate(eff):
                y = H - RH * (i + 1)
                tw(ct, (8, y + 13), f"#{m.get('r', '?')} {m.get('n', '?')}", C3, 0.8, maxw=230)
                tw(ct, (330, y + 13), f"{float(m.get('s', 0)):.1f}", GRN, 0.8, 'right')
        Network.fetch(self.api, "ally_ranking", callback=cb)

    # ── news (accumulating "More") ──
    def t_news(self):
        self.news_items = []
        self._news_load(None, self.c)

    def _news_load(self, offset, c):
        def cb(news):
            if not self.live(c):
                return
            ok = isinstance(news, list)
            if ok:
                self.news_items += news
            self._news_draw(c, ok and len(news) == 10)
        Network.fetch(self.api, "ally_news", (offset,), callback=cb)

    def _news_draw(self, c, more):
        for ch in c.get_children():
            ch.delete()
        items = self.news_items
        if not items:
            return self._empty(c, L("no_news"))
        RH = 44
        top = 40 if more else 6
        sc, ct, H = listbox(c, (6, top), (CW - 12, CH - top - 6), len(items), RH)
        for i, n in enumerate(items):
            y = H - RH * (i + 1)
            tw(ct, (8, y + 28), n.get("text", ""), C4, 0.75, maxw=345)
            tw(ct, (8, y + 10), n.get("time", ""), C3, 0.6)
            sep(ct, (6, y), CW - 24)
        if more:
            last = items[-1].get("id")
            btn(c, (149, 6), (80, 28), L("more"), lambda: self._news_load(last, c))

    # ── chat ──
    def t_chat(self):
        c = self.c
        self._chat_sig = None
        self.chat_sc = bui.scrollwidget(parent=c, position=(6, 46), size=(CW - 12, CH - 52), border_opacity=0.4)
        self.chat_ct = bui.containerwidget(parent=self.chat_sc, size=(CW - 18, CH - 62), background=False)
        self.chat_inp = inp(c, (6, 6), (284, 34), '', 200, L("message"))
        btn(c, (296, 6), (76, 34), L("send"), self._send)
        token = self._chat_token

        def loop():
            if token != self._chat_token or not self.live(c) or self.tab != "chat":
                return
            self._chat_fetch(c, token, True)
        self._chat_fetch(c, token, True)

    def _chat_fetch(self, c, token, schedule):
        def cb(h):
            if token != self._chat_token or not self.live(c) or self.tab != "chat":
                return
            if isinstance(h, list):
                msgs = h[-50:]
                sig = (len(msgs), str(msgs[-1]) if msgs else "")
                if sig != self._chat_sig:
                    self._chat_sig = sig
                    try:
                        for ch in self.chat_ct.get_children():
                            ch.delete()
                        RH = 26
                        H = max(RH * len(msgs), CH - 62)
                        bui.containerwidget(edit=self.chat_ct, size=(CW - 18, H))
                        for i, m in enumerate(msgs):
                            y = H - RH * (i + 1)
                            tw(self.chat_ct, (6, y + 13), f"{m.get('name')}: {m.get('chat')}", C3, 0.75, maxw=345)
                        bui.scrollwidget(edit=self.chat_sc, vertical_scroll=0.0)
                    except Exception as e:
                        log(f"chat draw: {e}")
            if schedule:
                bui.apptimer(3.0, lambda: self._chat_fetch(c, token, True))
        Network.fetch(self.api, "ally_chat_history", callback=cb)

    def _send(self):
        try:
            msg = bui.textwidget(query=self.chat_inp).strip()
        except Exception:
            return
        if not msg:
            return
        bui.textwidget(edit=self.chat_inp, text="")
        c, token = self.c, self._chat_token

        def cb(r):
            if token == self._chat_token and self.live(c):
                self._chat_sig = None
                self._chat_fetch(c, token, False)
        Network.fetch(self.api, "ally_chat_send", (msg,), callback=cb)


# ═══════════════════════════════════════════════════════════════
# HUB WINDOW (not in an alliance)
# ═══════════════════════════════════════════════════════════════

class HubWin:
    def __init__(self, api, src=None):
        global _cur
        self.api = api
        self.order = "rank"
        self.sub = None
        self.w = Win((460, 400), src=src, on_close=lambda: _clear(self))
        _cur = self
        p = self.w.p
        tw(p, (19, 370), u"\ue010 " + L("hub_title"), C4, 1.0, maxw=320)
        tw(p, (19, 346), L("not_in_ally"), C3, 0.8, maxw=330)
        btn(p, (360, 350), (80, 34), L("logout"), self._logout, DNG, DNGT)
        sep(p, (17, 332), 426)
        self.b_create = btn(p, (19, 288), (205, 34), L("create_ally"), self._create_tab)
        self.b_join = btn(p, (236, 288), (205, 34), L("join_ally"), self._join_tab)
        sep(p, (17, 276), 426)
        self._join_tab()

    def alive(self):
        return self.w.alive()

    def _logout(self):
        self.api.logout()
        self.w.close()
        bui.apptimer(0.3, lambda: LoginWin(self.api, _route))

    def _mode(self, which):
        for b, k in ((self.b_create, "create"), (self.b_join, "join")):
            try:
                bui.buttonwidget(edit=b, color=C3 if k == which else C2,
                                 textcolor=(1, 1, 1) if k == which else C4)
            except Exception:
                pass

    def _fresh_sub(self):
        if self.sub is not None:
            try:
                self.sub.delete()
            except Exception:
                pass
        self.sub = bui.containerwidget(parent=self.w.p, position=(0, 0), size=(460, 270), background=False)
        return self.sub

    # ── create ──
    def _create_tab(self):
        self._mode("create")
        sub = self._fresh_sub()

        def cb(st):
            if not self.w.alive() or not sub.exists():
                return
            if not isinstance(st, dict) or "price" not in st:
                BTW(L("already_in_ally") if st == "0" else str(st))
                return
            tw(sub, (230, 215), f"{L('cost')}: {fmt(st['price'])} {L('coins')}", C5, 1.0, 'center')
            sep(sub, (17, 190), 426)
            tw(sub, (230, 160), L("alliance_name"), C3, 0.8, 'center')
            self.inp_name = inp(sub, (80, 110), (300, 36), '', 15, h='center')
            btn(sub, (150, 45), (160, 40), L("create_ally"), self._create)
        Network.fetch(self.api, "create_status", callback=cb)

    def _create(self):
        name = bui.textwidget(query=self.inp_name).strip()
        if not name:
            BTW(L("enter_name"))
            return

        def cb(r1):
            if r1 == "confirm_needed":
                def cb2(r2):
                    if isinstance(r2, dict) and "url" in r2:
                        ding(0, 1)
                        self.w.close()
                        bui.apptimer(0.8, _route)
                    elif isinstance(r2, dict) and "err" in r2:
                        BTW(str(r2["err"]))
                    else:
                        BTW(L("create_fail"))
                Network.fetch(self.api, "create_ally", (name, 1), callback=cb2)
            elif r1 == "already_in_ally":
                BTW(L("already_in_ally"))
            elif isinstance(r1, dict) and "err" in r1:
                BTW(str(r1["err"]))
            else:
                BTW(L("create_fail"))
        Network.fetch(self.api, "create_ally", (name, 0), callback=cb)

    # ── join ──
    def _join_tab(self):
        self._mode("join")
        sub = self._fresh_sub()
        self.order = "rank"
        self.inp_search = inp(sub, (17, 224), (270, 32), '', desc=L("search"))
        btn(sub, (297, 224), (146, 32), L("search"), self._search)
        self.obtn = {}
        for i, (code, key) in enumerate([("rank", "order_rank"), ("new", "order_new"),
                                         ("old", "order_old"), ("count", "order_count")]):
            self.obtn[code] = btn(sub, (17 + i * 107, 186), (102, 28), L(key), Call(self._set_order, code),
                                  C3 if code == "rank" else C2, (1, 1, 1) if code == "rank" else C4, 0.7)
        self.list_hold = bui.containerwidget(parent=sub, position=(0, 0), size=(460, 180), background=False)
        self._search()

    def _set_order(self, code):
        self.order = code
        for k, b in self.obtn.items():
            try:
                bui.buttonwidget(edit=b, color=C3 if k == code else C2, textcolor=(1, 1, 1) if k == code else C4)
            except Exception:
                pass
        self._search()

    def _search(self):
        hold = self.list_hold
        try:
            q = bui.textwidget(query=self.inp_search).strip()
        except Exception:
            q = ""

        def cb(allies):
            if not self.w.alive() or not hold.exists() or not isinstance(allies, list):
                return
            for ch in hold.get_children():
                ch.delete()
            vis = [a for a in allies if a.get("request") != -1]
            if not vis:
                tw(hold, (230, 90), L("empty"), C3, 0.9, 'center')
                return
            RH = 36
            sc, ct, H = listbox(hold, (17, 16), (426, 160), len(vis), RH)
            for i, a in enumerate(vis):
                y = H - RH * (i + 1)
                req = a.get("request")
                tw(ct, (8, y + 18), f"#{a.get('rank') or '-'} {a.get('name')}", C3, 0.85, maxw=270)
                btn(ct, (312, y + 5), (96, 28), L("request_btn") if req == 1 else L("join_btn"),
                    Call(self._join, a), C2, C4, 0.75)
        Network.fetch(self.api, "list_allies", (q, self.order), callback=cb)

    def _join(self, a):
        def cb(r):
            if r == "requested":
                TIP(L("request_sent"))
                ding(0, 1)
                self.w.close()
            elif r in ("./post/Ally", "./post.php?post=Ally", "already_in_ally") or (isinstance(r, str) and "post=Ally" in r):
                ding(0, 1)
                self.w.close()
                bui.apptimer(1.0, _route)
            elif r == "request_rejected":
                Msg(L("fail"), L("req_rejected"), "error")
            elif r == "request_unseen":
                Msg(L("fail"), L("req_pending"), "error")
            elif r == "already_left":
                Msg(L("fail"), L("already_left"), "error")
            else:
                reqs = []
                if a.get("coin"):
                    reqs.append(f"{L('min_coin')}: {a['coin']}")
                if a.get("top"):
                    reqs.append(f"{L('req_top')}: {a['top']}")
                if a.get("score"):
                    reqs.append(f"{L('min_score')}: {a['score']}")
                if a.get("bot"):
                    reqs.append(L("bot_link"))
                text = L("join_fail")
                if reqs:
                    text += f"\n\n{L('needed')}:\n- " + "\n- ".join(reqs)
                Msg(L("fail"), text, "error")
        Network.fetch(self.api, "join_ally", (a["id"],), callback=cb)


# ═══════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════

_api = None
_cur = None
_opening = False


def _clear(w):
    global _cur
    if _cur is w:
        _cur = None


def _ensure_api():
    global _api
    if _api is None:
        _api = BslifeAPI()
    return _api


def open_ally_manager(src=None):
    global _opening
    if _opening or (_cur is not None and _cur.alive()):
        return
    _opening = True
    api = _ensure_api()

    def check(who):
        global _opening
        _opening = False
        if not who:
            LoginWin(api, _route, src)
        else:
            _route(src)
    Network.fetch(api, "whoami", callback=check)


def _route(src=None):
    global _opening
    _opening = False
    api = _ensure_api()
    if _cur is not None and _cur.alive():
        _cur.w.close()

    def cb(st):
        if isinstance(st, dict) and "error" in st:
            BTW(L("net_error"))
            return
        if st in ("3", "0", "", None):
            api.logout()
            LoginWin(api, _route)
            return
        if isinstance(st, dict) and "name" in st:
            MainWin(api, src)
        else:
            HubWin(api, src)
    Network.fetch(api, "ally_status", callback=cb)


# ═══════════════════════════════════════════════════════════════
# PARTY WINDOW BUTTON (same style as Finder's, stacked under it)
# ═══════════════════════════════════════════════════════════════

def _make_button(z):
    sz = (80, 30)
    p = z._root_widget
    x, y = (-60, z._height - 85)
    bui.imagewidget(parent=p, size=(sz[0] * 1.34, sz[1] * 1.4),
                    position=(x - sz[0] * 0.14, y - sz[1] * 0.20),
                    texture=gt('softRect'), opacity=0.2, color=(0, 0, 0))
    holder = {}
    holder['b'] = bui.buttonwidget(
        parent=p, position=(x, y), size=sz, label='Ally', color=C1, textcolor=C3,
        texture=gt('white'), enable_sound=False,
        on_activate_call=lambda: open_ally_manager(holder['b']))


def _patch_party_window():
    original_init = party.PartyWindow.__init__

    def patched(self, *a, **k):
        original_init(self, *a, **k)
        try:
            _make_button(self)
        except Exception as e:
            log(f"Patch error: {e}")
    party.PartyWindow.__init__ = patched


# ba_meta export babase.Plugin
class BSLifeAllyMod(babase.Plugin):
    def on_app_running(self):
        log("--- Loaded (Finder style) ---")
        _patch_party_window()
