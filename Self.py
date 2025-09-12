# Auto Message v3.0 - API9
# Copyright 2025 - ByTaha
# ساخته شده توسط طاها استادشریف (@Taha_OstadSharif)
# این مود به صورت خودکار به پیام‌های دریافتی پاسخ می‌دهد
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
    app as APP,
    Call
)
from bascenev1 import (
    get_chat_messages as GCM,
    chatmessage as CM,
    get_connection_to_host_info_2 as get_connection_info,
    connect_to_party as original_connect,
    disconnect_from_host as original_disconnect,
    get_foreground_host_activity  # این خط را اضافه کنید
)
from _babase import get_string_width as strw
from datetime import datetime as DT
from bauiv1lib import party
from babase import apptimer as teck
from bauiv1lib.popup import PopupWindow, PopupMenu
from typing import Sequence, Tuple, Optional, Callable
from bauiv1lib.colorpicker import ColorPicker
import random
import math
import json
import os
import socket
import threading
import time
import bascenev1 as bs
import bauiv1 as bui
import _babase
import babase
import bascenev1 as bs
import bauiv1 as bui

# لیست جوک‌های فارسی کوتاه و متنوع
JOKES = [
    "پدر: درس خوندی؟ گفتم: خواب علمی بودم!",
    "مامان: گوشی دستته؟ گفتم: آپدیت زندگیه!",
    "همکار: چرا دیر اومدی؟ گفتم: ترافیک اینترنتی!",
    "دوست: چرا خسته‌ای؟ گفتم: تعطیلات تمرین میکنم!",
    "دختر: گرسنمه! گفتم: منم، برو مامان رو بگو!",
    "پسر: پول میخوام! گفتم: منم منتظر معجزم!",
    "فروشنده: تخفیف داریم! گفتم: پس فردا میام!",
    "همسر: دوسم داری؟ گفتم: بیشتر از دیروز!",
    "رئیس: چرا استرس داری؟ گفتم: تمرین آرامش میکنم!",
    "دکتر: ورزش کن! گفتم: چشم، کانال ورزشو نگاه!",
    "معلم: تکالیفتو نکردی؟ گفتم: فرصت طلایی دادم!",
    "پدر: بلند شو! گفتم: با تخت هنوز دعوامه!",
    "مامان: بیا کمک! گfتم: انرژی جمع میکنم!",
    "دختر: بیرون بریم! گفتم: مسافرت اینستا میرم!",
    "دوست: جواب نمیدی؟ گفتم: با خودم چت میکنم!",
    "پدر: درس نمیخونی؟ گفتم: استعدادم مخفیه!",
    "مامان: گوشی دستته؟ گفتم: بهش استراحت میدم!",
    "همکار: چرا شادابی؟ گفتم: قهوه و شوخی ترکیب!",
    "معلم: چرا خوابیدی؟ گفتم: رویای موفقیتت رو میبینم!",
    "پدر: بلند شو! گفتم: با بالش مبارزه میکنم!",
    "دختر: حوصلم سرره! گفتم: برو مامانو سرگرم کن!",
    "دوست: چرا ساکتی؟ گفتم: جا برای حرفت گذاشتم!",
    "رئیس: اشتباه کردی؟ گفتم: میخواستم انسان بودنم ثابت!",
    "فروشنده: این لباس؟ گفتم: بیشتر به پولم میاد!",
    "همسر: خرید کردی؟ گfتم: آره، با یه نون هم خرج!",
    "پسر: پیامم رو دیدی؟ گفتم: آره، تو خواب دیروز!",
    "دختر: گرسنمه! گفتم: منم، با هم گرسنگی کنیم!",
    "دوست: چرا جدی؟ گفتم: برای شوخی تمرین میکنم!",
    "رئیس: استعفا میدی؟ گفتم: مدیر شوخی میشم!",
    "معلم: نمیخندی؟ گfتم: دندونام سفید بمونه!",
    "پدر: نمیخونی؟ گfتم: استعدادمو مخفی میکنم!",
    "مامان: غذا نمیخوری؟ گfتم: تمرین گرسنگیمه!",
    "دوست: دیر اومدی؟ گfتم: راهو گم کردم، پیداش کردم!",
    "همکار: چرا شادابی؟ گfتم: قهوه با انرژی مثبت!",
    "دختر: ناراحتی؟ گfتم: برای شادی تمرین میکنم!",
    "پسر: بازی بخر! گfتم: منتظر قهرمان خریدم!",
    "فروشنده: این مدل؟ گfتم: قدیمیش هنوز خفن‌تره!",
    "همسر: کدومو دوست داری؟ گfتم: اونی که ساکته!",
    "رئیس: دیر کردی؟ گfتم: خواب بودم که دیر نشه!",
    "دکتر: دارو بخور! گfتم: چشم، بعد از اثرش!",
    "مامان: اتاقت رو تمیز کن! گfتم: حال طبیعی میدم!",
    "پدر: بلند شو! گfتم: با زمین کشتی میگیرم!",
    "معلم: نمیفهمی؟ گfتم: میخوام بیشتر توضیح بدید!",
    "دوست: جواب نمیدی؟ گfتم: با خودم چت میکنم!",
    "دختر: بیرون بریم! گfتم: الان مسافرت اینستا!",
    "پسر: پول میخوام! گfتم: منم منتظرم کسی بده!",
    "همکار: غمگینی؟ گfتم: برای شادی تمرین میکنم!",
    "دوست: چرا جدی‌ای؟ گfتم: برای شوخی تمرین میکنم!",
    "پدر: نمیخونی؟ گfتم: استعدادمو مخفی میکنم!",
    "مامان: غذا بخور! گfتم: الان رژیم فضایی دارم!",
    "رئیس: چرا اینکارو کردی؟ گfتم: ببینم توجه داری!",
    "فروشنده: تخفیف داریم! گfتم: پس فردا میام!",
    "همسر: دوسم داری؟ گfتم: بیشتر از دیروز، کمتر فردا!",
    "پسر: پول تو جیبی! گfتم: منم منتظرم!",
    "دختر: حوصلم سرره! گfتم: برو مامانو سرگرم کن!",
    "دوست: ساکتی؟ گfتم: جا برای حرفت گذاشتم!",
    "معلم: تکالیف؟ گfتم: میخواستم فرصت بدم!"
]

#ضرب المثل های فارسی کوتاه
PROVERBS = [
    "آب که از سر گذشت، چه یک وجب چه صد وجب.",
    "از کوزه همان برون تراود که در اوست.",
    "باد آورده را باد می‌برد.",
    "کار امروز را به فردا می‌انداز.",
    "هر که بامش بیش، برفش بیش‌تر.",
    "هرچه بکاری، همان را درو می‌کنی.",
    "نه هرکه چهره برافروخت، دل ربود.",
    "هر سخن جایی و هر نکته مکانی دارد.",
    "هر که طاووس خواهد، جور هندوستان کشد.",
    "دوستی کن اما دلبسته مباش.",
    "آفتاب مهربان‌تر از چراغ است.",
    "از دشمن باید بیم داشت، نه از دوست.",
    "دیگ به دیگ می‌گوید روت سیاه.",
    "تا نگوئی چرا، نمی‌فهمی.",
    "نه خانی آمده، نه خانی رفته.",
    "کوزه‌ای که نشکند، آب در آن نمی‌ماند.",
    "خشت اول چون نهد معمار کج، تا ثریا می‌رود دیوار کج.",
    "حساب پاک، دست پاک.",
    "کار نیکو کردن از پر کردن است.",
    "وقت طلاست.",
    "آب رفته را نمی‌توان به جوی بازگرداند.",
    "با دوستان باید مهربان بود.",
    "پیش از آنکه بخوری، ببین.",
    "خر خود را نشناسد، مردم چگونه بشناسند.",
    "قورباغه را دم اغشته می‌کنند.",
    "سیاه‌رویان همیشه در ظلمتند.",
    "دود از کنده بلند می‌شود.",
    "هر چه گوئی، گوش شنوا لازم است.",
    "ماه در آب پیدا نمی‌شود.",
    "گر صبر کنی، ز غوره حلوا سازی.",
    "بی‌صبر، بی‌کار.",
    "خنده بر هر درد بی‌درمان دواست.",
    "کار بزرگ را با قدم‌های کوچک شروع کن.",
    "چوب خدا صدا ندارد.",
    "عاقبت گرگ زاده گرگ شود.",
    "آب به آسیاب دشمن نریز.",
    "پایان شب سیه سپید است.",
    "سنگ بزرگ علامت نزدن است.",
    "پایان هر کار، شروع کار دیگر است.",
    "نه همه آنچه می‌درخشد طلاست.",
    "هر که bامش بیش، برfش بیش‌تر.",
    "با یک گل بهار نمی‌شود.",
    "کار را به اهلش بسپار.",
    "از این ستون تا آن ستون فرجی است.",
    "مار گزیده از ریسمان سیاه و سفید می‌ترسد.",
    "دو صد گفته، نیم کردار نیست.",
    "نه طوطی خوش است و نه سخن او.",
    "گربه دستش به گوشت نمی‌رسد، می‌گوید پیف پیف.",
    "کار نیکو کردن از پر کردن است.",
    "دیوار موش ندارد.",
    "هر که bامش بیش، برfش بیش‌تر.",
    "آب را گل نکن.",
    "گر صبر کنی، ز غوره حلوا سازی.",
    "یک دست صدا ندارد.",
    "آفتاب آمد دلیل آفتاب.",
    "کار امروز را به فردا می‌انداز.",
    "بی‌عقل، با عقل سر نمی‌کند.",
    "سختی کشیدن، آسانی می‌آورد.",
    "هر که bamش بیش، برfش بیش‌تر.",
    "یک ساعت فکر بهتر از صد ساعت کار بیهوده است.",
    "دوست آن باشد که در وقت تنگدستی یارت باشد.",
    "آتش گرفته را با آب خاموش می‌کنند.",
    "پیشگیری بهتر از درمان است.",
    "هر که صداقت داشت، نجات یافت."
]

#لیست چیستان های فارسی کوتاه
RIDDLES = [
    "سر داره بدن نداره؟ (سوزن)",
    "بالا میره پایین نمیاد؟ (سن)",
    "یک چشم داره نمی‌بینه؟ (سوزن)",
    "هر چی بدوی نمی‌رسی؟ (سایه)",
    "جلوته ولی دیده نمیشه؟ (آینده)",
    "پر از سوراخ آب نگه می‌داره؟ (اسفنج)",
    "می‌شکنه صدا نداره؟ (سکوت)",
    "پرواز می‌کنه بال نداره؟ (زمان)",
    "گرفته میشه پرتاب نمیشه؟ (سرما)",
    "هر چی برداری بزرگتر میشه؟ (چاله)",
    "تو دست میگیری لمس نمیشه? (نفس)",
    "می‌دوه پا نداره? (آب)",
    "حرف میزنه دهن نداره? (تلفن)",
    "راه میره نفس نمی‌کشه? (ساعت)",
    "از کوه رد میشه تکون نمیخوره? (جاده)",
    "همه می‌بینن دست نمیرسه? (ستاره)",
    "لباس داره تن نداره? (کتاب)",
    "استفاده کنی کوچیک میشه? (مداد)",
    "شب هست روز نیست? (ماه)",
    "اسمشو بیاری می‌شکنه? (سکوت)",
    "چهار پا داره راه نمیره? (میز)",
    "دندون داره گاز نمی‌گیره? (شونه)",
    "تو آب میره خیس نمیشه? (سایه)",
    "بیشتر بشه کمتر میبینی? (تاریکی)",
    "اول سبز وسط قرمز آخر سیاه? (زغال)",
    "هیچوقت کثیف نمیشه? (آینه)",
    "همه جا هست دیده نمیشه? (هوا)",
    "پرنده‌ست پر نداره? (بادبادک)",
    "می‌چرخه جایی نمیره? (پنکه)",
    "بدون پا حرکت میکنه? (مار)",
    "خیس میکنه خشک میشه? (حوله)",
    "سیاهه ولی روشن میکنه? (ذغال)",
    "می‌سوزه آتیش نداره? (شمع)",
    "صدا میده دیده نمیشه? (باد)",
    "پر باشه سبک‌تره? (بادکنک)",
    "پر غذاست نمی‌خوره? (یخچال)",
    "بالا پایین می‌پره پا نداره? (توپ)",
    "زرده همه رو روشن میکنه? (خورشید)",
    "هر جا بری دنبالت میاد? (سایه)",
    "وقتی رسیدی دیگه نیست? (فردا)",
    "میاد نمی‌مونه? (باران)",
    "همیشه گرسنه‌ست? (آتش)",
    "می‌دوه ولی نفس نداره? (ساعت شنی)",
    "روی زمین میاد کثیف نمیشه? (باران)",
    "پر از حرف ولی صدا نداره? (کتاب)",
    "بی‌بال پرواز میکنه? (خیال)",
    "بیشتر خرج کنی کوچیک میشه? (پول)",
    "دور می‌چرخه نور میده? (ماه)",
    "تو خونه‌ست راه میره? (مورچه)",
    "همیشه حرکت میکنه وای نمیسته? (زمان)",
    "همه جا هست جا نداره? (نور)",
    "بدون دهن می‌خنده? (ماسک)",
    "پا نداره ولی می‌ایسته? (عصا)",
    "بی‌زبان حرف میزنه? (چشم)",
    "هر روز میاد ولی پیر نمیشه? (خورشید)",
    "میاد و میره صدا میکنه? (باد)",
    "هیچ وقت نمیخوابه? (دریا)",
    "بی‌صدا گریه میکنه? (ابر)",
    "تکون نمیخوره ولی رشد میکنه? (گیاه)",
]

#جرعت
DARES = [
    "مثل مرغ قوقولی قوقو کن.",
    "ده ثانیه مثل پنگوئن راه برو.",
    "با لهجه شمالی حرف بزن.",
    "آهنگ عروسی را زمزمه کن.",
    "پشت سر هم سه تا پیف پیف بگو.",
    "یک داستان دروغ دو کلمه‌ای بگو.",
    "با چشم های بسته بچرخ و راه برو.",
    "یک آهنگ را با بینی ات بخوان.",
    "مثل یک ربات برقص.",
    "با دهان پر آب بخند.",
    "یک مدل موی مسخره درست کن.",
    "وانمود کن که گاو هستی.",
    "یک جمله را برعکس بگو.",
    "مثل بچه گربه میو میو کن.",
    "با دست غیرغالب خود بنویس.",
    "یک ایموجی مسخره با صورتت بساز.",
    "مثل فوتبالیستی گل بزن.",
    "با موز تلفن بازی کن.",
    "حرف بزن در حالی که زبانت بیرونه.",
    "یک کار کاملا تصادفی انجام بده.",
    "مثل خرگوش بپر.",
    "آهنگ کودکانه را بلند بخوان.",
    "خودت را به زور به خواب بزن.",
    "مثل دایناسور راه برو.",
    "با کفش هایت آب بخور.",
    "یک سالاد از تنقلات درست کن.",
    "مثل ماهی دهان باز کن و ببند.",
    "با بینی ات دکمه موبایل را بزن.",
    "مثل وزنه بردار ورزش کن.",
    "یک پیامک برای مخاطب آخرت بفرست.",
    "با چشم های بسته چیزی را لمس کن.",
    "مثل پرنده بال بزن.",
    "یک راز مسخره را فریاد بزن.",
    "مثل مارپیچ بچرخ.",
    "با دست و پا راه برو.",
    "مثل گورخر شیهه بکش.",
    "یک داستان ترسناک دو جمله ای بگو.",
    "مثل لاک پشت حرکت کن.",
    "با دهان بسته آواز بخوان.",
    "مثل میمون از درخت بالا برو.",
    "یک شکلک با سشوار درست کن.",
    "مثل جاروبرقی صدا دربیار.",
    "با پاشنه پا راه برو.",
    "مثل پروانه پرواز کن.",
    "یک شعر کودکانه بلند بخوان.",
    "مثل کرم حرکت کن.",
    "با بینی ات شکلک دربیار.",
    "مثل فرشته بال بزن.",
    "یک داستان عاشقانه دروغی بگو.",
    "مثل زنبور وزوز کن.",
    "با چشمان بسته نقاشی بکش.",
    "مثل اسب یورتمه برو.",
    "یک جوک مسخره تعریف کن.",
    "مثل قورباغه بپر.",
    "با دست هایت پازل درست کن.",
    "مثل فیل trumpet بزن.",
    "یک کار غیرمنتظره انجام بده.",
    "مثل شیر غرش کن.",
    "با پاهایت چیزی را بردار.",
    "مثل جیرجیرک صدا دربیار."
]

