# ba_meta require api 9
# (see https://ballistica.net/wiki/meta-tag-system)

"""گیم‌مود Boss Fight برای BombSquad (Ballistica API 9).

یک باسِ مکعبیِ بزرگ وسطِ مپ اسپاون می‌شه. باس سرِ جاش ثابت می‌مونه،
فقط آروم بالا/پایین شناور می‌شه، نزدیک‌ترین پلیرِ زنده رو دنبال
می‌کنه، و به‌طورِ دوره‌ای یک مکعبِ کوچیکِ هدایت‌شونده (homing) به
سمتش پرتاب می‌کنه. این مکعب دقیقاً دنبالِ پلیر می‌گرده تا بهش بخوره
(نه یک شلیکِ خطیِ الکی)، ولی برای این‌که هیچ‌وقت از مپ خارج نشه و
باعثِ اسپمِ پیامِ out-of-bounds و قفل‌شدنِ تردِ لاجیک نشه، شعاعِ
چرخشش و محدوده‌ی حرکتش کنترل می‌شه. برخوردِ این مکعب با پلیر یک
انفجارِ واقعی (دقیقاً مثلِ یک بمبِ معمولیِ بازی) می‌سازه که طبقِ
سیستمِ استانداردِ دمیجِ خودِ بازی به هر پلیرِ داخلِ شعاعِ انفجار
(نه فقط هدفِ اصلی) آسیب می‌زنه.

باس فقط با برخوردِ مستقیمِ فیزیکیِ یک بمبِ زنده آسیب می‌بینه
(تشخیص از طریقِ bs.getcollision() که خودِ متریالِ بمب رو معرفی
می‌کنه، نه با حدس‌زدنِ نوعِ دلگیت)، و هر ضربه دقیقاً یک واحد دمیج
می‌زنه. شعاعِ انفجارِ بمب (Blast/HitMessage) هیچ آسیبی به باس
نمی‌زنه -- فقط تماسِ مستقیمِ خودِ بدنه‌ی بمب با بدنه‌ی باس دمیج
حساب می‌شه.

سختیِ مبارزه ثابت نیست: هرچی HP باس کمتر بشه، باس عصبانی‌تر و
خطرناک‌تر می‌شه (سیستمِ خشم/rage، رجوع به BossActor._current_phase):
فاصله‌ی بینِ شلیک‌ها کوتاه‌تر می‌شه، پرتابه‌ها سریع‌تر و بهتر
هدایت می‌شن، و در فازِ آخر هر شلیک شاملِ دو پرتابه‌ی هم‌زمان با یک
زاویه‌ی بازِ کوچیکه. این گذارها با تغییرِ رنگِ چشم/نورِ باس، یک
پیامِ هشدار روی صفحه، و آپدیتِ نوارِ سلامتی به پلیرها اعلام می‌شه.

اگه یک پلیرِ خاص چندین بار پشتِ‌سرِهم شلیک بهش نخوره (این عدد هم
هرچی باس عصبانی‌تر باشه کمتر می‌شه)، همون‌جا فریز می‌شه؛ برخوردِ
بعدیِ هر پرتابه با پلیرِ فریزشده، طبقِ همون سیستمِ معمولیِ
انفجار، بهش آسیب می‌زنه.

وقتی HP صفر بشه، با افکتِ انفجار از بین می‌ره و بعد از ۳۰ ثانیه
دوباره اسپاون می‌شه (با فازِ خشمِ صفرشده).

نکته: بعد از کپی‌کردنِ فایل توی پوشه‌ی mods، باید از تنظیماتِ بازی
(Settings -> Advanced -> Run Meta Scan) اسکن متا رو دستی اجرا کنی یا
بازی رو کامل ببندی و دوباره باز کنی.
"""

from __future__ import annotations

import math
import random
import weakref
from typing import TYPE_CHECKING

import babase
import bascenev1 as bs
from bascenev1lib.gameutils import SharedObjects
from bascenev1lib.actor.bomb import Bomb, Blast
from bascenev1lib.actor.spazbot import SpazBot
from bascenev1lib.actor.playerspaz import PlayerSpaz

if TYPE_CHECKING:
    from typing import Any, Sequence


# -----------------------------------------------------------------------
# ثابت‌ها
# -----------------------------------------------------------------------

BOSS_MAX_HP: int = 10
BOSS_HP_PER_EXTRA_PLAYER: int = 3
BOSS_DAMAGE_PER_BOMB_HIT: int = 1
BOSS_VULNERABLE_DAMAGE_BONUS: int = 1
BOSS_VULNERABLE_WINDOW: float = 3.1
BOSS_SPAWN_HEIGHT: float = 3.0
BOSS_BODY_SCALE: float = 2.5
BOSS_MESH_SCALE: float = 2.5

# -----------------------------------------------------------------------
# صداهای اسکلتی
# -----------------------------------------------------------------------
# به‌جایِ صدای زنگِ بوکس (boxingBell) که بیشتر حسِ «مسابقه» می‌ده،
# از صداهای خودِ اسکلتِ داخلیِ بازی (bonesDeath/gasp) استفاده
# می‌کنیم تا باس -- که مدلش bonesHead هست -- صدایی هم‌خوان با
# ظاهرش داشته باشه. هر کدوم داخلِ یک تلاشِ try/except صدا زده
# می‌شن (رجوع به _play_boss_sound)، پس اگه اسمِ یک صدا در نسخه‌ای
# از بازی موجود نباشه، هیچ‌وقت گیم‌مود کرش نمی‌کنه -- فقط همون یک
# صدا نواخته نمی‌شه و بعدیِ لیست امتحان می‌شه.
BOSS_SOUND_SPAWN: tuple[str, ...] = (
    'bonesDeath', 'bones1', 'bones2', 'bones3', 'gasp',
)
BOSS_SOUND_PHASE_CHANGE: tuple[str, ...] = (
    'bonesDeath', 'bones3', 'hiss', 'gong', 'gasp',
)
BOSS_SOUND_HIT: tuple[str, ...] = (
    'bones1', 'bones2', 'bones3', 'impact_medium', 'hiss', 'gasp',
)
BOSS_SOUND_FREEZE: tuple[str, ...] = (
    'bonesFall', 'bonesDeath', 'freeze', 'hiss', 'gasp',
)
BOSS_SOUND_DEATH: tuple[str, ...] = (
    'bonesDeath', 'explosion01', 'explosion02', 'gong', 'hiss',
)
BOSS_SOUND_AMBIENT: tuple[str, ...] = (
    'bones1', 'bones2', 'bones3', 'bonesFall', 'hiss', 'gasp',
)
BOSS_SOUND_ATTACK_WARN: tuple[str, ...] = (
    'bones1', 'bones2', 'bones3', 'hiss', 'gasp',
)
BOSS_SOUND_ATTACK_BIG: tuple[str, ...] = (
    'bonesDeath', 'bonesFall', 'hiss', 'gong', 'explosion01',
)
BOSS_SOUND_BREATHER: tuple[str, ...] = (
    'bones2', 'bones3', 'hiss', 'powerdown01', 'gasp',
)
BOSS_SOUND_REGEN: tuple[str, ...] = (
    'bonesDeath', 'bones3', 'hiss', 'powerdown01', 'shield_up', 'gasp',
)

# -----------------------------------------------------------------------
# جهتِ صورتِ باس
# -----------------------------------------------------------------------
# رفعِ باگ («کله رو به آسمونه»): مدلِ استفاده‌شده برایِ باس دقیقاً
# همون 'bonesHead' یِ خودِ UFC_BSLIFE11.py (کلاسِ CustomModel2)
# هست. اونجا هیچ‌وقت orientation دستی روی نود ست نمی‌شه -- نود فقط
# با orientation پیش‌فرضِ موتور ساخته می‌شه و دیگه هیچ‌وقت دست‌کاری
# نمی‌شه -- و همین باعث می‌شه کله دقیقاً رو به جلو دیده بشه. نسخه‌ی
# قبلیِ این فایل یک کوترنیونِ اصلاحیِ دستی (BOSS_FACE_PITCH/YAW/
# ROLL_DEGREES) هر تیک روی نود ست می‌کرد که فقط یک حدسِ آزمایشیِ
# تست‌نشده بود و باعثِ همون چرخشِ اشتباه می‌شد. الان دقیقاً مثلِ
# UFC، هیچ‌جا (نه در __init__، نه در _animate، نه در
# _recover_from_out_of_bounds) orientation دستی ست نمی‌شه.

# آفستِ محلیِ چشم‌ها نسبت به مرکزِ باس (قبل از ضرب در BOSS_MESH_SCALE).
# کله هیچ‌وقت نمی‌چرخه (body از نوعِ 'puck' + بدونِ هیچ برخوردِ
# فیزیکیِ گشتاورساز؛ رجوع به کامنتِ بالای BossActor.__init__)، پس
# مشِ کله همیشه با همون جهتِ ثابتِ اولیه (رو به رو) رندر می‌شه؛ در
# نتیجه این سه‌تا عدد دقیقاً همون موقعیتِ ثابتیه که چشم‌ها روش
# می‌شینن. برای این‌که چشم‌ها داخلِ
# حفره‌ی چشمِ خودِ مش (هرکدوم از bonesHead/bomb/tnt که لود شده)
# دقیقاً جا بیفتن، همین سه‌تا عدد رو دستی تنظیم کن:
#   X: فاصله‌ی افقی از مرکزِ کله تا هرکدوم از دو چشم (چپ/راست)
#   Y: ارتفاعِ چشم نسبت به مرکزِ کله (مثبت = بالاتر)
#   Z: عمقِ چشم رو به جلو/عقب نسبت به مرکزِ کله (این جهتیه که
#      همیشه "جلوی" مشِ کله حساب می‌شه، چون کله هیچ‌وقت نمی‌چرخه)
# فاصله‌ی بینِ دو تا دایره‌ی چشم (قبل از ضرب در BOSS_MESH_SCALE).
# این عدد مستقیماً کنترل می‌کنه چقدر دو چشم از هم دور/نزدیک باشن؛
# هرچی بزرگ‌تر باشه فاصله‌ی بینِ دو دایره بیشتر می‌شه. (این مقدار
# جایگزینِ BOSS_EYE_OFFSET_X شد؛ خودِ آفستِ X از رویِ همین محاسبه
# می‌شه: هر چشم نصفِ این فاصله از مرکز فاصله می‌گیره.)
BOSS_EYE_GAP: float = 0.3

# جابه‌جاییِ سراسریِ افقیِ هر دو چشم با هم (قبل از ضرب در
# BOSS_MESH_SCALE). این عدد به آفستِ X هردو چشم اضافه می‌شه، پس
# فاصله‌ی بینشون (BOSS_EYE_GAP) رو تغییر نمی‌ده، فقط کلِ جفتِ چشم
# رو یکجا به راست (مثبت) یا چپ (منفی) می‌بره.
BOSS_EYE_SHIFT_X: float = 0.1

# مقدارِ اضافی که فقط به ارتفاعِ چشمِ راست اضافه می‌شه (قبل از ضرب
# در BOSS_MESH_SCALE). چشمِ چپ دست‌نخورده می‌مونه؛ فقط چشمِ راست
# به همین اندازه بالاتر می‌ره.
BOSS_EYE_RIGHT_LIFT: float = 0.05

BOSS_EYE_OFFSET_X: float = BOSS_EYE_GAP / -4.0
BOSS_EYE_OFFSET_Y: float = 0.145
BOSS_EYE_OFFSET_Z: float = 0.23

# سایزِ هر دایره‌ی چشم (قبل از ضرب در BOSS_MESH_SCALE). هرچی
# بزرگ‌تر باشه دایره‌ی چشم بزرگ‌تر دیده می‌شه.
BOSS_EYE_SIZE: float = 0.1

# حداکثر جابه‌جاییِ "مردمک" داخلِ حفره به سمتِ هدف (قبل از ضرب در
# BOSS_MESH_SCALE). این یک عددِ کوچیکه که فقط باعثِ یک حرکتِ محدودِ
# چشم به سمتِ پلیر می‌شه، نه چرخشِ کاملِ دورِ کله. هرچی بزرگ‌تر باشه
# چشم بیشتر جابه‌جا می‌شه؛ اگه صفر بشه چشم‌ها کاملاً بی‌حرکت می‌مونن.
BOSS_EYE_MOVE_RADIUS: float = 0.065
BOSS_FLOAT_AMPLITUDE: float = 0.35
BOSS_FLOAT_PERIOD: float = 3.0
BOSS_RESPAWN_DELAY: float = 30.0
BOSS_AMBIENT_FX_INTERVAL: float = 2.0    # افکتِ محیطی خیلی کم‌تر شد
BOSS_TARGET_SCAN_INTERVAL: float = 0.3
BOSS_REGEN_DELAY: float = 13.0
BOSS_REGEN_INTERVAL: float = 4.0
BOSS_REGEN_AMOUNT: int = 1
BOSS_REGEN_MAX_FRACTION: float = 1.0
BOSS_REGEN_NOTICE_INTERVAL: float = 10.0

# -----------------------------------------------------------------------
# سیاه‌چاله‌ی مرگِ باس
# -----------------------------------------------------------------------
# طبقِ درخواست: وقتی باس می‌میره، سرِ جاش دقیقاً همون کلاسِ BlackHole
# (رجوع به bascenev1lib/actor/anomalies.py در پروژه‌ی overclocked:
# https://github.com/HeyErfan/overclocked/blob/master/src/assets/
# ba_data/python/bascenev1lib/actor/anomalies.py) اسپاون می‌شه --
# نه یک پیاده‌سازیِ سفارشیِ مشابه، بلکه عیناً همون کلاس (رجوع به
# بخشِ «کلاسِ BlackHole (عیناً پورت‌شده...)» پایین‌ترِ همین فایل).
# این سیاه‌چاله دقیقاً BLACKHOLE_LIFETIME ثانیه سرِ جاش می‌مونه (فارغ
# از این‌که چیزی رو بلعیده باشه یا نه) و بعدش خودش جمع می‌شه و
# ناپدید می‌شه؛ فقط از همون لحظه‌ی ناپدیدشدن، شمارشِ
# BOSS_RESPAWN_DELAY ثانیه‌ای برای اسپاونِ باسِ بعدی شروع می‌شه (نه
# هم‌زمان با مرگِ خودِ باس). BLACKHOLE_RADIUS/XSPEED/SSIZE دقیقاً
# همون پارامترهای سازنده‌ی خودِ کلاسِ BlackHole هستن (radius/xspeed/
# ssize)؛ با مقادیرِ پیش‌فرضِ خودِ کلاس (radius=10.0, xspeed=1.0)
# رشدِ کاملِ سیاه‌چاله هم دقیقاً حدودِ ۱۰ ثانیه طول می‌کشه، پس با
# BLACKHOLE_LIFETIME هماهنگه.
BLACKHOLE_LIFETIME: float = 20.0
BLACKHOLE_RADIUS: float = 15.0
BLACKHOLE_XSPEED: float = 2.0
BLACKHOLE_SSIZE: float = 0.0

MINI_BLACKHOLE_LIFETIME: float = 2.7
MINI_BLACKHOLE_RADIUS: float = 3.8
MINI_BLACKHOLE_XSPEED: float = 3.8
MINI_BLACKHOLE_SSIZE: float = 0.0

# اولین شلیکِ باس بعدِ هر اسپاون، به‌جایِ نزدیک‌ترین پلیر، دقیقاً
# همین نقطه‌ی ثابت رو هدف می‌گیره -- و کاملاً نامرئیه (بدونِ مش/
# نور/جرقه/صدا)، پس هیچ‌کس نمی‌بینتش. بعدِ همون یک شلیک، باس دوباره
# طبقِ روالِ عادی نزدیک‌ترین پلیر رو دنبال و هدف می‌گیره.
BOSS_FIRST_SHOT_TARGET: tuple[float, float, float] = (0.0, 3.0, 9.0)

# -----------------------------------------------------------------------
# سیستمِ خشم / سختیِ پویا (rage system)
# -----------------------------------------------------------------------
# هرچی جونِ باس کمتر بشه، باس تهاجمی‌تر و خطرناک‌تر می‌شه -- دقیقاً
# مثلِ باس‌فایت‌های واقعی. مبارزه سه فاز داره که فقط بر اساسِ درصدِ
# HP فعلیِ باس تعیین می‌شن (نه زمان یا چیزِ دیگه):
#   فازِ ۰ (نرمال): از ۱۰۰٪ تا BOSS_RAGE_PHASE2_HP_FRACTION
#   فازِ ۱ (خشمگین): زیرِ همون درصد تا BOSS_RAGE_PHASE3_HP_FRACTION
#   فازِ ۲ (در آستانه‌ی جنون): زیرِ اون درصد تا مرگ
# هر فاز، فاصله‌ی شلیک رو کوتاه‌تر، سرعتِ پرتابه رو بیشتر، و در
# فازِ آخر تعدادِ پرتابه‌ی هر شلیک رو دوتا می‌کنه.
BOSS_RAGE_PHASE2_HP_FRACTION: float = 0.66   # زیرِ این درصد -> فازِ ۱
BOSS_RAGE_PHASE3_HP_FRACTION: float = 0.33   # زیرِ این درصد -> فازِ ۲

BOSS_ATTACK_INTERVAL_PHASE: tuple[float, float, float] = (6.2, 4.8, 3.6)
BOSS_PROJECTILE_SPEED_MULT_PHASE: tuple[float, float, float] = (0.9, 1.05, 1.22)
BOSS_PROJECTILE_TURN_MULT_PHASE: tuple[float, float, float] = (0.85, 0.95, 1.05)
BOSS_PROJECTILE_COUNT_PHASE: tuple[int, int, int] = (1, 1, 2)
BOSS_MULTISHOT_SPREAD_DEGREES: float = 18.0  # زاویه‌ی بازشدنِ پرتابه‌ها در فازِ خشم
BOSS_ATTACK_TELEGRAPH_DELAY: float = 0.85
BOSS_BIG_ATTACK_COOLDOWN: float = 10.0
BOSS_DIRECTOR_MEMORY: float = 16.0
BOSS_DIRECTOR_HIT_MEMORY: float = 12.0
BOSS_DIRECTOR_NO_DAMAGE_MERCY_TIME: float = 15.0
BOSS_THREAT_LIMIT: int = 4
BOSS_MAX_LIVE_PROJECTILES: int = 3
BOSS_AMBIENT_SOUND_INTERVAL: tuple[float, float] = (4.8, 8.8)
BOSS_ATTACK_THREAT_COST: dict[str, int] = {
    'breather': 0,
    'fake_telegraph': 0,
    'homing': 1,
    'warning_homing': 1,
    'focus_shot': 1,
    'burst': 2,
    'gap_shockwave': 3,
    'shockwave': 3,
    'mini_blackhole': 4,
}
BOSS_ATTACK_TYPES_PHASE: tuple[tuple[str, ...], ...] = (
    ('homing', 'homing', 'shockwave'),
    ('homing', 'homing', 'burst', 'shockwave'),
    ('homing', 'burst', 'shockwave', 'mini_blackhole'),
)