#حقیقت
TRUTHS = [
    "خجالت‌آورترین لحظه مدرسه‌ات را تعریف کن.",
    "اگر همیشه یک بوی خاص داشته باشی، چه بویی می‌خواهی باشد?",
    "بدترین هدیۀ تولدی که گرفتی چه بود?",
    "عجیب‌ترین چیزی که تا به حال خورده‌ای چیست?",
    "اگر مجبور باشی یک عضو بدنت را حذف کنی کدام است?",
    "اشتباهی که دوست داری از زندگی دیگران پاک کنی کدام است?",
    "اگر روح یک حیوان در تو حلول کند، کدام حیوان است?",
    "بدترین nickname ای که داشته‌ای چه بوده?",
    "اگر یک وسیله خانه باشی، کدام وسیله هستی?",
    "مسخره‌ترین دلیلی که برای گریه کردن داشته‌ای چیست?",
    "اگر برای 24 ساعت نامرئی شوی چه کار می‌کنی?",
    "بدترین مدل مو یا رنگی که داشته‌ای چیست?",
    "اگر یک غذای بنجل بتوانی باشی، کدام هستی?",
    "عجیب‌ترین خرافاتی که به آن اعتقاد داری چیست?",
    "اگر بتوانی صداهای بدن کسی را کنترل کنی، چه می‌کنی?",
    "مسخره‌ترین چیزی که به آن افتخار می‌کنی چیست?",
    "اگر مجبور باشی فقط یک اپلیکیشن داشته باشی کدام است?",
    "بدترین لباسی که پوشیده‌ای و فکر می‌کردی خفن است?",
    "اگر یک مشکل کوچک بتواند همیشه آزارت دهد، کدام است?",
    "عجیب‌ترین ترسی که در کودکی داشتی چیست?",
    "اگر بتوانی یک صدای مزاحم را برای همیشه حذف کنی کدام است?",
    "مسخره‌ترین درگیری که در شبکه‌های اجتماعی داشته‌ای?",
    "اگر بتوانی یک عادت بد همه را اصلاح کنی، کدام است?",
    "بدترین شغلی که می‌توانی تصور کنی چیست?",
    "اگر مجبور باشی یک کلمه را همیشه غلط تلفظ کنی کدام است?",
    "عجیب‌ترین چیزی که در مورد جنس مخالف نمی‌فهمی چیست?",
    "اگر یک وسیله آشپزخانه باشی، کدام هستی?",
    "مسخره‌ترین دلیلی که برای دعوا داشته‌ای چیست?",
    "اگر بتوانی یک حس را برای همیشه حذف کنی کدام است?",
    "بدترین خرید زندگی‌ات چیست?",
    "اگر یک بیماری مسخره داشته باشی، چه بیماری است?",
    "عجیب‌ترین خوابی که در مکان عمومی دیده‌ای چیست?",
    "اگر بتوانی یک صدا را با بینی ات دربیاوری کدام است?",
    "مسخره‌ترین اشتباهی که در یک امتحان داشته‌ای چیست?",
    "اگر مجبور باشی همیشه یک آهنگ زمزمه کنی کدام است?",
    "بدترین توصیه‌ای که به کسی کرده‌ای چیست?",
    "اگر یک نقص فنی کوچک در تو باشد چیست?",
    "عجیب‌ترین چیزی که برای آرامش خود انجام می‌دهی?",
    "اگر بتوانی یک کار خانه را برای همیشه حذف کنی کدام است?",
    "مسخره‌ترین حرفی که در خواب گفته‌ای چیست?",
    "اگر یک ابرقهرمان با قدرت بی‌فایده باشی، قدرتت چیست?",
    "بدترین چیزی که از کسی تقلید کرده‌ای چیست?",
    "اگر بتوانی یک قانون فیزیکی را نقض کنی کدام است?",
    "عجیب‌ترین دلیلی که باعث شد کسی را دوست داشته باشی?",
    "اگر مجبور باشی یک овоح باشی، کدام هستی?",
    "مسخره‌ترین دروغی که در کودکی گفته‌ای چیست?",
    "اگر یک مشکل نرم افزاری در تو باشد چیست?",
    "بدترین پیشبینی که در مورد تو شده چیست?",
    "اگر بتوانی یک صدای بدن را کنترل کنی کدام است?",
    "عجیب‌ترین چیزی که در طبیعت تو را آزار می‌دهد?",
    "اگر مجبور باشی همیشه یک داستان تکراری تعریف کنی کدام است?",
    "مسخره‌ترین اشتباه لپی که داشته‌ای چیست?",
    "اگر یک نقص طراحی در تو باشد چیست?",
    "بدترین تجربه آرایشگاه یا سلمانی تو چیست?",
    "اگر بتوانی یک کار روزمره را حذف کنی کدام است?",
    "عجیب‌ترین چیزی که باعث اضطراب تو می‌شود چیست?",
    "اگر مجبور باشی یک کلمه را هرگز نگویی کدام است?",
    "مسخره‌ترین چیزی که از آن می‌ترسی چیست?"
]

def generate_fonts(text: str) -> dict:
    fonts = {
        "Bold": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                              "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭"
                              "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇"),
        "Italic": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                "𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁"
                                "𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛"),
        "Cursive": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                 "𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵"
                                 "𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏"),
        "DoubleStruck": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                      "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"
                                      "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫"),
        "Fraktur": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                 "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ"
                                 "𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷"),
        "Parentheses": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                     "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ"
                                     "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ"),
        "Tiny": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                              "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ"
                              "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ"),
        "Serif": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                               "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾᵠᴿˢᵀᵁⱽᵂˣʸᶻ"
                               "ᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖᑫʳˢᵗᵘᵛʷˣʸᶻ"),
        "Monospace": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                   "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉"
                                   "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣"),
        "SmallCaps": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                   "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                                   "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ"),
        "Bubble": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩"
                                "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩"),
        "Squares": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                 "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉"
                                 "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉"),
        "Wide": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                              "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"
                              "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"),
        # 20 فونت جدید اضافه شده
        "Circle": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                               "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ"
                               "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ"),
        "Negative": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                 "🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉"
                                 "🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉"),
        "Script": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                               "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩"
                               "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃"),
        "Gothic": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                               "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ"
                               "𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷"),
        "MathBold": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                 "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙"
                                 "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳"),
        "MathItalic": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                   "𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍"
                                   "𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧"),
        "MathBoldItalic": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                       "𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁"
                                       "𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛"),
        "MathScript": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                   "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩"
                                   "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃"),
        "MathDoubleStruck": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                         "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"
                                         "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫"),
        "MathFraktur": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                    "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ"
                                    "𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷"),
        "MathSans": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                 "𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹"
                                 "𝖺𝖻𝖼𝖽𝖾𝖿𝗀𝗁𝗂𝗃𝗄𝗅𝗆𝗇𝗈𝗉𝗊𝗋𝗌𝗍𝗎𝗏𝗐𝗑𝗒𝗓"),
        "MathSansBold": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                     "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭"
                                     "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇"),
        "MathSansItalic": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                       "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡"
                                       "𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻"),
        "MathSansBoldItalic": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                           "𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕"
                                           "𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯"),
        "SmallCaps2": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                   "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                                   "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ"),
        "FullWidth": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                  "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"
                                  "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕ｣ｗｘｙｚ"),
        "Squared": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉"
                                "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉"),
    }
    return {name: text.translate(trans) for name, trans in fonts.items()}

# تاس‌های مختلف
DICE = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]

# پیام‌های پیش‌فرض چت سریع
DEFAULT_QUICK_MESSAGES = [
    "سلام!",
    "چطوری?",
    "باحال بود!",
    "بیا بازی کنیم",
    "مرسی",
    "خداحافظ",
    "اوکی",
    "بزن بریم"
]

# متغیرهای پینگ و اطلاعات سرور - واقعی
current_ping = 0.0
server_ip = "127.0.0.1"
server_port = 43210
server_name = "Local Server"

# تعریف متغیرهای global
original_buttonwidget = bui.buttonwidget
original_containerwidget = bui.containerwidget
original_checkboxwidget = bui.checkboxwidget
original_have_pro = None
original_add_transaction = bui.app.plus.add_v1_account_transaction

# اورراید کردن تابع connect برای گرفتن آیپی واقعی
def new_connect_to_party(address, port=43210, print_progress=False):
    global server_ip, server_port
    server_ip = address
    server_port = port
    print(f"اتصال به سرور: {address}:{port}")
    return original_connect(address, port, print_progress)

# اورراید کردن disconnect
def new_disconnect_from_host():
    global server_ip, server_port
    server_ip = "127.0.0.1"
    server_port = 43210
    print("قطع اتصال از سرور")
    return original_disconnect()

"""کلاس thread برای بررسی پینگ واقعی"""
class RealPingThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.running = True

    def run(self):
        global current_ping
        while self.running:
            try:
                if server_ip != "127.0.0.1" and server_port != 43210:
                    # پینگ واقعی با استفاده از سوکت
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.settimeout(1)
                    start_time = time.time()
                    
                    # ارسال بسته پینگ (همانند بازی)
                    sock.sendto(b'\x0b', (server_ip, server_port))
                    
                    try:
                        # دریافت پاسخ
                        data, addr = sock.recvfrom(10)
                        if data == b'\x0c':  # پونگ
                            ping = (time.time() - start_time) * 1000.0
                            current_ping = round(ping, 2)
                        else:
                            current_ping = 999
                    except socket.timeout:
                        current_ping = 999
                    except:
                        current_ping = 0
                    finally:
                        sock.close()
                else:
                    current_ping = 0
            except:
                current_ping = 0
            
            time.sleep(1)  # هر 1 ثانیه بروزرسانی

    def stop(self):
        self.running = False

# اورراید کردن توابع اصلی بازی
original_connect = None
original_disconnect = None