BOSS_SHOCKWAVE_RING_COUNT_PHASE: tuple[int, int, int] = (6, 8, 10)
BOSS_SHOCKWAVE_RADIUS_PHASE: tuple[float, float, float] = (2.8, 3.6, 4.4)
BOSS_SHOCKWAVE_BLAST_RADIUS: float = 0.75
BOSS_SHOCKWAVE_STEP_DELAY: float = 0.075

BOSS_TARGET_LAST_HITTER_CHANCE: float = 0.35
BOSS_TARGET_RUNAWAY_CHANCE: float = 0.30
BOSS_MISS_WARNING_MARGIN: int = 1

# بازه‌ی تعدادِ شلیکِ ناموفقِ لازم برای فریزکردنِ یک پلیر، به‌ازایِ
# هر فاز. هرچی باس عصبانی‌تر باشه، زودتر پلیرِ فراری رو فریز می‌کنه.
BOSS_MISS_THRESHOLD_RANGE_PHASE: tuple[tuple[int, int], ...] = (
    (3, 5), (2, 4), (2, 3),
)

# رنگ‌ها و اثراتِ چشم/نور به‌ازایِ هر فاز (چشم‌ها هرچی باس
# عصبانی‌تر می‌شه، سرخ‌تر و پرنورتر می‌شن).
BOSS_PHASE_EYE_LIGHT_COLOR: tuple[tuple[float, float, float], ...] = (
    (1.2, 0.0, 0.0), (1.6, 0.05, 0.0), (2.2, 0.15, 0.0),
)
BOSS_PHASE_EYE_LOCATOR_COLOR: tuple[tuple[float, float, float], ...] = (
    (3.0, 0.0, 0.0), (3.6, 0.2, 0.0), (4.2, 0.4, 0.0),
)
BOSS_PHASE_GLOW_COLOR: tuple[tuple[float, float, float], ...] = (
    (1.0, 0.05, 0.05), (1.0, 0.15, 0.02), (1.0, 0.3, 0.0),
)
BOSS_PHASE_ANNOUNCE_TEXT: tuple[str | None, ...] = (
    None,
    'باس عصبانی شد! سرعتِ حمله‌ش بیشتر شد!',
    'باس به‌شدت خشمگین شده! مراقبِ شلیک‌های سریع و هم‌زمان باش!',
)

# تنظیماتِ نورِ کلِ مپ برای حسِ ترسناک/تاریک‌تر. این مقادیر روی
# globalsnode ست می‌شن (نه فقط دورِ خودِ باس)، پس کلِ صحنه تاریک‌تر
# و دراماتیک‌تر می‌شه. اگه خواستی دوباره روشن‌تر بشه، این عددها رو
# به سمتِ 1.0 (مقدارِ عادیِ بازی) ببر.
# تنظیماتِ رنگ و تاریکیِ لبه‌ی کلِ مپ برای حسِ ترسناک/تاریک‌تر. این
# مقادیر روی globalsnode ست می‌شن (نه فقط دورِ خودِ باس)، پس کلِ
# صحنه سردتر و ترسناک‌تر می‌شه -- بدونِ این‌که نورِ واقعیِ صحنه
# (روشناییِ کلی) کم بشه؛ فقط رنگ‌آمیزی و تیرگیِ لبه‌ها تغییر می‌کنه.
# اگه خواستی دوباره حالتِ عادی بشه، این عددها رو به نزدیکِ (1,1,1)
# برگردون.
MAP_TINT: tuple[float, float, float] = (0.55, 0.5, 0.62)
MAP_VIGNETTE_OUTER: tuple[float, float, float] = (0.35, 0.32, 0.4)
MAP_VIGNETTE_INNER: tuple[float, float, float] = (0.7, 0.68, 0.75)

PROJECTILE_SPEED: float = 3.2            # آروم‌تر، طبقِ درخواست
PROJECTILE_LIFETIME: float = 5.0
PROJECTILE_SCALE: float = 0.55
PROJECTILE_TURN_RATE: float = 3.0        # چرخشِ نرم به‌جای قفل‌شدنِ آنی روی هدف
PROJECTILE_SPEED_BLEND: float = 0.22    # how quickly projectile speed adjusts

# شعاعِ انفجارِ واقعیِ Blast که پرتابه‌ی باس با برخورد به پلیر
# ایجاد می‌کنه (به‌جایِ یک مرگِ خشکِ بدونِ افکت). با یک بمبِ نرمالِ
# بازی قابلِ‌مقایسه‌ست تا حسِ «واقعاً منفجر شد» بده.
PROJECTILE_BLAST_RADIUS: float = 2.2

# فاصله‌ی اسپاونِ پرتابه از مرکزِ بدنِ باس، فقط دقیقاً به‌اندازه‌ی
# یک شکافِ کوچیک بیرونِ بدنه (نه یک فاصله‌ی بزرگ که حسِ «پرتابه از
# جایی دیگه میاد، نه از خودِ باس» بده). این عدد پایین نگه داشته
# می‌شه چون حالا (برخلافِ قبل) خودِ متریالِ پرتابه صریحاً پاسخِ
# فیزیکیِ برخورد با بدنِ باس رو غیرفعال کرده (رجوع به
# BossProjectile.__init__)، پس دیگه نیازی به یک آفستِ بزرگ برای
# فرارکردن از برخوردِ فیزیکیِ خودِ باس نیست.
PROJECTILE_SPAWN_OFFSET_MULT: float = 0.55

TICK_INTERVAL: float = 1.0 / 30.0

# محدوده‌ی مجازِ حرکتِ پرتابه نسبت به نقطه‌ی اسپاونِ باس (متر). اگه
# پرتابه به هر دلیلی (مثلاً پلیر از لبه‌ی مپ رد بشه) از این محدوده
# خارج بشه، به‌جایِ این‌که بره تو out-of-bounds و اسپم/فریز بسازه،
# خودش رو همون‌جا حذف می‌کنیم.
PROJECTILE_MAX_RANGE: float = 9.0

# رویکردِ نهایی، دقیقاً همون چیزی که توی خودِ UFC_BSLIFE11.py برایِ
# کله‌ی اسکلتی (CustomModel2 با model='bonesHead') استفاده شده:
# هیچ‌جا دستی روی node.orientation چیزی ست نمی‌شه و هیچ محاسبه‌ی
# quaternion/look-at ای در کار نیست. کله فقط با orientation
# پیش‌فرض (هویتی) ساخته می‌شه و همون‌جوری می‌مونه؛ خودِ مشِ
# 'bonesHead' طوری طراحی شده که با orientation هویتی از قبل رو به
# جلو (رو به بازیکن‌ها) دیده می‌شه.
#
# این‌که کله هیچ‌وقت نمی‌چرخه، صرفاً حاصلِ دو چیزه (نه یک سیستمِ
# جداگانه‌ی قفل‌کردن):
#   ۱) body از نوعِ 'puck' هست (دقیقاً مثلِ UFC) -- این بدنه ذاتاً
#      یک دیسکِ افقیه و در پیچ/رول قفل می‌مونه، فقط دورِ محورِ
#      عمودی (yaw) می‌تونه بچرخه.
#   ۲) هر برخوردی که ممکنه یک ایمپالسِ فیزیکی/گشتاور به بدنه وارد
#      کنه (بمب، پلیر، پاورآپ‌باکس...) از قبل با
#      ('modify_part_collision', 'physical', False) روی
#      self._bomb_contact_material غیرفعال شده، پس اصلاً هیچ
#      نیرویی به بدنه اعمال نمی‌شه که بخواد بچرخوندش. زیرِ همین
#      شرایط، دقیقاً مثلِ کله‌ی اسکلتیِ UFC، چیزی برای چرخوندنِ کله
#      وجود نداره.


class _BombTouchMessage:
    """پیامِ سبکِ داخلی: یعنی «یک چیزیِ دارایِ object_material به
    باس خورد». خودِ handlemessage باس با bs.getcollision() چک
    می‌کنه که آیا اون «چیز» واقعاً یک Bomb زنده‌ست یا نه (نه پلیر،
    نه جعبه، نه چیزِ دیگه)."""


class _ProjectileHitPlayerMessage:
    """پیامِ سبکِ داخلی: یعنی «این پرتابه دقیقاً به پلیرِ هدفش
    خورد». این پیام مستقل از bs.DieMessage و قبل از اون فرستاده
    می‌شه، تا خودِ BossProjectile بتونه دقیقاً تشخیص بده که آیا
    مرگش به‌خاطرِ برخورد با پلیر بوده (hit) یا به‌خاطرِ تمام‌شدنِ
    عمرش/خروج از محدوده بوده (miss)، و این نتیجه رو به باس گزارش
    بده."""


def _play_boss_sound(
    candidates: tuple[str, ...],
    volume: float = 1.0,
    position: tuple[float, float, float] | None = None,
) -> None:
    """پخشِ اولین صدایی که از رویِ لیستِ `candidates` واقعاً در
    دسترسِ bs.getsound() باشه. برای هر باس بجای وابستگیِ سفت به
    یک اسمِ ثابت (مثلِ boxingBell)، از چند اسمِ صدایِ اسکلتی/طبیعیِ
    خودِ بازی به‌ترتیب امتحان می‌شه؛ اگه هیچ‌کدوم پیدا نشد، بی‌سروصدا
    رد می‌شه بدونِ کرش."""
    names = list(candidates)
    random.shuffle(names)
    for name in names:
        try:
            sound = bs.getsound(name)
            if position is not None:
                sound.play(volume, position=position)
            else:
                sound.play(volume)
            return
        except Exception:
            try:
                bs.getsound(name).play()
                return
            except Exception:
                continue


def _play_boss_sound_burst(
    candidates: tuple[str, ...],
    count: int = 2,
    spacing: float = 0.14,
    volume: float = 1.0,
    position: tuple[float, float, float] | None = None,
) -> None:
    """Play a few short creepy layers without requiring any specific sound."""
    for i in range(max(1, count)):
        delay = i * spacing
        if delay <= 0.0:
            _play_boss_sound(candidates, volume=volume, position=position)
        else:
            bs.timer(
                delay,
                bs.CallStrict(_play_boss_sound, candidates, volume, position),
            )


def chasattr(obj: Any, name: str) -> bool:
    """معادلِ محلیِ era.utils.chasattr (که در پروژه‌ی اصلیِ
    anomalies.py استفاده شده و در این پروژه در دسترس نیست): یک
    hasattr امن که هر Exception احتمالی حینِ خوندنِ attribute (نه
    فقط AttributeError) رو هم قورت می‌ده و False برمی‌گردونه. کلاسِ
    BlackHole دقیقاً به همین رفتار برای پیمایشِ bs.getnodes() نیاز
    داره."""
    try:
        getattr(obj, name)
        return True
    except Exception:
        return False


def _safe_position(actor_or_node: Any) -> tuple[float, float, float] | None:
    """گرفتنِ موقعیتِ یک نود/اکتور به‌صورتِ امن."""
    try:
        node = getattr(actor_or_node, 'node', actor_or_node)
        if not node:
            return None
        return tuple(node.position)
    except Exception:
        return None


# -----------------------------------------------------------------------
# نوارِ سلامتیِ باس
# -----------------------------------------------------------------------

class _FakeTargetNode:
    """نودِ ساختگی برای _FirstTargetActor. فقط position و
    handlemessage رو داره -- دقیقاً همون دو چیزی که بقیه‌ی کد
    (_safe_position، _attempt_attack، _freeze_target_actor) از رویِ
    node یک actor واقعی استفاده می‌کنن."""

    def __init__(self, position: tuple[float, float, float]) -> None:
        self.position = position

    def handlemessage(self, msg: Any) -> None:
        # فریز/ثاو روی این هدفِ ساختگی معنایی نداره؛ بی‌خطر نادیده
        # گرفته می‌شه.
        return None


class _FirstTargetActor:
    """یک «پلیرِ ساختگی» که دقیقاً روی BOSS_FIRST_SHOT_TARGET
    ایستاده. طبقِ درخواست، باس باید برای اولین هدف‌گیریِ بعدِ هر
    اسپاون، دقیقاً همون مسیرِ معمولیِ هدف‌گیری/قفل‌کردن/شلیک رو طی
    کنه -- انگار یک پلیرِ واقعی همون‌جا ایستاده -- نه یک مسیرِ
    جداگانه‌ی مصنوعی. برای همین یک شیء با همون شکلِ ظاهریِ یک actor
    (یعنی attribute یِ node با position) ساخته می‌شه و مستقیماً
    به‌عنوانِ self._current_target ست می‌شه؛ کدهای _attempt_attack،
    _animate (چشم‌ها/orientation)، _on_projectile_result و
    _freeze_target_actor بدونِ هیچ تغییری همون رفتارِ عادیِ
    هدف‌گیریِ یک پلیرِ واقعی رو روی این هدف اجرا می‌کنن، یعنی شلیکِ
    حاصل کاملاً عادی، مرئی، و انفجاریه."""

    def __init__(self, position: tuple[float, float, float]) -> None:
        self.node = _FakeTargetNode(position)

    def is_alive(self) -> bool:
        return True


class BossHealthBar:
    """یک نوارِ سلامتیِ همیشگی و روی صفحه برای باس."""

    def __init__(self, max_hp: int) -> None:
        self._max_hp = max_hp
        self._current_hp = max_hp

        self._bg_texture = bs.gettexture('bar')
        self._bar_texture = bs.gettexture('bar')

        self._bg_image = bs.NodeActor(bs.newnode(
            'image',
            attrs={
                'texture': self._bg_texture,
                'position': (0, 0),
                'scale': (500, 34),
                'opacity': 0.4,
                'color': (0.1, 0.1, 0.1),
                'attach': 'topCenter',
                'vr_depth': 0,
            },
        ))

        self._fg_image = bs.NodeActor(bs.newnode(
            'image',
            attrs={
                'texture': self._bar_texture,
                'position': (0, 0),
                'scale': (490, 26),
                'opacity': 0.95,
                'color': (0.85, 0.1, 0.1),
                'attach': 'topCenter',
                'vr_depth': 0,
            },
        ))

        self._title_text = bs.NodeActor(bs.newnode(
            'text',
            attrs={
                'text': 'BOSS',
                'h_align': 'center',
                'v_align': 'center',
                'position': (0, 26),
                'scale': 1.0,
                'color': (1, 1, 1, 1),
                'shadow': 1.0,
                'flatness': 1.0,
                'h_attach': 'center',
                'v_attach': 'top',
            },
        ))

        self._reposition(90)
        self.set_hp(max_hp, animate=False)

    def _reposition(self, top_offset: float) -> None:
        if self._bg_image.node:
            self._bg_image.node.position = (0, -top_offset)
        if self._fg_image.node:
            self._fg_image.node.position = (0, -top_offset)
        if self._title_text.node:
            self._title_text.node.position = (0, -top_offset + 26)

    def set_hp(self, hp: int, animate: bool = True) -> None:
        self._current_hp = max(0, min(self._max_hp, hp))
        fraction = self._current_hp / float(self._max_hp)
        width = max(0.0, 490.0 * fraction)

        if not self._fg_image.node:
            return

        if animate:
            bs.animate_array(
                self._fg_image.node, 'scale', 2,
                {0.0: (490, 34), 0.08: (width, 26)},
            )
        else:
            self._fg_image.node.scale = (width, 26)

        if fraction > 0.6:
            color = (0.85, 0.15, 0.15)
        elif fraction > 0.3:
            color = (0.9, 0.5, 0.05)
        else:
            color = (0.95, 0.85, 0.05)
        self._fg_image.node.color = color

    def set_phase(self, phase: int) -> None:
        """آپدیتِ عنوانِ نوارِ سلامتی به‌ازایِ فازِ فعلیِ خشم، به‌همراه
        یک فلاشِ کوچیکِ پس‌زمینه برایِ جلبِ توجه به این‌که سختی
        همین الان بیشتر شد."""
        titles = ('BOSS', 'BOSS \u2013 خشمگین', 'BOSS \u2013 در آستانه‌ی جنون')
        title_colors = (
            (1.0, 1.0, 1.0, 1.0),
            (1.0, 0.75, 0.3, 1.0),
            (1.0, 0.35, 0.2, 1.0),
        )
        if self._title_text.node:
            self._title_text.node.text = titles[phase]
            self._title_text.node.color = title_colors[phase]

        if self._bg_image.node and phase > 0:
            bs.animate_array(
                self._bg_image.node, 'color', 3,
                {0.0: (1.0, 0.25, 0.05), 0.2: (0.1, 0.1, 0.1)},
            )

    def hide(self) -> None:
        for actor in (self._bg_image, self._fg_image, self._title_text):
            if actor.node:
                actor.node.delete()


# -----------------------------------------------------------------------
# پرتابه‌ای که باس شلیک می‌کنه
# -----------------------------------------------------------------------