"""تبدیل تاریخ میلادی به شمسی"""
def gregorian_to_jalali(gy, gm, gd):
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if gm > 2:
        gy2 = gy + 1
    else:
        gy2 = gy
    days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
    jy = -1595 + (33 * (days // 12053))
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if days > 365:
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if days < 186:
        jm = 1 + (days // 31)
        jd = 1 + (days % 31)
    else:
        jm = 7 + ((days - 186) // 30)
        jd = 1 + ((days - 186) % 30)
    return jy, jm, jd

"""افزودن پاسخ"""
class Add:
    def __init__(s,t):
        w = AR.cw(
            source=t,
            size=(500,295),
            ps=AR.UIS()*0.8
        )
        # افزودن دکمه بستن
        AR.add_close_button(w, position=(460, 260))
        
        a = []
        for i in range(2):
            j = ['اگر پیدا شد','پاسخ با'][i]
            tw(
                parent=w,
                text=j+':',
                position=(30,250-70*i)
            )
            t = tw(
                parent=w,
                maxwidth=230,
                size=(230,30),
                editable=True,
                v_align='center',
                color=(0.75,0.75,0.75),
                position=(30,218-70*i),
                allow_clear_button=False
            )
            a.append(t)
            AR.bw(
                parent=w,
                size=(20,30),
                iconscale=1.3,
                icon=gt('file'),
                position=(265,218-70*i),
                on_activate_call=Call(s.paste,a[i])
            )
        for i in range(2):
            tw(
                parent=w,
                text=['بعد از','ثانیه'][i],
                position=(30+160*i,105)
            )
        s.t = tw(
            parent=w,
            size=(90,30),
            editable=True,
            text=var('time'),
            h_align='center',
            position=(95,105),
            color=(0.75,0.75,0.75),
            allow_clear_button=False
        )
        s.cbv = False
        s.cb = cb(
            parent=w,
            size=(250,30),
            position=(27.5,65),
            text='جستجو در پیام',
            value=s.cbv,
            on_value_change_call=Call(setattr,s,'cbv'),
            color=(0.75,0.75,0.75),
            textcolor=(1,1,1),
        )
        tw(
            parent=w,
            scale=0.5,
            position=(300,200),
            text = f'💬 %m: نام شما\n\
📨 %s: نام فرستنده\n⏰ %t: زمان فعلی\n📅 %d: تاریخ میلادی\n🗓 %f: تاریخ شمسی\n😂 %j: جوک تصادفی\n🧩 %ch: چیستان کوتاه\n📜 %z: ضرب المثل\n🎰 %dice: شرط بندی (تاس)\n❓ %tr: بازی جرعت یا حقیقت (حقیقت)\n🔍 %da: بازی جرعت یا حقیقت (جرعت)\n🌐 %ip: ایپی و پورت سرور\n📡 %p : ارسال پینگ',
            maxwidth=190,
            color=(1,1,0)
        )
        AR.bw(
            parent=w,
            label='افزودن',
            size=(50,35),
            position=(230,25),
            on_activate_call=Call(s._add,a)
        )
        AR.swish()
    """واقعاً اضافه کن"""
    def _add(s,a):
        z = tw(query=s.t)
        try: z = float(z)
        except: AR.err('زمان نامعتبر است. ورودی خود را اصلاح کنید!'); return
        var('time',str(z))
        i,j = [tw(query=t).strip().replace('\n',' ') for t in a]
        if not i or not j: AR.err('چیزی بنویسید!'); return
        l = var('l') or {}
        lc = var('lc') or {}
        ic = i.lower()
        if ic in lc: AR.err('ماشه از قبل وجود دارد!'); return
        l.update({i:(j,z,s.cbv)})
        lc.update({ic:(j,z,s.cbv)})
        var('l',l)
        var('lc',lc)
        [tw(t,text='') for t in a]
        AR.ok()
    """چسباندن"""
    def paste(s,t):
        if not CIS(): AR.err('پشتیبانی نمی‌شود!'); return
        if not CHT(): AR.err('کلیپ‌بورد شما خالی است!'); return
        tw(t,text=CGT().replace('\n',' '),color=(0,1,0))
        gs('gunCocking').play()
        teck(0.3,Call(tw,t,color=(1,1,1)))

"""حذف یک پاسخ"""
class Nuke:
    def __init__(s,t):
        i = len(var('l'))
        if not i: AR.err('ابتدا چند ماشه اضافه کنید!'); return
        w = AR.cw(
            source=t,
            size=(260,350),
            ps=AR.UIS()*0.5
        )
        # افزودن دکمه بستن
        AR.add_close_button(w, position=(250, 315))
        
        a = sw(
            parent=w,
            size=(220,290),
            position=(20,40)
        )
        s.c = cw(
            parent=a,
            size=(220,i*30),
            background=False
        )
        AR.bw(
            parent=w,
            label='حذف',
            size=(60,25),
            position=(180,10),
            on_activate_call=Call(s._nuke)
        )
        s.kids = []
        s.sl = None
        s.fresh()
        AR.swish()
    """واقعاً حذف کن"""
    def _nuke(s):
        if s.sl is None: AR.err('چیزی انتخاب کنید!'); return
        l = var('l')
        lc = var('lc')
        l.pop(list(l)[s.sl])
        lc.pop(list(lc)[s.sl])
        var('l',l)
        var('lc',lc)
        s.sl = None
        s.fresh()
        AR.bye()
    """تازه کردن"""
    def fresh(s):
        [k.delete() for k in s.kids]
        s.kids.clear()
        l = var('l'); k = list(l); j = len(l)
        [s.kids.append(tw(
            text=k[i],
            parent=s.c,
            size=(220,30),
            selectable=True,
            click_activate=True,
            position=(0,(30*j)-30*(i+1)),
            on_activate_call=Call(s.hl,i),
        )) for i in range(j)]
        cw(s.c,size=(220,j*30))
    """هایلایت"""
    def hl(s,i):
        [tw(t,color=(1,1,1)) for t in s.kids]
        tw(s.kids[i],color=(0,1,0))
        s.sl = i

"""تنظیمات"""
class Tune:
    def __init__(s,t):
        w = AR.cw(
            source=t,
            size=(350, 250),  # ارتفاع را افزایش دهید
            ps=AR.UIS()*0.8
        )
        # افزودن دکمه بستن
        AR.add_close_button(w, position=(315, 215))
        
        AR.swish()
        for i in range(5):  # از 4 به 5 تغییر دهید
            j = [
                'اعلان هنگام پاسخ',
                'صدای زنگ هنگام پاسخ',
                'پاسخ به '+byTaha.me(),
                'حساس به حروف',
                'کنترل سرعت بازی'  # گزینه جدید
            ][i]
            c = f'tune{i}'
            if i == 4:  # برای گزینه کنترل سرعت
                bw(
                    parent=w,
                    label=j,
                    size=(290, 30),
                    position=(30, 20+40*i),
                    on_activate_call=Call(SpeedControl, w),
                    color=(0.3, 0.5, 0.8),
                    textcolor=(1, 1, 1)
                )
            else:
                chk(
                    text=j,
                    parent=w,
                    size=(290, 30),
                    textcolor=(1, 1, 1),
                    value=var(c),
                    position=(30, 20+40*i),
                    color=(0.13, 0.13, 0.13),
                    on_value_change_call=Call(var,c)
                )
                
"""تنظیمات"""
class Tune:
    def __init__(s,t):
        w = AR.cw(
            source=t,
            size=(350, 250),  # ارتفاع را افزایش دهید
            ps=AR.UIS()*0.8
        )
        # افزودن دکمه بستن
        AR.add_close_button(w, position=(315, 215))
        
        AR.swish()
        for i in range(5):  # از 4 به 5 تغییر دهید
            j = [
                'اعلان هنگام پاسخ',
                'صدای زنگ هنگام پاسخ',
                'پاسخ به '+byTaha.me(),
                'حساس به حروف',
                'کنترل سرعت بازی'  # گزینه جدید
            ][i]
            c = f'tune{i}'
            if i == 4:  # برای گزینه کنترل سرعت
                bw(
                    parent=w,
                    label=j,
                    size=(290, 30),
                    position=(30, 20+40*i),
                    on_activate_call=Call(SpeedControl, w),
                    color=(0.3, 0.5, 0.8),
                    textcolor=(1, 1, 1)
                )
            else:
                chk(
                    text=j,
                    parent=w,
                    size=(290, 30),
                    textcolor=(1, 1, 1),
                    value=var(c),
                    position=(30, 20+40*i),
                    color=(0.13, 0.13, 0.13),
                    on_value_change_call=Call(var,c)
                )

"""لیست پاسخ‌ها"""
class List:
    def __init__(s,t):
        i = len(var('l'))
        if not i: AR.err('ابتدا چند ماشه اضافه کنید!'); return
        w = AR.cw(
            source=t,
            size=(450,300),
            ps=AR.UIS()*0.8
        )
        # افزودن دکمه بستن
        AR.add_close_button(w, position=(440, 265))
        
        a = sw(
            parent=w,
            size=(150,260),
            position=(30,20)
        )
        s.c = cw(
            parent=a,
            size=(220,i*30),
            background=False,
        )
        s.txt = []
        for i in range(3):
            j = ['ماشه','پاسخ','تجزیه شده'][i]
            k = [(0,1,1),(1,1,0),(1,0,1)][i]
            tw(
                color=k,
                parent=w,
                text=j+':',
                position=(190,240-80*i)
            )
            t = tw(
                parent=w,
                maxwidth=250,
                max_height=60,
                v_align='top',
                position=(190,215-80*i)
            )
            s.txt.append(t)
        bw(
            parent=w,
            position=(390,240),
            size=(40,40),
            label='',
            texture=gt('achievementEmpty'),
            on_activate_call=s.info,
            color=(1,1,1),
            enable_sound=False
        )
        s.kids = []
        s.sl = None
        s.fresh()
        AR.swish()
    """نمایش اطلاعات"""
    def info(s):
        i = s.sl
        if i is None: AR.err('ابتدا یک ماشه انتخاب کنید!'); return
        a,b,c = list(var('l').items())[i][1]
        push(f'ترتیب ماشه: {i+1}\nپاسخ پس از: {b} ثانیه\nویلدکارت: {c}')
        gs('tap').play()
    """تازه کردن"""
    def fresh(s):
        [k.delete() for k in s.kids]
        s.kids.clear()
        l = var('l'); k = list(l); j = len(l)
        [s.kids.append(tw(
            text=k[i],
            parent=s.c,
            size=(150,30),
            selectable=True,
            click_activate=True,
            position=(0,(30*j)-30*(i+1)),
            on_activate_call=Call(s.hl,i),
        )) for i in range(j)]
        cw(s.c,size=(220,j*30))
    """هایلایت"""
    def hl(s,i):
        [tw(t,color=(1,1,1)) for t in s.kids]
        tw(s.kids[i],color=(0,1,0))
        s.sl = i
        l = var('l')
        v = list(l)[i]
        r = l[v][0]
        p = AR.parse(t=r)
        [tw(s.txt[i],text=sn([v,r,p][i])) for i in range(3)]

"""چت سریع"""
class QuickChat:
    def __init__(s, t):
        w = s.w = AR.cw(
            source=t,
            size=(400, 300),
            ps=AR.UIS()*0.8
        )
        # افزودن دکمه بستن
        AR.add_close_button(w, position=(370, 265))
        
        # عنوان
        tw(
            parent=w,
            text='چت سریع',
            scale=1.2,
            position=(180, 250),
            h_align='center',
            color=(1, 1, 0)
        )
        
        # اسکرول برای نمایش پیام‌ها
        s.scroll = sw(
            parent=w,
            size=(360, 150),
            position=(20, 70)
        )
        s.container = cw(
            parent=s.scroll,
            size=(360, 400),
            background=False
        )
        
        # دکمه‌های مدیریت (با اضافه کردن دکمه بازنشانی)
        buttons = [
            ('افزودن', s.add_message, (20, 15)),
            ('حذف', s.remove_message, (150, 15)),
            ('بازنشانی', s.reset_messages, (280, 15)),
        ]
        
        for label, callback, pos in buttons:
            AR.bw(
                parent=w,
                label=label,
                size=(90, 35),
                position=pos,
                on_activate_call=callback
            )
        
        s.refresh_messages()
        AR.swish()
    
    def refresh_messages(s):
        # پاک کردن پیام‌های قبلی
        for child in s.container.get_children():
            child.delete()
        
        # بارگذاری پیام‌ها
        messages = load_quick_messages()
        
        # نمایش پیام‌ها با قابلیت اسکرول
        y_pos = len(messages) * 43 - 25
        for msg in messages:
            btn = bw(
                parent=s.container,
                label=msg[:30] + '...' if len(msg) > 30 else msg,
                size=(340, 40),
                position=(10, y_pos),
                on_activate_call=Call(s.send_message, msg),
                color=(0.3, 0.5, 0.8),
                textcolor=(1, 1, 1)
            )
            y_pos -= 45
        
        # تنظیم اندازه کانتینر برای اسکرول
        cw(s.container, size=(360, len(messages) * 45))
    
    def send_message(s, message):
        try:
            CM(message)
            push(f'ارسال شد: {message}', color=(0, 1, 0))
            gs('dingSmall').play()
            AR.swish(s.w)  # بستن پنجره پس از ارسال
        except Exception as e:
            AR.err(f'خطا در ارسال: {str(e)}')
    
    def add_message(s):
        def save_new():
            new_msg = tw(query=txt_widget).strip()
            if new_msg:
                messages = load_quick_messages()
                if new_msg not in messages:
                    messages.append(new_msg)
                    save_quick_messages(messages)
                    s.refresh_messages()
                    push(f'اضافه شد: "{new_msg}"', color=(0, 1, 0))
                    gs('dingSmallHigh').play()
                else:
                    AR.err('این پیام از قبل وجود دارد!')
            AR.swish(win)
        
        win = AR.cw(
            source=s.w,
            size=(300, 140),
            ps=AR.UIS()*0.6
        )
        
        # افزودن دکمه بستن
        AR.add_close_button(win, position=(250, 105))
        
        tw(
            parent=win,
            text='پیام جدید:',
            position=(20, 90),
            scale=0.9,
            color=(1, 1, 1)
        )
        
        txt_widget = tw(
            parent=win,
            position=(20, 60),
            size=(260, 30),
            editable=True,
            text='',
            color=(0.9, 0.9, 0.9)
        )
        
        AR.bw(
            parent=win,
            label='تأیید',
            size=(80, 30),
            position=(60, 20),
            on_activate_call=save_new
        )
        
        AR.bw(
            parent=win,
            label='انصراف',
            size=(80, 30),
            position=(160, 20),
            on_activate_call=Call(AR.swish, win)
        )
    
    def remove_message(s):
        messages = load_quick_messages()
        
        if not messages:
            AR.err('پیامی برای حذف وجود ندارد!')
            return
        
        # ایجاد پنجره لیست پیام‌ها برای حذف
        win = AR.cw(
            source=s.w,
            size=(350, min(450, 200 + len(messages) * 45)),
            ps=AR.UIS()*0.6
        )
        
        # افزودن دکمه بستن
        AR.add_close_button(win, position=(350, 350))
        
        # عنوان
        tw(
            parent=win,
            text='پیام را برای حذف انتخاب کنید:',
            scale=1.0,
            position=(150, min(400, 0 + len(messages) * 45)),
            h_align='center',
            color=(1, 1, 0)
        )
        
        # اسکرول برای لیست پیام‌ها
        scroll = sw(
            parent=win,
            size=(330, min(300, 100 + len(messages) * 40)),
            position=(10, 50)
        )
        
        container = cw(
            parent=scroll,
            size=(330, len(messages) * 45),
            background=False
        )
        
        # نمایش پیام‌ها به صورت لیست با اسکرول
        y_pos = len(messages) * 44 - 25
        for msg in messages:
            bw(
                parent=container,
                label=f'حذف: {msg[:20]}...' if len(msg) > 20 else f'حذف: {msg}',
                size=(310, 40),
                position=(10, y_pos),
                on_activate_call=Call(s.confirm_remove, msg, win),
                color=(0.8, 0.2, 0.2),
                textcolor=(1, 1, 1)
            )
            y_pos -= 45
    
    def confirm_remove(s, msg, parent_win):
        messages = load_quick_messages()
        if msg in messages:
            messages.remove(msg)
            save_quick_messages(messages)
            s.refresh_messages()
            push(f'حذف شد: "{msg}"', color=(1, 0.5, 0))
            gs('dingSmallLow').play()
        AR.swish(parent_win)
    
    def reset_messages(s):
        save_quick_messages(DEFAULT_QUICK_MESSAGES.copy())
        s.refresh_messages()
        push('پیام‌ها به حالت پیش‌فرض بازنشانی شدند', color=(0, 1, 1))
        gs('dingSmallHigh').play()

"""جوین دوباره (اتصال مجدد)"""
class Reconnect:
    def __init__(s, t):
        w = s.w = AR.cw(
            source=t,
            size=(350, 200),
            ps=AR.UIS()*0.8
        )
        # افزودن دکمه بستن
        AR.add_close_button(w, position=(320, 165))
        
        # عنوان
        tw(
            parent=w,
            text='اتصال مجدد',
            scale=1.2,
            position=(160, 170),
            h_align='center',
            color=(0, 1, 1)
        )
        
        # نمایش اطلاعات سرور فعلی
        s.server_info = tw(
            parent=w,
            text=f'سرور فعلی:\nIP :{server_ip}\nPORT : {server_port}',
            position=(155, 140),
            scale=0.8,
            color=(1, 1, 1),
            h_align='center',
            maxwidth=300
        )
        
        # دکمه اتصال مجدد
        s.reconnect_btn = AR.bw(
            parent=w,
            label='اتصال مجدد',
            size=(120, 50),
            position=(115, 30),
            on_activate_call=s.do_reconnect,
            icon=gt('replayIcon')
        )
        
        # دکمه قطع اتصال
        s.disconnect_btn = AR.bw(
            parent=w,
            label='قطع اتصال',
            size=(120, 50),
            position=(115, 15),
            on_activate_call=s.do_disconnect,
            icon=gt('closeIcon'),
            color=(0.8, 0.2, 0.2)
        )
        
        # تایمر برای بروزرسانی اطلاعات
        teck(1.0, s.update_info)
        AR.swish()
    
    def update_info(s):
        """بروزرسانی اطلاعات سرور"""
        if hasattr(s, 'server_info') and s.server_info.exists():
            conn_info = get_connection_info()
            status = "متصل" if conn_info else "قطع"
            
            tw(s.server_info, 
               text=f'وضعیت: {status}\n'
                    f'سرور: {server_ip}:{server_port}\n'
                    f'پینگ: {current_ping} ms')
        
        # ادامه بروزرسانی
        teck(1.0, s.update_info)
    
    def do_reconnect(s):
        """انجام اتصال مجدد"""
        try:
            if server_ip != "127.0.0.1" and server_port != 43210:
                # قطع اتصال فعلی اگر وجود دارد
                conn_info = get_connection_info()
                if conn_info:
                    original_disconnect()
                    push('قطع اتصال...', color=(1, 0.5, 0))
                    time.sleep(1)
                
                # اتصال مجدد
                push(f'اتصال به {server_ip}:{server_port}...', color=(0, 1, 0))
                new_connect_to_party(server_ip, server_port)
                gs('dingSmallHigh').play()
            else:
                AR.err('هیچ سروری برای اتصال وجود ندارد!')
        except Exception as e:
            AR.err(f'خطا در اتصال: {str(e)}')
    
    def do_disconnect(s):
        """قطع اتصال"""
        try:
            conn_info = get_connection_info()
            if conn_info:
                original_disconnect()
                push('اتصال قطع شد', color=(1, 0, 0))
                gs('dingSmallLow').play()
            else:
                AR.err('شما به سروری متصل نیستید!')
        except Exception as e:
            AR.err(f'خطا در قطع اتصال: {str(e)}')
#سرعت بازی            
class SpeedControl:
    def __init__(self, source):
        self._root_widget = bui.containerwidget(
            parent=bui.get_special_widget('overlay_stack'),
            size=(1000, 700),
            scale=0.7,
            transition='in_scale',
            color=(0.18, 0.18, 0.18),
            on_outside_click_call=self.close
        )
        
        # عنوان
        bui.textwidget(
            parent=self._root_widget,
            text='کنترل سرعت بازی',
            scale=3.0,
            position=(500, 600),
            h_align='center',
            color=(1, 1, 0)
        )
        
        # دکمه‌های حالت‌های سرعت - موقعیت‌ها را اصلاح کردم
        speed_modes = [
            ('عادی (1.0x)', 1.0, (80, 400)),
            ('اسلو (0.7x)', 0.7, (80, 290)),
            ('آپیک (0.5x)', 0.5, (80, 180)),
            ('اولترا اسلو (0.3x)', 0.3, (80, 70))
        ]
        
        for label, speed, pos in speed_modes:
            bui.buttonwidget(
                parent=self._root_widget,
                label=label,
                size=(900, 120),  # ارتفاع را کمی کاهش دادم
                position=pos,
                on_activate_call=lambda s=speed, l=label: self.set_speed(s, l),
                color=(0.3, 0.5, 0.8),
                textcolor=(1, 1, 1),
                text_scale=2.5  # متن را گنده‌تر کردم
            )
        
        # دکمه بستن - موقعیت و اندازه را اصلاح کردم
        bui.buttonwidget(
            parent=self._root_widget,
            label='بستن',
            size=(150, 100),
            position=(850, 600),
            on_activate_call=self.close,
            color=(0.8, 0.2, 0.2),
            textcolor=(1, 1, 1),
            text_scale=1.8  # متن دکمه بستن را گنده‌تر کردم
        )
    
    def set_speed(self, speed, label):
        """تنظیم سرعت بازی"""
        try:
            activity = bs.get_foreground_host_activity()
            if activity and hasattr(activity, 'globalsnode'):
                activity.globalsnode.slow_motion = speed
                bui.screenmessage(f'حالت سرعت: {label}', color=(0, 1, 0))
                bui.getsound('dingSmallHigh').play()
                self.close()
            else:
                bui.screenmessage('فعالیت بازی یافت نشد!', color=(1, 0, 0))
        except Exception as e:
            bui.screenmessage(f'خطا در تنظیم سرعت: {str(e)}', color=(1, 0, 0))
    
    def close(self):
        bui.containerwidget(self._root_widget, transition='out_scale')
            
"""Server Information"""
class ServerInfo:
    def __init__(s, t):
        w = s.w = AR.cw(
            source=t,
            size=(400, 350),
            ps=AR.UIS()*0.8
        )
        # افزودن دکمه بستن
        AR.add_close_button(w, position=(370, 290))
        
        # عنوان
        tw(
            parent=w,
            text='Server Information',
            scale=1.2,
            position=(180, 280),
            h_align='center',
            color=(0, 1, 1)
        )
        
        # دریافت اطلاعات سرور
        global server_ip, server_port, current_ping
        
        # دریافت اطلاعات اتصال
        conn_info = get_connection_info()
        if conn_info:
            server_name = conn_info.name
            server_status = "Connected"
        else:
            server_name = "Local Server"
            server_status = "Local"
        
        # ایجاد ویجت‌های متن برای اطلاعات سرور
        s.info_widgets = []
        info_labels = [
            "🌐 Server IP:",
            "🚪 Server Port:", 
            "🏷️ Server Name:",
            "📶 Current Ping:",
            "🔗 Connection Status:"
        ]
        
        y_pos = 250
        for i, label in enumerate(info_labels):
            # برچسب
            tw(
                parent=w,
                text=label,
                position=(30, y_pos),
                scale=0.8,
                color=(1, 1, 0.8),
                h_align='left'
            )
            # مقدار - تنظیم موقعیت برای همه مقادیر 30 پیکسل به راست
            value_x = 230 # همه مقادیر 30 پیکسل به راست نسبت به قبل
            
            value_widget = tw(
                parent=w,
                text="",  # مقدار اولیه خالی
                position=(value_x, y_pos),
                scale=0.8,
                color=(1, 1, 1),
                h_align='left'
            )
            s.info_widgets.append(value_widget)
            y_pos -= 30
        
        # مقادیر اولیه
        s.update_server_info()
        
        # دکمه‌های کپی
        copy_buttons = [
            ('کپی آیپی', server_ip, (20, 70)),
            ('کپی پورت', str(server_port), (150, 70)),
            ('کپی همه', f"{server_ip}:{server_port}", (280, 70))
        ]
        
        for label, data, pos in copy_buttons:
            AR.bw(
                parent=w,
                label=label,
                size=(100, 35),
                position=pos,
                on_activate_call=Call(s.copy_to_clipboard, data)
            )
        # شروع تایمر برای بروزرسانی خودکار
        s.timer = teck(1.0, s.update_server_info)
        AR.swish()
    
    def update_server_info(s):
        """بروزرسانی اطلاعات سرور"""
        if not hasattr(s, 'w') or not s.w.exists():
            return
        
        # دریافت اطلاعات اتصال
        conn_info = get_connection_info()
        
        if conn_info:
            server_name = conn_info.name
            server_status = "Connected"
        else:
            server_name = "Local Server"
            server_status = "Local"
        
        # مقادیر برای نمایش
        values = [
            server_ip,
            str(server_port),
            server_name,
            f"{current_ping} ms",
            server_status
        ]
        
        # بروزرسانی ویجت‌های متن
        for i, value in enumerate(values):
            if i < len(s.info_widgets) and s.info_widgets[i].exists():
                tw(s.info_widgets[i], text=value)
        
        # تغییر رنگ پینگ بر اساس مقدار
        if 3 < len(s.info_widgets) and s.info_widgets[3].exists():
            ping_color = (0, 1, 0) if current_ping < 100 else (1, 1, 0) if current_ping < 300 else (1, 0, 0)
            tw(s.info_widgets[3], color=ping_color)
        
        # تغییر رنگ وضعیت اتصال
        if 4 < len(s.info_widgets) and s.info_widgets[4].exists():
            status_color = (0, 1, 0) if server_status == "Connected" else (1, 1, 0) if server_status == "Local" else (1, 0, 0)
            tw(s.info_widgets[4], color=status_color)
        
        # ادامه تایمر
        s.timer = teck(1.0, s.update_server_info)
    
    def copy_to_clipboard(s, text):
        """کپی متن به کلیپ‌بورد"""
        try:
            if CIS():
                from babase import clipboard_set_text
                clipboard_set_text(text)
                push(f'Copied: {text}', color=(0, 1, 0))
                gs('dingSmall').play()
            else:
                AR.err('Clipboard not supported!')
        except Exception as e:
            AR.err(f'Copy error: {str(e)}')
    
    def __del__(s):
        """تمیزکاری هنگام حذف"""
        if hasattr(s, 'timer') and s.timer:
            s.timer = None
            
"""اسپم خودکار"""
class Spam:
    # نگهداری یک نمونه فعال برای مدیریت تایمر و وضعیت
    active_instance = None

    def __init__(s, source):
        # ثبت خود به عنوان نمونه فعال
        Spam.active_instance = s

        w = s.w = AR.cw(
            source=source,
            size=(400, 350),
            ps=AR.UIS()*0.8
        )
        AR.add_close_button(w, position=(370, 280))

        # عنوان
        tw(
            parent=w,
            text='اسپم خودکار',
            scale=1.2,
            position=(200, 280),
            h_align='center',
            color=(1, 0.5, 0)
        )

        # فیلد پیام
        tw(parent=w, text='پیام اسپم:', position=(30, 250), scale=0.9, color=(1, 1, 1))
        s.message_widget = tw(parent=w, position=(30, 220), size=(340, 30), editable=True,
                              text='اسپم تست', color=(0.9, 0.9, 0.9))

        # فیلد تعداد
        tw(parent=w, text='تعداد:', position=(30, 180), scale=0.9, color=(1, 1, 1))
        s.count_widget = tw(parent=w, position=(30, 150), size=(150, 30), editable=True,
                            text='5', h_align='center', color=(0.9, 0.9, 0.9))

        # فیلد تأخیر
        tw(parent=w, text='تأخیر (ثانیه):', position=(200, 180), scale=0.9, color=(1, 1, 1))
        s.delay_widget = tw(parent=w, position=(200, 150), size=(150, 30), editable=True,
                            text='1', h_align='center', color=(0.9, 0.9, 0.9))

        # وضعیت
        s.status_text = tw(parent=w, text='آماده', position=(30, 110), scale=0.8, color=(0.8, 0.8, 1))

        # دکمه شروع
        s.start_btn = bw(parent=w, label='شروع اسپم', size=(120, 40), position=(20, 60),
                         on_activate_call=Call(s.start_spam), color=(0, 0.6, 0), textcolor=(1, 1, 1))

        # دکمه استپ جداگانه
        s.stop_btn = bw(parent=w, label='استپ', size=(120, 40), position=(160, 60),
                        on_activate_call=Call(s.stop_spam), color=(0.6, 0, 0), textcolor=(1, 1, 1))

        s.spamming = False
        s.spam_timer = None
        s.remaining_count = 0
        s.sent_count = 0  # شمارنده پیام‌های ارسال شده
        AR.swish()

    @staticmethod
    def start_spam():
        s = Spam.active_instance
        try:
            message = tw(query=s.message_widget).strip()
            count = int(tw(query=s.count_widget))
            delay = float(tw(query=s.delay_widget))

            if not message:
                AR.err('لطفاً یک پیام وارد کنید!')
                return

            if count <= 0 or delay <= 0:
                AR.err('مقادیر باید بزرگتر از صفر باشند!')
                return

            s.spamming = True
            s.remaining_count = count
            s.spam_message = message
            s.spam_delay = delay
            s.sent_count = 0  # ریست شمارنده

            tw(s.status_text, text=f'در حال اسپم: {s.remaining_count} باقیمانده', color=(0, 1, 0))

            s.do_spam()

            push(f'شروع اسپم: {count} پیام با تأخیر {delay} ثانیه', color=(0, 1, 0))

        except ValueError:
            AR.err('لطفاً اعداد معتبر وارد کنید!')
        except Exception as e:
            AR.err(f'خطا: {str(e)}')

    @staticmethod
    def stop_spam():
        s = Spam.active_instance
        if not s.spamming:
            return  # جلوگیری از پیام چندباره

        s.spamming = False

        if s.spam_timer:
            try:
                s.spam_timer.cancel()
            except:
                pass
            s.spam_timer = None

        tw(s.status_text, text='⛔ متوقف شد', color=(1, 0.5, 0))
        push('⛔ اسپم متوقف شد', color=(1, 0.5, 0))

    @staticmethod
    def do_spam():
        s = Spam.active_instance
        if not s.spamming or s.remaining_count <= 0:
            s.spamming = False
            if s.spam_timer:
                try:
                    s.spam_timer.cancel()
                except:
                    pass
                s.spam_timer = None
            tw(s.status_text, text='✅ اسپم تموم شد', color=(0, 1, 0))
            push('✅ اسپم تموم شد', color=(0, 1, 0))
            return

        try:
            # شمارنده پیام ارسال شده
            s.sent_count += 1

            # بررسی زوج/فرد برای اضافه کردن نقطه
            message_to_send = s.spam_message
            if s.sent_count % 2 == 0:
                message_to_send += "."

            CM(message_to_send)
            s.remaining_count -= 1

            if s.w.exists():
                tw(s.status_text, text=f'در حال اسپم: {s.remaining_count} باقیمانده')

            if s.remaining_count > 0 and s.spamming:
                s.spam_timer = teck(s.spam_delay, s.do_spam)
            else:
                s.spamming = False
                if s.spam_timer:
                    try:
                        s.spam_timer.cancel()
                    except:
                        pass
                    s.spam_timer = None
                tw(s.status_text, text='✅ اسپم تموم شد', color=(0, 1, 0))
                push('✅ اسپم تموم شد', color=(0, 1, 0))

        except Exception as e:
            AR.err(f'خطا در ارسال: {str(e)}')
            Spam.stop_spam()

"""راهنما"""
class Help:
    def __init__(s,t):
        w = AR.cw(
            source=t,
            size=(400,400),
            ps=AR.UIS()*0.8
        )
        # افزودن دکمه بستن
        AR.add_close_button(w, position=(385, 310))
        
        s.scroll = sw(
            parent=w,
            size=(360,300),
            position=(20,30)
        )
        s.container = cw(
            parent=s.scroll,
            size=(360,700),
            background=True
        )
        
        # محتوای راهنما
        contents = [
    "📖 راهنمای مود Auto Message",
    "👨‍💻 ساخته شده توسط: طاها استادشریف (@Taha_OstadSharif)",
    "🔹 Auto Message چیست؟",
    "این مود به‌طور هوشمند به پیام‌های دریافتی\n در چت پاسخ می‌دهد و با ماشه‌هایی که تعریف می‌کنید به‌صورت خودکار جواب\n ارسال می‌کند. 😎⚡",
    "",
    "🔹 متغیرهای قابل استفاده:",
    "%m → نام حساب شما در بازی",
    "%s → نام فرستنده پیام",
    "%t → زمان فعلی (ساعت:دقیقه:ثانیه)",
    "%d → تاریخ میلادی (سال-ماه-روز)",
    "%f → تاریخ شمسی دقیق",
    "%j → جوک تصادفی خنده‌دار",
    "%ch → چیستان کوتاه با جواب",
    "%z → ضرب المثل",
    "%dice → شرط بندی (تاس)",
    "%tr → بازی جرعت حقیقت (حقیقت)",
    "%da → بازی جرعت حقیقت (جرعت)",
    "%ip → آیپی و پورت سرور"
    "",
    "🔹 نکات حرفه‌ای:",
    "✅ تاریخ شمسی همیشه دقیق محاسبه می‌شود 📆",
    "✅ ترکیب متغیرها باعث می‌شود پاسخ‌ها طبیعی و متنوع باشند 🎭",
    "✅ با چیستان‌ها می‌توانید دوستان خود را سرگرم کنید 🧩","✅با ضرب المثل چیز های جدید یاد بگیر 📜","✅ با جوک همیشه با رفیقات درحال خنده ای 😂",
    "✅ پینگ سرور در بخش آمار نمایش داده می‌شود 📶",
    "",
    "🔥 با این مود یک ربات گفت‌وگوی واقعی در بازی بسازید و دوستان خود را شگفت‌زده\n کنید!"
]
        
        y_pos = 550
        for content in contents:
            color = (1,1,1)
            scale = 0.4
            if content.startswith("📖"):
                color = (0,1,1)
                scale = 0.6
            elif content.startswith("🔹"):
                color = (1,1,0)
                scale = 0.5
            
            tw(
                parent=s.container,
                text=content,
                position=(10,y_pos),
                scale=scale,
                color=color,
                maxwidth=340
            )
            y_pos -= 20
        
        cw(s.container, size=(360,600-y_pos))
        AR.swish()

"""پایه پیام اتوماتیک"""
class AR:
    @classmethod
    def UIS(c=0):
        i = APP.ui_v1.uiscale
        return [1.5,1.1,0.8][0 if i == uis.SMALL else 1 if i == uis.MEDIUM else 2]
    
    @classmethod
    def add_close_button(c, window, position=(10, 10)):
        """افزودن دکمه بستن به پنجره"""
        close_btn = bw(
            parent=window,
            size=(30, 30),
            position=position,
            label='X',
            color=(0.8, 0.2, 0.2),
            textcolor=(1, 1, 1),
            on_activate_call=Call(c.swish, t=window)
        )
        return close_btn
    
    @classmethod
    def parse(c=0,t=0,s=None):
        me = byTaha.me()
        now = DT.now()
        
        # تبدیل تاریخ به شمسی
        jy, jm, jd = gregorian_to_jalali(now.year, now.month, now.day)
        persian_date = f"{jy}-{jm:02d}-{jd:02d}"
        
        # پینگ واقعی (شبیه‌سازی شده)
        bet = random.randint(1, 6)
        
        # پاسخ تصادفی اگر وجود دارد
        if '%r' in t and '|' in t:
            parts = t.split('%r')
            options = parts[1].split('|')[0].split(';')
            random_response = random.choice(options)
            t = parts[0] + random_response + '|'.join(parts[1].split('|')[1:])
        
        # جایگزینی جوک تصادفی
        if '%j' in t:
            t = t.replace('%j', random.choice(JOKES))
        # جایگزینی چیستان تصادفی
        if '%ch' in t:
            t = t.replace('%ch', random.choice(RIDDLES))
         # جایگزینی ضرب المثل تصادفی
        if '%z' in t:
            t = t.replace('%z', random.choice(PROVERBS))
        #جایگزینی حقیقت تصادفی
        if '%tr' in t:
            t = t.replace('%tr',random.choice(TRUTHS))
         #جایگزینی جرعت تصادفی
        if '%da' in t:
            t = t.replace('%da',random.choice(DARES))
# جایگزینی تاس تصادفی
        if '%dice' in t:
            t = t.replace('%dice', random.choice(DICE))
        #جایگزینی آیپی سرور واقعی
        if '%ip' in t:
            t = t.replace('%ip', f"IP : {server_ip} Port : {server_port}")
        if '%p' in t:
            t = t.replace('%p', f"{current_ping} ms")

        return (t.replace('%t', now.strftime("%H:%M:%S"))
                   .replace('%d', now.strftime("%Y-%m-%d"))
                   .replace('%s', s or byTaha.v2+'ByTaha')
                   .replace('%m', me)
                   .replace('%f', persian_date))
    
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
    
    @classmethod
    def cw(c,source,ps=0,**k):
        o = source.get_screen_space_center() if source else None
        r = cw(
            **k,
            scale=c.UIS()+ps,
            transition='in_scale',
            color=(0.18,0.18,0.18),
            parent=gsw('overlay_stack'),
            scale_origin_stack_offset=o
        )
        cw(r,on_outside_click_call=Call(c.swish,t=r))
        return r
    
    swish = lambda c=0,t=0: (gs('swish').play(),cw(t,transition='out_scale') if t else t)
    err = lambda t: (gs('block').play(),push(t,color=(1,1,0)))
    ok = lambda: (gs('dingSmallHigh').play(),push('باشه!',color=(0,1,0)))
    bye = lambda: (gs('laser').play(),push('خداحافظ!',color=(0,1,0)))
    
    def __init__(s, source: bw = None) -> None:
        w = s.w = s.cw(
            source=source,
            size=(600,600),
        )
        # افزودن دکمه بستن به پنجره اصلی
        s.add_close_button(w, position=(600, 520))
        
        [tw(
            scale=1.0,
            parent=w,
            text='پیام اتوماتیک',
            h_align='center',
            position=(450,470-i*3),
            color=[(1,1,1),(0.6,0.6,0.6)][i]
        ) for i in [1,0]]
        
        # اضافه کردن متن توضیحی در سمت چپ
        tw(
    parent=w,
    text="🤖 ربات پاسخگو\n\n"
         "با این مود می‌توانید:\n"
         "• پاسخ خودکار تنظیم کنید\n"
         "• چت سریع داشته باشید\n"
         "• با دوستانتان بازی کنید\n"
         "• و خیلی بیشتر!",
    position=(400, 410),
    scale=0.75,
    color=(0.8, 0.8, 1),
    maxwidth=150,
    h_align='left'
)

        # اضافه کردن آمار و اطلاعات (با پینگ واقعی)
        s.stats_text = tw(
            parent=w,
            text=f"📊 آمار:\n"
                 f"• {len(var('l') or {})} ماشه فعال\n"
                 f"• {len(load_quick_messages())} پیام سریع\n"
                 f"• وضعیت: {'فعال' if var('state') else 'غیرفعال'}\n"
                 f"• پینگ: {current_ping} ms\n"
                 f"• سرور: {server_ip}:{server_port}",
            position=(400, 270),
            scale=0.65,
            color=(0.8, 1, 0.8),
            maxwidth=160,
            h_align='left'
        )

        # تایمر برای بروزرسانی آمار هر 1 ثانیه
        teck(1.0, s.update_stats)

        # اضافه کردن متن راهنما
        tw(
    parent=w,
    text="💡 نکته:\n"
         "برای اطلاعات بیشتر به\n"
         "بخش راهنما مراجعه کنید",
    position=(400, 140),
    scale=0.75,
    color=(1, 1, 0.5),
    maxwidth=150,
    h_align='left'
)
        
        # ایجاد اسکرول ویجت برای دکمه‌ها
        s.scroll_widget = sw(
            parent=w,
            size=(300, 400),
            position=(30, 100)
        )
        
        # ایجاد کانتینر برای دکمه‌ها
        s.buttons_container = cw(
            parent=s.scroll_widget,
            size=(300, 600),
            background=False
        )
        
        mem = globals()
        buttons = [
             ('افزودن', 'Add', 'ouyaOButton', 550),
             ('حذف', 'Nuke', 'ouyaAButton', 485),
             ('تنظیمات', 'Tune', 'ouyaUButton', 420),             ('لیست', 'List', 'ouyaYButton', 355),
             ('چت سریع', 'QuickChat','achievementOutline', 290),
             ('اسپم', 'Spam', 'egg1', 95),
             ('اطلاعات سرور', 'ServerInfo', 'star', 225),
             ('اتصال مجدد', 'Reconnect', 'replayIcon', 160),      
             ('راهنما', 'Help', 'logo', 30)
]
        
        for label, cls_name, icon, y_pos in buttons:
            b = s.bw(
                label=label,
                parent=s.buttons_container,
                size=(260,60),
                position=(20,y_pos),
                icon=gt(icon)
            )
            bw(b,on_activate_call=Call(mem[cls_name],b))
        
        # تنظیم اندازه کانتینر برای اسکرول
        cw(s.buttons_container, size=(300, 650))
        
        s.b = bw(
            parent=w,
            size=(70,45),
            position=(550,450),
            enable_sound=False,
            button_type='square',
            on_activate_call=s.but
        )
        s.but(1)
        s.swish()
    
    def update_stats(s):
        """بروزرسانی آمار شامل پینگ واقعی"""
        if hasattr(s, 'stats_text') and s.stats_text.exists():
            # گرفتن اطلاعات اتصال فعلی
            conn_info = get_connection_info()
            server_status = f"{server_ip}:{server_port}" if server_ip != "127.0.0.1" else "محلی"
            
            tw(s.stats_text, 
               text=f"📊 آمار:\n"
                    f"• {len(var('l') or {})} ماشه فعال\n"
                    f"• {len(load_quick_messages())} پیام سریع\n"
                    f"• وضعیت: {'فعال' if var('state') else 'غیرفعال'}\n"
                    f"• پینگ: {current_ping} ms\n"
                    f"• سرور: {server_status}")
        teck(1.0, s.update_stats)
    
    def but(s,dry=0):
        v = var('state')
        if not dry:
            v = not v
            var('state',v)
            gs('deek').play()
        bw(
            s.b,
            label=['خاموش','روشن'][v],
            color=[(0.35,0,0),(0,0.45,0)][v],
            textcolor=[(0.5,0,0),(0,0.6,0)][v]
        )

# توابع مدیریت پیام‌های چت سریع
def load_quick_messages():
    """بارگذاری پیام‌های چت سریع از فایل"""
    try:
        config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Configs')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        msg_path = os.path.join(config_dir, 'quick_chat_msgs.json')
        
        if not os.path.exists(msg_path):
            save_quick_messages(DEFAULT_QUICK_MESSAGES.copy())
            return DEFAULT_QUICK_MESSAGES.copy()
        
        with open(msg_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading quick messages: {e}")
        return DEFAULT_QUICK_MESSAGES.copy()

def save_quick_messages(messages):
    """ذخیره پیام‌های چت سریع در فایل"""
    try:
        config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Configs')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        msg_path = os.path.join(config_dir, 'quick_chat_msgs.json')
        
        with open(msg_path, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving quick messages: {e}")

# پیکربندی
pr = 'ar3_'
def var(s,v=None):
    c = APP.config
    s = pr+s
    if v is None: return c.get(s,v)
    c[s] = v
    c.commit()
def reset_conf(): cfg = APP.config; [(cfg.pop(c) if c.startswith(pr) else None) for c in cfg.copy()]; cfg.commit()

# پیش‌فرض
for i in range(4): j = f'tune{i}'; v = var(j); var(j,i<3) if v is None else v
None if var('state') else var('state',1)
None if var('time') else var('time','0.5')
None if var('l') else var('l',{})
None if var('lc') else var('lc',{})

# ابزارهای کوچک
SW = lambda s: strw(s,suppress_warning=True)
def sn(s):
    out = ''
    w = 0.0
    for c in s:
        ch_w = SW(c)
        if w + ch_w > 520:
            out += '\n'
            w = 0.0
        out += c
        w += ch_w
    return out

# اورراید کردن توابع اصلی
def setup_connection_overrides():
    global original_connect, original_disconnect
    from bascenev1 import connect_to_party, disconnect_from_host
    
    if original_connect is None:
        original_connect = connect_to_party
        original_disconnect = disconnect_from_host
        
        # اورراید کردن توابع
        import bascenev1
        bascenev1.connect_to_party = new_connect_to_party
        bascenev1.disconnect_from_host = new_disconnect_from_host
        print("توابع اتصال اورراید شدند")

# شروع thread پینگ واقعی
ping_thread = RealPingThread()
ping_thread.start()

"""منوی استیکر با قابلیت مدیریت - فقط ایموجی"""
class StickerMenu:
    def __init__(s, source):
        w = s.w = AR.cw(
            source=source,
            size=(300, 400),
            ps=AR.UIS()*0.7
        )
        # افزودن دکمه بستن
        AR.add_close_button(w, position=(280, 325))
        
        # عنوان
        tw(
            parent=w,
            text='منوی استیکر',
            scale=1.0,
            position=(130, 320),
            h_align='center',
            color=(1, 1, 0)
        )
        
        # بارگذاری استیکرها از تنظیمات
        s.stickers = load_stickers()
        
        # ایجاد ویجت اسکرول
        s.scroll_widget = sw(
            parent=w,
            size=(260, 200),
            position=(20, 110)
        )
        
        # ایجاد کانتینر برای استیکرها
        s.container = cw(
            parent=s.scroll_widget,
            size=(260, len(s.stickers) * 55),
            background=False
        )
        
        # دکمه‌های مدیریت
        buttons = [
            ('➕ افزودن', s.add_sticker, (20, 80)),
            ('🗑️ حذف', s.remove_sticker, (120, 80)),
            ('🔄 بازنشانی', s.reset_stickers, (220, 80))
        ]
        
        for label, callback, pos in buttons:
            AR.bw(
                parent=w,
                label=label,
                size=(90, 30),
                position=pos,
                on_activate_call=callback,
                scale=0.8
            )
        
        s.refresh_stickers()
        AR.swish()
    
    def refresh_stickers(s):
        """تازه کردن لیست استیکرها"""
        # پاک کردن استیکرهای قبلی
        for child in s.container.get_children():
            child.delete()
        
        # نمایش استیکرها به صورت لیست با قابلیت اسکرول
        y_pos = len(s.stickers) * 50 - 25
        for sticker in s.stickers:
            btn = bw(
                parent=s.container,
                label=sticker,
                size=(240, 45),
                position=(10, y_pos),
                on_activate_call=Call(s.send_sticker, sticker),
                color=(0.3, 0.5, 0.7),
                textcolor=(1, 1, 1),
                text_scale=0.8  # اینجا تغییر دادم - متن استیکر کوچک‌تر شد
            )
            y_pos -= 50
        
        # تنظیم اندازه کانتینر
        cw(s.container, size=(260, len(s.stickers) * 55))
    
    def send_sticker(s, sticker):
        """ارسال استیکر"""
        try:
            CM(sticker)
            push(f'ارسال شد: {sticker}', color=(0, 1, 0))
            gs('dingSmall').play()
            AR.swish(s.w)
        except Exception as e:
            AR.err(f'خطا در ارسال: {str(e)}')
    
    def add_sticker(s):
        """افزودن استیکر جدید - فقط ایموجی"""
        def save_new_sticker():
            new_sticker = tw(query=txt_widget).strip()
            
            if not new_sticker:
                AR.err('لطفاً یک ایموجی وارد کنید!')
                gs('error').play()
                return
            
            # بررسی دقیق که فقط ایموجی باشد
            if not is_valid_emoji(new_sticker):
                AR.err('فقط می‌توانید ایموجی وارد کنید! متن مجاز نیست.')
                gs('error').play()
                return
            
            # بررسی طول (ایموجی‌ها معمولاً 1-4 کاراکتر هستند)
            if len(new_sticker) > 4:
                AR.err('ایموجی نامعتبر! لطفاً فقط یک ایموجی وارد کنید.')
                gs('error').play()
                return
            
            stickers = load_stickers()
            
            # بررسی تکراری نبودن
            if new_sticker in stickers:
                AR.err('این ایموجی از قبل وجود دارد!')
                gs('error').play()
                return
            
            # بررسی تعداد استیکرها
            if len(stickers) >= 20:
                AR.err('حداکثر ۲۰ استیکر می‌توانید داشته باشید!')
                gs('error').play()
                return
                
            # اضافه کردن استیکر جدید
            stickers.append(new_sticker)
            save_stickers(stickers)
            s.stickers = stickers
            s.refresh_stickers()
            push(f'ایموجی اضافه شد: {new_sticker}', color=(0, 1, 0))
            gs('dingSmallHigh').play()
            AR.swish(win)
        
        win = AR.cw(
            source=s.w,
            size=(350, 200),
            ps=AR.UIS()*0.6
        )
        
        AR.add_close_button(win, position=(320, 170))
        
        tw(
            parent=win,
            text='ایموجی جدید:',
            position=(20, 160),
            scale=0.9,
            color=(1, 1, 1)
        )
        
        txt_widget = tw(
            parent=win,
            position=(20, 120),
            size=(310, 40),
            editable=True,
            text='',
            color=(0.9, 0.9, 0.9),
            max_chars=3,  # محدودیت برای ایموجی
            h_align='center'
        )
        
        # راهنمای اضافی
        tw(
            parent=win,
            text='⚠️ فقط ایموجی قابل قبول است (متن مجاز نیست)',
            position=(20, 80),
            scale=0.6,
            color=(1, 0.5, 0.5)
        )
        
        tw(
            parent=win,
            text='📱 از کیبورد ایموجی دستگاه خود استفاده کنید',
            position=(20, 60),
            scale=0.6,
            color=(0.8, 0.8, 1)
        )
        
        AR.bw(
            parent=win,
            label='تأیید',
            size=(100, 35),
            position=(125, 20),
            on_activate_call=save_new_sticker
        )
    
    def remove_sticker(s):
        """حذف استیکر"""
        if not s.stickers:
            AR.err('استیکری برای حذف وجود ندارد!')
            return
        
        win = AR.cw(
            source=s.w,
            size=(350, min(450, 250 + len(s.stickers) * 45)),
            ps=AR.UIS()*0.6
        )
        
        AR.add_close_button(win, position=(320, min(420, 220 + len(s.stickers) * 45)))
        
        tw(
            parent=win,
            text='ایموجی را برای حذف انتخاب کنید:',
            scale=1.0,
            position=(175, min(400, 170 + len(s.stickers) * 45)),
            h_align='center',
            color=(1, 1, 0)
        )
        
        scroll = sw(
            parent=win,
            size=(330, min(300, 150 + len(s.stickers) * 40)),
            position=(10, 50)
        )
        
        container = cw(
            parent=scroll,
            size=(330, len(s.stickers) * 45),
            background=False
        )
        
        y_pos = len(s.stickers) * 44 - 25
        for sticker in s.stickers:
            bw(
                parent=container,
                label=f'🗑️ {sticker}',
                size=(310, 40),
                position=(10, y_pos),
                on_activate_call=Call(s.confirm_remove, sticker, win),
                color=(0.8, 0.2, 0.2),
                textcolor=(1, 1, 1),
                text_scale=0.8  # اینجا هم تغییر دادم - متن کوچک‌تر شد
            )
            y_pos -= 45
    
    def confirm_remove(s, sticker, parent_win):
        """تأیید حذف استیکر"""
        stickers = load_stickers()
        if sticker in stickers:
            stickers.remove(sticker)
            save_stickers(stickers)
            s.stickers = stickers
            s.refresh_stickers()
            push(f'ایموجی حذف شد: {sticker}', color=(1, 0.5, 0))
            gs('dingSmallLow').play()
        AR.swish(parent_win)
    
    def reset_stickers(s):
        """بازنشانی به حالت پیش‌فرض"""
        save_stickers(DEFAULT_STICKERS.copy())
        s.stickers = DEFAULT_STICKERS.copy()
        s.refresh_stickers()
        push('استیکرها به حالت پیش‌فرض بازنشانی شدند', color=(0, 1, 1))
        gs('dingSmallHigh').play()

# استیکرهای پیش‌فرض
DEFAULT_STICKERS = [
    "😂", "😐", "🗿", "🌚", "❤️", "💣", "🤫", "🙏", "😭"
]

def is_valid_emoji(text):
    """
    بررسی دقیق که متن فقط ایموجی باشد
    """
    if not text:
        return False
    
    # حذف فاصله‌ها و کاراکترهای خالی
    cleaned_text = text.strip()
    
    # بررسی طول معقول برای ایموجی
    if len(cleaned_text) > 4:
        return False
    
    # بررسی کاراکترهای غیر ایموجی
    # کاراکترهای معمولی (حروف، اعداد، علائم نگارشی) نباید وجود داشته باشند
    regular_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
    
    for char in cleaned_text:
        if char in regular_chars:
            return False
        
        # بررسی محدوده یونیکد ایموجی‌ها
        char_code = ord(char)
        
        # محدوده‌های اصلی ایموجی در یونیکد
        emoji_ranges = [
            (0x1F600, 0x1F64F),  # Emoticons
            (0x1F300, 0x1F5FF),  # Miscellaneous Symbols and Pictographs
            (0x1F680, 0x1F6FF),  # Transport and Map Symbols
            (0x1F700, 0x1F77F),  # Alchemical Symbols
            (0x1F780, 0x1F7FF),  # Geometric Shapes Extended
            (0x1F800, 0x1F8FF),  # Supplemental Arrows-C
            (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs
            (0x1FA00, 0x1FA6F),  # Chess Symbols
            (0x1FA70, 0x1FAFF),  # Symbols and Pictographs Extended-A
            (0x2600, 0x26FF),    # Miscellaneous Symbols
            (0x2700, 0x27BF),    # Dingbats
            (0xFE00, 0xFE0F),    # Variation Selectors
        ]
        
        is_emoji_char = any(start <= char_code <= end for start, end in emoji_ranges)
        
        if not is_emoji_char:
            # اگر کاراکتر در محدوده ایموجی نبود، احتمالاً متن است
            return False
    
    return True

def load_stickers():
    """بارگذاری استیکرها از فایل"""
    try:
        config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Configs')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        stickers_path = os.path.join(config_dir, 'stickers.json')
        
        if not os.path.exists(stickers_path):
            save_stickers(DEFAULT_STICKERS.copy())
            return DEFAULT_STICKERS.copy()
        
        with open(stickers_path, 'r', encoding='utf-8') as f:
            loaded_stickers = json.load(f)
            
            # فیلتر کردن استیکرهای غیر معتبر
            valid_stickers = [s for s in loaded_stickers if is_valid_emoji(s)]
            
            if len(valid_stickers) != len(loaded_stickers):
                # اگر استیکرهای نامعتبر وجود داشت، ذخیره مجدد
                save_stickers(valid_stickers)
            
            return valid_stickers
            
    except Exception as e:
        print(f"Error loading stickers: {e}")
        return DEFAULT_STICKERS.copy()

def save_stickers(stickers):
    """ذخیره استیکرها در فایل"""
    try:
        # فیلتر کردن استیکرهای نامعتبر قبل از ذخیره
        valid_stickers = [s for s in stickers if is_valid_emoji(s)]
        
        config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Configs')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        stickers_path = os.path.join(config_dir, 'stickers.json')
        
        with open(stickers_path, 'w', encoding='utf-8') as f:
            json.dump(valid_stickers, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving stickers: {e}")
        
"""چت لاگ با نمایش 300 پیام آخر"""
class ChatLog:
    def __init__(s, source):
        try:
            w = s.w = AR.cw(
                source=source,
                size=(400, 300),  # اندازه قبلی
                ps=AR.UIS()*0.8
            )
            
            # عنوان کوچک
            tw(
                parent=w,
                text='💬 چت (500+)',
                scale=0.9,
                position=(180, 265),
                h_align='center',
                color=(0, 1, 1)
            )
            
            # دکمه بستن
            AR.add_close_button(w, position=(375, 270))
            
            # فیلد جستجو
            s.search_input = tw(
                parent=w,
                position=(20, 240),
                size=(250, 25),
                editable=True,
                text='',
                color=(0.9, 0.9, 0.9),
                description='جستجو...'
            )
            
            # دکمه‌های اکشن
            buttons = [
                ('🔍', s.apply_search, (280, 240), (0.3, 0.6, 0.8)),
                ('⏰', s.toggle_time, (320, 240), (0.5, 0.4, 0.7)),
                ('📊', s.show_stats, (360, 240), (0.8, 0.5, 0.3))
            ]
            
            for label, callback, pos, color in buttons:
                bw(
                    parent=w,
                    label=label,
                    size=(30, 25),
                    position=pos,
                    on_activate_call=callback,
                    color=color,
                    textcolor=(1, 1, 1)
                )
            
            # اسکرول با اسکرول بار برای 300 پیام
            s.scroll = sw(
                parent=w,
                size=(380, 180),
                position=(10, 50)
            )
            
            s.container = cw(
                parent=s.scroll,
                size=(380, 6000),  # ارتفاع زیاد برای اسکرول
                background=False
            )
            
            # وضعیت
            s.status_text = tw(
                parent=w,
                text='...',
                position=(200, 25),
                scale=0.6,
                color=(0.8, 0.8, 1),
                h_align='center'
            )
            
            # متغیرهای حالت
            s.all_messages = []
            s.filtered_messages = []
            s.search_text = ""
            s.show_time = False
            s.showing_stats = False
            
            s.refresh_chat_log()
            AR.swish()
            
        except Exception as e:
            AR.err(f'خطا: {str(e)}')
    
    def refresh_chat_log(s):
        """بارگذاری تاریخچه چت"""
        try:
            s.all_messages = GCM()
            # گرفتن 300 پیام آخر
            s.all_messages = s.all_messages[-300:] if len(s.all_messages) > 300 else s.all_messages
            s.filtered_messages = s.all_messages.copy()
            s.display_messages()
            
        except Exception as e:
            AR.err(f'خطا: {str(e)}')
    
    def apply_search(s):
        """اعمال جستجو"""
        s.search_text = tw(query=s.search_input).strip().lower()
        s.showing_stats = False
        
        if s.search_text:
            if s.search_text.startswith('user:'):
                username = s.search_text[5:].strip()
                s.filtered_messages = [
                    msg for msg in s.all_messages 
                    if msg.lower().startswith(username + ':')
                ]
            else:
                s.filtered_messages = [
                    msg for msg in s.all_messages 
                    if s.search_text in msg.lower()
                ]
        else:
            s.filtered_messages = s.all_messages.copy()
        
        s.display_messages()
    
    def toggle_time(s):
        """نمایش/مخفی کردن زمان"""
        s.show_time = not s.show_time
        s.showing_stats = False
        s.display_messages()
    
    def show_stats(s):
        """نمایش آمار"""
        s.showing_stats = True
        s.display_stats()
    
    def display_messages(s):
        """نمایش پیام‌ها با اسکرول"""
        try:
            # پاک کردن قبلی
            for child in s.container.get_children():
                child.delete()
            
            if s.showing_stats:
                s.display_stats()
                return
            
            # استفاده از پیام‌های فیلتر شده یا همه
            messages_to_show = s.filtered_messages
            
            y_pos = len(messages_to_show) * 18 - 9  # فاصله خیلی کم
            for i, message in enumerate(messages_to_show):
                # نمایش زمان اگر فعال باشد
                display_text = message
                if s.show_time:
                    timestamp = time.strftime("%H:%M", time.localtime(time.time() - (len(messages_to_show) - i) * 2))
                    display_text = f"[{timestamp}] {message}"
                
                # کوتاه کردن متن بیشتر
                if len(display_text) > 45:
                    display_text = display_text[:42] + "..."
                
                # دکمه کپی کوچکتر
                bw(
                    parent=s.container,
                    label='📋',
                    size=(22, 16),
                    position=(345, y_pos),
                    on_activate_call=Call(s.copy_message, message),
                    color=(0.3, 0.6, 0.3),
                    text_scale=0.5
                )
                
                # متن پیام با فونت ریز
                tw(
                    parent=s.container,
                    text=display_text,
                    position=(10, y_pos),
                    scale=0.35,  # فونت خیلی ریز
                    color=(1, 1, 1),
                    maxwidth=325,  # عرض بیشتر
                    h_align='left'
                )
                
                y_pos -= 18  # فاصله خیلی کم
            
            # بروزرسانی وضعیت
            status_text = f'{len(messages_to_show)}/500'
            if s.search_text:
                status_text += f' | {s.search_text[:8]}'
            if s.show_time:
                status_text += ' | ⏰'
            
            tw(s.status_text, text=status_text)
            cw(s.container, size=(380, len(messages_to_show) * 18 + 10))
            
        except Exception as e:
            AR.err(f'خطا: {str(e)}')
    
    def display_stats(s):
        """نمایش آمار فشرده"""
        try:
            for child in s.container.get_children():
                child.delete()
            
            # تحلیل داده‌ها
            user_stats = {}
            for message in s.all_messages:
                if ':' in message:
                    username = message.split(':', 1)[0].strip()
                    user_stats[username] = user_stats.get(username, 0) + 1
            
            # نمایش آمار فشرده
            stats = [
                f"📊 {len(s.all_messages)}",
                f"👥 {len(user_stats)}",
                f"📈 {len(s.all_messages) // max(len(user_stats), 1)}"
            ]
            
            y_pos = 150
            for stat in stats:
                tw(
                    parent=s.container,
                    text=stat,
                    position=(190, y_pos),
                    scale=0.7,
                    color=(1, 1, 1),
                    h_align='center'
                )
                y_pos -= 25
            
            # نمایش کاربر برتر
            if user_stats:
                top_user = max(user_stats.items(), key=lambda x: x[1])
                tw(
                    parent=s.container,
                    text=f"🏆 {top_user[0][:10]}:{top_user[1]}",
                    position=(190, y_pos),
                    scale=0.5,
                    color=(1, 1, 0),
                    h_align='center'
                )
            
            cw(s.container, size=(380, 200))
            tw(s.status_text, text='📊 آمار 500 پیام')
            
        except Exception as e:
            AR.err(f'خطا: {str(e)}')
    
    def copy_message(s, message):
        """کپی پیام"""
        try:
            if CIS():
                from babase import clipboard_set_text
                clipboard_set_text(message)
                push('✅', color=(0, 1, 0))
        except Exception as e:
            AR.err(f'❌ {str(e)}')
     
class FontMaker:
    def __init__(s, source):
        # پنجره با ارتفاع کمتر و هماهنگ با بقیه
        w = s.w = AR.cw(
            source=source,
            size=(500, 350),  # ارتفاع کمتر
            ps=AR.UIS() * 0.6
        )
        AR.add_close_button(w, position=(470, 300))

        # عنوان هماهنگ با بقیه
        tw(parent=w, text="🎨 فونت‌ساز", position=(200, 300), scale=1.0, color=(1,1,0))

        # تکست‌باکس ورودی هماهنگ
        tw(parent=w, text="Text:", position=(20, 265), scale=0.8, color=(1,1,1))
        s.input_widget = tw(parent=w, position=(80, 255), size=(390, 40),
                            editable=True, text="متن خود را وارد کنید", 
                            color=(0.9,0.9,0.9), description="")

        # دکمه ساخت هماهنگ
        AR.bw(parent=w, label="ساخت فونت‌ها", size=(120, 30),
              position=(190, 200), on_activate_call=s.show_fonts)

        # اسکرول لیست فونت‌ها با ارتفاع کمتر
        s.scroll = sw(parent=w, size=(460, 150), position=(20, 50))
        s.container = cw(parent=s.scroll, size=(440, 1000), background=False)

        # ویجت وضعیت هماهنگ
        s.status_text = tw(parent=w, text="آماده", 
                          position=(230, 25), scale=0.6, color=(0.8,0.8,1))

        AR.swish()

    def show_fonts(s):
        text = tw(query=s.input_widget).strip()
        if not text or text == "متن خود را وارد کنید":
            AR.err("لطفاً یک متن وارد کنید!")
            return

        fonts = generate_fonts(text)

        # پاکسازی قبلی
        for child in s.container.get_children():
            child.delete()

        # نمایش فونت‌ها با قابلیت اسکرول
        y_pos = len(fonts) * 40 - 20
        total_height = 0
        
        for name, styled in fonts.items():
            # نام فونت - متن کوچکتر
            tw(parent=s.container, text=f"{name}:  ", position=(10, y_pos),
               color=(1,1,1), scale=0.6, maxwidth=90)
            
            # متن استایل شده - متن کوچکتر
            tw(parent=s.container, text=styled, position=(100, y_pos),
               color=(0,1,0), scale=0.65, maxwidth=250)
            
            # دکمه کپی هماهنگ
            AR.bw(parent=s.container, label="کپی", size=(50, 20),
                  position=(360, y_pos - 3),
                  on_activate_call=Call(s.copy_font, styled, name),
                  text_scale=0.5)
            
            y_pos -= 40
            total_height += 40

        # تنظیم اندازه کانتینر برای اسکرول صحیح
        cw(s.container, size=(440, max(300, total_height)))
        
        # بروزرسانی وضعیت
        tw(s.status_text, text=f"{len(fonts)} فونت ساخته شد")

    def copy_font(s, text, font_name):
        try:
            from babase import clipboard_set_text
            clipboard_set_text(text)
            push(f'فونت {font_name} کپی شد', color=(0,1,0))
            gs('dingSmall').play()
        except:
            AR.err("کلیپ‌بورد پشتیبانی نمی‌شود!")
            
"""اطلاعات بازیکنان - عرض بزرگتر، ارتفاع کمتر"""
class PlayerInfo:
    def __init__(s, source):
        # ویندوز با عرض 600 و ارتفاع 320
        w = s.w = AR.cw(
            source=source,
            size=(600, 320),
            ps=AR.UIS()*0.7
        )
        # دکمه بستن
        AR.add_close_button(w, position=(570, 285))

        # عنوان
        tw(
            parent=w,
            text='👥 اطلاعات بازیکنان',
            scale=1.1,
            position=(280, 270),  # مرکز پنجره جدید
            h_align='center',
            color=(0, 1, 1)
        )

        # دریافت لیست بازیکنان
        s.players = s.get_players()

        # اسکرول با عرض بیشتر
        s.scroll = sw(
            parent=w,
            size=(560, 200),
            position=(20, 50)
        )

        s.container = cw(
            parent=s.scroll,
            size=(560, len(s.players) * 45),
            background=False
        )

        # دکمه‌های مدیریت
        buttons = [
            ('🔄 بروزرسانی', s.refresh_players, (30, 20), (120, 30)),
            ('📋 کپی همه', s.copy_all_info, (250, 20), (120, 30)),
            ('🚫 اخراج همه', s.kick_all, (450, 20), (120, 30))
        ]
        
        for label, callback, pos, size in buttons:
            bw(
                parent=w,
                label=label,
                size=size,
                position=pos,
                on_activate_call=callback,
                color=(0.3, 0.5, 0.8),
                text_scale=0.8,
                textcolor=(1, 1, 1)
            )

        s.display_players()
        AR.swish()

    def get_players(s):
        players = []
        try:
            roster = bs.get_game_roster()
            for player in roster:
                if 'players' in player and player['players']:
                    for p in player['players']:
                        device_name = player.get('display_string', 'دستگاه ناشناس')
                        players.append({
                            'name': p.get('name', 'بازیکن ناشناس'),
                            'full_name': p.get('name_full', 'بازیکن ناشناس'),
                            'client_id': player.get('client_id', -1),
                            'is_host': player.get('client_id', -1) == -1,
                            'device': device_name
                        })
        except Exception:
            pass
        return players

    def display_players(s):
        for child in s.container.get_children():
            child.delete()

        if not s.players:
            tw(
                parent=s.container,
                text='⚠️ بازیکنی یافت نشد',
                position=(280, 90),
                scale=0.8,
                color=(1, 0.5, 0),
                h_align='center'
            )
            return

        # هدرهای ستون‌ها با عرض جدید
        headers = [
            ('نام بازیکن', 30, 0.6, (1, 1, 1)),
            ('ID', 120, 0.6, (0.8, 0.8, 1)),
            ('دستگاه', 170, 0.6, (0.6, 1, 0.6)),
            ('وضعیت', 300, 0.6, (1, 1, 0.8)),
            ('عملیات', 440, 0.6, (1, 1, 1))
        ]

        y_pos = len(s.players) * 40 + 20
        for text, x, scale, color in headers:
            tw(
                parent=s.container,
                text=text,
                position=(x, y_pos),
                scale=scale,
                color=color,
                h_align='center'
            )

        y_pos = len(s.players) * 40 - 15
        for i, player in enumerate(s.players):
            bg_color = (0.2, 0.2, 0.3) if i % 2 == 0 else (0.25, 0.25, 0.35)
            
            # پس‌زمینه ردیف
            bw(
                parent=s.container, 
                label='', 
                size=(540, 35),  # عرض بزرگتر مطابق با کانتینر
                position=(10, y_pos), 
                color=bg_color, 
                enable_sound=False
            )

            # نام بازیکن
            pname = player['name'][:18] + '...' if len(player['name']) > 18 else player['name']
            if player['is_host']:
                pname = f"👑 {pname}"
            
            tw(
                parent=s.container, 
                text=pname,
                position=(20, y_pos + 5), 
                scale=0.65,
                color=(1, 1, 1), 
                maxwidth=160,  # کمی بزرگتر
                h_align='left'
            )

            # ID بازیکن
            tw(
                parent=s.container, 
                text=f"{player['client_id']}",
                position=(120, y_pos + 5), 
                scale=0.6,
                color=(0.8, 0.8, 1), 
                h_align='center'
            )

            # نام دستگاه
            device_text = player['device'][:18] + '...' if len(player['device']) > 18 else player['device']
            tw(
                parent=s.container, 
                text=device_text,
                position=(160, y_pos + 5), 
                scale=0.55,
                color=(0.6, 1, 0.6), 
                maxwidth=140, 
                h_align='left'
            )

            # وضعیت میزبان
            status_text = "میزبان" if player['is_host'] else "بازیکن"
            status_color = (1, 1, 0) if player['is_host'] else (0.8, 0.8, 1)
            tw(
                parent=s.container, 
                text=status_text,
                position=(300, y_pos + 5), 
                scale=0.6,
                color=status_color, 
                h_align='center'
            )

            # اکشن‌ها
            actions = [
                ('📋', s.copy_player_info, (400, y_pos + 5), player),
                ('@', s.mention_player, (450, y_pos + 5), player),
                ('🚫', s.kick_player, (500, y_pos + 5), player)
            ]
            
            for label, callback, pos, data in actions:
                bw(
                    parent=s.container, 
                    label=label, 
                    size=(25, 25),
                    position=pos, 
                    on_activate_call=Call(callback, data),
                    color=(0.3, 0.5, 0.8), 
                    text_scale=0.6
                )

            y_pos -= 40

        cw(s.container, size=(540, len(s.players) * 40 + 40))

    def refresh_players(s):
        s.players = s.get_players()
        s.display_players()
        push('🔄 لیست بازیکنان بروزرسانی شد', color=(0, 1, 0))
        gs('dingSmall').play()

    def copy_player_info(s, player):
        info = (f"نام بازیکن: {player['name']}\n"
                f"شناسه: {player['client_id']}\n"
                f"دستگاه: {player['device']}\n"
                f"وضعیت: {'میزبان' if player['is_host'] else 'بازیکن'}")
        
        if CIS():
            from babase import clipboard_set_text
            clipboard_set_text(info)
            push(f'📋 اطلاعات {player["name"]} کپی شد', color=(0, 1, 0))
            gs('dingSmall').play()
        else:
            AR.err('❌ کلیپ‌بورد پشتیبانی نمی‌شود!')

    def copy_all_info(s):
        if not s.players:
            AR.err('❌ بازیکنی برای کپی وجود ندارد!')
            return
            
        all_info = "👥 لیست بازیکنان:\n\n"
        for player in s.players:
            status = "👑 میزبان" if player['is_host'] else "👤 بازیکن"
            all_info += f"• {player['name']} (ID: {player['client_id']}) - {player['device']} - {status}\n"
        
        if CIS():
            from babase import clipboard_set_text
            clipboard_set_text(all_info)
            push('📋 اطلاعات همه بازیکنان کپی شد', color=(0, 1, 0))
            gs('dingSmallHigh').play()
        else:
            AR.err('❌ کلیپ‌بورد پشتیبانی نمی‌شود!')

    def mention_player(s, player):
        try:
            message = f"@{player['name']}"
            CM(message)
            push(f"📍 {player['name']} منشن شد", color=(0, 1, 1))
            gs('dingSmall').play()
        except Exception:
            AR.err(f"❌ خطا در ارسال منشن")

    def kick_player(s, player):
        if player['is_host']:
            AR.err('❌ نمی‌توان میزبان را اخراج کرد!')
            return
        
        try:
            from bascenev1 import disconnect_client
            disconnect_client(player['client_id'])
            push(f"🚫 {player['name']} اخراج شد", color=(1, 0.5, 0))
            gs('dingSmallLow').play()
            teck(1.0, s.refresh_players)
        except Exception:
            AR.err(f"❌ خطا در اخراج")

    def kick_all(s):
        if not s.players:
            AR.err('❌ بازیکنی برای اخراج وجود ندارد!')
            return
            
        try:
            from bascenev1 import disconnect_client
            kicked_count = 0
            
            for player in s.players:
                if not player['is_host']:
                    try:
                        disconnect_client(player['client_id'])
                        kicked_count += 1
                    except:
                        continue
            
            if kicked_count > 0:
                push(f"🚫 {kicked_count} بازیکن اخراج شدند", color=(1, 0.5, 0))
                gs('dingSmallLow').play()
                teck(1.0, s.refresh_players)
            else:
                AR.err('❌ هیچ بازیکنی برای اخراج وجود ندارد!')
                
        except Exception:
            AR.err(f"❌ خطا در اخراج گروهی")
            
"""تغییر رنگ UI"""
class UIColorChanger:
    def __init__(s, source):
        # فقط مستقیماً پنجره تغییر رنگ را باز کن
        launch_colorscheme_selection_window()

class ColorScheme:
    """
    Apply a colorscheme to the game.
    """

    def __init__(self, color=None, highlight=None):
        self.color = color
        self.highlight = highlight

    def _custom_buttonwidget(self, *args, **kwargs):
        if self.highlight is not None:
            kwargs["color"] = self.highlight
        return original_buttonwidget(*args, **kwargs)

    def _custom_containerwidget(self, *args, **kwargs):
        if self.color is not None:
            kwargs["color"] = self.color
        return original_containerwidget(*args, **kwargs)

    def _custom_checkboxwidget(self, *args, **kwargs):
        if self.highlight is not None:
            kwargs["color"] = self.highlight
        return original_checkboxwidget(*args, **kwargs)

    def _apply_color(self):
        if self.color is not None:
            bui.containerwidget = self._custom_containerwidget

    def _apply_highlight(self):
        if self.highlight is not None:
            bui.buttonwidget = self._custom_buttonwidget
            bui.checkboxwidget = self._custom_checkboxwidget

    def apply(self):
        if self.color:
            self._apply_color()
        if self.highlight:
            self._apply_highlight()

    @staticmethod
    def _disable_color():
        bui.buttonwidget = original_buttonwidget
        bui.checkboxwidget = original_checkboxwidget

    @staticmethod
    def _disable_highlight():
        bui.containerwidget = original_containerwidget

    @classmethod
    def disable(cls):
        cls._disable_color()
        cls._disable_highlight()

class ColorSchemeWindow(bui.Window):
    def __init__(self, default_colors=((0.41, 0.39, 0.5), (0.5, 0.7, 0.25))):
        self._default_colors = default_colors
        self._color, self._highlight = babase.app.config.get("ColorScheme", (None, None))

        self._last_color = self._color
        self._last_highlight = self._highlight

        ColorScheme.disable()

        # Allow pro features for color picking
        global original_have_pro
        original_have_pro = bui.app.classic.accounts.have_pro
        bui.app.classic.accounts.have_pro = lambda: True

        self.draw_ui()

    def draw_ui(self):
        uiscale = bui.app.ui_v1.uiscale
        self._width = width = 480.0 if uiscale is babase.UIScale.SMALL else 380.0
        self._x_inset = x_inset = 40.0 if uiscale is babase.UIScale.SMALL else 0.0
        self._height = height = (
            275.0
            if uiscale is babase.UIScale.SMALL
            else 288.0
            if uiscale is babase.UIScale.MEDIUM
            else 300.0
        )
        spacing = 40
        self._base_scale = (
            2.05
            if uiscale is babase.UIScale.SMALL
            else 1.5
            if uiscale is babase.UIScale.MEDIUM
            else 1.0
        )
        top_extra = 15

        super().__init__(
            root_widget=bui.containerwidget(
                size=(width, height + top_extra),
                on_outside_click_call=self.cancel_on_outside_click,
                transition="in_right",
                scale=self._base_scale,
                stack_offset=(0, 15) if uiscale is babase.UIScale.SMALL else (0, 0),
            )
        )

        cancel_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(52 + x_inset, height - 60),
            size=(155, 60),
            scale=0.8,
            autoselect=True,
            label=babase.Lstr(resource="cancelText"),
            on_activate_call=self._cancel,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=cancel_button)

        save_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(width - (177 + x_inset), height - 110),
            size=(155, 60),
            autoselect=True,
            scale=0.8,
            label=babase.Lstr(resource="saveText"),
        )
        bui.widget(edit=save_button, left_widget=cancel_button)
        bui.buttonwidget(edit=save_button, on_activate_call=self.save)
        bui.widget(edit=cancel_button, right_widget=save_button)
        bui.containerwidget(edit=self._root_widget, start_button=save_button)

        reset_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(width - (177 + x_inset), height - 60),
            size=(155, 60),
            color=(0.2, 0.5, 0.6),
            autoselect=True,
            scale=0.8,
            label=babase.Lstr(resource="settingsWindowAdvanced.resetText"),
        )
        bui.widget(edit=reset_button, left_widget=reset_button)
        bui.buttonwidget(edit=reset_button, on_activate_call=self.reset)
        bui.widget(edit=cancel_button, right_widget=reset_button)
        bui.containerwidget(edit=self._root_widget, start_button=reset_button)

        v = height - 65.0
        v -= spacing * 3.0
        b_size = 80
        b_offs = 75

        self._color_button = bui.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(self._width * 0.5 - b_offs - b_size * 0.5, v - 50),
            size=(b_size, b_size),
            color=self._last_color or self._default_colors[0],
            label="",
            button_type="square",
        )
        bui.buttonwidget(
            edit=self._color_button, on_activate_call=babase.Call(self._pick_color, "color")
        )
        bui.textwidget(
            parent=self._root_widget,
            h_align="center",
            v_align="center",
            position=(self._width * 0.5 - b_offs, v - 65),
            size=(0, 0),
            draw_controller=self._color_button,
            text=babase.Lstr(resource="editProfileWindow.colorText"),
            scale=0.7,
            color=bui.app.ui_v1.title_color,
            maxwidth=120,
        )

        self._highlight_button = bui.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(self._width * 0.5 + b_offs - b_size * 0.5, v - 50),
            size=(b_size, b_size),
            color=self._last_highlight or self._default_colors[1],
            label="",
            button_type="square",
        )

        bui.buttonwidget(
            edit=self._highlight_button,
            on_activate_call=babase.Call(self._pick_color, "highlight"),
        )
        bui.textwidget(
            parent=self._root_widget,
            h_align="center",
            v_align="center",
            position=(self._width * 0.5 + b_offs, v - 65),
            size=(0, 0),
            draw_controller=self._highlight_button,
            text=babase.Lstr(resource="editProfileWindow.highlightText"),
            scale=0.7,
            color=bui.app.ui_v1.title_color,
            maxwidth=120,
        )

    def _pick_color(self, tag):
        if tag == "color":
            initial_color = self._color or self._default_colors[0]
        elif tag == "highlight":
            initial_color = self._highlight or self._default_colors[1]
        else:
            raise ValueError("Unexpected color picker tag: {}".format(tag))
        ColorPicker(
            parent=self._root_widget,
            position=(0, 0),
            initial_color=initial_color,
            delegate=self,
            tag=tag,
        )

    def cancel_on_outside_click(self):
        bui.getsound("swish").play()
        self._cancel()

    def _cancel(self):
        if self._last_color and self._last_highlight:
            colorscheme = ColorScheme(self._last_color, self._last_highlight)
            colorscheme.apply()
        # Restore original pro check
        bui.app.classic.accounts.have_pro = original_have_pro
        bui.containerwidget(edit=self._root_widget, transition="out_right")

    def reset(self, transition_out=True):
        if transition_out:
            bui.getsound("gunCocking").play()
        babase.app.config["ColorScheme"] = (None, None)
        # Restore original pro check
        bui.app.classic.accounts.have_pro = original_have_pro
        babase.app.config.commit()
        bui.containerwidget(edit=self._root_widget, transition="out_right")

    def save(self, transition_out=True):
        if transition_out:
            bui.getsound("gunCocking").play()
        colorscheme = ColorScheme(
            self._color or self._default_colors[0],
            self._highlight or self._default_colors[1],
        )
        colorscheme.apply()
        # Restore original pro check
        bui.app.classic.accounts.have_pro = original_have_pro
        babase.app.config["ColorScheme"] = (
            self._color or self._default_colors[0],
            self._highlight or self._default_colors[1],
        )
        babase.app.config.commit()
        bui.containerwidget(edit=self._root_widget, transition="out_right")

    def _set_color(self, color):
        self._color = color
        if self._color_button:
            bui.buttonwidget(edit=self._color_button, color=color)

    def _set_highlight(self, color):
        self._highlight = color
        if self._highlight_button:
            bui.buttonwidget(edit=self._highlight_button, color=color)

    def color_picker_selected_color(self, picker, color):
        if not self._root_widget:
            return
        tag = picker.get_tag()
        if tag == "color":
            self._set_color(color)
        elif tag == "highlight":
            self._set_highlight(color)

    def color_picker_closing(self, picker):
        pass

def launch_colorscheme_selection_window():
    ColorSchemeWindow()

def load_colorscheme():
    color, highlight = babase.app.config.get("ColorScheme", (None, None))
    if color and highlight:
        colorscheme = ColorScheme(color, highlight)
        colorscheme.apply()

# بارگذاری پلاگین رنگ‌ها هنگام راه‌اندازی
load_colorscheme()

class ColorSchemeWindow(bui.Window):
    def __init__(self, default_colors=((0.41, 0.39, 0.5), (0.5, 0.7, 0.25))):
        self._default_colors = default_colors
        self._color, self._highlight = babase.app.config.get("ColorScheme", (None, None))

        self._last_color = self._color
        self._last_highlight = self._highlight

        # Let's set the game's default colorscheme before opening the Window.
        # Otherwise the colors in the Window are tinted as per the already
        # applied custom colorscheme thereby making it impossible to visually
        # differentiate between different colors.
        ColorScheme.disable()

        # A hack to let players select any RGB color value through the UI,
        # otherwise this is limited only to pro accounts.
        bui.app.classic.accounts.have_pro = lambda: True

        self.draw_ui()

    def draw_ui(self):
        # NOTE: Most of the stuff here for drawing the UI is referred from the
        # legacy (1.6 < version <= 1.7.19) game's bastd/ui/profile/edit.py, and
        # so there could be some cruft here due to my oversight.
        uiscale = bui.app.ui_v1.uiscale
        self._width = width = 480.0 if uiscale is babase.UIScale.SMALL else 380.0
        self._x_inset = x_inset = 40.0 if uiscale is babase.UIScale.SMALL else 0.0
        self._height = height = (
            275.0
            if uiscale is babase.UIScale.SMALL
            else 288.0
            if uiscale is babase.UIScale.MEDIUM
            else 300.0
        )
        spacing = 40
        self._base_scale = (
            2.05
            if uiscale is babase.UIScale.SMALL
            else 1.5
            if uiscale is babase.UIScale.MEDIUM
            else 1.0
        )
        top_extra = 15

        super().__init__(
            root_widget=bui.containerwidget(
                size=(width, height + top_extra),
                on_outside_click_call=self.cancel_on_outside_click,
                transition="in_right",
                scale=self._base_scale,
                stack_offset=(0, 15) if uiscale is babase.UIScale.SMALL else (0, 0),
            )
        )

        cancel_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(52 + x_inset, height - 60),
            size=(155, 60),
            scale=0.8,
            autoselect=True,
            label=babase.Lstr(resource="cancelText"),
            on_activate_call=self._cancel,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=cancel_button)

        save_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(width - (177 + x_inset), height - 110),
            size=(155, 60),
            autoselect=True,
            scale=0.8,
            label=babase.Lstr(resource="saveText"),
        )
        bui.widget(edit=save_button, left_widget=cancel_button)
        bui.buttonwidget(edit=save_button, on_activate_call=self.save)
        bui.widget(edit=cancel_button, right_widget=save_button)
        bui.containerwidget(edit=self._root_widget, start_button=save_button)

        reset_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(width - (177 + x_inset), height - 60),
            size=(155, 60),
            color=(0.2, 0.5, 0.6),
            autoselect=True,
            scale=0.8,
            label=babase.Lstr(resource="settingsWindowAdvanced.resetText"),
        )
        bui.widget(edit=reset_button, left_widget=reset_button)
        bui.buttonwidget(edit=reset_button, on_activate_call=self.reset)
        bui.widget(edit=cancel_button, right_widget=reset_button)
        bui.containerwidget(edit=self._root_widget, start_button=reset_button)

        v = height - 65.0
        v -= spacing * 3.0
        b_size = 80
        b_offs = 75

        self._color_button = bui.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(self._width * 0.5 - b_offs - b_size * 0.5, v - 50),
            size=(b_size, b_size),
            color=self._last_color or self._default_colors[0],
            label="",
            button_type="square",
        )
        bui.buttonwidget(
            edit=self._color_button, on_activate_call=babase.Call(self._pick_color, "color")
        )
        bui.textwidget(
            parent=self._root_widget,
            h_align="center",
            v_align="center",
            position=(self._width * 0.5 - b_offs, v - 65),
            size=(0, 0),
            draw_controller=self._color_button,
            text=babase.Lstr(resource="editProfileWindow.colorText"),
            scale=0.7,
            color=bui.app.ui_v1.title_color,
            maxwidth=120,
        )

        self._highlight_button = bui.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(self._width * 0.5 + b_offs - b_size * 0.5, v - 50),
            size=(b_size, b_size),
            color=self._last_highlight or self._default_colors[1],
            label="",
            button_type="square",
        )

        bui.buttonwidget(
            edit=self._highlight_button,
            on_activate_call=babase.Call(self._pick_color, "highlight"),
        )
        bui.textwidget(
            parent=self._root_widget,
            h_align="center",
            v_align="center",
            position=(self._width * 0.5 + b_offs, v - 65),
            size=(0, 0),
            draw_controller=self._highlight_button,
            text=babase.Lstr(resource="editProfileWindow.highlightText"),
            scale=0.7,
            color=bui.app.ui_v1.title_color,
            maxwidth=120,
        )

    def _pick_color(self, tag):
        if tag == "color":
            initial_color = self._color or self._default_colors[0]
        elif tag == "highlight":
            initial_color = self._highlight or self._default_colors[1]
        else:
            raise ValueError("Unexpected color picker tag: {}".format(tag))
        ColorPicker(
            parent=None,
            position=(0, 0),
            initial_color=initial_color,
            delegate=self,
            tag=tag,
        )

    def cancel_on_outside_click(self):
        bui.getsound("swish").play()
        self._cancel()

    def _cancel(self):
        if self._last_color and self._last_highlight:
            colorscheme = ColorScheme(self._last_color, self._last_highlight)
            colorscheme.apply()
        # Good idea to revert this back now so we do not break anything else.
        bui.app.classic.accounts.have_pro = original_have_pro
        bui.containerwidget(edit=self._root_widget, transition="out_right")

    def reset(self, transition_out=True):
        if transition_out:
            bui.getsound("gunCocking").play()
        babase.app.config["ColorScheme"] = (None, None)
        # Good idea to revert this back now so we do not break anything else.
        bui.app.classic.accounts.have_pro = original_have_pro
        babase.app.config.commit()
        bui.containerwidget(edit=self._root_widget, transition="out_right")

    def save(self, transition_out=True):
        if transition_out:
            bui.getsound("gunCocking").play()
        colorscheme = ColorScheme(
            self._color or self._default_colors[0],
            self._highlight or self._default_colors[1],
        )
        colorscheme.apply()
        # Good idea to revert this back now so we do not break anything else.
        bui.app.classic.accounts.have_pro = original_have_pro
        babase.app.config["ColorScheme"] = (
            self._color or self._default_colors[0],
            self._highlight or self._default_colors[1],
        )
        babase.app.config.commit()
        bui.containerwidget(edit=self._root_widget, transition="out_right")

    def _set_color(self, color):
        self._color = color
        if self._color_button:
            bui.buttonwidget(edit=self._color_button, color=color)

    def _set_highlight(self, color):
        self._highlight = color
        if self._highlight_button:
            bui.buttonwidget(edit=self._highlight_button, color=color)

    def color_picker_selected_color(self, picker, color):
        # The `ColorPicker` calls this method in the delegate once a color
        # is selected from the `ColorPicker` Window.
        if not self._root_widget:
            return
        tag = picker.get_tag()
        if tag == "color":
            self._set_color(color)
        elif tag == "highlight":
            self._set_highlight(color)
        else:
            raise ValueError("Unexpected color picker tag: {}".format(tag))

    def color_picker_closing(self, picker):
        # The `ColorPicker` expects this method to exist in the delegate,
        # so here it is!
        pass


class CustomTransactions:
    def __init__(self):
        self.custom_transactions = {}

    def _handle(self, transaction, *args, **kwargs):
        transaction_code = transaction.get("code")
        transaction_fn = self.custom_transactions.get(transaction_code)
        if transaction_fn is not None:
            return transaction_fn(transaction, *args, **kwargs)
        return original_add_transaction(transaction, *args, **kwargs)

    def add(self, transaction_code, transaction_fn):
        self.custom_transactions[transaction_code] = transaction_fn

    def enable(self):
        bui.app.plus.add_v1_account_transaction = self._handle


def launch_colorscheme_selection_window():
    # We store whether the player is a pro account or not since we
    # temporarily attempt to bypass the limitation where only pro
    # accounts can set custom RGB color values, and we restore this
    # value back later on.

    # Also, we attempt to store this value here (and not in the
    # beginning) since the player might be using other dedicated
    # pro-unlocker plugins which may attempt to override the game
    # method early on in the beginning, therefore, leading us to a
    # race-condition and we may not correctly store whether the player
    # has pro-unlocked or not if our plugin runs before the dedicated
    # pro-unlocker plugin has been applied.
    global original_have_pro
    original_have_pro = bui.app.classic.accounts.have_pro

    ColorSchemeWindow()


def colorscheme_transaction(transaction, *args, **kwargs):
    launch_colorscheme_selection_window()