class BossProjectile:
    """یک مکعبِ کوچیکِ هدایت‌شونده که آروم و مداوم به سمتِ موقعیتِ
    فعلیِ هدف حرکت می‌کنه تا بهش برسه. اگه هدف از دست بره، از مپ
    خارج بشه، یا ظرفِ PROJECTILE_LIFETIME ثانیه به چیزی نخوره، خودش
    بی‌سروصدا حذف می‌شه (به‌جایِ رفتن به out-of-bounds که باعثِ
    اسپمِ پیام و فریزِ تردِ لاجیک می‌شد)."""

    def __init__(
        self,
        position: Sequence[float],
        direction: Sequence[float],
        owner_activity: bs.Activity,
        assets: dict[str, Any],
        target: Any = None,
        on_result: Any = None,
        speed_scale: float = 1.0,
        turn_rate_scale: float = 1.0,
        invisible: bool = False,
    ) -> None:
        self._invisible = invisible
        shared = SharedObjects.get()

        material = bs.Material()
        if self._invisible:
            # اولین شلیکِ نامرئی نباید اصلاً به پلیر بخوره یا
            # کسی رو منفجر کنه -- فقط بی‌سروصدا به سمتِ
            # BOSS_FIRST_SHOT_TARGET می‌ره و با تمام‌شدنِ عمرش
            # (یا برخورد به زمین/دیوار) بدونِ هیچ افکت/انفجاری
            # حذف می‌شه.
            material.add_actions(
                conditions=('they_have_material', shared.player_material),
                actions=('modify_part_collision', 'collide', False),
            )
        else:
            material.add_actions(
                conditions=('they_have_material', shared.player_material),
                actions=(
                    ('message', 'our_node', 'at_connect',
                     _ProjectileHitPlayerMessage()),
                    ('message', 'our_node', 'at_connect',
                     bs.DieMessage()),
                ),
            )
        # مهم: دیگه با برخورد به زمین/دیوار (footing_material) حذف
        # نمی‌شه. طبقِ درخواست، پرتابه فقط با خوردن به پلیر یا با
        # گذشتِ PROJECTILE_LIFETIME ثانیه (تایمرِ _force_expire)
        # از بین می‌ره -- نه با برخورد به هر چیزِ دیگه‌ای.
        material.add_actions(
            conditions=('they_have_material', shared.footing_material),
            actions=('modify_part_collision', 'collide', False),
        )

        # رفعِ باگِ «انگار خودِ باس بمب رو پرت نمی‌کنه»: تا قبل از
        # این، پرتابه باید با یک آفستِ نسبتاً بزرگ بیرونِ بدنِ باس
        # اسپاون می‌شد، وگرنه با بدنِ خودِ باس (که هم object_material
        # داره) برخوردِ فیزیکی می‌کرد و یک ایمپالسِ ناخواسته مسیرش رو
        # کج می‌کرد -- انگار همیشه فقط از یک زاویه‌ی ثابت بیرون
        # می‌زد. با این قانون، هرگونه پاسخِ فیزیکیِ برخورد با هر چیزی
        # که object_material داره (ازجمله خودِ بدنِ باس) از همون
        # اول کاملاً غیرفعاله؛ برخورد هنوز تشخیص داده می‌شه (اگه
        # لازم باشه)، ولی هیچ نیرو/ایمپالسی اعمال نمی‌شه. همین باعث
        # می‌شه بشه پرتابه رو خیلی نزدیک‌تر به بدنِ باس (رجوع به
        # PROJECTILE_SPAWN_OFFSET_MULT در _attempt_attack) اسپاون
        # کرد، بدونِ این‌که مسیرش کج بشه یا گیر کنه.
        material.add_actions(
            conditions=('they_have_material', shared.object_material),
            actions=('modify_part_collision', 'physical', False),
        )

        self._origin = tuple(position)
        self._die_time = bs.time() + PROJECTILE_LIFETIME
        self._direction = tuple(direction)
        self._target = target
        # سرعت/چرخشِ این پرتابه‌ی خاص می‌تونه بسته به فازِ خشمِ باس
        # (رجوع به BossActor._current_phase) از مقدارِ پایه‌ی
        # PROJECTILE_SPEED/PROJECTILE_TURN_RATE بیشتر باشه؛ این
        # مقیاس‌ها همون‌جا در لحظه‌ی شلیک محاسبه و پاس داده می‌شن.
        self._speed_scale = max(0.1, speed_scale)
        self._turn_rate_scale = max(0.1, turn_rate_scale)
        # مهم: این رفرنس جدا از self._target نگه داشته می‌شه. وقتی
        # clear_target صدا زده می‌شه (مثلاً چون هدف الان فریز شده)،
        # self._target خالی می‌شه (هدایت‌شوندگی قطع می‌شه)، ولی هنوز
        # باید نتیجه‌ی نهاییِ این پرتابه (خورد/نخورد) به همون
        # پلیرِ اصلی گزارش بشه.
        self._target_for_report = target
        self._on_result = on_result
        self._hit_reported = False
        self._dead = False
        self._update_timer: bs.Timer | None = None
        self._lifetime_timer: bs.Timer | None = None
        self._trail_timer: bs.Timer | None = None

        self.node = bs.newnode(
            'prop',
            delegate=self,
            attrs={
                'body': 'crate',
                'position': position,
                'mesh': None if self._invisible else assets['projectile_mesh'],
                'color_texture': (
                    None if self._invisible else assets['projectile_tex']
                ),
                'body_scale': PROJECTILE_SCALE,
                'mesh_scale': PROJECTILE_SCALE,
                'gravity_scale': 0.0,
                'density': 6.0,
                'reflection': 'powerup',
                'reflection_scale': [0.0 if self._invisible else 0.7],
                'shadow_size': 0.0 if self._invisible else 0.35,
                'materials': [material],
            },
        )

        speed = PROJECTILE_SPEED * self._speed_scale
        self.node.velocity = (
            self._direction[0] * speed,
            self._direction[1] * speed,
            self._direction[2] * speed,
        )

        self._light = None
        if not self._invisible:
            self._light = bs.newnode(
                'light',
                owner=self.node,
                attrs={
                    'position': position,
                    'color': (1.0, 0.25, 0.05),
                    'radius': 0.32,
                    'height_attenuated': False,
                },
            )
            bs.animate(
                self._light, 'intensity', {0.0: 0.7, 0.5: 1.1, 1.0: 0.7},
                loop=True,
            )

        if not self._invisible:
            self._trail_timer = bs.timer(
                0.09, bs.WeakCallStrict(self._emit_trail), repeat=True)

        self._update_timer = bs.timer(
            TICK_INTERVAL, bs.WeakCallStrict(self._update), repeat=True)

        # تایمرِ مستقلِ حذفِ اجباری: جدا از تایمرِ آپدیتِ هر تیک،
        # این یکی مستقلاً و فقط یک‌بار بعد از PROJECTILE_LIFETIME
        # ثانیه اجرا می‌شه و مکعب رو حذف می‌کنه، حتی اگه به هر
        # دلیلی تایمرِ آپدیتِ تیک‌به‌تیک متوقف شده باشه (مثلاً به
        # خاطرِ weak-ref شدنِ دلگیت). این تضمین می‌کنه هر مکعبی که
        # شلیک می‌شه دقیقاً ۵ ثانیه فرصت داره و بعدش قطعاً محو می‌شه.
        self._lifetime_timer = bs.timer(
            PROJECTILE_LIFETIME, bs.WeakCallStrict(self._force_expire),
            repeat=False)

    def _force_expire(self) -> None:
        if self._dead:
            return
        self.handlemessage(bs.DieMessage())

    def _emit_trail(self) -> None:
        if self._dead or not self.node:
            return
        pos = self.node.position
        bs.emitfx(
            position=pos,
            velocity=(0, 0.05, 0),
            count=2,
            scale=0.35,
            spread=0.15,
            chunk_type='spark',
        )

    def _update(self) -> None:
        if self._dead or not self.node:
            return
        if bs.time() >= self._die_time:
            self.handlemessage(bs.DieMessage())
            return

        pos = self.node.position

        # چکِ محدوده‌ی Y (ارتفاع): اگه پرتابه خیلی بالا یا خیلی
        # پایین‌تر از سطحِ اسپاون بره، قبل از این‌که موتور خودش
        # out-of-bounds بده، بی‌سروصدا حذفش می‌کنیم. این چک زودتر
        # از موتور اجرا می‌شه چون هر تیک (۳۰هرتز) اجرا می‌شه.
        if pos[1] < (self._origin[1] - 6.0) or pos[1] > (self._origin[1] + 10.0):
            self.handlemessage(bs.DieMessage())
            return

        # اگه از محدوده‌ی مجاز خارج شد (نسبت به نقطه‌ی شروع)، خودش
        # رو بی‌سروصدا حذف کن، قبل از این‌که موتور out-of-bounds بده.
        dist_from_origin = (
            (pos[0] - self._origin[0]) ** 2
            + (pos[1] - self._origin[1]) ** 2
            + (pos[2] - self._origin[2]) ** 2
        ) ** 0.5
        if dist_from_origin > PROJECTILE_MAX_RANGE:
            self.handlemessage(bs.DieMessage())
            return

        if self._light:
            self._light.position = pos

        target_pos = _safe_position(self._target)
        if target_pos is not None:
            dx = target_pos[0] - pos[0]
            dy = target_pos[1] - pos[1]
            dz = target_pos[2] - pos[2]
            length = max(0.0001, (dx * dx + dy * dy + dz * dz) ** 0.5)
            desired = (dx / length, dy / length, dz / length)

            blend = min(1.0, PROJECTILE_TURN_RATE * self._turn_rate_scale * TICK_INTERVAL)
            old = self._direction
            new_dir = (
                old[0] + (desired[0] - old[0]) * blend,
                old[1] + (desired[1] - old[1]) * blend,
                old[2] + (desired[2] - old[2]) * blend,
            )
            norm = max(0.0001, (
                new_dir[0] ** 2 + new_dir[1] ** 2 + new_dir[2] ** 2
            ) ** 0.5)
            self._direction = (
                new_dir[0] / norm, new_dir[1] / norm, new_dir[2] / norm,
            )

            # smooth speed blending to give projectile momentum
            try:
                cur_v = tuple(self.node.velocity)
                cur_speed = (cur_v[0] ** 2 + cur_v[1] ** 2 + cur_v[2] ** 2) ** 0.5
            except Exception:
                cur_speed = PROJECTILE_SPEED * self._speed_scale

            target_speed = PROJECTILE_SPEED * self._speed_scale
            new_speed = cur_speed + (target_speed - cur_speed) * PROJECTILE_SPEED_BLEND
            self.node.velocity = (
                self._direction[0] * new_speed,
                self._direction[1] * new_speed,
                self._direction[2] * new_speed,
            )

    def _report_result(self, hit: bool) -> None:
        """گزارشِ یک‌بارِ نتیجه‌ی نهاییِ این پرتابه (خورد/نخورد) به
        کالبکِ باس، اگه قبلاً گزارش نشده باشه."""
        if self._hit_reported:
            return
        self._hit_reported = True
        if self._on_result is not None:
            try:
                self._on_result(self._target_for_report, hit)
            except Exception:
                pass

    def _spawn_explosion(self) -> None:
        """طبقِ درخواست: برخوردِ پرتابه با پلیر باید یک انفجارِ
        واقعی بسازه (نه فقط یک مرگِ خشک). یک bascenev1lib.actor.
        bomb.Blast دقیقاً روی موقعیتِ فعلیِ پرتابه اسپاون می‌شه؛
        خودِ Blast طبقِ سیستمِ استانداردِ دمیجِ بازی به هر پلیرِ
        داخلِ شعاعش (نه فقط هدفِ اصلی) آسیب می‌زنه. source_player
        عمداً None می‌مونه چون این پرتابه از طرفِ خودِ باس شلیک
        می‌شه، نه یک پلیرِ خاص."""
        if not self.node:
            return
        try:
            pos = tuple(self.node.position)
        except Exception:
            return
        try:
            Blast(
                position=pos,
                velocity=(0.0, 0.0, 0.0),
                blast_radius=PROJECTILE_BLAST_RADIUS,
                blast_type='normal',
            ).autoretain()
        except Exception:
            pass

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, _ProjectileHitPlayerMessage):
            self._report_result(True)
            self._spawn_explosion()
            return None
        if isinstance(msg, bs.DieMessage):
            if self._dead:
                return None
            # اگه تا این‌جا هنوز نتیجه‌ای گزارش نشده (یعنی این مرگ
            # به‌خاطرِ برخوردِ واقعی با پلیر نبوده، بلکه تمام‌شدنِ
            # عمر/خروج از محدوده/OutOfBounds بوده)، یعنی این یک
            # miss بوده.
            self._report_result(False)
            self._dead = True
            # تلاش برای کنسل کردنِ تایمرها (درصورتی که قابلیت cancel
            # داشته باشن) تا بار اضافیِ تیک‌ها نداشته باشیم.
            for timer_attr in ('_update_timer', '_lifetime_timer', '_trail_timer'):
                timer = getattr(self, timer_attr, None)
                if timer is not None:
                    try:
                        timer.cancel()
                    except Exception:
                        pass
                    setattr(self, timer_attr, None)
            if self.node:
                pos = self.node.position
                if not self._invisible:
                    bs.emitfx(
                        position=pos,
                        velocity=(0, 0.6, 0),
                        count=8,
                        scale=0.6,
                        spread=0.5,
                        chunk_type='spark',
                    )
                self.node.delete()
            if self._light:
                self._light.delete()
            return None
        if isinstance(msg, bs.OutOfBoundsMessage):
            self.handlemessage(bs.DieMessage())
            return None
        return None

    def is_dead(self) -> bool:
        """برای اجازه‌دادن به BossActor که رفرنسِ پرتابه‌های مرده رو
        از لیستِ رفرنس‌های قوی حذف کنه."""
        return self._dead

    def clear_target(self) -> None:
        """توقفِ هدایت‌شوندگی: ارتباطِ پرتابه با هدفش رو قطع می‌کنه،
        بدونِ این‌که خودِ پرتابه رو حذف کنه. پرتابه با همون جهتِ
        فعلیِ حرکتش مستقیم ادامه می‌ده تا طبقِ عمرش
        (PROJECTILE_LIFETIME) خودش‌به‌خود حذف بشه. فعلاً جایی صدا
        زده نمی‌شه، ولی به‌عنوانِ یک قابلیتِ عمومی نگه داشته شده
        (مثلاً برای موردهایی که هدف باید ناگهان از تعقیب خارج بشه)."""
        self._target = None


# -----------------------------------------------------------------------
# کلاسِ BlackHole (عیناً پورت‌شده از bascenev1lib/actor/anomalies.py
# در پروژه‌ی HeyErfan/overclocked)
# -----------------------------------------------------------------------
# طبقِ درخواستِ صریح: این پایین دقیقاً همون کلاسِ BlackHole از
# https://github.com/HeyErfan/overclocked/blob/master/src/assets/
# ba_data/python/bascenev1lib/actor/anomalies.py هست -- بدونِ هیچ
# تغییری در منطق/رفتار/فرمولِ خودش. تنها تغییرات، صرفاً برایِ
# سازگاریِ importها با این پروژه بوده (نه تغییرِ رفتار):
#   ۱) `from era.utils import chasattr` در این پروژه وجود نداره؛
#      به‌جاش از تابعِ محلیِ chasattr (بالایِ همین فایل) که دقیقاً
#      همون رفتارِ hasattr-امن رو پیاده می‌کنه استفاده شده.
#   ۲) `from bauiv1 import SpecialChar, charstr` حذف شده، چون
#      خودِ کلاسِ BlackHole (برخلافِ Coin/Portal که در همون فایلِ
#      اصلی هستن) اصلاً از این دو استفاده نمی‌کنه.
#   ۳) PlayerSpaz/SpazBot از همون مسیرهای اصلیِ خودِ بازی
#      (bascenev1lib.actor.playerspaz/spazbot) بالایِ این فایل
#      ایمپورت شدن.
# بقیه‌ی کد -- از جمله نام‌گذاریِ متدها/پارامترها، فرمول‌های فیزیک،
# انیمیشن‌ها و صداها -- کلمه‌به‌کلمه همون نسخه‌ی اصلیه.
class BlackHole(bs.Actor):
    """A black hole that tries to consume and destroy all objects

    category: Gameplay Classes
    """

    def __init__(
        self,
        position: Sequence[float] = (0.0, 0.0, 0.0),
        source_player: bs.Player | None = None,
        radius: float = 10.0,
        xspeed: float = 1.0,
        ssize: float = 0.0,
    ):
        super().__init__()
        self._source_player = source_player

        shared = SharedObjects.get()

        dev_material = bs.Material()
        dev_material.add_actions(
            conditions=('they_have_material', shared.object_material),
            actions=('modify_part_collision', 'collide', True),
        )
        dev_material.add_actions(
            actions=(
                ('modify_part_collision', 'physical', False),
                ('call', 'at_connect', self.kill),
            )
        )

        self.node = bs.newnode(
            'region',
            delegate=self,
            attrs={
                'position': position,
                'scale': (0, 0, 0),
                'type': 'sphere',
                'materials': [dev_material],
            },
        )

        bs.animate_array(
            self.node,
            'scale',
            3,
            {
                0: (ssize, ssize, ssize),
                radius / xspeed: (radius / 10, radius / 10, radius / 10),
            },
        )

        un_material = bs.Material()
        un_material.add_actions(
            actions=('modify_part_collision', 'collide', False)
        )

        self.visual_node0 = bs.newnode(
            'prop',
            owner=self.node,
            attrs={
                'body': 'sphere',
                'mesh': bs.getmesh('shield'),
                'color_texture': bs.gettexture('black'),
                'shadow_size': 0,
                'reflection_scale': [0],
                'materials': [un_material],
                'gravity_scale': 0,
                'density': 0,
            },
        )
        self.visual_node0.is_area_of_interest = True

        mnode = bs.newnode(
            'math',
            owner=self.node,
            attrs={'input1': (0, 0.1, 0), 'operation': 'add'},
        )
        self.node.connectattr('position', mnode, 'input2')
        mnode.connectattr('output', self.visual_node0, 'position')

        bs.animate(
            self.visual_node0,
            'mesh_scale',
            {0: ssize, radius / xspeed: radius / 10},
        )

        self.visual_node1 = bs.newnode(
            'shield', owner=self.node, attrs={'color': (5, 5, 5)}
        )
        self.node.connectattr('position', self.visual_node1, 'position')
        bs.animate(
            self.visual_node1,
            'radius',
            {0: ssize * 2.1, radius / xspeed: radius / 10 * 2.1},
        )

        self._update_timer = bs.Timer(
            0.016666667, bs.WeakCallStrict(self._update), repeat=True
        )
        self._dtimer: bs.Timer | None = None

        self._skid_sound = bs.getsound('gravelSkid')
        self.snode = bs.newnode(
            'sound', owner=self.node, attrs={'sound': self._skid_sound}
        )
        bs.animate(self.snode, 'volume', {0: 0, radius / xspeed: radius / 5})

    def _update(self):
        for node in bs.getnodes():
            if (
                chasattr(node, 'materials')
                and chasattr(node, 'position')
                and SharedObjects.get().object_material in node.materials
                and not (chasattr(node, 'invincible') and node.invincible)
            ):
                drct = (
                    self.node.position[0] - node.position[0],
                    self.node.position[1] - node.position[1],
                    self.node.position[2] - node.position[2],
                )
                dstnc = math.sqrt(drct[0] ** 2 + drct[1] ** 2 + drct[2] ** 2)
                cradius = self.node.scale[0] * 10
                if dstnc != 0 and dstnc <= cradius:
                    nv = (drct[0] / dstnc, drct[1] / dstnc, drct[2] / dstnc)
                    node.handlemessage(
                        'impulse',
                        node.position[0],
                        node.position[1],
                        node.position[2],
                        nv[0],
                        nv[1],
                        nv[2],
                        cradius * 2,
                        0,
                        0,
                        0,
                        nv[0],
                        nv[1],
                        nv[2],
                    )

    def kill(self):
        node = bs.getcollision().opposingnode
        spaz = node.getdelegate(PlayerSpaz) or node.getdelegate(SpazBot)
        if spaz and (
            spaz.last_player_attacked_by in (None, spaz)
            or bs.time() - spaz.last_attacked_time >= 4
        ):
            spaz.last_attacked_time = bs.time()
            spaz.last_player_attacked_by = bs.existing(self._source_player)
            spaz.last_attacked_type = ('explosion', 'dev')

        light = bs.newnode(
            'light',
            attrs={
                'position': node.position,
                'height_attenuated': False,
                'color': (1, 0, 0),
                'intensity': 20,
            },
        )
        bs.animate(light, 'radius', {0: 0, 0.1: 0.1, 0.2: 0.1, 0.3: 0})
        bs.timer(0.3, light.delete)

        node.handlemessage(bs.DieMessage())

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.DieMessage):
            if self.node:
                if msg.immediate:
                    self.node.delete()
                else:
                    bs.animate(
                        self.visual_node0,
                        'mesh_scale',
                        {
                            0: self.visual_node0.mesh_scale,
                            0.1: 0,
                            0.2: 0.25,
                            0.3: 0.25,
                            0.4: 0,
                        },
                    )
                    bs.animate(
                        self.visual_node1,
                        'radius',
                        {
                            0: self.visual_node1.radius,
                            0.1: 0,
                            0.2: 0.5,
                            0.3: 0.5,
                            0.4: 0,
                        },
                    )
                    bs.animate(
                        self.snode, 'volume', {0: self.snode.volume, 0.1: 0}
                    )
                    bs.timer(0.4, self.last_breath)
                    bs.timer(0.4, self.node.delete)
                self._update_timer = None
        else:
            return super().handlemessage(msg)
        return None

    def last_breath(self):
        self._dtimer = bs.Timer(
            0.016666667,
            bs.CallStrict(
                bs.emitfx,
                self.node.position,
                count=100,
                spread=6,
                emit_type='distortion',
            ),
            repeat=True,
        )
        from bascenev1lib.actor.bomb import Blast

        Blast(
            position=self.node.position,
            blast_type='tnt',
            hit_subtype='tnt',
        ).autoretain()
        bs.timer(1, bs.CallStrict(self.__setattr__, '_dtimer', None))


# -----------------------------------------------------------------------
# خودِ باس
# -----------------------------------------------------------------------

class BossActor:
    """باسِ مکعبیِ بزرگ: سرِ جاش ثابت می‌مونه، فقط بالا/پایین شناور
    می‌شه، نزدیک‌ترین پلیر رو دنبال می‌کنه، و به‌طورِ دوره‌ای یک یا
    چند پرتابه‌ی هدایت‌شونده شلیک می‌کنه. فقط با برخوردِ مستقیمِ بمب
    آسیب می‌بینه. هرچی HP کمتر بشه، طبقِ سیستمِ خشم/rage (رجوع به
    _current_phase) تهاجمی‌تر و خطرناک‌تر می‌شه."""

    def __init__(
        self,
        activity: bs.Activity,
        position: Sequence[float],
        on_death: Any,
        assets: dict[str, Any],
        max_hp: int = BOSS_MAX_HP,
    ) -> None:
        # مهم (رفعِ باگِ کرشِ خروج از مپ): این‌جا باید فقط یک
        # weakref به activity نگه داشته بشه، نه یک رفرنسِ قوی.
        # BossActor خودش توسطِ self._boss در BossFight (که خودِ
        # activity هست) نگه داشته می‌شه؛ اگه BossActor هم برگرده و
        # یک رفرنسِ قویِ مستقیم به همون activity نگه داره، یک
        # چرخه‌ی رفرنسِ قوی درست می‌شه:
        #   BossFight -> self._boss -> BossActor -> self._activity -> BossFight
        # این چرخه باعث می‌شه رفرنس‌کانتِ activity هیچ‌وقت به صفر
        # نرسه، پس وقتی پلیر از مپ خارج می‌شه/راند تموم می‌شه و
        # موتور می‌خواد activity رو نابود کنه، activity (و درنتیجه
        # تمومِ اکتورهای وابسته بهش مثلِ Bomb/PowerupBox/Blast/
        # Player) هیچ‌وقت واقعاً نمی‌میرن -- دقیقاً همون ارورِ
        # «Activity is not dying when expected» و کرشِ نهاییِ گیم.
        self._activity_ref: weakref.ReferenceType[bs.Activity] = (
            weakref.ref(activity)
        )
        self._base_position = tuple(position)

        # رفعِ باگ: دیگه هیچ کوترنیونِ اصلاحیِ دستی محاسبه/نگه‌داری
        # نمی‌شه. دقیقاً مثلِ خودِ UFC_BSLIFE11.py (کلاسِ
        # CustomModel2، مدلِ 'bonesHead')، نودِ باس با orientation
        # پیش‌فرضِ موتور ساخته می‌شه و بعدش هیچ‌وقت دستی دست‌کاری
        # نمی‌شه؛ چون خودِ مشِ 'bonesHead' با همین orientation
        # پیش‌فرض از قبل رو به جلو دیده می‌شه.

        self._on_death_callback = on_death
        self._max_hp = max(1, max_hp)
        self._hp = self._max_hp
        self._dead = False
        self._spawn_time = bs.time()
        self._assets = assets
        self._attack_timer: bs.Timer | None = None
        self._regen_timer: bs.Timer | None = None
        self._vulnerable_until = 0.0
        self._last_damage_actor: Any = None
        self._last_damage_time = 0.0
        self._last_regen_notice_time = -999.0
        self._boss_damage_times: list[float] = []
        self._player_hit_times: list[float] = []
        self._last_attack_kind: str | None = None
        self._last_big_attack_time = -999.0
        self._shockwave_active_until = 0.0
        self._next_spooky_sound_time = (
            self._spawn_time + random.uniform(*BOSS_AMBIENT_SOUND_INTERVAL)
        )
        self._last_target_actor: Any = None
        self._target_repeat_count = 0

        shared = SharedObjects.get()

        # متریالِ خودِ باس: فقط برای اصطکاک با زمین.
        self._material = bs.Material()
        self._material.add_actions(
            conditions=('they_have_material', shared.footing_material),
            actions=('modify_part_collision', 'friction', 0.3),
        )

        # متریالِ دمیج: هر چیزی که object_material داره (بمب، جعبه،
        # پلیر...) وقتی به باس بخوره، یک پیامِ سبکِ _BombTouch به
        # باس می‌فرسته. داخلِ handlemessage، از رویِ bs.getcollision()
        # (دقیقاً همون روشی که خودِ گیم‌مودهای داخلیِ بازی مثلِ
        # Hockey برای تشخیصِ نوعِ برخورد استفاده می‌کنن) چک می‌شه که
        # طرفِ مقابل واقعاً یک Bomb زنده و منفجرنشده هست یا نه. اگه
        # بود، دمیج اعمال می‌شه و خودِ بمب هم بلافاصله محو می‌شه --
        # دیگه لازم نیست منتظرِ انفجار بمونیم.
        #
        # نکته‌ی حیاتی (علتِ واقعیِ چرخشِ کله): تا همین‌جا، برخوردِ
        # باس با هر چیزی که object_material داره (پلیر، بمب،
        # پاورآپ‌باکس، حتی پرتابه‌های خودش) یک برخوردِ کاملاً
        # فیزیکی بود -- یعنی موتور یک ایمپالسِ واقعی به بدنه‌ی
        # 'crate' یِ باس اعمال می‌کرد. چون این ایمپالس‌ها معمولاً از
        # مرکزِ جرمِ باس منحرف‌ان (نقطه‌ی برخورد وسطِ بدنه نیست)، یک
        # گشتاورِ چرخشی (torque) به بدنه وارد می‌شد -- دقیقاً همون
        # چیزی که کله رو می‌چرخوند، مخصوصاً وقتیِ جاذبه فعاله و
        # یک‌دفعه چندین شیء هم‌زمان بهش برخورد می‌کنن. صفرکردنِ
        # velocity/angular_velocity توی _animate هم نمی‌تونست کاملاً
        # جلوش رو بگیره چون گشتاور همون لحظه‌ی برخورد (بینِ دو تیکِ
        # اسکریپت) اعمال می‌شد.
        #
        # راه‌حل: با ('modify_part_collision', 'physical', False)
        # پاسخِ فیزیکیِ این برخورد رو کاملاً غیرفعال می‌کنیم -- یعنی
        # موتور همچنان تماس رو تشخیص می‌ده و پیامِ _BombTouchMessage
        # (برایِ دمیج) رو می‌فرسته، ولی دیگه هیچ نیرو/ایمپالس/گشتاوری
        # به بدنه‌ی باس اعمال نمی‌شه. نتیجه: هیچ‌چیزی -- نه پلیر، نه
        # بمب، نه پاورآپ‌باکس، نه در طولِ توانایی جاذبه -- دیگه
        # نمی‌تونه فیزیکی باس رو هل بده یا بچرخونه.
        self._bomb_contact_material = bs.Material()
        self._bomb_contact_material.add_actions(
            conditions=('they_have_material', shared.object_material),
            actions=(
                ('modify_part_collision', 'physical', False),
                ('message', 'our_node', 'at_connect', _BombTouchMessage()),
            ),
        )

        # رفعِ باگِ واقعیِ «کله رو به آسمونه»: تا همین‌جا از
        # body='puck' استفاده می‌شد، دقیقاً با این استدلال که puck
        # فیزیکاً یک دیسکِ صاف/افقیه و در pitch/roll قفل می‌مونه.
        # ولی خودِ همین قفل، علتِ اصلیِ باگ بود: چون puck همیشه
        # پیچ/رول رو به‌زور صاف/افقی نگه می‌داره، هر orientation ای
        # که دستی ست بشه بی‌فایده‌ست -- فیزیکِ خودِ موتور همیشه
        # کله رو به همون حالتِ افقی (که این‌جا یعنی رو به آسمون)
        # برمی‌گردونه (تست شد: با ۱۲ زاویه‌ی مختلف هیچ تغییری دیده
        # نشد، چون اصلاً به orientation دستی توجه نمی‌شه).
        #
        # برای همین از 'crate' استفاده می‌کنیم -- بدنه‌ای که در هر
        # سه محور آزاده و orientation دستی رو واقعاً اعمال می‌کنه.
        # نگرانیِ قبلی («crate ممکنه با برخورد تاب بخوره») دیگه
        # موضوعیت نداره، چون بالاتر با
        # ('modify_part_collision', 'physical', False) پاسخِ
        # فیزیکیِ هر برخوردی (بمب/پلیر/پاورآپ‌باکس) از قبل کاملاً
        # غیرفعال شده -- یعنی اصلاً هیچ نیرو/گشتاوری به بدنه اعمال
        # نمی‌شه که بخواد بچرخوندش. صفرکردنِ velocity/angular_velocity
        # در _animate هم به‌عنوانِ یک لایه‌ی اطمینانِ اضافی نگه
        # داشته می‌شه.
        self.node = bs.newnode(
            'prop',
            delegate=self,
            attrs={
                'body': 'crate',
                'position': (
                    self._base_position[0],
                    self._base_position[1] + BOSS_SPAWN_HEIGHT,
                    self._base_position[2],
                ),
                'mesh': assets['boss_mesh'],
                'color_texture': assets['boss_tex'],
                'body_scale': BOSS_BODY_SCALE,
                'mesh_scale': BOSS_MESH_SCALE,
                'gravity_scale': 0.0,
                'density': 8.0,
                'reflection': 'powerup',
                'reflection_scale': [0.6],
                'shadow_size': 1.2,
                'materials': [
                    shared.object_material, self._material,
                    self._bomb_contact_material,
                ],
            },
        )

        # دیگه هیچ حالتِ تستی/چرخنده‌ای در کار نیست: نود با
        # orientation پیش‌فرضِ ثابتِ موتور ساخته می‌شه و دیگه هیچ‌جا
        # (نه این‌جا، نه در _animate) دستی دست‌کاری نمی‌شه، پس
        # همیشه دقیقاً همون‌جوری که ساخته شده ثابت می‌مونه و
        # هیچ‌وقت تغییر نمی‌کنه.

        # افکتِ اسپاون: ترکیبی از جرقه، دود و یک فلاشِ نوریِ کوتاه
        # برای حسِ ورودِ دراماتیک‌تر.
        bs.emitfx(
            position=self.node.position,
            velocity=(0, 2.0, 0),
            count=28,
            scale=1.3,
            spread=1.1,
            chunk_type='spark',
        )
        bs.emitfx(
            position=self.node.position,
            velocity=(0, 0.6, 0),
            count=14,
            scale=1.6,
            spread=0.9,
            chunk_type='spark',
        )
        _play_boss_sound_burst(
            BOSS_SOUND_SPAWN,
            count=3,
            spacing=0.16,
            volume=1.25,
            position=self.node.position,
        )

        spawn_flash = bs.newnode(
            'light',
            attrs={
                'position': self.node.position,
                'color': (1.0, 0.2, 0.05),
                'radius': 1.4,
                'height_attenuated': False,
            },
        )
        bs.animate(spawn_flash, 'intensity', {0.0: 3.0, 0.5: 0.0})
        bs.timer(0.6, spawn_flash.delete)

        self._glow_light = bs.newnode(
            'light',
            owner=self.node,
            attrs={
                'position': self.node.position,
                'color': (1.0, 0.05, 0.05),
                'radius': 0.55,
                'height_attenuated': False,
            },
        )
        bs.animate(
            self._glow_light, 'intensity',
            {0.0: 0.4, 0.9: 0.9, 1.8: 0.4}, loop=True,
        )

        # چشم‌های قرمز: هرکدوم از دو تا locator صافِ قرمزِ additive
        # (دقیقاً همون تکنیکِ رنگِ (120,0,0) که توی نقشه‌ی UFC_BSLIFE
        # برای چشمِ جمجمه استفاده شده بود، تا خودِ رنگِ سطحِ چشم واقعاً
        # قرمز دیده بشه، نه فقط یک نورِ اطراف) + یک لایتِ کوچیکِ همراه
        # برای درخشش تشکیل شده.
        #
        # موقعیتِ دقیقِ این دو چشم نسبت به مرکزِ باس، از رویِ ثابت‌های
        # قابلِ‌تنظیمِ BOSS_EYE_GAP/OFFSET_Y/OFFSET_Z و BOSS_EYE_SHIFT_X
        # (بالایِ فایل) ساخته می‌شه. اگه چشم‌ها دقیقاً وسطِ حفره‌ی
        # چشمِ مش ننشستن، همون ثابت‌ها رو عوض کن -- نیازی به تغییرِ
        # این‌جا نیست.
        local_eye_offset_x = BOSS_EYE_OFFSET_X * BOSS_MESH_SCALE
        local_eye_offset_y = BOSS_EYE_OFFSET_Y * BOSS_MESH_SCALE
        local_eye_offset_z = BOSS_EYE_OFFSET_Z * BOSS_MESH_SCALE
        eye_shift_x = BOSS_EYE_SHIFT_X * BOSS_MESH_SCALE
        right_eye_lift = BOSS_EYE_RIGHT_LIFT * BOSS_MESH_SCALE
        self._local_eye_offsets = (
            (local_eye_offset_x + eye_shift_x, local_eye_offset_y, local_eye_offset_z),
            (-local_eye_offset_x + eye_shift_x, local_eye_offset_y + right_eye_lift, local_eye_offset_z),
        )
        eye_size = BOSS_EYE_SIZE * BOSS_MESH_SCALE
        self._eye_locators = [
            bs.newnode(
                'locator',
                owner=self.node,
                attrs={
                    'shape': 'circle',
                    'position': self.node.position,
                    'color': (3.0, 0.0, 0.0),
                    'opacity': 1.0,
                    'draw_beauty': True,
                    'additive': True,
                    'size': [eye_size],
                },
            )
            for _ in self._local_eye_offsets
        ]
        self._eye_lights = [
            bs.newnode(
                'light',
                owner=self.node,
                attrs={
                    'position': self.node.position,
                    'color': (1.2, 0.0, 0.0),
                    'radius': 0.09,
                    'height_attenuated': False,
                },
            )
            for _ in self._local_eye_offsets
        ]
        for eye_light in self._eye_lights:
            bs.animate(
                eye_light, 'intensity',
                {0.0: 0.15, 1.0: 0.65, 2.0: 0.15}, loop=True,
            )

        # حرکتِ کوچیکِ خودِ چشم‌ها داخلِ حفره: علاوه بر این‌که چشم‌ها با
        # یک جابه‌جاییِ محدود (BOSS_EYE_MOVE_RADIUS، در _animate) به
        # سمتِ هدف کمی شیفت می‌کنن، یک لرزشِ خیلی ریزِ اضافی هم به
        # موقعیتِ محلیِ هرکدوم اضافه می‌شه (max_local_shift) تا حسِ
        # «تکون‌خوردنِ مردمکِ چشم داخلِ حفره» رو بده -- بدونِ این‌که
        # هیچ‌وقت از حفره بیرون بزنه یا دورِ کله بچرخه.
        self._eye_jitter_phase = random.uniform(0.0, 2.0 * math.pi)

        self._health_bar = BossHealthBar(self._max_hp)

        # افکتِ آتشِ قرمزِ دائمی روی بدنه‌ی باس: طبقِ کدِ درخواست‌شده،
        # یک نورِ قرمز/نارنجیِ چشمک‌زن (Firelight) به بدنه‌ی باس
        # وصل می‌شه و هر ۰.۱ ثانیه یک دسته ذره‌ی 'sweat' (که با
        # velocity رو به بالا، حسِ شعله/جرقه‌ی بالارونده می‌ده) از
        # روی باس ساطع می‌شه. رجوعِ کاملِ منطق به self._start_fire_fx.
        self._start_fire_fx()

        # طبقِ درخواست: اولین هدفی که باس (قبل از این‌که هنوز
        # _scan_for_target واقعی اجرا بشه) قفل می‌کنه، نه None
        # بلکه یک «پلیرِ ساختگی» دقیقاً روی BOSS_FIRST_SHOT_TARGET
        # هست. با اولین اجرایِ _scan_for_target (طبقِ
        # BOSS_TARGET_SCAN_INTERVAL)، این خودبه‌خود با نزدیک‌ترین
        # پلیرِ واقعی جایگزین می‌شه؛ ولی اگه فاصله‌ی حمله کوتاه‌تر
        # از اسکنِ اول باشه، همین هدفِ ساختگی برای اولین شلیک
        # استفاده می‌شه -- دقیقاً مثلِ یک پلیرِ واقعی که همون‌جا
        # ایستاده.
        self._current_target: Any = _FirstTargetActor(BOSS_FIRST_SHOT_TARGET)
        # نگه‌داشتنِ رفرنسِ قویِ پایتون به هر پرتابه‌ی زنده. بدونِ
        # این لیست، به‌محضِ خروج از تابعِ _attempt_attack هیچ رفرنسِ
        # قوی‌ای به آبجکتِ BossProjectile باقی نمی‌مونه، پایتون
        # سریعاً garbage-collect ش می‌کنه، تایمرهاش (که با
        # WeakCallStrict ثبت شدن) دیگه هیچ‌وقت اجرا نمی‌شن، و نودِ
        # prop یِ خودِ موتور (که مستقل از پایتونه) برای همیشه بدونِ
        # هیچ منطقی شناور می‌مونه و مدام out-of-bounds می‌ده.
        self._live_projectiles: list[BossProjectile] = []
        self._live_blackholes: list[BlackHole] = []

        # ردیابیِ شلیک‌های ناموفق (miss) به هر پلیر، به‌طورِ جداگانه.
        # کلیدِ این دیکشنری‌ها خودِ اکتور (actor) پلیره -- دقیقاً
        # همون شیءای که self._current_target هم ازش استفاده می‌کنه.
        # وقتی یک پلیرِ خاص بینِ ۳ تا ۵ بار (رندوم، هر بار جداگانه
        # برای هر پلیر انتخاب می‌شه) پرتابه بهش شلیک بشه و نخوره،
        # فریزش می‌کنیم؛ در حالتِ فریز، هر برخوردِ بعدیِ پرتابه
        # (طبقِ سیستمِ موجود) باعثِ انفجار و آسیب‌دیدنِ اونه.
        self._miss_streak: dict[Any, int] = {}
        self._miss_threshold: dict[Any, int] = {}
        self._frozen_actors: set[Any] = set()
        self._warned_actors: set[Any] = set()

        # فازِ فعلیِ خشم (۰ = نرمال، ۱ = خشمگین، ۲ = در آستانه‌ی
        # جنون)؛ هر بار که با ضربه‌ی بمب عوض بشه، _on_phase_changed
        # صدا زده می‌شه تا افکت/رنگ/سرعتِ حمله آپدیت بشه.
        self._phase: int = 0

        self._anim_timer = bs.timer(
            TICK_INTERVAL, bs.WeakCallStrict(self._animate), repeat=True)
        self._ambient_fx_timer = bs.timer(
            BOSS_AMBIENT_FX_INTERVAL,
            bs.WeakCallStrict(self._emit_ambient_fx), repeat=True)
        self._target_scan_timer = bs.timer(
            BOSS_TARGET_SCAN_INTERVAL,
            bs.WeakCallStrict(self._scan_for_target), repeat=True)
        self._regen_timer = bs.timer(
            BOSS_REGEN_INTERVAL,
            bs.WeakCallStrict(self._regen_tick),
            repeat=True,
        )

        # برخلافِ قبل، دیگه یک تایمرِ تکرارشونده با فاصله‌ی ثابت
        # نیستیم؛ چون فاصله‌ی حمله باید هر فاز عوض بشه (رجوع به
        # BOSS_ATTACK_INTERVAL_PHASE)، از یک تایمرِ یک‌باره‌ی
        # خودزمان‌بندی‌کن استفاده می‌کنیم که بعدِ هر شلیک، فاصله‌ی
        # بعدی رو از رویِ فازِ فعلی دوباره محاسبه می‌کنه.
        self._schedule_next_attack()

    @property
    def _activity(self) -> bs.Activity | None:
        """دسترسیِ امن به activity از رویِ weakref. اگه activity
        از قبل مرده باشه (weakref مرده)، None برمی‌گرده -- کدهایی
        مثلِ _scan_for_target که از self._activity.players استفاده
        می‌کنن خودشون از قبل توسطِ چکِ `self._dead or not self.node`
        محافظت می‌شن، ولی برای اطمینانِ بیشتر این‌جا هم None
        برگردوندنِ صریح باعثِ کرش نمی‌شه چون همیشه قبل از استفاده
        بررسیِ حیاتِ باس/نود انجام می‌شه."""
        return self._activity_ref()

    # -- انیمیشن ---------------------------------------------------

    def _animate(self) -> None:
        if self._dead or not self.node:
            return
        t = bs.time() - self._spawn_time

        # هرچی باس خشمگین‌تر باشه (فازِ بالاتر)، شناوریِ بالا/پایینش
        # هم تندتر و پرتحرک‌تره -- یک نشونه‌ی بصریِ ساده و همیشگی از
        # این‌که باس داره جری‌تر می‌شه، جدا از رنگِ چشم‌ها و نوارِ HP.
        rage_phase = self._current_phase()
        float_period = BOSS_FLOAT_PERIOD / (1.0 + rage_phase * 0.35)
        float_amplitude = BOSS_FLOAT_AMPLITUDE * (1.0 + rage_phase * 0.2)

        float_phase = (t % float_period) / float_period
        float_offset = math.sin(float_phase * 2.0 * math.pi) * float_amplitude
        base_y = self._base_position[1] + BOSS_SPAWN_HEIGHT

        self.node.position = (
            self._base_position[0],
            base_y + float_offset,
            self._base_position[2],
        )
        self.node.velocity = (0.0, 0.0, 0.0)
        # زدنِ صفر روی angular_velocity هر تیک: یک لایه‌ی اطمینانِ
        # اضافیه که جلوی هرگونه spin احتمالیِ باقی‌مونده رو می‌گیره.
        try:
            self.node.angular_velocity = (0.0, 0.0, 0.0)
        except Exception:
            pass
        # دیگه هیچ orientation ای دستی این‌جا ست نمی‌شه -- دقیقاً
        # مثلِ UFC، نود از همون orientation پیش‌فرضِ اولیه‌ش دست‌نخورده
        # می‌مونه.

        if self._glow_light:
            self._glow_light.position = self.node.position

        boss_pos = self.node.position
        target_pos = None
        if self._actor_is_alive(self._current_target):
            target_pos = _safe_position(self._current_target)
        if target_pos is None:
            self._scan_for_target()
            target_pos = _safe_position(self._current_target)

        # نکته‌ی مهم: کله هیچ‌وقت نمی‌چرخه (رجوع به کامنتِ بالای
        # __init__)، پس خودِ مشِ کله همیشه دقیقاً با همون جهتِ اولیه
        # رندر می‌شه -- نه با فیزیک، نه با کدِ این‌جا. آفستِ محلیِ
        # چشم‌ها هم عمداً با هیچ کوترنیونی چرخونده نمی‌شه (چرخوندنِ
        # چشم‌ها دورِ کله، درحالی‌که خودِ کله ثابت مونده، حسِ بدی
        # می‌ده). موقعیتِ
        # پایه‌ی هر چشم دقیقاً boss_pos + BOSS_EYE_OFFSET_X/Y/Z (ثابت
        # و قابل‌تنظیم، بالایِ فایل) هست، و فقط یک جابه‌جاییِ خیلی
        # کوچیک و محدود (در حدِ BOSS_EYE_MOVE_RADIUS) به سمتِ هدف
        # بهش اضافه می‌شه تا حسِ «نگاه‌کردن» بده، بدونِ این‌که چشم از
        # حفره‌ی خودش بیرون بزنه یا دورِ کله بچرخه.
        if getattr(self, '_eye_locators', None) or getattr(
            self, '_eye_lights', None
        ):
            move_radius = BOSS_EYE_MOVE_RADIUS * BOSS_MESH_SCALE
            look_x, look_y = 0.0, 0.0
            if target_pos is not None:
                ddx = target_pos[0] - boss_pos[0]
                ddy = target_pos[1] - boss_pos[1]
                ddz = target_pos[2] - boss_pos[2]
                full_len = max(
                    0.0001,
                    math.sqrt(ddx * ddx + ddy * ddy + ddz * ddz),
                )
                # فقط مولفه‌ی افقی (چپ/راست) و عمودی (بالا/پایین) رو
                # به‌عنوانِ یک جابه‌جاییِ کوچیک اعمال می‌کنیم؛ مولفه‌ی
                # عمق (z) دست‌نخورده می‌مونه چون چشم نباید تویِ کله
                # فرو بره یا از صورت بیرون بزنه.
                look_x = (ddx / full_len) * move_radius
                look_y = (ddy / full_len) * move_radius

            # لرزشِ خیلی ریزِ اضافی: یک نوسانِ کوچیک که به جابه‌جاییِ
            # بالا اضافه می‌شه تا حسِ «تکون‌خوردنِ مردمکِ چشم داخلِ
            # حفره» رو بده؛ اندازه‌ش نسبت به BOSS_EYE_MOVE_RADIUS
            # مقیاس می‌شه تا هیچ‌وقت از حفره بیرون نزنه.
            max_local_shift = 0.18 * move_radius
            jitter_x = math.sin(
                t * 1.7 + self._eye_jitter_phase
            ) * max_local_shift
            jitter_y = math.sin(
                t * 1.3 + self._eye_jitter_phase * 1.4
            ) * max_local_shift * 0.6

            for i, local_offset in enumerate(self._local_eye_offsets):
                lx, ly, lz = local_offset
                world_pos = (
                    boss_pos[0] + lx + look_x + jitter_x,
                    boss_pos[1] + ly + look_y + jitter_y,
                    boss_pos[2] + lz,
                )
                if i < len(self._eye_locators) and self._eye_locators[i]:
                    self._eye_locators[i].position = world_pos
                if i < len(self._eye_lights) and self._eye_lights[i]:
                    self._eye_lights[i].position = world_pos

    def _emit_ambient_fx(self) -> None:
        if self._dead or not self.node:
            return
        pos = self.node.position
        bs.emitfx(
            position=(pos[0], pos[1] - 0.4, pos[2]),
            velocity=(random.uniform(-0.3, 0.3), 0.5,
                      random.uniform(-0.3, 0.3)),
            count=5,
            scale=0.9,
            spread=0.4,
            chunk_type='spark',
        )
        bs.emitfx(
            position=(pos[0], pos[1] - 0.2, pos[2]),
            velocity=(random.uniform(-0.15, 0.15), 0.3,
                      random.uniform(-0.15, 0.15)),
            count=2,
            scale=1.1,
            spread=0.25,
            chunk_type='spark',
        )
        now = bs.time()
        if now >= self._next_spooky_sound_time:
            _play_boss_sound_burst(
                BOSS_SOUND_AMBIENT,
                count=random.choice((1, 2)),
                spacing=0.18,
                volume=0.95,
                position=pos,
            )
            low, high = BOSS_AMBIENT_SOUND_INTERVAL
            phase = self._current_phase()
            self._next_spooky_sound_time = now + max(
                5.0, random.uniform(low, high) - phase * 1.2
            )

    # -- افکتِ آتشِ قرمز ----------------------------------------------
    # این دو متد دقیقاً همون منطقِ کدِ درخواست‌شده رو پیاده می‌کنن:
    # یک نودِ 'light' قرمز/نارنجیِ چشمک‌زن که با connectattr به
    # موقعیتِ باس وصل می‌شه و رنگش با یک الگویِ نوسانی (prefixAnim)
    # پیوسته انیمیت می‌شه، به‌علاوه‌ی یک تایمرِ تکرارشونده‌ی ۰.۱
    # ثانیه‌ای که هر بار یک دسته ذره‌ی 'sweat' (با سرعتِ روبه‌بالا)
    # از روی باس ساطع می‌کنه. تنها تفاوت با کدِ اصلی این‌ست که همه‌
    # چیز درونِ self نگه داشته می‌شه (نه یک آبجکتِ actor بیرونی) و
    # تایمرها با bs.WeakCallStrict ثبت می‌شن، دقیقاً طبقِ همون الگویی
    # که بقیه‌ی تایمرهای BossActor (مثلِ _anim_timer/_ambient_fx_timer)
    # در این فایل استفاده می‌کنن -- تا نه رفرنسِ چرخه‌ای بسازه و نه
    # با مرگِ باس بی‌سروصدا برای همیشه روشن بمونه.
    def _start_fire_fx(self) -> None:
        if not self.node:
            return

        self._fire_light = bs.newnode(
            'light',
            owner=self.node,
            attrs={
                'position': self.node.position,
                'color': (2.1, 0.6, 0),
                'radius': 0.3,
                'volume_intensity_scale': 15.0,
            },
        )

        prefix_anim = {
            0: (2.2, 1.0, 0),
            0.040: (2.3, 1.1, 0.1),
            0.080: (2.4, 1.2, 0.2),
            0.120: (2.5, 1.3, 0.3),
            0.160: (2.5, 1.4, 0.4),
            0.200: (2.6, 1.5, 0.5),
            0.240: (2.6, 1.6, 0.6),
            0.280: (2.5, 1.5, 0.5),
            0.320: (2.4, 1.4, 0.4),
            0.360: (2.3, 1.3, 0.3),
            0.400: (2.2, 1.2, 0.2),
            0.440: (2.2, 1.1, 0.1),
            0.480: (2.2, 1.0, 0),
        }
        bs.animate_array(self._fire_light, 'color', 3, prefix_anim, loop=True)
        bs.animate(
            self._fire_light, 'intensity',
            {0: 0.8, 0.200: 0.4, 0.400: 0.8}, loop=True,
        )
        self.node.connectattr('position', self._fire_light, 'position')

        self._fire_timer = bs.timer(
            0.100, bs.WeakCallStrict(self._emit_fire_particles), repeat=True)

    def _emit_fire_particles(self) -> None:
        if self._dead or not self.node:
            self._fire_timer = None
            return
        pos = self.node.position
        bs.emitfx(
            position=(pos[0], pos[1] + 0.3, pos[2]),
            velocity=(0, 1.5, 0),
            count=5,
            spread=0.3,
            scale=4.0,
            chunk_type='sweat',
        )

    # -- هوشِ مصنوعی / هدف‌گیری --------------------------------------

    def _current_phase(self) -> int:
        """فازِ فعلیِ خشمِ باس (۰/۱/۲) صرفاً بر اساسِ درصدِ HP فعلی.
        این تابع منبعِ حقیقتِ کلِ سیستمِ سختیِ پویاست: فاصله‌ی حمله،
        سرعتِ پرتابه، تعدادِ شلیک، و آستانه‌ی فریزکردن همه از همین
        یک مقدار مشتق می‌شن، پس همیشه هماهنگ با هم می‌مونن."""
        frac = self._hp / float(self._max_hp)
        if frac <= BOSS_RAGE_PHASE3_HP_FRACTION:
            return 2
        if frac <= BOSS_RAGE_PHASE2_HP_FRACTION:
            return 1
        return 0

    @staticmethod
    def _rotate_direction_y(
        direction: tuple[float, float, float], degrees: float
    ) -> tuple[float, float, float]:
        """چرخوندنِ یک بردارِ جهتِ واحد به اندازه‌ی `degrees` دورِ
        محورِ عمودی (Y). برای بازکردنِ زاویه‌ی چندتا پرتابه‌ی هم‌زمان
        در فازِ خشمِ باس استفاده می‌شه، تا پرتابه‌ها دقیقاً روی هم
        شلیک نشن."""
        rad = math.radians(degrees)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        x, y, z = direction
        return (x * cos_a - z * sin_a, y, x * sin_a + z * cos_a)

    @staticmethod
    def _actor_is_alive(actor: Any) -> bool:
        try:
            return bool(actor and actor.node and actor.is_alive())
        except Exception:
            try:
                return bool(actor and actor.node)
            except Exception:
                return False

    def _set_eye_alert(self, duration: float = 0.45) -> None:
        if self._dead:
            return
        for eye_light in getattr(self, '_eye_lights', []):
            if eye_light:
                try:
                    bs.animate(
                        eye_light, 'intensity',
                        {0.0: 1.8, duration: 0.65},
                    )
                except Exception:
                    pass
        for eye_locator in getattr(self, '_eye_locators', []):
            if eye_locator:
                try:
                    bs.animate_array(
                        eye_locator, 'color', 3,
                        {
                            0.0: (5.0, 1.0, 0.2),
                            duration: BOSS_PHASE_EYE_LOCATOR_COLOR[self._phase],
                        },
                    )
                except Exception:
                    pass

    def _trim_director_memory(self) -> None:
        now = bs.time()
        self._boss_damage_times = [
            t for t in self._boss_damage_times
            if now - t <= BOSS_DIRECTOR_MEMORY
        ]
        self._player_hit_times = [
            t for t in self._player_hit_times
            if now - t <= BOSS_DIRECTOR_HIT_MEMORY
        ]
        self._live_projectiles = [
            p for p in self._live_projectiles if not p.is_dead()
        ]
        self._live_blackholes = [
            h for h in self._live_blackholes if getattr(h, 'node', None)
        ]

    def _living_player_actors(self) -> list[Any]:
        activity = self._activity
        if activity is None:
            return []
        actors: list[Any] = []
        try:
            players = list(activity.players)
        except Exception:
            return actors
        for player in players:
            try:
                if player.is_alive() and player.actor and player.actor.node:
                    actors.append(player.actor)
            except Exception:
                continue
        return actors

    def _active_threat_score(self) -> int:
        self._trim_director_memory()
        score = len(self._live_projectiles)
        score += 3 * len(self._live_blackholes)
        if bs.time() < self._shockwave_active_until:
            score += 2
        return score

    def _director_snapshot(self) -> dict[str, Any]:
        now = bs.time()
        actors = self._living_player_actors()
        last_damage_time = max(self._last_damage_time, self._spawn_time)
        threat = self._active_threat_score()
        recent_boss_damage = len(self._boss_damage_times)
        recent_player_hits = len(self._player_hit_times)
        no_damage_time = now - last_damage_time
        mode = 'normal'
        if (
            len(actors) <= 1
            or recent_player_hits >= 2
            or threat >= BOSS_THREAT_LIMIT
            or no_damage_time >= BOSS_DIRECTOR_NO_DAMAGE_MERCY_TIME
        ):
            mode = 'mercy'
        elif (
            len(actors) >= 2
            and recent_boss_damage >= 3
            and recent_player_hits == 0
            and threat <= 1
        ):
            mode = 'pressure'
        return {
            'actors': actors,
            'living_players': len(actors),
            'threat': threat,
            'recent_boss_damage': recent_boss_damage,
            'recent_player_hits': recent_player_hits,
            'no_damage_time': no_damage_time,
            'mode': mode,
        }

    @staticmethod
    def _weighted_choice(weighted: list[tuple[str, float]]) -> str:
        total = sum(max(0.0, weight) for _, weight in weighted)
        if total <= 0.0:
            return 'homing'
        pick = random.uniform(0.0, total)
        upto = 0.0
        for name, weight in weighted:
            upto += max(0.0, weight)
            if pick <= upto:
                return name
        return weighted[-1][0]

    def _choose_attack(self, target_actor: Any) -> str:
        snap = self._director_snapshot()
        mode = snap['mode']
        phase = self._current_phase()
        threat = snap['threat']
        now = bs.time()
        big_ready = now - self._last_big_attack_time >= BOSS_BIG_ATTACK_COOLDOWN

        # When the scene is already busy, the boss should calm the fight down.
        if threat >= BOSS_THREAT_LIMIT:
            return 'breather' if random.random() < 0.55 else 'homing'

        weighted: list[tuple[str, float]]
        if mode == 'mercy':
            weighted = [
                ('breather', 2.8),
                ('warning_homing', 2.4),
                ('homing', 2.2),
                ('fake_telegraph', 0.45),
            ]
            if phase >= 1 and big_ready and threat <= 0:
                weighted.append(('gap_shockwave', 0.35))
        elif mode == 'pressure':
            weighted = [
                ('focus_shot', 2.6),
                ('homing', 2.0),
                ('warning_homing', 0.9),
                ('burst', 0.8 + phase * 0.25),
            ]
            if big_ready and threat <= 1:
                weighted.append(('gap_shockwave', 0.7 + phase * 0.25))
            if phase >= 2 and big_ready and threat <= 0:
                weighted.append(('mini_blackhole', 0.25))
        else:
            weighted = [
                ('homing', 2.4),
                ('warning_homing', 1.2),
                ('focus_shot', 0.7),
                ('fake_telegraph', 0.25),
            ]
            if phase >= 1 and threat <= 1:
                weighted.append(('burst', 0.65))
            if big_ready and threat <= 1:
                weighted.append(('gap_shockwave', 0.55 + phase * 0.15))
            if phase >= 2 and big_ready and threat <= 0:
                weighted.append(('mini_blackhole', 0.18))

        if self._last_attack_kind is not None:
            weighted = [
                (name, weight * (0.35 if name == self._last_attack_kind else 1.0))
                for name, weight in weighted
            ]

        attack_kind = self._weighted_choice(weighted)
        cost = BOSS_ATTACK_THREAT_COST.get(attack_kind, 1)
        if threat + cost > BOSS_THREAT_LIMIT:
            attack_kind = 'breather' if mode == 'mercy' else 'homing'
        if (
            attack_kind in {'gap_shockwave', 'shockwave', 'mini_blackhole'}
            and not big_ready
        ):
            attack_kind = 'homing'
        if self._last_target_actor is target_actor:
            self._target_repeat_count += 1
        else:
            self._target_repeat_count = 0
            self._last_target_actor = target_actor
        if self._target_repeat_count >= 2 and attack_kind in {
            'focus_shot', 'burst', 'mini_blackhole'
        }:
            attack_kind = 'warning_homing'
        return attack_kind

    def _schedule_next_attack(self) -> None:
        """فاصله‌ی حمله‌ی بعدی رو از رویِ فازِ فعلی دوباره محاسبه
        می‌کنه و یک تایمرِ یک‌باره می‌سازه. این‌طوری هرچی HP باس
        کمتر بشه، بدونِ نیاز به لغو/بازسازیِ یک تایمرِ تکرارشونده،
        شلیک‌ها خودبه‌خود تندتر می‌شن."""
        if self._dead or not self.node:
            return
        # لغو تایمر قبلی اگر وجود داشته باشد
        if self._attack_timer is not None:
            try:
                self._attack_timer.cancel()
            except Exception:
                pass
            self._attack_timer = None
        interval = BOSS_ATTACK_INTERVAL_PHASE[self._current_phase()]
        snap = self._director_snapshot()
        living_players = snap['living_players']
        if living_players <= 1:
            interval += 1.15
        elif living_players >= 3 and snap['mode'] == 'pressure':
            interval = max(3.1, interval - 0.25)
        if snap['mode'] == 'mercy':
            interval += 1.1
        elif snap['mode'] == 'pressure':
            interval = max(3.1, interval - 0.35)
        if snap['threat'] >= BOSS_THREAT_LIMIT:
            interval += 1.4
        elif snap['threat'] >= BOSS_THREAT_LIMIT - 1:
            interval += 0.65
        if self._max_hp > 0 and self._hp / self._max_hp > 0.7:
            interval += 0.35
        self._attack_timer = bs.timer(
            interval, bs.WeakCallStrict(self._attack_tick), repeat=False)

    def _attack_tick(self) -> None:
        self._attempt_attack()
        self._schedule_next_attack()

    def _on_phase_changed(self, phase: int) -> None:
        """وقتی HP باس از یک آستانه رد می‌شه (سخت‌تر می‌شه)، ظاهرِ
        باس (رنگِ چشم/نور) و پیامِ هشدار به‌روزرسانی می‌شن، تا
        پلیرها بفهمن باس داره خطرناک‌تر می‌شه -- نه این‌که سختی
        بی‌سروصدا و ناگهانی تغییر کنه."""
        self._health_bar.set_phase(phase)

        for eye_light in getattr(self, '_eye_lights', []):
            if eye_light:
                eye_light.color = BOSS_PHASE_EYE_LIGHT_COLOR[phase]
        for eye_locator in getattr(self, '_eye_locators', []):
            if eye_locator:
                eye_locator.color = BOSS_PHASE_EYE_LOCATOR_COLOR[phase]
        if self._glow_light:
            self._glow_light.color = BOSS_PHASE_GLOW_COLOR[phase]
            self._glow_light.radius = 0.55 + phase * 0.25

        announce = BOSS_PHASE_ANNOUNCE_TEXT[phase]
        if announce is None or not self.node:
            return

        try:
            bs.screenmessage(announce, color=BOSS_PHASE_EYE_LOCATOR_COLOR[phase])
        except Exception:
            pass
        pos = self.node.position
        _play_boss_sound_burst(
            BOSS_SOUND_PHASE_CHANGE,
            count=3,
            spacing=0.18,
            volume=1.35,
            position=pos,
        )
        bs.emitfx(position=pos, velocity=(0, 1.8, 0), count=20, scale=1.3,
                  spread=1.0, chunk_type='spark')
        rage_flash = bs.newnode(
            'light',
            attrs={
                'position': pos,
                'color': BOSS_PHASE_GLOW_COLOR[phase],
                'radius': 2.2,
                'height_attenuated': False,
            },
        )
        bs.animate(rage_flash, 'intensity', {0.0: 3.0, 0.4: 0.0})
        bs.timer(0.5, rage_flash.delete)

        try:
            gnode = bs.getactivity().globalsnode
            if gnode:
                gnode.shake_scale = 1.4
                bs.timer(0.25, bs.CallStrict(setattr, gnode, 'shake_scale', 1.0))
        except Exception:
            pass

    def _scan_for_target(self) -> None:
        if self._dead or not self.node:
            return
        activity = self._activity
        if activity is None:
            # activity دیگه وجود نداره (weakref مرده)؛ خودِ باس هم
            # به‌زودی با همون چرخه‌ی تخریبِ activity حذف می‌شه، پس
            # فعلاً فقط از کرش‌کردن جلوگیری می‌کنیم.
            self._current_target = None
            return
        nearest = None
        nearest_dist_sq = None
        runaway = None
        runaway_score = -1
        boss_pos = self.node.position
        alive_actors: set[Any] = set()

        for player in activity.players:
            if not player.is_alive():
                continue
            actor = player.actor
            if actor is None or not actor.node:
                continue
            alive_actors.add(actor)
            ppos = actor.node.position
            dist_sq = (
                (ppos[0] - boss_pos[0]) ** 2
                + (ppos[1] - boss_pos[1]) ** 2
                + (ppos[2] - boss_pos[2]) ** 2
            )
            if nearest_dist_sq is None or dist_sq < nearest_dist_sq:
                nearest_dist_sq = dist_sq
                nearest = actor
            streak = self._miss_streak.get(actor, 0)
            if streak > runaway_score:
                runaway_score = streak
                runaway = actor

        target = nearest
        if (
            self._actor_is_alive(self._last_damage_actor)
            and self._last_damage_actor in alive_actors
            and bs.time() - self._last_damage_time <= 10.0
            and random.random() < BOSS_TARGET_LAST_HITTER_CHANCE
        ):
            target = self._last_damage_actor
        elif (
            runaway is not None
            and runaway_score > 0
            and random.random() < BOSS_TARGET_RUNAWAY_CHANCE
        ):
            target = runaway
        if (
            target is self._last_target_actor
            and self._target_repeat_count >= 2
            and len(alive_actors) > 1
        ):
            alternatives = [a for a in alive_actors if a is not target]
            if alternatives:
                target = random.choice(alternatives)

        self._current_target = target

        # پاک‌سازیِ ردِ پلیرهایی که دیگه زنده/معتبر نیستن (مردن یا
        # خارج شدن)، تا این دیکشنری‌ها بی‌نهایت بزرگ نشن و رفرنسِ
        # اکتورِ مرده رو برای همیشه نگه ندارن.
        stale = [a for a in self._miss_streak if a not in alive_actors]
        for a in stale:
            self._miss_streak.pop(a, None)
            self._miss_threshold.pop(a, None)
            self._warned_actors.discard(a)
        stale_frozen = [a for a in self._frozen_actors if a not in alive_actors]
        for a in stale_frozen:
            self._frozen_actors.discard(a)
        if self._last_damage_actor not in alive_actors:
            self._last_damage_actor = None

    def _attempt_attack(self) -> None:
        if self._dead or not self.node:
            return
        if self._current_target is None or not self._actor_is_alive(
            self._current_target
        ):
            self._scan_for_target()
        if self._current_target is None:
            return
        target_actor = self._current_target
        if not hasattr(target_actor, 'node') or not target_actor.node:
            return

        attack_kind = self._choose_attack(target_actor)
        self._telegraph_attack(target_actor, attack_kind)
        return

        boss_pos = self.node.position
        target_pos = target_actor.node.position

        dx = target_pos[0] - boss_pos[0]
        dy = target_pos[1] - boss_pos[1]
        dz = target_pos[2] - boss_pos[2]
        length = max(0.0001, (dx * dx + dy * dy + dz * dz) ** 0.5)
        direction = (dx / length, dy / length, dz / length)

        phase = self._current_phase()
        shot_count = BOSS_PROJECTILE_COUNT_PHASE[phase]
        speed_scale = BOSS_PROJECTILE_SPEED_MULT_PHASE[phase]
        turn_scale = BOSS_PROJECTILE_TURN_MULT_PHASE[phase]

        # در فازِ نرمال/خشمگین فقط یک پرتابه‌ی مستقیم شلیک می‌شه. در
        # فازِ آخر (در آستانه‌ی جنون)، دو پرتابه‌ی هم‌زمان با یک
        # زاویه‌ی کوچیک از هم باز می‌شن، تا فرار کردن سخت‌تر بشه --
        # بدونِ این‌که فرار کاملاً غیرممکن بشه.
        if shot_count <= 1:
            shot_directions = [direction]
        else:
            half_spread = BOSS_MULTISHOT_SPREAD_DEGREES / 2.0
            step = BOSS_MULTISHOT_SPREAD_DEGREES / (shot_count - 1)
            shot_directions = [
                self._rotate_direction_y(direction, -half_spread + i * step)
                for i in range(shot_count)
            ]

        # پرتابه رو فقط با یک شکافِ کوچیک بیرونِ بدنِ خودِ باس،
        # دقیقاً روی همون راستایِ شلیک اسپاون کن. چون بالاتر (رجوع
        # به BossProjectile.__init__) پاسخِ فیزیکیِ برخورد با هر
        # چیزِ object_material‌داری از جمله خودِ باس کاملاً غیرفعال
        # شده، دیگه نیازی به یک آفستِ بزرگ برای فرار از برخوردِ
        # فیزیکیِ خودِ باس نیست؛ همین شکافِ کوچیک کافیه که پرتابه
        # داخلِ مشِ خودِ باس رندر نشه، و بازم دقیقاً حسِ «از کنارِ
        # خودِ باس شلیک شد» رو بده، نه از یک فاصله‌ی دور.
        spawn_offset = BOSS_BODY_SCALE * PROJECTILE_SPAWN_OFFSET_MULT

        # قبل از ساختنِ پرتابه‌ی جدید، رفرنسِ پرتابه‌های مرده رو از
        # لیست پاک کن تا لیست بی‌نهایت بزرگ نشه.
        self._live_projectiles = [
            p for p in self._live_projectiles if not p.is_dead()
        ]

        for shot_dir in shot_directions:
            spawn_pos = (
                boss_pos[0] + shot_dir[0] * spawn_offset,
                boss_pos[1] + shot_dir[1] * spawn_offset,
                boss_pos[2] + shot_dir[2] * spawn_offset,
            )
            projectile = BossProjectile(
                position=spawn_pos,
                direction=shot_dir,
                owner_activity=self._activity,
                assets=self._assets,
                target=target_actor,
                on_result=self._on_projectile_result,
                speed_scale=speed_scale,
                turn_rate_scale=turn_scale,
            )
            # نگه‌داشتنِ رفرنسِ قوی، وگرنه پایتون بلافاصله این
            # آبجکت رو جمع‌آوری می‌کنه و تایمرهاش (که weak reference
            # هستن) دیگه هیچ‌وقت اجرا نمی‌شن -- دقیقاً همون چیزی که
            # باعثِ اسپمِ out-of-bounds و باگِ حذف‌نشدنِ مکعب‌ها می‌شد.
            self._live_projectiles.append(projectile)

        _play_boss_sound_burst(
            BOSS_SOUND_ATTACK_WARN,
            count=2 if burst else 1,
            spacing=0.1,
            volume=0.85,
            position=boss_pos,
        )

    def _telegraph_attack(self, target_actor: Any, attack_kind: str) -> None:
        if self._dead or not self.node:
            return
        target_pos = _safe_position(target_actor)
        if target_pos is None:
            return
        self._current_target = target_actor

        self._set_eye_alert(BOSS_ATTACK_TELEGRAPH_DELAY)
        if attack_kind in {'gap_shockwave', 'shockwave', 'mini_blackhole'}:
            _play_boss_sound_burst(
                BOSS_SOUND_ATTACK_BIG,
                count=3,
                spacing=0.14,
                volume=1.25,
                position=self.node.position,
            )
        elif attack_kind != 'breather':
            _play_boss_sound_burst(
                BOSS_SOUND_ATTACK_WARN,
                count=2,
                spacing=0.12,
                volume=0.95,
                position=self.node.position,
            )
        boss_pos = self.node.position
        marker_pos = (
            boss_pos if attack_kind in {'shockwave', 'gap_shockwave', 'breather'}
            else (target_pos[0], target_pos[1] + 0.05, target_pos[2])
        )
        marker_size = {
            'breather': 1.1,
            'fake_telegraph': 0.85,
            'homing': 0.9,
            'warning_homing': 0.75,
            'focus_shot': 0.8,
            'burst': 1.25,
            'shockwave': BOSS_SHOCKWAVE_RADIUS_PHASE[self._current_phase()],
            'gap_shockwave': BOSS_SHOCKWAVE_RADIUS_PHASE[self._current_phase()],
            'mini_blackhole': MINI_BLACKHOLE_RADIUS * 0.45,
        }.get(attack_kind, 0.9)
        marker_color = {
            'breather': (0.25, 1.2, 0.35),
            'fake_telegraph': (2.2, 0.15, 0.1),
            'homing': (3.0, 0.35, 0.0),
            'warning_homing': (2.4, 0.7, 0.0),
            'focus_shot': (4.0, 0.1, 0.0),
            'burst': (3.5, 0.6, 0.0),
            'shockwave': (2.5, 0.2, 0.0),
            'gap_shockwave': (2.2, 0.35, 0.0),
            'mini_blackhole': (1.4, 0.25, 2.0),
        }.get(attack_kind, (3.0, 0.35, 0.0))

        marker = bs.newnode(
            'locator',
            attrs={
                'shape': 'circle',
                'position': marker_pos,
                'color': marker_color,
                'opacity': 0.85,
                'draw_beauty': True,
                'additive': True,
                'size': [marker_size],
            },
        )
        bs.animate(marker, 'opacity', {0.0: 0.2, 0.18: 0.95, 0.7: 0.2})
        bs.timer(BOSS_ATTACK_TELEGRAPH_DELAY, marker.delete)

        light = bs.newnode(
            'light',
            attrs={
                'position': marker_pos,
                'color': marker_color,
                'radius': min(2.5, max(0.8, marker_size * 0.45)),
                'height_attenuated': False,
            },
        )
        bs.animate(light, 'intensity', {0.0: 0.0, 0.2: 1.7, 0.7: 0.0})
        bs.timer(BOSS_ATTACK_TELEGRAPH_DELAY, light.delete)
        bs.timer(
            BOSS_ATTACK_TELEGRAPH_DELAY,
            bs.WeakCallStrict(self._perform_attack, target_actor, attack_kind),
        )

    def _perform_attack(self, target_actor: Any, attack_kind: str) -> None:
        if self._dead or not self.node:
            return
        self._last_attack_kind = attack_kind
        if attack_kind in {'shockwave', 'gap_shockwave', 'mini_blackhole'}:
            self._last_big_attack_time = bs.time()

        if attack_kind == 'breather':
            _play_boss_sound_burst(
                BOSS_SOUND_BREATHER,
                count=2,
                spacing=0.18,
                volume=1.05,
                position=self.node.position,
            )
            self._vulnerable_until = bs.time() + BOSS_VULNERABLE_WINDOW + 1.2
            self._show_vulnerable_flash()
            return
        if attack_kind == 'fake_telegraph':
            self._set_eye_alert(0.35)
            return
        if attack_kind == 'gap_shockwave':
            self._fire_shockwave(target_actor)
        elif attack_kind == 'shockwave':
            self._fire_shockwave()
        elif attack_kind == 'mini_blackhole':
            self._spawn_mini_blackhole(target_actor)
        elif attack_kind == 'burst':
            self._fire_projectiles(target_actor, burst=True)
        elif attack_kind == 'focus_shot':
            self._fire_projectiles(target_actor, focus=True)
        elif attack_kind == 'warning_homing':
            self._fire_projectiles(target_actor, warning=True)
        else:
            self._fire_projectiles(target_actor, burst=False)

        self._vulnerable_until = bs.time() + BOSS_VULNERABLE_WINDOW
        self._show_vulnerable_flash()

    def _show_vulnerable_flash(self) -> None:
        if not self.node:
            return
        pos = self.node.position
        vuln_light = bs.newnode(
            'light',
            attrs={
                'position': pos,
                'color': (0.2, 1.0, 0.35),
                'radius': 1.0,
                'height_attenuated': False,
            },
        )
        bs.animate(
            vuln_light, 'intensity',
            {0.0: 1.8, BOSS_VULNERABLE_WINDOW: 0.0},
        )
        bs.timer(BOSS_VULNERABLE_WINDOW, vuln_light.delete)

    def _regen_tick(self) -> None:
        if self._dead or not self.node:
            return
        max_regen_hp = max(1, int(round(self._max_hp * BOSS_REGEN_MAX_FRACTION)))
        if self._hp >= max_regen_hp:
            return
        now = bs.time()
        last_damage_time = max(self._last_damage_time, self._spawn_time)
        if now - last_damage_time < BOSS_REGEN_DELAY:
            return

        self._hp = min(max_regen_hp, self._hp + BOSS_REGEN_AMOUNT)
        self._health_bar.set_hp(self._hp, animate=True)
        new_phase = self._current_phase()
        if new_phase != self._phase:
            self._phase = new_phase
            self._health_bar.set_phase(new_phase)
            for eye_light in getattr(self, '_eye_lights', []):
                if eye_light:
                    eye_light.color = BOSS_PHASE_EYE_LIGHT_COLOR[new_phase]
            for eye_locator in getattr(self, '_eye_locators', []):
                if eye_locator:
                    eye_locator.color = BOSS_PHASE_EYE_LOCATOR_COLOR[new_phase]
            if self._glow_light:
                self._glow_light.color = BOSS_PHASE_GLOW_COLOR[new_phase]

        self._show_regen_fx()

    def _show_regen_fx(self) -> None:
        if not self.node:
            return
        pos = self.node.position
        _play_boss_sound_burst(
            BOSS_SOUND_REGEN,
            count=3,
            spacing=0.16,
            volume=1.35,
            position=pos,
        )
        bs.emitfx(
            position=(pos[0], pos[1] + 0.2, pos[2]),
            velocity=(0.0, 1.1, 0.0),
            count=10,
            scale=1.15,
            spread=0.65,
            chunk_type='spark',
        )
        bs.emitfx(
            position=(pos[0], pos[1] - 0.15, pos[2]),
            velocity=(0.0, 0.45, 0.0),
            count=6,
            scale=1.0,
            spread=0.45,
            chunk_type='sweat',
        )
        regen_light = bs.newnode(
            'light',
            attrs={
                'position': pos,
                'color': (0.25, 1.0, 0.45),
                'radius': 1.4,
                'height_attenuated': False,
            },
        )
        bs.animate(regen_light, 'intensity', {0.0: 0.0, 0.1: 2.2, 0.8: 0.0})
        bs.timer(0.85, regen_light.delete)

        now = bs.time()
        if now - self._last_regen_notice_time >= BOSS_REGEN_NOTICE_INTERVAL:
            self._last_regen_notice_time = now
            try:
                bs.screenmessage(
                    'The boss is regenerating...',
                    color=(0.35, 1.0, 0.45),
                )
            except Exception:
                pass

    def _fire_projectiles(
        self,
        target_actor: Any,
        burst: bool = False,
        warning: bool = False,
        focus: bool = False,
    ) -> None:
        if self._dead or not self.node:
            return
        if not self._actor_is_alive(target_actor):
            return

        boss_pos = self.node.position
        target_pos = target_actor.node.position
        dx = target_pos[0] - boss_pos[0]
        dy = target_pos[1] - boss_pos[1]
        dz = target_pos[2] - boss_pos[2]
        length = max(0.0001, (dx * dx + dy * dy + dz * dz) ** 0.5)
        direction = (dx / length, dy / length, dz / length)

        phase = self._current_phase()
        shot_count = BOSS_PROJECTILE_COUNT_PHASE[phase]
        if burst:
            shot_count = max(2, min(3, shot_count + phase + 1))
        if warning or focus:
            shot_count = 1
        speed_scale = BOSS_PROJECTILE_SPEED_MULT_PHASE[phase] * (
            0.9 if burst else 1.0
        )
        turn_scale = BOSS_PROJECTILE_TURN_MULT_PHASE[phase] * (
            0.85 if burst else 1.0
        )
        if warning:
            direction = self._rotate_direction_y(
                direction, random.uniform(-16.0, 16.0)
            )
            speed_scale *= 0.82
            turn_scale *= 0.55
        elif focus:
            speed_scale *= 1.08
            turn_scale *= 1.12

        if shot_count <= 1:
            shot_directions = [direction]
        else:
            spread = BOSS_MULTISHOT_SPREAD_DEGREES * (2.2 if burst else 1.0)
            half_spread = spread / 2.0
            step = spread / (shot_count - 1)
            shot_directions = [
                self._rotate_direction_y(direction, -half_spread + i * step)
                for i in range(shot_count)
            ]

        spawn_offset = BOSS_BODY_SCALE * PROJECTILE_SPAWN_OFFSET_MULT
        self._live_projectiles = [
            p for p in self._live_projectiles if not p.is_dead()
        ]
        available_slots = BOSS_MAX_LIVE_PROJECTILES - len(self._live_projectiles)
        if available_slots <= 0:
            return
        shot_directions = shot_directions[:available_slots]
        for shot_dir in shot_directions:
            spawn_pos = (
                boss_pos[0] + shot_dir[0] * spawn_offset,
                boss_pos[1] + shot_dir[1] * spawn_offset,
                boss_pos[2] + shot_dir[2] * spawn_offset,
            )
            projectile = BossProjectile(
                position=spawn_pos,
                direction=shot_dir,
                owner_activity=self._activity,
                assets=self._assets,
                target=target_actor,
                on_result=self._on_projectile_result,
                speed_scale=speed_scale,
                turn_rate_scale=turn_scale,
            )
            self._live_projectiles.append(projectile)
        _play_boss_sound(('spawn', 'gasp'))

    def _fire_shockwave(self, gap_actor: Any | None = None) -> None:
        if self._dead or not self.node:
            return
        boss_pos = self.node.position
        phase = self._current_phase()
        count = BOSS_SHOCKWAVE_RING_COUNT_PHASE[phase]
        radius = BOSS_SHOCKWAVE_RADIUS_PHASE[phase]
        gap_angle = None
        if gap_actor is not None:
            target_pos = _safe_position(gap_actor)
            if target_pos is not None:
                gap_angle = math.atan2(
                    target_pos[2] - boss_pos[2],
                    target_pos[0] - boss_pos[0],
                )
                count = max(5, count - 2)
        self._shockwave_active_until = (
            bs.time() + count * BOSS_SHOCKWAVE_STEP_DELAY + 0.6
        )
        for i in range(count):
            ang = (2.0 * math.pi * i) / max(1, count)
            if gap_angle is not None:
                diff = abs((ang - gap_angle + math.pi) % (2.0 * math.pi) - math.pi)
                if diff < 0.55:
                    continue
            pos = (
                boss_pos[0] + math.cos(ang) * radius,
                self._base_position[1] + 0.45,
                boss_pos[2] + math.sin(ang) * radius,
            )
            bs.timer(
                i * BOSS_SHOCKWAVE_STEP_DELAY,
                bs.WeakCallStrict(self._spawn_shockwave_blast, pos),
            )

    def _spawn_shockwave_blast(
        self, position: tuple[float, float, float]
    ) -> None:
        if self._dead:
            return
        try:
            Blast(
                position=position,
                velocity=(0.0, 0.0, 0.0),
                blast_radius=BOSS_SHOCKWAVE_BLAST_RADIUS,
                blast_type='normal',
            ).autoretain()
        except Exception:
            pass

    def _spawn_mini_blackhole(self, target_actor: Any) -> None:
        if self._dead or not self.node:
            return
        self._live_blackholes = [
            h for h in self._live_blackholes if getattr(h, 'node', None)
        ]
        if self._live_blackholes or self._active_threat_score() > 0:
            return
        target_pos = _safe_position(target_actor)
        if target_pos is None:
            target_pos = self.node.position
        try:
            black_hole = BlackHole(
                position=target_pos,
                radius=MINI_BLACKHOLE_RADIUS,
                xspeed=MINI_BLACKHOLE_XSPEED,
                ssize=MINI_BLACKHOLE_SSIZE,
            )
        except Exception:
            return
        self._live_blackholes.append(black_hole)
        bs.timer(
            MINI_BLACKHOLE_LIFETIME,
            bs.CallStrict(black_hole.handlemessage, bs.DieMessage()),
        )

    def _on_projectile_result(self, target_actor: Any, hit: bool) -> None:
        """نتیجه‌ی هر پرتابه (خورد/نخورد) از رویِ همون سیستمِ موجودِ
        شلیک به نزدیک‌ترین پلیر گزارش می‌شه -- هیچ سیستمِ جدیدی
        جایگزینِ هدف‌گیری نمی‌شه. فقط ردِ شلیک‌های ناموفق به هر
        پلیر جداگانه نگه داشته می‌شه: اگه یک پلیرِ خاص بینِ ۳ تا ۵
        بار (رندوم) پشتِ‌سرِهم بهش شلیک بشه و نخوره، همون‌جا فریزش
        می‌کنیم. پلیرِ فریزشده با هر برخوردِ بعدیِ پرتابه -- طبقِ
        همون سیستمِ موجود که هر برخورد یک انفجارِ واقعی می‌سازه --
        به‌احتمالِ زیاد از بین می‌ره."""
        if self._dead or target_actor is None:
            return
        if not getattr(target_actor, 'node', None):
            # پلیر دیگه معتبر نیست (مرده/خارج شده)؛ ردش رو پاک کن.
            self._miss_streak.pop(target_actor, None)
            self._miss_threshold.pop(target_actor, None)
            self._frozen_actors.discard(target_actor)
            self._warned_actors.discard(target_actor)
            return

        if hit:
            self._player_hit_times.append(bs.time())
            self._trim_director_memory()
            # خورد (و طبقِ سیستمِ موجود بلافاصله می‌میره)؛ ردیابیِ
            # استریکِ میس براش دیگه لازم نیست.
            self._miss_streak.pop(target_actor, None)
            self._miss_threshold.pop(target_actor, None)
            self._frozen_actors.discard(target_actor)
            self._warned_actors.discard(target_actor)
            return

        # اگه از قبل فریزه، فریز می‌مونه (منتظرِ شلیکِ بعدی که
        # بهش می‌خوره و طبقِ سیستمِ موجود می‌میره)؛ دیگه لازم نیست
        # استریک رو بازشماری کنیم.
        if target_actor in self._frozen_actors:
            return

        threshold = self._miss_threshold.get(target_actor)
        if threshold is None:
            lo, hi = BOSS_MISS_THRESHOLD_RANGE_PHASE[self._current_phase()]
            snap = self._director_snapshot()
            if snap['mode'] == 'mercy':
                lo += 2
                hi += 2
            if snap['living_players'] <= 1:
                lo += 2
                hi += 2
            threshold = random.randint(lo, hi)
            self._miss_threshold[target_actor] = threshold

        streak = self._miss_streak.get(target_actor, 0) + 1
        self._miss_streak[target_actor] = streak

        warn_at = max(1, threshold - BOSS_MISS_WARNING_MARGIN)
        if streak >= warn_at and target_actor not in self._warned_actors:
            self._warn_target_actor(target_actor)
            return

        if streak >= threshold:
            self._freeze_target_actor(target_actor)

    def _warn_target_actor(self, target_actor: Any) -> None:
        if not getattr(target_actor, 'node', None):
            return
        self._warned_actors.add(target_actor)
        self._set_eye_alert(0.65)
        try:
            pos = target_actor.node.position
        except Exception:
            return
        marker = bs.newnode(
            'locator',
            attrs={
                'shape': 'circle',
                'position': (pos[0], pos[1] + 0.05, pos[2]),
                'color': (4.0, 2.0, 0.0),
                'opacity': 0.9,
                'draw_beauty': True,
                'additive': True,
                'size': [1.0],
            },
        )
        bs.animate(marker, 'opacity', {0.0: 0.2, 0.18: 0.95, 0.7: 0.0})
        bs.timer(0.75, marker.delete)
        try:
            bs.screenmessage('Boss locked on a runner!', color=(1.0, 0.8, 0.1))
        except Exception:
            pass

    def _freeze_target_actor(self, target_actor: Any) -> None:
        """فریزکردنِ یک پلیرِ خاص بعد از این‌که ۳ تا ۵ بار (رندوم)
        بهش شلیک شده و نخورده. پلیر تا وقتی یک پرتابه بهش بخوره
        فریز می‌مونه (خودِ برخورد طبقِ سیستمِ موجود یک انفجارِ واقعی
        می‌سازه)."""
        if not getattr(target_actor, 'node', None):
            return
        try:
            target_actor.node.handlemessage(bs.FreezeMessage())
        except Exception:
            return
        self._frozen_actors.add(target_actor)
        self._miss_streak.pop(target_actor, None)
        self._miss_threshold.pop(target_actor, None)
        self._warned_actors.discard(target_actor)
        _play_boss_sound_burst(
            BOSS_SOUND_FREEZE,
            count=2,
            spacing=0.16,
            volume=1.1,
            position=target_actor.node.position,
        )

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.DieMessage):
            self._die()
            return None

        if isinstance(msg, _BombTouchMessage):
            # چکِ واقعیِ برخورد: bs.getcollision() دقیقاً همون
            # روشیه که خودِ گیم‌مودهای داخلیِ بازی (مثلِ Hockey) از
            # روش استفاده می‌کنن تا بفهمن طرفِ مقابلِ برخورد واقعاً
            # چه actor ای بوده. اگه طرفِ مقابل یک Bomb زنده باشه
            # (چه هنوز منفجر نشده)، دقیقاً یک واحد دمیج می‌زنیم و
            # خودِ بمب رو بلافاصله محو می‌کنیم -- دیگه لازم نیست
            # منتظرِ انفجارِ بمب بمونیم.
            try:
                collision = bs.getcollision()
                opposing = collision.opposingnode
                bomb_actor = opposing.getdelegate(Bomb, True)
            except Exception:
                return None

            if bomb_actor is not None:
                self._last_damage_time = bs.time()
                try:
                    source_player = bomb_actor.get_source_player(bs.Player)
                    if source_player is not None:
                        self._last_damage_actor = source_player.actor
                except Exception:
                    pass
                self._apply_damage(BOSS_DAMAGE_PER_BOMB_HIT)
                bomb_actor.handlemessage(bs.DieMessage())
            return None

        if isinstance(msg, bs.HitMessage):
            # طبقِ درخواست: باس دیگه از شعاعِ انفجار (blast/HitMessage)
            # هیچ آسیبی نمی‌بینه. تنها منبعِ دمیج، برخوردِ مستقیمِ
            # فیزیکیِ یک Bomb زنده با بدنه‌ی باسه که بالاتر توسطِ
            # _BombTouchMessage (از رویِ bs.getcollision()) تشخیص داده
            # می‌شه. عمداً هیچ کاری این‌جا انجام نمی‌شه.
            return None

        if isinstance(msg, bs.OutOfBoundsMessage):
            self._recover_from_out_of_bounds()
            return None

        return None

    def _recover_from_out_of_bounds(self) -> None:
        if self._dead or not self.node:
            return
        self.node.position = (
            self._base_position[0],
            self._base_position[1] + BOSS_SPAWN_HEIGHT,
            self._base_position[2],
        )
        self.node.velocity = (0.0, 0.0, 0.0)
        try:
            self.node.angular_velocity = (0.0, 0.0, 0.0)
        except Exception:
            pass
        # دیگه هیچ orientation ای دستی این‌جا ست نمی‌شه (رجوعِ کاملِ
        # این تصمیم به کامنتِ بالای __init__).

    def _apply_damage(self, amount: int) -> None:
        if self._dead:
            return
        if bs.time() <= self._vulnerable_until:
            amount += BOSS_VULNERABLE_DAMAGE_BONUS
        self._boss_damage_times.append(bs.time())
        self._trim_director_memory()
        self._hp = max(0, self._hp - amount)
        self._health_bar.set_hp(self._hp, animate=True)

        # اگه این ضربه باعثِ عبور از یک آستانه‌ی خشم شد، سیستمِ
        # سختیِ پویا رو آپدیت کن (فاصله‌ی حمله کوتاه‌تر، پرتابه
        # سریع‌تر، و در فازِ آخر شلیکِ دوتایی).
        new_phase = self._current_phase()
        if new_phase != self._phase:
            self._phase = new_phase
            self._on_phase_changed(new_phase)

        if self.node:
            pos = self.node.position
            _play_boss_sound_burst(
                BOSS_SOUND_HIT,
                count=2,
                spacing=0.1,
                volume=0.95,
                position=pos,
            )
            bs.emitfx(
                position=pos,
                velocity=(0, 1.2, 0),
                count=12,
                scale=0.9,
                spread=0.6,
                chunk_type='spark',
            )
            bs.emitfx(
                position=pos,
                velocity=(0, 0.5, 0),
                count=4,
                scale=1.0,
                spread=0.5,
                chunk_type='spark',
            )
            hit_flash = bs.newnode(
                'light',
                attrs={
                    'position': pos,
                    'color': (1.0, 0.9, 0.3),
                    'radius': 0.8,
                    'height_attenuated': False,
                },
            )
            bs.animate(hit_flash, 'intensity', {0.0: 2.2, 0.25: 0.0})
            bs.timer(0.3, hit_flash.delete)

            try:
                gnode = bs.getactivity().globalsnode
                if gnode:
                    gnode.shake_scale = 0.6
                    bs.timer(0.2, bs.CallStrict(setattr, gnode, 'shake_scale', 1.0))
            except Exception:
                pass

        if self._hp <= 0:
            self._die()

    def _die(self) -> None:
        if self._dead:
            return
        self._dead = True

        pos = self.node.position if self.node else self._base_position

        # افکتِ مرگ: انفجارِ چندلایه‌ی بزرگ (جرقه + دود + آتش) به‌همراه
        # چند فلاشِ نوریِ پشت‌سرِهم برای حسِ دراماتیک‌ترِ نابودیِ باس.
        bs.emitfx(position=pos, velocity=(0, 3, 0), count=45, scale=1.9,
                  spread=1.5, chunk_type='spark')
        bs.emitfx(position=pos, velocity=(0, 1.5, 0), count=25, scale=2.2,
                  spread=1.3, chunk_type='spark')
        bs.emitfx(position=pos, velocity=(0, 0.8, 0), count=18, scale=1.6,
                  spread=1.0, chunk_type='splinter')

        explosion_light = bs.newnode(
            'light',
            attrs={
                'position': pos,
                'color': (1.0, 0.6, 0.1),
                'radius': 1.6,
                'height_attenuated': False,
            },
        )
        bs.animate(explosion_light, 'intensity',
                   {0.0: 2.5, 0.15: 1.6, 0.4: 0.9, 1.0: 0.0})
        bs.timer(1.05, explosion_light.delete)

        secondary_flash = bs.newnode(
            'light',
            attrs={
                'position': pos,
                'color': (1.0, 1.0, 0.8),
                'radius': 2.0,
                'height_attenuated': False,
            },
        )
        bs.animate(secondary_flash, 'intensity', {0.0: 0.0, 0.05: 3.0, 0.3: 0.0})
        bs.timer(0.4, secondary_flash.delete)

        _play_boss_sound_burst(
            BOSS_SOUND_DEATH,
            count=4,
            spacing=0.16,
            volume=1.35,
            position=pos,
        )

        try:
            gnode = bs.getactivity().globalsnode
            if gnode:
                gnode.shake_scale = 2.2
                bs.timer(
                    0.6,
                    bs.CallStrict(setattr, gnode, 'shake_scale', 1.0),
                )
        except Exception:
            pass

        self._health_bar.set_hp(0, animate=True)
        bs.timer(1.5, bs.WeakCallStrict(self._cleanup_health_bar))

        if self.node:
            self.node.delete()
        if self._glow_light:
            self._glow_light.delete()
        for eye_light in getattr(self, '_eye_lights', []):
            if eye_light:
                eye_light.delete()
        for eye_locator in getattr(self, '_eye_locators', []):
            if eye_locator:
                eye_locator.delete()

        # افکتِ آتشِ قرمز هم باید با مرگِ باس کاملاً متوقف بشه: چکِ
        # self._dead داخلِ _emit_fire_particles از ادامه‌ی ساطع‌شدنِ
        # ذرات جلوگیری می‌کنه، ولی خودِ نودِ نورِ آتش (owner=self.node
        # بود و با delete شدنِ self.node به‌طورِ خودکار پاک می‌شه) رو
        # اینجا هم صریحاً حذف می‌کنیم تا هیچ نورِ باقی‌مونده‌ای معلق
        # نمونه.
        fire_light = getattr(self, '_fire_light', None)
        if fire_light:
            try:
                fire_light.delete()
            except Exception:
                pass
        self._fire_timer = None

        # مهم: هر پرتابه‌ی زنده‌ای که هنوز روی نقشه شناوره رو هم
        # همین الان حذف کن. اگه این کار انجام نشه، وقتی پلیر سریع
        # از مپ خارج می‌شه (مثلاً همون لحظه‌ای که باس تازه مرده)،
        # پرتابه‌ها بدونِ هیچ منطقِ ارتباطی به activity برای چند
        # ثانیه‌ی باقی‌مانده از عمرشون شناور می‌مونن و می‌تونن باعثِ
        # همون ارورهای پشت‌سرِهمِ out-of-bounds/کرش بشن.
        for projectile in self._live_projectiles:
            try:
                if not projectile.is_dead():
                    projectile.handlemessage(bs.DieMessage())
            except Exception:
                pass
        self._live_projectiles = []
        for black_hole in self._live_blackholes:
            try:
                if getattr(black_hole, 'node', None):
                    black_hole.handlemessage(bs.DieMessage())
            except Exception:
                pass
        self._live_blackholes = []

        # هر پلیری که به‌خاطرِ ۳ تا ۵ شلیکِ ناموفق فریز شده بود رو
        # آزاد کن، وگرنه بعدِ مرگِ باس برای همیشه فریز می‌مونه.
        for frozen_actor in list(self._frozen_actors):
            try:
                if getattr(frozen_actor, 'node', None):
                    frozen_actor.node.handlemessage(bs.ThawMessage())
            except Exception:
                pass
        self._frozen_actors.clear()
        self._miss_streak.clear()
        self._miss_threshold.clear()
        self._warned_actors.clear()

        # لغو تایمر حمله
        if self._attack_timer is not None:
            try:
                self._attack_timer.cancel()
            except Exception:
                pass
            self._attack_timer = None
        if self._regen_timer is not None:
            try:
                self._regen_timer.cancel()
            except Exception:
                pass
            self._regen_timer = None

        # طبقِ درخواست: به‌جایِ صدازدنِ مستقیمِ کال‌بکِ مرگ (که باعثِ
        # شروعِ فوریِ شمارشِ ۳۰ ثانیه‌ایِ اسپاونِ باسِ بعدی می‌شد)،
        # سرِ جایِ مرگِ باس دقیقاً همون کلاسِ BlackHole (پورت‌شده‌ی
        # عینیِ anomalies.py از overclocked -- رجوع به تعریفِ کلاس
        # بالایِ همین فایل) اسپاون می‌شه. این سیاه‌چاله دقیقاً
        # BLACKHOLE_LIFETIME (۱۰) ثانیه سرِ جاش می‌مونه و طبقِ
        # منطقِ خودِ کلاس (متدِ _update) هرچیزِ دارایِ
        # object_material رو -- بدونِ استثنا: پاورآپ، بمب/TNT،
        # پلیرها -- به سمتِ مرکزش می‌کشه و با برخوردِ مستقیم
        # (متدِ kill) نابودش می‌کنه. فقط وقتی این ۱۰ ثانیه تموم شد
        # و خودِ سیاه‌چاله (با bs.DieMessage) جمع شد، کال‌بکِ
        # self._on_death_callback صدا زده می‌شه -- یعنی شمارشِ
        # ۳۰ ثانیه‌ایِ اسپاونِ باسِ بعدی از همون لحظه شروع می‌شه، نه
        # هم‌زمان با خودِ مرگِ باس.
        try:
            black_hole = BlackHole(
                position=pos,
                radius=BLACKHOLE_RADIUS,
                xspeed=BLACKHOLE_XSPEED,
                ssize=BLACKHOLE_SSIZE,
            )
        except Exception:
            # اگه به هر دلیلی ساختِ سیاه‌چاله شکست خورد، حداقل
            # کال‌بکِ مرگ رو صدا بزن تا باسِ بعدی هیچ‌وقت برای
            # همیشه اسپاون نشه.
            self._on_death_callback()
        else:
            bs.timer(
                BLACKHOLE_LIFETIME,
                bs.CallStrict(black_hole.handlemessage, bs.DieMessage()),
            )
            bs.timer(BLACKHOLE_LIFETIME, self._on_death_callback)

    def _cleanup_health_bar(self) -> None:
        self._health_bar.hide()