def load_colorscheme():
    color, highlight = babase.app.config.get("ColorScheme", (None, None))
    if color and highlight:
        colorscheme = ColorScheme(color, highlight)
        colorscheme.apply()


def load_plugin():
    # Allow access to changing colorschemes manually through the in-game
    # console.
    _babase.ColorScheme = ColorScheme
    # Adds a new advanced code entry named "colorscheme" which can be
    # entered through Settings -> Advanced -> Enter Code, allowing
    # colorscheme modification through a friendly UI.
    custom_transactions = CustomTransactions()
    custom_transactions.add("colorscheme", colorscheme_transaction)
    custom_transactions.enable()
    # Load any previously saved colorscheme.
    load_colorscheme()

# بارگذاری پلاگین رنگ‌ها هنگام راه‌اندازی
load_plugin()

# فلگ متوقف کردن ارسال
_stop_sending_icons = False
_icon_timers = []  # لیست همه تایمرهای فعال
_icons_menu_opened = False  # بررسی اینکه منو باز است یا نه

def show_icons_menu(source_widget=None):
    """نمایش منوی نمادها - ویندوز باریک و بلند با کنترل توقف"""
    global _icons_menu_opened
    if _icons_menu_opened:
        return  # اگر منو باز است، دوباره ایجاد نشود
    _icons_menu_opened = True

    try:
        icons = [
            ('', ' نماد 1'),
            ('', ' نماد 2'),
            ('', ' نماد 3'),
            ('', ' نماد 4'),
            ('', ' نماد 5'),
            ('', ' نماد 6'),
            ('', ' نماد 7'),
            ('', ' نماد 8'),
            ('', ' نماد 9'),
            ('', ' نماد 10'),
            ('', ' نماد 11'),
            ('', ' نماد 12'),
            ('', ' نماد 13'),
            ('', ' نماد 14'),
            ('', ' نماد 15'),
            ('', ' نماد 16'),
            ('', ' نماد 17'),
            ('', ' نماد 18'),
            ('', ' نماد 19'),
            ('', ' نماد 20'),
            ('', ' نماد 21'),
            ('', ' نماد 22'),
            ('', ' نماد 23'),
            ('', ' نماد 24'),
            ('', ' نماد 25'),
            ('', ' نماد 26'),
            ('', ' نماد 27'),
            ('', ' نماد 28'),
            ('', ' نماد 29'),
            ('', ' نماد 30'),
            ('', ' نماد 31'),
            ('', ' نماد 32'),
            ('', ' نماد 33'),
            ('', ' نماد 34'),
            ('', ' نماد 35'),
            ('', ' نماد 36')
        ]

        w = bui.containerwidget(
            parent=bui.get_special_widget('overlay_stack'),
            size=(800, 700),
            scale=1.0,
            transition='in_scale',
            color=(0.12, 0.12, 0.12)
        )

        bui.textwidget(
            parent=w,
            text='نمادهای بازی',
            position=(400, 660),
            scale=1.3,
            color=(1, 1, 0),
            h_align='center'
        )

        scroll = bui.scrollwidget(
            parent=w,
            size=(700, 550),
            position=(60, 90)
        )

        column = bui.columnwidget(parent=scroll, left_border=10)

        for icon, label in icons:
            bui.buttonwidget(
                parent=column,
                size=(650, 50),
                label=label,
                on_activate_call=lambda i=icon: send_icon(i),
                color=(0.35, 0.35, 0.45),
                textcolor=(1, 1, 1)
            )

        # دکمه ارسال همه
        bui.buttonwidget(
            parent=w,
            position=(100, 30),
            size=(200, 60),
            label='ارسال همه (2ثانیه)',
            on_activate_call=lambda: send_all_icons_delayed(icons, 2.0),
            color=(0.2, 0.6, 0.2),
            textcolor=(1, 1, 1)
        )

        # دکمه توقف ارسال
        bui.buttonwidget(
            parent=w,
            position=(525, 30),
            size=(180, 60),
            label='⛔ توقف ارسال',
            on_activate_call=stop_sending_icons,
            color=(0.8, 0.3, 0.3),
            textcolor=(1, 1, 1)
        )

        # دکمه بستن
        bui.buttonwidget(
            parent=w,
            position=(350, 30),
            size=(120, 60),
            label='بستن',
            on_activate_call=lambda: close_icons_menu(w),
            color=(0.6, 0.2, 0.2),
            textcolor=(1, 1, 1)
        )

    except Exception as e:
        print(f"Error showing icons menu: {e}")

def close_icons_menu(widget):
    """بستن منوی نمادها"""
    global _icons_menu_opened
    _icons_menu_opened = False
    bui.containerwidget(edit=widget, transition='out_scale')

def send_icon(icon: str):
    """ارسال نماد به چت"""
    try:
        bs.chatmessage(icon)
        bui.screenmessage(f'ارسال شد: {icon}', color=(0, 1, 0))
        bui.getsound('dingSmall').play()
    except Exception as e:
        print(f"Error sending icon: {e}")

def send_all_icons_delayed(icons, delay_seconds=2.0):
    """ارسال همه نمادها با تأخیر"""
    global _stop_sending_icons, _icon_timers
    _stop_sending_icons = False
    _icon_timers = []

    try:
        bui.screenmessage(f'شروع ارسال همه نمادها (هر {delay_seconds} ثانیه)...', color=(0, 1, 1))
        for i, (icon, _) in enumerate(icons):
            t = bui.apptimer(i * delay_seconds, lambda ic=icon: send_single_icon_delayed(ic))
            _icon_timers.append(t)
    except Exception as e:
        print(f"Error starting delayed send: {e}")

def send_single_icon_delayed(icon: str):
    """ارسال تک نماد با تأخیر"""
    global _stop_sending_icons
    try:
        if _stop_sending_icons:
            return
        bs.chatmessage(icon)
        bui.screenmessage(f'ارسال شد: {icon}', color=(0, 1, 0))
    except Exception as e:
        print(f"Error sending delayed icon: {e}")