# -----------------------------------------------------------------------
# گیم‌مود
# -----------------------------------------------------------------------

# ba_meta export bascenev1.GameActivity
class BossFight(bs.TeamGameActivity[bs.Player, bs.Team]):
    """گیم‌مودِ Boss Fight."""

    name = 'Boss Fight'
    description = 'در برابرِ یک باسِ مکعبیِ غول‌پیکر دووم بیار. باهاش با بمب بجنگ!'
    available_settings = []
    scoreconfig = bs.ScoreConfig(label='زمان', scoretype=bs.ScoreType.SECONDS)

    @classmethod
    def get_available_settings(
        cls, sessiontype: type[bs.Session]
    ) -> list[bs.Setting]:
        return [
            bs.IntChoiceSetting(
                'زمانِ راند',
                choices=[
                    ('نامحدود', 0),
                    ('۲ دقیقه', 120),
                    ('۵ دقیقه', 300),
                    ('۱۰ دقیقه', 600),
                ],
                default=0,
            ),
        ]

    @classmethod
    def get_supported_maps(cls, sessiontype: type[bs.Session]) -> list[str]:
        return bs.app.classic.getmaps('melee')

    @classmethod
    def supports_session_type(cls, sessiontype: type[bs.Session]) -> bool:
        return issubclass(sessiontype, bs.CoopSession) or issubclass(
            sessiontype, bs.FreeForAllSession
        ) or issubclass(sessiontype, bs.DualTeamSession)

    def __init__(self, settings: dict) -> None:
        super().__init__(settings)
        self._boss: BossActor | None = None
        self._respawn_timer: bs.Timer | None = None
        self._round_time = settings.get('زمانِ راند', 0)
        self._assets: dict[str, Any] = {}
        self._respawn_timers: dict[bs.Player, bs.Timer] = {}

    def _load_assets(self) -> None:
        # باس: از مِشِ 'bonesHead' با تکسچرِ 'bonesColor' استفاده
        # می‌کنیم (دقیقاً همون کله‌ی اسکلتی که توی اسِست‌های داخلیِ
        # بازی موجوده). اگه به هر دلیلی در دسترس نبود، به مکعبِ بمب
        # و بعدش TNT بازمی‌گرده تا هیچ‌وقت گیم‌مود کرش نکنه.
        try:
            boss_mesh = bs.getmesh('bonesHead')
            boss_tex = bs.gettexture('bonesColor')
        except Exception:
            try:
                boss_mesh = bs.getmesh('bomb')
                boss_tex = bs.gettexture('bombColor')
            except Exception:
                boss_mesh = bs.getmesh('tnt')
                boss_tex = bs.gettexture('tnt')

        # پرتابه: یک مِشِ کوچیک‌تر و متفاوت (میخِ خاردار/سنبله) که
        # باعث می‌شه پرتابه از خودِ باس بصری متمایز باشه و حسِ
        # «شلیکِ خطرناک» بده.
        try:
            proj_mesh = bs.getmesh('impactBomb')
            proj_tex = bs.gettexture('impactBombColor')
        except Exception:
            proj_mesh = bs.getmesh('tnt')
            proj_tex = bs.gettexture('tnt')

        self._assets = {
            'boss_mesh': boss_mesh,
            'boss_tex': boss_tex,
            'projectile_mesh': proj_mesh,
            'projectile_tex': proj_tex,
        }

    def get_instance_description(self) -> str | Sequence:
        return 'باسِ غول‌پیکر رو نابود کن!'

    def on_transition_in(self) -> None:
        super().on_transition_in()
        self.setup_standard_time_limit(self._round_time)
        self.setup_standard_powerup_drops()
        self._apply_dark_atmosphere()

    def _apply_dark_atmosphere(self) -> None:
        # فقط رنگ‌آمیزیِ کلی و تاریکیِ لبه‌ها رو تغییر می‌دیم -- نورِ
        # واقعیِ صحنه (ambient_color/shadow_offset) دست‌نخورده می‌مونه.
        # اگه نخواستی، مقادیرِ MAP_* بالایِ فایل رو به نزدیکِ (1,1,1)
        # برگردون.
        try:
            gnode = self.activity.globalsnode
            if gnode:
                gnode.tint = MAP_TINT
                gnode.vignette_outer = MAP_VIGNETTE_OUTER
                gnode.vignette_inner = MAP_VIGNETTE_INNER
        except Exception:
            pass

    def on_begin(self) -> None:
        super().on_begin()
        self._load_assets()
        self._spawn_boss()

    def _spawn_boss(self) -> None:
        if self._boss is not None:
            try:
                self._boss.handlemessage(bs.DieMessage())
            except Exception:
                pass
            self._boss = None

        try:
            map_center = tuple(self.map.get_flag_position(None))
        except Exception:
            map_center = (0.0, 1.0, 0.0)

        player_count = 0
        try:
            player_count = sum(1 for player in self.players if player)
        except Exception:
            player_count = 1
        max_hp = BOSS_MAX_HP + max(0, player_count - 1) * BOSS_HP_PER_EXTRA_PLAYER

        self._boss = BossActor(
            activity=self,
            position=map_center,
            on_death=bs.WeakCallStrict(self._on_boss_died),
            assets=self._assets,
            max_hp=max_hp,
        )

    def _on_boss_died(self) -> None:
        self._boss = None
        self._respawn_timer = bs.timer(
            BOSS_RESPAWN_DELAY, bs.WeakCallStrict(self._spawn_boss))

    def on_expire(self) -> None:
        if self._boss is not None:
            try:
                self._boss.handlemessage(bs.DieMessage())
            except Exception:
                pass
            self._boss = None
        if self._respawn_timer is not None:
            try:
                self._respawn_timer.cancel()
            except Exception:
                pass
            self._respawn_timer = None
        # لغو تمام تایمرهای ریسپاون پلیرها
        for timer in self._respawn_timers.values():
            try:
                timer.cancel()
            except Exception:
                pass
        self._respawn_timers.clear()
        super().on_expire()

    def spawn_player(self, player: bs.Player) -> bs.Actor:
        return self.spawn_player_spaz(player)

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.PlayerDiedMessage):
            # مهم: اول به super() پاس بده تا خودِ موتور مکانیزمِ
            # استانداردِ مرگِ پلیر (ثبتِ آمار، پاک‌سازیِ داخلیِ اکتور
            # و آبجکت‌های وابسته مثلِ PowerupBoxِ حمل‌شده) کامل انجام
            # بشه.
            super().handlemessage(msg)
            player = msg.getplayer(bs.Player)
            # لغو تایمر قبلی اگر وجود داشت
            if player in self._respawn_timers:
                try:
                    self._respawn_timers[player].cancel()
                except Exception:
                    pass
                del self._respawn_timers[player]
            timer = bs.timer(5.0, bs.WeakCallStrict(self._respawn_player_safe, player))
            self._respawn_timers[player] = timer
            return None

        # فوروارد کردن OutOfBounds به باس
        if isinstance(msg, bs.OutOfBoundsMessage):
            if self._boss is not None:
                self._boss.handlemessage(msg)
            return super().handlemessage(msg)

        # هر پیامِ دیگه‌ای (ازجمله OutOfBoundsMessage که وقتی پلیر
        # یا هر شیءِ دیگه از مپ خارج می‌شه فرستاده می‌شه) باید همیشه
        # به پیاده‌سازیِ پیش‌فرضِ TeamGameActivity برسه، بدونِ هیچ
        # استثنایی. گم‌شدنِ این پیام‌ها همون چیزیه که باعثِ اسپمِ
        # ارور و در نهایت کرشِ گیم می‌شه.
        return super().handlemessage(msg)

    def _respawn_player_safe(self, player: bs.Player) -> None:
        # اگه پلیر دیگه توی سشن نیست (مثلاً خودش خارج شده)، کاری
        # نکن. وگرنه دوباره اسپاونش کن؛ این دقیقاً همون چیزیه که
        # spawn_player_spaz از طریقِ self.spawn_player انجام می‌ده.
        if player in self._respawn_timers:
            del self._respawn_timers[player]
        if not player:
            return
        try:
            if not player.exists():
                return
        except Exception:
            pass
        try:
            self.spawn_player(player)
        except Exception:
            pass


# ba_meta export babase.Plugin
class BossFightPlugin(babase.Plugin):
    """نقطه‌ی ثبتِ صریح برای تأییدِ لود‌شدنِ این ماژول."""

    def __init__(self) -> None:
        pass