def stop_sending_icons():
    """توقف کامل ارسال همه نمادها"""
    global _stop_sending_icons, _icon_timers
    _stop_sending_icons = True
    # همه تایمرها رو لغو کنیم
    for t in _icon_timers:
        try:
            t.cancel()
        except Exception:
            pass
    _icon_timers = []
    bui.screenmessage('⛔ ارسال همه نمادها متوقف شد', color=(1, 0, 0))

# ba_meta require api 9
# ba_meta export plugin
class byTaha(Plugin):
    me = lambda c=0: APP.plus.get_v1_account_name() if APP.plus.get_v1_account_state() == 'signed_in' else '???'
    v2 = cs(sc.V2_LOGO)
    B = '​'
    
    def __init__(s):
        # اورراید کردن توابع اتصال
        setup_connection_overrides()
        
        # اضافه کردن متغیر آنتی اسپم
        s.last_command_time = {}
        s.cooldown_time = 1.5  # 4 ثانیه تأخیر بین دستورات
        
        o = party.PartyWindow.__init__
        def e(s,*a,**k):
            r = o(s,*a,**k)
            
            b_icons = AR.bw(
                icon=gt('star'),  
                position=(s._width+10, s._height-112), 
                parent=s._root_widget,
                iconscale=0.6,
                size=(80, 25),
                label='نمادها'
            )
            bw(b_icons, on_activate_call=Call(show_icons_menu, source_widget=b_icons))
            
            
            # دکمه تغییر رنگ UI (همانند قبل)
            b_uicolor = AR.bw(
                icon=gt('egg2'),
                position=(s._width+10, s._height-144),
                parent=s._root_widget,
                iconscale=0.6,
                size=(80,25),
                label='رنگ UI'
            )
            bw(b_uicolor, on_activate_call=Call(UIColorChanger, source=b_uicolor))
                  # دکمه اطلاعات بازیکنان - زیر تغییر رنگ UI
            b_playerinfo = AR.bw(
                icon=gt('ouyaOButton'),
                position=(s._width+10, s._height-176),  # زیر تغییر رنگ UI
                parent=s._root_widget,
                iconscale=0.6,
                size=(80,25),
                label='بازیکنان'
            )
            bw(b_playerinfo, on_activate_call=Call(PlayerInfo, source=b_playerinfo))
            
            # دکمه چت لاگ - بالای استیکر
            b_chatlog = AR.bw(
                icon=gt('logo'),
                position=(s._width+10,s._height-240),  # بالای استیکر
                parent=s._root_widget,
                iconscale=0.6,
                size=(80,25),
                label='چت لاگ'
            )
            bw(b_chatlog,on_activate_call=Call(ChatLog,source=b_chatlog))
            
            # دکمه فونت‌ساز - بالای استیکر
            b_font = AR.bw(
                icon=gt('star'),
                position=(s._width+10, s._height-208),  # 30px بالاتر از استیکر
                parent=s._root_widget,
                iconscale=0.6,
                size=(80,25),
                label='فونت‌ساز'
            )
            bw(b_font, on_activate_call=Call(FontMaker, source=b_font))
            
            # دکمه استیکر - زیر چت لاگ
            b_sticker = AR.bw(
                icon=gt('heart'),
                position=(s._width+10,s._height-272),  # زیر چت لاگ
                parent=s._root_widget,
                iconscale=0.6,
                size=(80,25),
                label='استیکر'
            )
            bw(b_sticker,on_activate_call=Call(StickerMenu,source=b_sticker))
            
            # دکمه اصلی پیام اتوماتیک
            b_main = AR.bw(
                icon=gt('achievementOutline'),
                position=(s._width+10,s._height-45),
                parent=s._root_widget,
                iconscale=0.7,
                size=(90,30),
                label='پیام اتوماتیک'
            )
            bw(b_main,on_activate_call=Call(AR,source=b_main))
            
            return r
        party.PartyWindow.__init__ = e
        s.z = []
        teck(5,s.ear)
    
    def __del__(s):
        # توقف thread پینگ هنگام حذف پلاگین
        if ping_thread:
            ping_thread.stop()
    
    def ear(s):
        z = GCM()
        teck(0.3,s.ear)
        if z == s.z: return
        
        # بررسی وضعیت خاموش/روشن
        if not var('state'):  # اگر حالت خاموش است
            s.z = z  # به روز رسانی ولی هیچ پاسخی نده
            return
        
        s.z = z;
        v = z[-1]
        if v.endswith(s.B): return
        
        # بررسی فرمت پیام
        if ': ' not in v:
            return
            
        f,m = v.split(': ',1)
        k = s.me()
        if f in [k,s.v2+k] and not var('tune2'): return
        
        # سیستم آنتی اسپم - بررسی تأخیر 4 ثانیه
        current_time = time.time()
        if f in s.last_command_time:
            time_since_last = current_time - s.last_command_time[f]
            if time_since_last < s.cooldown_time:
                return  # هنوز تأخیر تمام نشده
        
        if var('tune3'): 
            l = var('l')
        else: 
            m = m.lower()
            l = var('lc')
            
        h = l.get(m,None)
        if h is not None: # equal
            a,b,_ = h
            s.S(b,a,f,0)
            s.last_command_time[f] = current_time  # ثبت زمان آخرین دستور
        else: # wild
            re = [y for y,_ in sorted([(y,m.find(y)) for y in l if y in m],key=lambda x: x[1])]
            for r in re:
                a,b,c = l.get(r,[0,0,0])
                if not r or not c: continue # unwild :c
                s.S(b,a,f,1)
                s.last_command_time[f] = current_time  # ثبت زمان آخرین دستور
                break  # فقط به یک دستور پاسخ بده
    
    def S(s,b,a,f,j):
        p = AR.parse(t=a,s=f)
        teck(b,Call(CM,p+s.B))
        push(f"{['برابر','شامل'][j]}!\nپاسخ به: {f}\nبا متن: {p}\nبعد از {b} ثانیه!",color=(0,0.8,0.8)) if var('tune0') else None
        gs('dingSmallHigh').play() if var('tune1') else None
