# -*- coding: utf-8 -*-
# SinglMod v5.1 - Ultimate Edition
# Copyright 2025 - Edit by Amiry | @Amiry_11228
import babase
import _babase
import bauiv1
import bascenev1
import os
import sys
import socket
import threading
import random
import time
import bascenev1 as bs
import bauiv1 as bui
import json
import math
import re
from datetime import datetime as DT
from babase import apptimer as teck

sys.path.append(os.path.join(os.path.dirname(__file__), 'bombsquad_files'))

ba = babase
_ba = _babase
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
from bauiv1lib import party
from babase import apptimer as teck
from bauiv1 import Call

PARTY_COLORS = [
    ("قرمز", (9,0,0)),

    ("صورتی تیره", (5,0,3)),
    ("زرد لیمویی", (7,9,0)),
    ("آبی برقی", (0,7,9))
]

# متغیرهای پینگ و اطلاعات سرور - واقعی
current_ping = 0.0
server_ip = "127.0.0.1"
server_port = 43210
server_name = "Local Server"

JOKES = [
    "یارو تو دایرکت pm می‌ده، فکر کرده منم مثل خودش بیکارم!",
    "شلوارم انقدر تنگه، فکر کنم قلبمم توش گیر کرده!",
    "تو کلاب رقصیدم تا صبح، فقط عرقم دراومد، یکی نیومد مخمو بزنه!",
    "دختره انقدر فیلتر اینستا عوض کرد، آخرش قلبش فیلتر شد!",
    "پسره تو جیم فقط سلفی می‌گیره، فکر کنم می‌خواد سیکس‌پکشو pm کنه!",
    "تو مهمونی انقدر مشروب خوردم، آخرش به جای یار، میزو بغل کردم!",
    "گربه‌م انقدر پررو شده، فکر کنم چون دیده من با همه دم تکون می‌دم!",
    "تو کافه قلیون کشیدم، انقدر غلیظ بود فکر کردم الان یکی میاد مخمو بزنه!",
    "چرا یارو آفلاینه؟ چون تو دایرکت یکی دیگه داره حالشو می‌بره!",
    "دختره استوری غمگین گذاشت، ولی تو دایرکت داره قربون‌صدقه یکی می‌ره!",
    "تو ماشین آهنگ شاد پلی می‌کنم که ملت فکر کنن یکی بغلم نشسته!",
    "یارو تو تخت انقدر خرناس کشید، فکر کردم داره موتور گازی روشن می‌کنه!",
    "چرا پسره همیشه تو اینستا گریه می‌کنه؟ چون دایرکتش خالیه!",
    "دختره انقدر آرایش کرد، فکر کردم داره واسه فیلما تست گریم می‌ده!",
    "تو پارتی انقدر رقصیدم، آخرش فقط جورابم یکیو تور کرد!",
    "چرا یارو همیشه تو چت لاس می‌زنه؟ چون کیبوردش ازش پرروتره!",
    "دختره تو جیم فقط با گوشی کار می‌کنه، فکر کنم داره قلب یکیو دمبل می‌زنه!",
    "تو کافه یکی بهم چشمک زد، ولی بعد فهمیدم قلیون تو چشمش رفته!",
    "پسره تو دایرکت قلب فرستاد، ولی من فقط لایک کردم که ضایع شه!",
    "چرا شلوار جین پاره‌ست؟ چون صاحبش زیادی دنبال عشق و حال بوده!",
    "تو مهمونی انقدر مست کردم، فکر کردم میز داره باهام حرف می‌زنه!",
    "دختره انقدر فیلتر گذاشت، فکر کردم داره واسه ناسا عکس می‌فرسته!",
    "یارو تو کلاب گفت مخمو می‌زنم، ولی فقط شماره گارسونو گرفت!",
    "چرا پسره همیشه تو اینستا آنلاینه؟ چون منتظره یکی pm بده!",
    "تو جیم انقدر وزنه زدم، آخرش فقط دل یکیو زدم!",
    "دختره استوری گذاشت 'تنهام'، ولی تو دایرکت داره پارتی راه می‌ندازه!",
    "چرا یارو تو کافه سیگار می‌کشه؟ چون فکر می‌کنه اینجوری باکلاسه!",
    "تو پارتی یکی گفت عاشقتم، ولی بعد فهمیدم مشروب حرفشو زده!",
    "پسره تو اینستا فالو کرد، ولی من بلاکش کردم که حالش جا بیاد!",
    "چرا شلوارم انقدر پاره‌ست؟ چون تو مهمونی زیادی قر دادم!",
    "دختره تو جیم فقط سلفی می‌گیره، فکر کنم می‌خواد قلب یکیو استوری کنه!",
    "تو کلاب انقدر رقصیدم، آخرش فقط کفشم یکیو گرفت!",
    "یارو تو دایرکت گفت می‌میرم برات، ولی من فقط خوندم و رد شدم!",
    "چرا پسره همیشه تو چت قلب می‌فرسته؟ چون کیبوردش فقط بلده عاشق بشه!",
    "تو کافه قلیون کشیدم، انقدر غلیظ بود فکر کردم عشقم پیدام کرد!",
    "دختره انقدر آرایش کرد، فکر کردم داره واسه هالووین آماده می‌شه!",
    "تو پارتی انقدر مشروب خوردم، آخرش به جای یار، دیوارو بوسیدم!",
    "چرا یارو تو اینستا استوری غمگین می‌ذاره؟ چون دایرکتش مثه کویر لوطه!",
    "پسره تو جیم فقط دمبل می‌زنه، ولی قلبشو هیچ‌کس بلند نکرد!",
    "دختره تو چت گفت دلم تنگه، ولی تو دایرکت داره با یکی دیگه عشق و حال می‌کنه!",
    "تو کلاب یکی بهم گفت خوشگلی، ولی بعد فهمیدم مست بود و منو با گارسون اشتباه گرفت!",
    "چرا یارو تو پارتی ساکته؟ چون منتظره یکی بیاد مخشو بزنه!",
    "دختره تو اینستا فقط قلب می‌ذاره، ولی تو واقعیت قلبشو یکی دیگه برده!",
    "تو جیم انقدر سلفی گرفتم، فکر کنم قلب یکیو تو استوری زدم!",
    "یارو تو دایرکت گفت بیا قرار بذاریم، ولی من فقط بلاکش کردم!",
    "چرا پسره تو کافه سیگار می‌کشه؟ چون فکر می‌کنه اینجوری یکی میاد مخشو بزنه!",
    "تو پارتی انقدر رقصیدم، آخرش فقط جورابم پاره شد!",
    "دختره تو اینستا استوری کرد 'بی‌خوابم'، ولی تو دایرکت داره پارتی می‌کنه!",
    "چرا یارو تو چت انقدر لاس می‌زنه؟ چون فکر می‌کنه کیبوردش شهناز تهرانیه!",
    "تو کلاب انقدر مست کردم، فکر کردم گارسون عشقمه و بغلش کردم!",
    "تو دایرکت گفت بیا مخمو بزن، ولی من فقط بلاکش کردم که حالش جا بیاد!",
    "شلوارم انقدر تنگه، فکر کنم عشقمم توش گیر کرده!",
    "تو پارتی انقدر رقصیدم، آخرش فقط یکی کفشمو دزدید!",
    "دختره تو اینستا استوری کرد 'تنهام'، ولی تو دایرکت داره با سه تا عشق و حال می‌کنه!",
    "چرا یارو تو جیم فقط سلفی می‌گیره؟ چون می‌خواد سیکس‌پکشو تو دایرکت pm کنه!",
    "تو کلاب انقدر مست کردم، به گارسون گفتم عاشقتم، اونم گفت بشین بابا!",
    "دختره انقدر آرایش کرد، فکر کردم داره واسه فیلم زامبیا گریم می‌کنه!",
    "چرا پسره تو چت قلب می‌فرسته؟ چون کیبوردش فکر می‌کنه عاشق شده!",
    "تو کافه قلیون کشیدم، انقدر غلیظ بود فکر کردم الان یکی میاد زنم بشه!",
    "یارو تو دایرکت گفت می‌میرم برات، منم گفتم بمیر، من که pm نمیدم!",
    "چرا شلوار جینم پاره‌ست؟ چون تو پارتی زیادی قر دادم و عشقم پاره کرد!",
    "دختره تو جیم فقط با فیلتر سلفی می‌گیره، فکر کنم می‌خواد قلب یکیو استوری کنه!",
    "تو پارتی یکی بهم چشمک زد، ولی بعد فهمیدم قلیون تو چشمش پریده!",
    "پسره تو اینستا استوری غمگین گذاشت، ولی تو دایرکت داره با یکی قربون‌صدقه می‌ره!",
    "چرا یارو تو کلاب ساکته؟ چون منتظره یکی بیاد مخشو بزنه، ولی فقط گارسون پیداشه!",
    "تو جیم انقدر وزنه زدم، آخرش فقط قلبمو یکی بلند کرد و برد!",
    "دختره تو چت گفت دلم تنگه، ولی تو دایرکت داره با یکی دیگه عشقشو آپدیت می‌کنه!",
    "چرا یارو تو کافه سیگار می‌کشه؟ چون فکر می‌کنه اینجوری یکی میاد pm بده!",
    "تو پارتی انقدر مشروب خوردم، آخرش به جای یار، دیوارو بغل کردم!",
    "پسره تو دایرکت قلب فرستاد، منم بلاکش کردم که بفهمه قلبش مال من نیست!",
    "چرا دختره تو اینستا فیلتر عوض می‌کنه؟ چون می‌خواد قلب یکیو تو استوری تور کنه!",
    "تو کلاب انقدر رقصیدم، آخرش فقط جورابم یکیو گرفت و رفت!",
    "یارو تو چت گفت بیا قرار بذاریم، منم گفتم برو با کیبوردت قرار بذار!",
    "چرا پسره تو جیم دمبل می‌زنه؟ چون فکر می‌کنه اینجوری یکی دلشو بلند می‌کنه!",
    "تو کافه یکی بهم گفت خوشگلی، ولی بعد فهمیدم مست بود و منو با لیوان اشتباه گرفت!",
    "دختره تو اینستا استوری کرد 'بی‌خوابم'، ولی تو دایرکت داره با یکی پارتی می‌کنه!",
    "چرا یارو تو پارتی انقدر مشروب خورد؟ چون فکر کرد اینجوری یکی میاد بغلش!",
    "پسره تو دایرکت گفت عاشقتم، منم گفتم برو گمشو، من فقط فالو می‌کنم!",
    "تو جیم انقدر سلفی گرفتم، فکر کردم قلب یکیو تو اینستا استوری کردم!",
    "چرا شلوارم انقدر پاره‌ست؟ چون تو کلاب زیادی دنبال عشق و حال بودم!",
    "دختره تو چت گفت دلم برات تنگه، ولی تو دایرکت داره با یکی دیگه عشقشو آپلود می‌کنه!",
    "تو پارتی انقدر رقصیدم، آخرش فقط کفشم پاره شد و یارو رفت!",
    "چرا پسره تو اینستا همیشه آنلاینه؟ چون منتظره یکی pm بده، ولی فقط اسپم میاد!",
    "دختره انقدر آرایش کرد، فکر کردم داره واسه فیلم ترسناک آماده می‌شه!",
    "تو کلاب یکی بهم گفت مخمو می‌زنم، ولی آخرش فقط شماره گارسونو گرفتم!",
    "چرا یارو تو چت لاس می‌زنه؟ چون فکر می‌کنه کیبوردش شهناز تهرانیه!",
    "تو پارتی انقدر مست کردم، فکر کردم دیوار داره باهام رقص تانگو می‌کنه!",
    "دختره تو اینستا استوری کرد 'تنها'، ولی تو دایرکت داره با پنج تا چت می‌کنه!",
    "چرا پسره تو جیم فقط سینه می‌زنه؟ چون می‌خواد قلب یکیو تو دایرکت بزنه!",
    "تو کافه قلیون کشیدم، انقدر غلیظ بود فکر کردم الان یکی میاد منو بغل کنه!",
    "یارو تو دایرکت گفت بیا عشق و حال، منم گفتم برو با فیلتر اینستا حال کن!",
    "چرا شلوار جینم انقدر تنگه؟ چون تو پارتی زیادی قر دادم و عشقم پاره کرد!",
    "دختره تو جیم سلفی گرفت، فکر کنم می‌خواد قلب یکیو تو استوری دمبل کنه!",
    "تو کلاب یکی بهم چشمک زد، ولی بعد فهمیدم مشروب تو چشمش پریده!",
    "چرا پسره تو اینستا استوری غمگین می‌ذاره؟ چون دایرکتش مثه قبرستونه!",
    "تو پارتی انقدر مشروب خوردم، آخرش به جای یار، بطریو بوسیدم!",
    "دختره تو چت گفت عاشقتم، ولی تو دایرکت داره با یکی دیگه عشقشو استوری می‌کنه!",
    "چرا یارو تو کافه سیگار می‌کشه؟ چون فکر می‌کنه اینجوری یکی میاد مخشو بزنه!",
    "تو جیم انقدر وزنه زدم، آخرش فقط قلبمو یکی دزدید و رفت!",
    "پسره تو دایرکت گفت بیا قرار، منم گفتم برو با کیبوردت قرار بذار که تنهاست!"
]

RIDDLES = [
    ("آن چیست که در ابتدا چهار پا دارد، سپس دو پا و در نهایت سه پا؟", "انسان"),
    ("آن چیست که روز می‌دود و شب پاسبان اتاق است؟", "کفش"),
    ("خانه‌ای یک طبقه که تماماً از چوب سرخ‌چوب ساخته شده، پله‌هایش چه رنگی است؟", "پله ندارد"),
    ("آن چیست که هر چه بیشتر می‌گیری، کوچکتر می‌شود؟", "سوراخ"),
    ("چه چیزی بالا و پایین می‌شود اما حرکت نمی‌کند؟", "آسانسور"),
    ("آن چیست که در دست راست نگه می‌داریم اما در دست چپ نه؟", "آرنج"),
    ("آن چیست که چیستان است، در شهر خراسان است، در جیب بزرگان است؟", "تسبیح"),
    ("آن چیست که هم در دریا هست و هم در غذا؟", "نمک"),
    ("آن چیست که ما می‌رویم و آن می‌ماند؟", "سایه"),
    ("آن چیست که بدنش از آجر یا چوب ساخته شده و در و پنجره‌های زیادی دارد؟", "اجاق گاز"),
    ("آن چیست که خوش طعم و شیرین است، می‌توانی لیسش بزنی، هم در پیاله است و هم در قیف؟", "بستنی"),
    ("اگر یک فیل بالای درخت برود چی می‌شود؟", "یک فیل از فیل‌های روی زمین کم می‌شود"),
    ("دو اتومبیل آبی و قرمز با سرعت‌های ۶۰ و ۴۰ مایل حرکت می‌کنند و از هم عبور می‌کنند، کجا؟", "در آینه عقب"),
    ("سه مرد در اتاقی با پنجره کوچک زندانی‌اند و نمی‌رسند، چطور فرار کنند؟", "از در"),
    ("آن چیست که در آشپزخانه هست و در اتومبیل هم؟", "فر"),
    ("پسر مادربزرگ و پدربزرگ شماست اما عموی شما نیست؟", "پدرتان"),
    ("آن چیست که هرگز خیس نمی‌شود؟", "دریا"),
    ("آن چیست که صدای بلند دارد اما دهان ندارد؟", "آواز"),
    ("آن چیست که پرواز می‌کند بدون بال؟", "زمان"),
    ("آن چیست که می‌رود دور بدون چرخ؟", "دور"),
    ("آن چیست که همه جا هست اما دیده نمی‌شود؟", "هوا"),
    ("آن چیست که زنده است بدون نفس؟", "درخت"),
    ("آن چیست که می‌خورد و نمی‌نوشد؟", "آتش"),
    ("آن چیست که می‌بیند بدون چشم؟", "ذهن"),
    ("آن چیست که می‌آید بدون دعوت؟", "خواب"),
    ("آن چیست که می‌ریزد بدون باران؟", "اشک"),
    ("آن چیست که می‌چرخد بدون چرخ؟", "سر"),
    ("آن چیست که می‌خندد بدون دهان؟", "دنیا"),
    ("آن چیست که می‌میرد بدون کشته شدن؟", "امید"),
    ("آن چیست که می‌دوئه بدون پا؟", "ماشین"),
    ("آن چیست که همه را می‌خورد؟", "زمان"),
    ("آن چیست که همیشه می‌آید؟", "فردا"),
    ("آن چیست که هرگز نمی‌رود؟", "گذشته"),
    ("آن چیست که همه را می‌بیند؟", "خورشید"),
    ("آن چیست که همه را گرم می‌کند؟", "آتش"),
    ("آن چیست که همه را روشن می‌کند؟", "نور"),
    ("آن چیست که همه را می‌شوید؟", "باران"),
    ("آن چیست که همه را می‌برد؟", "باد"),
    ("آن چیست که همه را می‌پوشاند؟", "برف"),
    ("آن چیست که همه را می‌سازد؟", "خدا"),
    ("آن چیست که همه را می‌شکند؟", "غم"),
    ("آن چیست که همه را می‌سازد؟", "عشق"),
    ("آن چیست که در زمستان سرد است و در تابستان گرم؟", "آب"),
    ("آن چیست که بدون دست می‌نویسد؟", "قلم"),
    ("آن چیست که بدون پا راه می‌رود؟", "ساعت"),
    ("آن چیست که بدون چشم می‌بیند؟", "عکس"),
    ("آن چیست که بدون گوش می‌شنود؟", "رادیو"),
    ("آن چیست که بدون دهان حرف می‌زند؟", "تلفن"),
    ("آن چیست که بدون بال پرواز می‌کند؟", "بالن"),
    ("آن چیست که بدون چرخ می‌چرخد؟", "توپ"),
    ("آن چیست که بدون سر می‌خوابد؟", "رودخانه"),
    ("آن چیست که بدون قلب می‌زند؟", "در"),
    ("آن چیست که بدون نفس نفس می‌کشد؟", "باد"),
    ("آن چیست که بدون دست می‌گیرد؟", "مگنت"),
    ("آن چیست که بدون پا می‌دود؟", "آب"),
    ("آن چیست که بدون چشم گریه می‌کند؟", "ابر")
]

POEMS = [
    "در خاطرت مانده / آن شب که تو را کردم / از خواب خوشت بیدار؟",
    "گفتم که بخور این را / سرخ است و پر از آب است / این سیب خودم چیدم / از آن طرف دیوار",
    "خوردی و خوشت آمد / خنده به لبت آمد / گفتی که بکن حالا / تعریف از این دیدار",
    "یادش همگی خوش باد / میدادی و میکردم / تو درس محبت را / من گوش به این اقرار",
    "من عاشق و تو عاشق / گفتم که بده، دادی / وآنگاه فشردم من / دستان تو را ای یار",
    "شب بود و نفهمیدی / در پشت تو بنشستم / تا صبح تو را کردم / هر لحظه دعا بسیار",
    "یک لحظه نفهمیدم / آب آمد و رویت ریخت / فنجان چپه شد یک دم / از دست من بیمار",
    "انگشت خود آوردم / کردم همگی سیخش / تا بهر تو برچینم / یک شاخه گل تبدار",
    "در دست تو نسپرده / تو داد زدی ای وای / گفتی که بکش بیرون / از ناخن من این خار",
    "چون پرده به بالا رفت / تو داد زدی در دم / بیرون همه روشن هست / از نور چراغ انگار",
    "گفتم که برو آنور / برگرد و بکش پایین/از پنجره آن‌ پرده / کین نور دهد آزار",
    "آن شب شب خوبی بود / هی کردم و هی دادی / من‌ گریه برای تو / تو عشق به این دلدار"
]

TRUTH_QUESTIONS = [
"آخرین بار کی گریه کردی و چرا؟",

"یه چیزی که باهاش بزرگ شدی ولی از دستش دادی چیه؟",
"eگه بتونی فقط یه جمله به یکی بگی و بعدش ناپدید شی، چی می‌گی؟",
]

CHOICE_CATEGORIES = {
    "آسون": [
        "بهترین تعطیلاتت کجا بود؟",
        "آخرین فیلمی که دیدی چی بود؟",
        "دوست داری کدوم کشور رو سفر کنی؟",
    ],
    "متوسط": [
        "eگه یه قدرت مافوق بشری داشتی چی می‌خواستی؟",
        "بهترین تصمیم زندگیت چی بود؟",
    ],
    "سخت": [
        "eگه فقط 24 ساعت دیگه زنده بودی چی کار می‌کردی؟",
        "کدوم راز رو هیچ‌وقت به کسی نگفتی؟",

    ],
    "شخصی": [
        "بهترین دوستت کیه و چرا؟",
        "نزدیک‌ترین کس به قلبت کیه？",
        "کدوم عضو خانواده رو بیشتر دوست داری？",
    ],
    "تصادفی": [
        "eگه بتونی یه چیز رو اختراع کنی چی می‌سازی？",
        "eگه بتونی به 10 سال پیش برگردی چی به خودت می‌گی？",
    ]
}
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
            
DICE = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
            
current_ping = 0.0
server_ip = "127.0.0.1"
server_port = 43210
server_name = "Local Server"

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

""" تاريخ """
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
    return (jy, jm, jd)

def send_in_char_chunks(message):
    """
    ارسال پیام با تقسیم هوشمند کلمات
    - از تنظیمات پلاگین برای حداکثر طول و تاخیر استفاده می‌کند
    """
    if not var('enable_splitting'):
        CM(message)
        return
        
    max_chars = var('max_chars') or 200
    delay = var('split_delay') or 0.7
    
    chunks = []
    current_chunk = ""
    
    if '\n' in message:
        lines = message.split('\n')
        for line in lines:
            if len(line) <= max_chars:
                chunks.append(line)
            else:
                words = line.split()
                current_line = ""
                for word in words:
                    if len(current_line) + len(word) + 1 <= max_chars:
                        current_line += word + " "
                    else:
                        if current_line:
                            chunks.append(current_line.strip())
                        current_line = word + " "
                if current_line:
                    chunks.append(current_line.strip())
    else:
        words = message.split()
        current_chunk = ""
        for word in words:
            if len(current_chunk) + len(word) + 1 <= max_chars:
                current_chunk += word + " "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = word + " "
        if current_chunk:
            chunks.append(current_chunk.strip())
    
    for i, chunk in enumerate(chunks):
        teck(i * delay, Call(CM, chunk))

        """chat"""
class ChatLog:
    def __init__(s, source):
        try:
            w = s.w = AR.cw(
                source=source,
                size=(380, 300),
                ps=AR.UIS()*0.8
            )
            
            tw(
                parent=w,
                text='Chat  Recently',
                scale=0.9,
                position=(180, 265),
                h_align='center',
                color=(1, 1, 0)
            )
            
            s.search_input = tw(
                parent=w,
                position=(20, 20),
                size=(150, 25),
                editable=True,
                text='',
                color=(0.9, 0.9, 0.9),
                description='Searching...'
            )
            
            AR.bw(
                parent=w,
                label='Search',
                size=(150, 30),
                position=(40, 230),
                on_activate_call=s.apply_search,
                icon=gt('achievementFlawlessVictory'),  
                iconscale=0.8,
            )
            
            AR.bw(
                parent=w,
                label='Show time',
                size=(100, 30),
                position=(260, 10),
                on_activate_call=s.toggle_time,
                icon=gt('achievementInControl'),  
                iconscale=0.8,
            )
            
            AR.bw(
                parent=w,
                label='Maneager',
                size=(150, 30),
                position=(200, 230),
                on_activate_call=s.show_stats,
                icon=gt('bombButton'),
                iconscale=0.8,
            )
            
            s.scroll = sw(
                parent=w,
                size=(380, 180),
                position=(10, 50)
            )
            
            s.container = cw(
                parent=s.scroll,
                size=(380, 6000),  
                background=False
            )
            
            s.status_text = tw(
                parent=w,
                text='...',
                position=(200, 25),
                scale=0.6,
                color=(0.8, 0.8, 1),
                h_align='center'
            )
            
            s.all_messages = []
            s.filtered_messages = []
            s.search_text = ""
            s.show_time = False
            s.showing_stats = False
            
            s.refresh_chat_log()
            AR.swish()
            
        except Exception as e:
            AR.err(f'Error: {str(e)}')
    
    def refresh_chat_log(s):
        """بارگذاری تاریخچه چت"""
        try:
            s.all_messages = GCM()
            s.all_messages = s.all_messages[-300:] if len(s.all_messages) > 300 else s.all_messages
            s.filtered_messages = s.all_messages.copy()
            s.display_messages()
            
        except Exception as e:
            AR.err(f'Error: {str(e)}')
    
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
            for child in s.container.get_children():
                child.delete()
            
            if s.showing_stats:
                s.display_stats()
                return
            
            messages_to_show = s.filtered_messages
            
            y_pos = len(messages_to_show) * 18 - 9  
            for i, message in enumerate(messages_to_show):
                display_text = message
                if s.show_time:
                    timestamp = time.strftime("%H:%M", time.localtime(time.time() - (len(messages_to_show) - i) * 2))
                    display_text = f"[{timestamp}] {message}"
                
                if len(display_text) > 45:
                    display_text = display_text[:42] + "..."

                AR.bw(
                    parent=s.container,
                    size=(22, 16),
                    position=(345, y_pos),
                    on_activate_call=Call(s.copy_message, message),
                    icon=gt('file'),  
                    iconscale=0.5
                )
                
                tw(
                    parent=s.container,
                    text=display_text,
                    position=(10, y_pos),
                    scale=0.35,  
                    color=(1, 1, 1),
                    maxwidth=325,  
                    h_align='left'
                )
                
                y_pos -= 18  
            
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
            
            user_stats = {}
            for message in s.all_messages:
                if ':' in message:
                    username = message.split(':', 1)[0].strip()
                    user_stats[username] = user_stats.get(username, 0) + 1
            
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
        w = s.w = AR.cw(
            source=source,
            size=(500, 350),
            ps=AR.UIS() * 0.6
        )

        tw(parent=w, text="🎨 Font Genarator", position=(200, 300), scale=1.0, color=(1,1,0))
        tw(parent=w, text="Text:", position=(20, 265), scale=0.8, color=(1,1,1))
        s.input_widget = tw(parent=w, position=(80, 255), size=(390, 40),
                            editable=True, text="", 
                            color=(0.9,0.9,0.9), description="")

        AR.bw(parent=w, label="Genart font", size=(120, 30),
              position=(190, 200), on_activate_call=s.show_fonts)

        s.scroll = sw(parent=w, size=(460, 150), position=(20, 50))
        s.container = cw(parent=s.scroll, size=(440, 1000), background=False)

        s.status_text = tw(parent=w, text="status", 
                          position=(230, 25), scale=0.6, color=(0.8,0.8,1))

        AR.swish()

    def show_fonts(s):
        text = tw(query=s.input_widget).strip()
        if not text or text == "input  your text!":
            AR.err("Error! Please Check your text")
            return

        fonts = generate_fonts(text)

        for child in s.container.get_children():
            child.delete()

        y_pos = len(fonts) * 40 - 20
        total_height = 0
        
        for name, styled in fonts.items():
            tw(parent=s.container, text=f"{name}:  ", position=(10, y_pos),
               color=(1,1,1), scale=0.6, maxwidth=90)
            
            tw(parent=s.container, text=styled, position=(100, y_pos),
               color=(0,1,0), scale=0.65, maxwidth=250)
            
            AR.bw(parent=s.container, label="Copy", size=(50, 20),
                  position=(360, y_pos - 3),
                  on_activate_call=Call(s.copy_font, styled, name),
                  text_scale=0.5)
            
            y_pos -= 40
            total_height += 40

        cw(s.container, size=(440, max(300, total_height)))
        
        tw(s.status_text, text=f"{len(fonts)} proces done!")

    def copy_font(s, text, font_name):
        try:
            from babase import clipboard_set_text
            clipboard_set_text(text)
            push(f'Font{font_name}copyed!', color=(0,1,0))
            gs('dingSmall').play()
        except:
            AR.err("Error")
            
"""PLAYER"""
class PlayerInfo:
    def __init__(s, source):
        w = s.w = AR.cw(
            source=source,
            size=(600, 320),
            ps=AR.UIS()*0.7
        )

        tw(
            parent=w,
            text='Player information',
            scale=1.1,
            position=(280, 270),  
            h_align='center',
        )

        s.players = s.get_players()

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

        AR.bw(
            parent=w,
            label='Refresh',
            size=(40, 30),
            position=(30, 20),
            on_activate_call=s.refresh_players,
            icon=gt('replayIcon'),
            iconscale=0.8,
        )
        
        AR.bw(
            parent=w,
            label='Copy All',
            size=(100, 30),
            position=(250, 20),
            on_activate_call=s.copy_all_info,
            icon=gt('file'),
            iconscale=0.8,
        )
        
        AR.bw(
            parent=w,
            label='Kick All',
            size=(100, 30),
            position=(450, 20),
            on_activate_call=s.kick_all,
            icon=gt('achievementBoxer'),
            iconscale=0.8,
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
                        device_name = player.get('display_string', 'Unknow device')
                        players.append({
                            'name': p.get('name', 'Unknow Player'),
                            'full_name': p.get('name_full', 'Unknow Player'),
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
                text='⚠️ not find player',
                position=(280, 90),
                scale=0.8,
                color=(1, 0.5, 0),
                h_align='center'
            )
            return

        headers = [
            ('Nick name', 30, 0.6, (1, 1, 1)),
            ('ID', 120, 0.6, (0.8, 0.8, 1)),
            ('acount', 170, 0.6, (0.6, 1, 0.6)),
            ('Status', 300, 0.6, (1, 1, 0.8)),
            ('activities', 440, 0.6, (1, 1, 1))
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
            
            bw(
                parent=s.container, 
                label='', 
                size=(540, 35),  
                position=(10, y_pos), 
                color=bg_color, 
                enable_sound=False
            )

            pname = player['name'][:18] + '...' if len(player['name']) > 18 else player['name']
            if player['is_host']:
                pname = f"👑 {pname}"
            
            tw(
                parent=s.container, 
                text=pname,
                position=(20, y_pos + 5), 
                scale=0.65,
                color=(1, 1, 1), 
                maxwidth=160,
                h_align='left'
            )

            tw(
                parent=s.container, 
                text=f"{player['client_id']}",
                position=(120, y_pos + 5), 
                scale=0.6,
                color=(0.8, 0.8, 1), 
                h_align='center'
            )

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

            status_text = "Host" if player['is_host'] else "Player"
            status_color = (1, 1, 0) if player['is_host'] else (0.8, 0.8, 1)
            tw(
                parent=s.container, 
                text=status_text,
                position=(300, y_pos + 5), 
                scale=0.6,
                color=status_color, 
                h_align='center'
            )

            actions = [
                ('Copy', s.copy_player_info, (400, y_pos + 5), player),
                ('@', s.mention_player, (450, y_pos + 5), player),
                ('Kick', s.kick_player, (500, y_pos + 5), player)
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
        push('🔄 Player list updated.', color=(0, 1, 0))
        gs('dingSmall').play()

    def copy_player_info(s, player):
        info = (f"Nick name {player['name']}\n"
                f"ID: {player['client_id']}\n"
                f"acount: {player['device']}\n"
                f"status: {'Host' if player['is_host'] else 'Player'}")
        
        if CIS():
            from babase import clipboard_set_text
            clipboard_set_text(info)
            push(f'📋 Information{player["name"]} copied', color=(0, 1, 0))
            gs('dingSmall').play()
        else:
            AR.err('Error!')

    def copy_all_info(s):
        if not s.players:
            AR.err('not found any player')
            return
            
        all_info = "👥 List of players:\n\n"
        for player in s.players:
            status = "👑 Host" if player['is_host'] else "👤 Player"
            all_info += f"• {player['name']} (ID: {player['client_id']}) - {player['device']} - {status}\n"
        
        if CIS():
            from babase import clipboard_set_text
            clipboard_set_text(all_info)
            push('📋 All players information copied.', color=(0, 1, 0))
            gs('dingSmallHigh').play()
        else:
            AR.err('Erorr')

    def mention_player(s, player):
        try:
            message = f"@{player['name']}"
            CM(message)
            push(f"📍 {player['name']}was mentioned", color=(0, 1, 1))
            gs('dingSmall').play()
        except Exception:
            AR.err(f"Error!")

    def kick_player(s, player):
        if player['is_host']:
            AR.err('Error')
            return
        
        try:
            from bascenev1 import disconnect_client
            disconnect_client(player['client_id'])
            push(f"🚫 {player['name']} Kicked", color=(1, 0.5, 0))
            gs('dingSmallLow').play()
            teck(1.0, s.refresh_players)
        except Exception:
            AR.err(f"Error!")

    def kick_all(s):
        if not s.players:
            AR.err('There are no players to send off!')
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
                push(f"🚫 {kicked_count}kicked player", color=(1, 0.5, 0))
                gs('dingSmallLow').play()
                teck(1.0, s.refresh_players)
            else:
                AR.err('There are no players to send off!')
                
        except Exception:
            AR.err(f"Error")

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

# راه‌اندازی اولیه
setup_connection_overrides()

# ba_meta require api 9
# ba_meta export babase.Plugin
class SinglMod(Plugin):
    me = lambda c=0: APP.plus.get_v1_account_name() if APP.plus.get_v1_account_state() == 'signed_in' else '???'
    v2 = cs(sc.V2_LOGO)
    credit_shown = False
    B = '​'  
    
    party_colors = PARTY_COLORS
    jokes = JOKES
    poems = POEMS
    truth_questions = TRUTH_QUESTIONS

    def extract_account_id(s, sender_name):
        """استخراج شناسه حساب از نام نمایشی"""
        if s.v2 in sender_name:
            parts = sender_name.split(s.v2)
            if len(parts) > 1:
                return parts[1].strip()
        return None

    def get_full_identifier(s, sender_name):
        """دریافت شناسه کامل برای بلاک"""
        account_id = s.extract_account_id(sender_name)
        return account_id or sender_name
    
    def send_swears_to_target(s, target_name):
        """ارسال تمام فحش‌های ذخیره شده به یک هدف خاص با تاخیر 5 ثانیه"""
        swear_words = list(var('swear_words') or [])
        if not swear_words:
            send_in_char_chunks("هیچ فحشی در لیست وجود ندارد!" + s.B)
            return
            
        send_in_char_chunks(f"ارسال فحش‌ها به {target_name} با تاخیر 5 ثانیه:" + s.B)
        
        for i, swear in enumerate(swear_words):
            delay = i * 5.0
            teck(delay, Call(s.send_targeted_swear, target_name, swear))
            
            if var('tune0'):
                push(f"زمان‌بندی فحش {i+1}: {swear} پس از {delay} ثانیه", color=(1,0,0))

    def send_targeted_swear(s, target_name, swear):
        """ارسال یک فحش خاص به هدف"""
        message = f"{target_name}: {swear}"
        send_in_char_chunks(message + s.B)
        
        if var('tune0'):
            push(f"فحش ارسال شد: {swear} به {target_name}", color=(1,0,0))
    
    def start_party_loop(s):
        """Party"""
        if hasattr(s, 'party_timer') and s.party_timer:
            try:
                s.party_timer.delete()
            except:
                pass
            s.party_timer = None
        
        if not var('party_mode'):
            return
        
        current_time = time.time()
        party_speed = var('party_speed') or 1.0
        
        s.last_party_time = current_time
        s.next_party_time = current_time + party_speed
        
        s.party_timer = teck(party_speed, s.send_party_message)
    
    def send_party_message(s):
        """PARTY_SENDER"""
        enabled_colors = var('party_colors_enabled') or [True] * len(s.party_colors)
        active_colors = [color for i, color in enumerate(s.party_colors) if enabled_colors[i]]
        
        if not active_colors:
            push("هیچ رنگی فعال نیست! لطفاً در تنظیمات رنگ‌ها را فعال کنید", color=(1,0,0))
            var('party_mode', False)
            return
            
        name, color = random.choice(active_colors)
        r, g, b = color
        
        msg = f"t {r} {g} {b}"
        
        CM(msg)
        s.last_party_time = time.time()
        
        if var('tune0'):
            push(f"ارسال خودکار: {name}", color=color)
        
        if var('party_mode'):
            party_speed = var('party_speed') or 1.0
            now = time.time()
            next_time = s.next_party_time + party_speed
            
            if next_time > now:
                wait_time = next_time - now
                s.party_timer = teck(wait_time, s.send_party_message)
            else:
                s.party_timer = teck(0.1, s.send_party_message)
            
            s.next_party_time = next_time
    
    def start_timer(s, seconds, message, sender_id):
        """شروع یک تایمر جدید برای ارسال پیام با تأخیر"""
        if not hasattr(s, 'active_timers'):
            s.active_timers = {}
            
        timer_id = f"{sender_id}_{time.time()}"
        
        for tid, tdata in list(s.active_timers.items()):
            if tdata['original_sender'] == sender_id:
                send_in_char_chunks("شما از قبل یک تایمر فعال دارید!" + s.B)
                return
        
        s.active_timers[timer_id] = {
            'remaining': seconds,
            'message': message,
            'original_sender': sender_id,
            'start_time': time.time()
        }
        
        start_msg = f"⏱ تایمر {seconds} ثانیه‌ای شروع شد! پیام: '{message}'"
        send_in_char_chunks(start_msg + s.B)
        
        s.update_timer(timer_id)
    
    def update_timer(s, timer_id):
        """TIMER"""
        if not hasattr(s, 'active_timers') or timer_id not in s.active_timers:
            return
            
        timer = s.active_timers[timer_id]
        timer['remaining'] -= 1
        
        if timer['remaining'] > 0:
            countdown = f"⏱ {timer['remaining']} ثانیه تا ارسال: '{timer['message']}'"
            send_in_char_chunks(countdown + s.B)
            
            teck(1.0, Call(s.update_timer, timer_id))
        else:
            parsed_message = AR.parse(t=timer['message'], s=timer['original_sender'])
            send_in_char_chunks(parsed_message + s.B)
            
            end_msg = f"✅ پیام ارسال شد: '{parsed_message}'"
            send_in_char_chunks(end_msg + s.B)
            
            del s.active_timers[timer_id]
    
    def send_riddle(s):
        """ارسال چیستان فعلی به صورت بخش‌بندی شده"""
        if not var('riddle_mode'):
            return
            
        index = var('current_riddle_index')
        riddles = s.get_riddles()
        if not riddles:
            CM("هیچ چیستان‌ای وجود ندارد! ابتدا چیستان اضافه کنید.")
            return
            
        index = index % len(riddles)
        riddle_text = riddles[index][0]
        
        send_in_char_chunks(f"چیستان {index+1}/{len(riddles)}: {riddle_text}" + s.B)
        
        correct_answer = riddles[index][1]
        if var('tune0'):
            push(f"جواب: {correct_answer}", color=(0,1,0))
    
    def update_spam_tracker(s, sender_id, sender_name):
        """SPAMER_BASE"""
        whitelist = list(var('whitelist_accounts') or [])
        if sender_id in whitelist:
            return False
        
        current_time = time.time()
        
        MESSAGE_THRESHOLD = var('spam_threshold') or 10
        TIME_WINDOW = var('spam_time_window') or 15
        WARNING_THRESHOLD = int(MESSAGE_THRESHOLD * 0.8)  
        
        if not hasattr(s, 'spam_tracker'):
            s.spam_tracker = {}
            
        if sender_id not in s.spam_tracker:
            s.spam_tracker[sender_id] = {
                'response_count': 0,  
                'response_times': [],
                'last_warning': 0,
                'warning_sent': False
            }
        
        data = s.spam_tracker[sender_id]
        
        data['response_times'] = [t for t in data['response_times'] if current_time - t <= TIME_WINDOW]
        data['response_count'] = len(data['response_times'])
        
        data['response_times'].append(current_time)
        data['response_count'] = len(data['response_times'])
        
        if not data['warning_sent'] and data['response_count'] >= WARNING_THRESHOLD:
            if current_time - data['last_warning'] > 10:
                warn_msg = f"⚠️ {sender_name}: لطفاً استفاده از مود رو کمتر کن! "
                send_in_char_chunks(warn_msg + s.B)
                data['last_warning'] = current_time
                data['warning_sent'] = True
        
        if data['response_count'] >= MESSAGE_THRESHOLD:
            ignore_accounts = list(var('ignore_accounts') or [])
            if sender_id not in ignore_accounts:
                ignore_accounts.append(sender_id)
                var('ignore_accounts', ignore_accounts)
                
                block_msg = f"🚫 {sender_name} از طرف سیستم آنتی اسپمر بلاک شد! (ارسال "
                send_in_char_chunks(block_msg + s.B)
                
                msgs = GCM()
                for i in range(len(msgs)-1, -1, -1):
                    if msgs[i].startswith(sender_name + ":"):
                        msgs.pop(i)
                
                if sender_id in s.spam_tracker:
                    del s.spam_tracker[sender_id]
            
            return True
        
        return False

    def start_truth_game(s):
        """شروع بازی جرعت حقیقت"""
        s.truth_game_active = True
        s.last_truth_message_time = time.time()  
        send_in_char_chunks("لطفا حقيقت را بگوييد!روشن شد(:" + s.B)
        if var('tune0'):
            push("سوالات توسط CHAT GPT طرح شده", color=(0.8,0.5,1))
    
    def stop_truth_game(s):
        """STOPTRUTH"""
        s.truth_game_active = False
        send_in_char_chunks("خاموش شد ):" + s.B)
    
    def next_truth_question(s):
        """SENDER DEALY"""
        if not s.truth_game_active:
            send_in_char_chunks("بازی جرعت حقیقت فعال نیست! برای شروع 'حقیقت روشن' بفرستید." + s.B)
            return
            
        players = list(var('truth_players') or [])
        if len(players) < 2:
            send_in_char_chunks("حداقل به دو بازیکن برای بازی نیاز است! ابتدا بازیکنان را اضافه کنید." + s.B)
            return
            
        current_time = time.time()
        time_since_last = current_time - s.last_truth_message_time
        if time_since_last < 3:  
            wait_time = 3 - time_since_last
            teck(wait_time, s.next_truth_question)
            return
            
        p1, p2 = random.sample(players, 2)
        
        s.last_truth_message_time = time.time()
        send_in_char_chunks(f"پرسشگر: {p1} | جواب دهنده: {p2}" + s.B)
        
        teck(3, Call(send_in_char_chunks, "در حال انتخاب سوال..." + s.B))
        

        teck(6.5, Call(s.send_truth_question, p1, p2))

    def send_truth_question(s, p1, p2):
        """SENDER"""
        current_time = time.time()
        time_since_last = current_time - s.last_truth_message_time
        if time_since_last < 3:  
            wait_time = 3 - time_since_last
            teck(wait_time, Call(s.send_truth_question, p1, p2))
            return
            
        s.last_truth_message_time = time.time()
        question = random.choice(s.truth_questions)
        send_in_char_chunks(f"سوال برای {p2}:\n{question}" + s.B)

    def show_players_list(s):
        """SHOW PLAYERS"""
        players = list(var('truth_players') or [])
        if not players:
            send_in_char_chunks("هیچ بازیکنی در لیست وجود ندارد!" + s.B)
            return
            
        player_list = " | ".join(players)
        send_in_char_chunks(f"لیست بازیکنان:\n{player_list}" + s.B)
    
    def clear_all_players(s):
        """DELETE ALL"""
        players = list(var('truth_players') or [])
        if not players:
            send_in_char_chunks("لیست بازیکنان از قبل خالی است!" + s.B)
            return
            
        var('truth_players', [])
        send_in_char_chunks("تمامی بازیکنان حذف شدند!" + s.B)

    def start_ping_updates(s, party_window):
        """شروع به روزرسانی خودکار دکمه پینگ"""
        s.update_ping_button(party_window)
    
    def update_ping_button(s, party_window):
        """به روزرسانی متن و رنگ دکمه پینگ"""
        if hasattr(party_window, 'ping_button') and party_window.ping_button.exists():
            # تنظیم متن دکمه
            bw(party_window.ping_button, label=f'{current_ping}ms')
        
            # تنظیم رنگ بر اساس وضعیت پینگ
            if current_ping == 0:
                color = (0.5, 0.5, 0.5)  # خاکستری - عدم اتصال
            elif current_ping < 50:
                color = (0, 0.6, 0)  # سبز - پینگ عالی
            elif current_ping<100:
                color = (0.2,0.8,0)
            elif current_ping<150:
                color = (0.9, 0.8, 0)
            elif current_ping < 200:
                color = (1, 1, 0)  # زرد - پینگ متوسط
            else:
                color = (1, 0, 0)  # قرمز - پینگ ضعیف
            
            bw(party_window.ping_button, color=color)
        
            # برنامه‌ریزی برای به روزرسانی بعدی
            teck(1.0, Call(s.update_ping_button, party_window))

    def send_ping_to_chat(s):
        """ارسال پینگ به چت"""
        if current_ping == 0:
            message = "🔌 در حال حاضر به سرور متصل نیستم"
        else:
            message = f"📶 پینگ من: {current_ping} میلی‌ثانیه"
    
        send_in_char_chunks(message + s.B)
    
        if var('tune0'):
            push("پینگ در چت ارسال شد", color=(0, 1, 0))
        
    def start_choice_game(s):
        """شروع بازی انتخاب از دو گزینه"""
        s.choice_game_active = True
        s.choice_game_state = "waiting_for_category"
        s.choice_category = None
        s.choice_player = None
        s.choice_questions = []
        s.current_question_index = 0
        
        teck(2.0, Call(send_in_char_chunks, "بازی انتخاب از دو گزینه روشن شد" + s.B))
        teck(4.5, Call(send_in_char_chunks, "این سوال ها توسط Chat GPT طرح شده و درصورت بی احترامی عذر خواهی میکنم" + s.B))
        teck(7.0, Call(send_in_char_chunks, "نام دسته رو وارد کنید:" + s.B))
        
        if var('tune0'):
            push("دسته‌های موجود: آسون، متوسط، سخت، شخصی، تصادفی", color=(0.8,0.5,1))
    
    def stop_choice_game(s):
        """توقف بازی انتخاب از دو گزینه"""
        s.choice_game_active = False
        send_in_char_chunks("بازی انتخاب از دو گزینه خاموش شد." + s.B)
    
    def list_categories(s):
        """نمایش دسته‌های موجود"""
        categories = list(CHOICE_CATEGORIES.keys())
        category_list = "، ".join(categories)
        send_in_char_chunks(f"دسته‌های موجود: {category_list}" + s.B)
    
    def select_category(s, category, sender_name):
        """انتخاب دسته برای بازی با تاخیر 2 ثانیه"""
        if category in CHOICE_CATEGORIES:
            s.choice_category = category
            s.choice_questions = random.sample(CHOICE_CATEGORIES[category], 2)
            s.choice_player = random.choice(list(var('truth_players') or []))
            s.current_question_index = 0
            s.choice_game_state = "playing"  
            
            teck(2.0, Call(send_in_char_chunks, f"دسته '{category}' با موفقیت انتخاب شد" + s.B))
            teck(4.0, Call(s.announce_player))
        else:
            teck(2.0, Call(send_in_char_chunks, "دسته وارد شده نامعتبر است!" + s.B))
            teck(4.0, Call(s.list_categories))
    
    def announce_player(s):
        """اعلام بازیکن و شروع سوالات با تاخیر"""
        if not s.choice_game_active or not s.choice_questions:
            return
            
        send_in_char_chunks(f"بازیکن: {s.choice_player}" + s.B)
        teck(3.0, s.ask_next_question)

    def ask_next_question(s):
        """پرسیدن سوال بعدی در بازی"""
        if not s.choice_game_active or not s.choice_questions:
            return
            
        if s.current_question_index < len(s.choice_questions):
            question = s.choice_questions[s.current_question_index]
            send_in_char_chunks(f"{s.choice_player}، {question} یا" + s.B)
            s.current_question_index += 1
            
            if s.current_question_index < len(s.choice_questions):
                teck(3.0, s.ask_next_question)
        else:
            s.current_question_index = 0
    
    def next_choice_question(s):
        """پرسیدن سوال بعدی پس از پاسخ"""
        if not s.choice_game_active:
            return
            
        if s.choice_questions and s.current_question_index < len(s.choice_questions):
            teck(3.0, s.ask_next_question)
        else:
            s.choice_player = random.choice(list(var('truth_players') or []))
            s.choice_questions = random.sample(CHOICE_CATEGORIES[s.choice_category], 2)
            s.current_question_index = 0
            teck(3.0, Call(s.announce_player))

    def swear_response(s, sender_name):
        """پاسخ با یک فحش تصادفی از لیست"""
        swear_words = list(var('swear_words') or [])
        if not swear_words:
            return
            
        swear = random.choice(swear_words)
        send_in_char_chunks(f"{sender_name}: {swear}" + s.B)
        if var('tune0'):
            push(f"Swear response sent to: {sender_name}", color=(1,0,0))
    
    def ear(s):
        allowed_users = [
            s.get_full_identifier(s.me()), 
            "Flam", 
            "legended",
            s.v2 + "Flam",
            s.v2 + "legended",
            s.me(),
            s.v2 + s.me(),
            "Flam",  
            "legended"  
        ]
        whitelist = list(var('whitelist_accounts') or [])
        
        if var('block_all_mode'):
            if (s.get_full_identifier(f) not in allowed_users and 
                f not in allowed_users and 
                s.get_full_identifier(f) not in whitelist):
                if var('tune0'):
                    push(f"پیام از کاربر غیرمجاز در حالت block all: {f}", color=(1,0,0))
                return
        
        ignore_accounts = list(var('ignore_accounts') or [])
        
        z = GCM()
        teck(0.01, s.ear)
        if z == s.z: 
            return
            
        s.z = z
        if not z:
            return
            
        v = z[-1]
        parts = v.split(': ', 1)
        if len(parts) < 2:
            return
            
        f, m = parts
        
        if s.B in m:
            if var('tune0'):
                push("Ignoring self-sent message", color=(0.5,0.5,0.5))
            return
            
        sender_id = s.get_full_identifier(f)
        your_id = s.me()
        your_full_id = s.get_full_identifier(your_id)
        
        if sender_id in ignore_accounts:
            if var('tune0'):
                push(f"پیام از کاربر بلاک شده: {f}", color=(1,0,0))
            return
        
        allowed_names = [
            your_full_id, 
            "Flam", 
            "legended",
            s.v2 + "Flam",
            s.v2 + "legended",
            your_id,  
            s.v2 + your_id, 
            "Flam",
            "legended"
        ]
        
        if sender_id in allowed_names or f in allowed_names:
            cmd = m.strip()
            
            if cmd == "خاموش شو":
                var('state', 0)
                send_in_char_chunks("SinglMod خاموش شد.).:" + s.B)
                return
                
            elif cmd == "روشن شو":
                var('state', 1)
                send_in_char_chunks("SinglMod روشن شد.(.:" + s.B)
                return
                
            elif cmd == "ریست":
                reset_conf()
                var('ignore_accounts', [])
                var('whitelist_accounts', [])
                if hasattr(s, 'spam_tracker'):
                    s.spam_tracker = {}
                if hasattr(s, 'active_timers'):
                    s.active_timers = {}
                send_in_char_chunks("تنظیمات ریست شد!" + s.B)
                return
                
            elif cmd == "لیست":
                commands = "دستورات ویژه:\n"
                commands += "خاموش شو, روشن شو, ریست\n"
                commands += "block [id], unblock [id]\n"
                commands += "whitelist [id], unwhitelist [id]\n"
                commands += "spamsettings [آستانه] [زمان]\n"
                commands += "پارتی [سرعت] m.s, پارتی خاموش\n"
                commands += "تایمر [زمان] [پیام]\n"
                commands += "چیستان, /بعدی, بازی خاموش\n"
                commands += "کدها - نمایش دستورات کد\n"
                commands += "حقیقت روشن - شروع بازی جرعت حقیقت\n"
                commands += "حقیقت خاموش - خاموش کردن بازی\n"
                commands += "انتخاب روشن - شروع بازی انتخاب از دو گزینه\n"
                commands += "انتخاب خاموش - خاموش کردن بازی انتخاب\n"
                commands += "دسته؟ - نمایش دسته‌های بازی انتخاب\n"
                commands += "جواب داد - رفتن به سوال بعدی در بازی انتخاب\n"
                commands += "تعویض دسته - تغییر دسته در حین بازی\n"
                commands += "all block - بلاک همه کاربران غیرمجاز\n"
                commands += "all unblock - غیرفعال کردن حالت بلاک همه\n"
                commands += "فحش: [کلمه] - افزودن فحش جدید\n"
                commands += "حذف فحش: [کلمه] - حذف فحش\n"
                commands += "لیست فحش - نمایش فحش‌ها\n"
                commands += "فحش روشن - فعال کردن پاسخ فحش\n"
                commands += "فحش خاموش - غیرفعال کردن پاسخ فحش"
                send_in_char_chunks(commands + s.B)
                return
                
            elif cmd.startswith("block "):
                identifier = cmd[6:].strip()
                if not identifier:
                    send_in_char_chunks("Usage: block <account_id>" + s.B)
                    return
                    
                ignore_accounts = list(var('ignore_accounts') or [])
                if identifier not in ignore_accounts:
                    ignore_accounts.append(identifier)
                    var('ignore_accounts', ignore_accounts)
                    send_in_char_chunks(f"Account ID '{identifier}' blocked" + s.B)
                else:
                    send_in_char_chunks(f"Account ID '{identifier}' is already blocked" + s.B)
                return
                
            elif cmd.startswith("unblock "):
                identifier = cmd[8:].strip()
                if not identifier:
                    send_in_char_chunks("Usage: unblock <account_id>" + s.B)
                    return
                    
                ignore_accounts = list(var('ignore_accounts') or [])
                if identifier in ignore_accounts:
                    ignore_accounts.remove(identifier)
                    var('ignore_accounts', ignore_accounts)
                    send_in_char_chunks(f"Account ID '{identifier}' unblocked" + s.B)
                else:
                    send_in_char_chunks(f"Account ID '{identifier}' not found in block list" + s.B)
                return
            
            elif cmd.startswith("whitelist "):
                identifier = cmd[10:].strip()
                if not identifier:
                    send_in_char_chunks("Usage: whitelist <account_id>" + s.B)
                    return
                    
                whitelist = list(var('whitelist_accounts') or [])
                if identifier not in whitelist:
                    whitelist.append(identifier)
                    var('whitelist_accounts', whitelist)
                    send_in_char_chunks(f"Account ID '{identifier}' added to whitelist" + s.B)
                else:
                    send_in_char_chunks(f"Account ID '{identifier}' is already whitelisted" + s.B)
                return
                
            elif cmd.startswith("unwhitelist "):
                identifier = cmd[12:].strip()
                if not identifier:
                    send_in_char_chunks("Usage: unwhitelist <account_id>" + s.B)
                    return
                    
                whitelist = list(var('whitelist_accounts') or [])
                if identifier in whitelist:
                    whitelist.remove(identifier)
                    var('whitelist_accounts', whitelist)
                    send_in_char_chunks(f"Account ID '{identifier}' removed from whitelist" + s.B)
                else:
                    send_in_char_chunks(f"Account ID '{identifier}' not found in whitelist" + s.B)
                return
                
            elif cmd.startswith("spamsettings "):
                try:
                    parts = cmd.split()
                    if len(parts) != 3:
                        send_in_char_chunks("Usage: spamsettings [threshold] [time_window]" + s.B)
                        return
                    
                    threshold = int(parts[1])
                    time_window = int(parts[2])
                    
                    if threshold < 5 or threshold > 30:
                        send_in_char_chunks("Threshold: 5-30" + s.B)
                        return
                    if time_window < 5 or time_window > 60:
                        send_in_char_chunks("Time window: 5-60" + s.B)
                        return
                    
                    var('spam_threshold', threshold)
                    var('spam_time_window', time_window)
                    send_in_char_chunks(f"Spam settings updated: {threshold} messages in {time_window} seconds" + s.B)
                except:
                    send_in_char_chunks("Invalid values! Usage: spamsettings [threshold] [time_window]" + s.B)
                return
            
            elif cmd.startswith("پارتی") and "s" in cmd:
                try:
                    parts = cmd.split()
                    speed = 1.0
                    
                    if len(parts) > 1 and parts[1].replace('.', '').isdigit():
                        speed = float(parts[1])
                    
                    if speed < 0.3:
                        speed = 0.3
                        CM("حداقل سرعت: 0.3 ثانیه (به دلیل جلوگیری از اسپم)")
                    
                    var('party_speed', speed)
                    var('party_mode', True)
                    s.start_party_loop()
                    
                    CM(f"پارتی روشن شد سرعت: هر {speed} ثانیه")
                    push("از دستور 'پارتی خاموش' برای غیرفعال کردن استفاده کنید", color=(0.8,0.5,1))
                except:
                    CM("فرمت سرعت نامعتبر! مثال: پارتی 1.5 m.s")
                return
                
            elif cmd == "پارتی خاموش":
                var('party_mode', False)
                if hasattr(s, 'party_timer') and s.party_timer:
                    try:
                        s.party_timer.delete()
                    except:
                        pass
                    s.party_timer = None
                s.last_party_time = 0
                s.next_party_time = 0
                CM("پارتی خاموش شد، لطفا هول نباشید/:")
                return
            
            elif cmd.startswith("تایمر "):
                try:
                    parts = cmd.split(" ", 2)
                    if len(parts) < 3:
                        send_in_char_chunks("فرمت نادرست! مثال: تایمر 10 سلام دنیا" + s.B)
                        return
                    
                    seconds = int(parts[1])
                    message = parts[2]
                    
                    if seconds < 1 or seconds > 300:
                        send_in_char_chunks("زمان باید بین 1 تا 300 ثانیه باشد!" + s.B)
                        return
                    
                    s.start_timer(seconds, message, sender_id)
                except:
                    send_in_char_chunks("فرمت نادرست! مثال: تایمر 10 سلام دنیا" + s.B)
                return
            
            elif cmd == "چیستان":
                var('riddle_mode', True)
                var('current_riddle_index', 0)
                send_in_char_chunks("بازی چیستان شروع شد! برای چیستان بعدی '/بعدی' بفرستید." + s.B)
                teck(1.4, s.send_riddle)
                return
                
            elif cmd == "/بعدی":
                if not var('riddle_mode'):
                    send_in_char_chunks("بازی چیستان فعال نیست. ابتدا 'چیستان' را بفرستید." + s.B)
                    return
                    
                index = (var('current_riddle_index') + 1) % len(s.get_riddles())
                var('current_riddle_index', index)
                teck(0.7, s.send_riddle)
                return
                
            elif cmd == "چيستان خاموش":
                var('riddle_mode', False)
                send_in_char_chunks("بازی چیستان خاموش شد." + s.B)
                return
                
            elif cmd == "کدها":
                code_commands = var('code_commands') or {}
                if not code_commands:
                    send_in_char_chunks("هنوز دستور کدی تعریف نشده!" + s.B)
                    return
                
                response = "دستورات کد فعال:\n"
                for trigger, (command, delay) in code_commands.items():
                    response += f"{trigger} → {command} (تاخیر: {delay} ثانیه)\n"
                send_in_char_chunks(response + s.B)
                return
                
            elif cmd == "حقیقت روشن" or cmd == "بازی جرعت حقیقت شروع":
                s.start_truth_game()
                return
                
            elif cmd == "حقیقت خاموش":
                s.stop_truth_game()
                return
                
            elif cmd == "حذف همه" or cmd == "حذف همه بازیکن ها":
                s.clear_all_players()
                return
                
            elif cmd == "نمایش بازیکن ها":
                s.show_players_list()
                return
                
            elif cmd == "انتخاب روشن":
                s.start_choice_game()
                return
                
            elif cmd == "انتخاب خاموش":
                s.stop_choice_game()
                return
                
            elif cmd == "دسته؟":
                s.list_categories()
                return
                
            elif cmd == "جواب داد":
                s.next_choice_question()
                return
                
            elif cmd == "all block":
                var('block_all_mode', True)
                send_in_char_chunks("حالت بلاک همه فعال شد! فقط کاربران ویژه (Singl و legended) و لیست سفید می‌توانند از پلاگین استفاده کنند." + s.B)
                return
                
            elif cmd == "all unblock":
                var('block_all_mode', False)
                send_in_char_chunks("حالت بلاک همه غیرفعال شد." + s.B)
                return
                
            elif cmd.startswith("فحش: "):
                word = cmd[5:].strip()
                if not word:
                    send_in_char_chunks("لطفاً کلمه فحش را وارد کنید! مثال: فحش: abbas" + s.B)
                    return
                    
                swear_words = list(var('swear_words') or [])
                if word in swear_words:
                    send_in_char_chunks(f"فحش '{word}' قبلاً وجود دارد!" + s.B)
                    return
                    
                swear_words.append(word)
                var('swear_words', swear_words)
                send_in_char_chunks(f"فحش '{word}' اضافه شد!" + s.B)
                return
                
            elif cmd.startswith("حذف فحش: "):
                word = cmd[10:].strip()
                if not word:
                    send_in_char_chunks("لطفاً کلمه فحش را وارد کنید! مثال: حذف فحش: abbas" + s.B)
                    return
                    
                swear_words = list(var('swear_words') or [])
                if word in swear_words:
                    swear_words.remove(word)
                    var('swear_words', swear_words)
                    send_in_char_chunks(f"فحش '{word}' حذف شد!" + s.B)
                else:
                    send_in_char_chunks(f"فحش '{word}' پیدا نشد!" + s.B)
                return
                
            elif cmd == "لیست فحش":
                swear_words = list(var('swear_words') or [])
                if not swear_words:
                    send_in_char_chunks("هیچ فحشی در لیست وجود ندارد!" + s.B)
                    return
                    
                swear_list = ", ".join(swear_words)
                send_in_char_chunks(f"لیست فحش‌ها:\n{swear_list}" + s.B)
                return
                
            elif cmd == "فحش روشن":
                var('swear_mode', True)
                send_in_char_chunks("سیستم فحش فعال شد!" + s.B)
                return
                
            elif cmd == "فحش خاموش":
                var('swear_mode', False)
                send_in_char_chunks("سیستم فحش غیرفعال شد!" + s.B)
                return
                
            elif cmd.startswith("فحش به:"):
                parts = cmd.split(":", 1)
                if len(parts) > 1:
                    target_name = parts[1].strip()
                    if target_name:
                        s.send_swears_to_target(target_name)
                    else:
                        send_in_char_chunks("لطفاً نام شخص را وارد کنید! مثال: فحش به: علی" + s.B)
                return
        
        if not var('state'):
            return
            
        code_commands = var('code_commands') or {}
        if var('code_mode') and sender_id in allowed_names:
            parts = m.split(maxsplit=1)
            if len(parts) > 0:
                trigger = parts[0].lower()
                argument = parts[1] if len(parts) > 1 else ""
                
                if trigger in code_commands:
                    command, delay_val = code_commands[trigger]
                    
                    if '%a' in command:
                        command = command.replace('%a', argument)
                    command = AR.parse(t=command, s=sender_id)
                    
                    teck(delay_val, Call(CM, command))
                    
                    if var('tune0'):
                        push(f"کد اجرا شد: {trigger} → {command} (تاخیر: {delay_val} ثانیه)", color=(0.5,1,0.5))
                    return
            
        if m.strip().startswith("add ") and len(m.split()) >= 2:
            name = m.split(' ', 1)[1].strip()
            if name:
                players = list(var('truth_players') or [])
                if name in players:
                    send_in_char_chunks(f"بازیکن '{name}' قبلاً وجود دارد." + s.B)
                else:
                    players.append(name)
                    var('truth_players', players)
                    send_in_char_chunks(f"بازیکن '{name}' اضافه شد." + s.B)
            return

        if m.strip().startswith("delete ") and len(m.split()) >= 2:
            name = m.split(' ', 1)[1].strip()
            if name:
                players = list(var('truth_players') or [])
                if name in players:
                    players.remove(name)
                    var('truth_players', players)
                    send_in_char_chunks(f"بازیکن '{name}' حذف شد." + s.B)
                else:
                    send_in_char_chunks(f"بازیکن '{name}' پیدا نشد." + s.B)
            return
            
        if var('riddle_mode'):
            index = var('current_riddle_index')
            riddles = s.get_riddles()
            if not riddles:
                return
                
            index = index % len(riddles)
            correct_answer = riddles[index][1]
            
            if m.strip().lower() == correct_answer.lower():
                send_in_char_chunks(f"درست بود! {f} جواب رو پیدا کرد!" + s.B)
                
                if var('tune0'):
                    push(f"جواب درست: {correct_answer}", color=(0,1,0))
                
                new_index = (index + 1) % len(riddles)
                var('current_riddle_index', new_index)
                teck(1.7, s.send_riddle)
                return
            
        if hasattr(s, 'choice_game_active') and s.choice_game_active:
            if sender_id in allowed_names:
                if m.strip() == "تعویض دسته":
                    s.choice_game_state = "waiting_for_category"
                    send_in_char_chunks("لطفاً نام دسته جدید را وارد کنید:" + s.B)
                    return
                    
                if s.choice_game_state == "waiting_for_category":
                    category = m.strip()
                    if category in CHOICE_CATEGORIES:
                        s.select_category(category, f)
                        return
                    else:
                        send_in_char_chunks("دسته وارد شده نامعتبر است! لطفاً از دسته‌های موجود استفاده کنید." + s.B)
                        s.list_categories()
                        return
                
                elif m.strip() == "جواب داد":
                    s.next_choice_question()
                    return
            
        if "جوک" in m:
            if var('state') and not s.update_spam_tracker(sender_id, f):
                joke = random.choice(s.jokes)
                send_in_char_chunks(joke + s.B)
                if var('tune0'):
                    push(f"Built-in joke response! To: {f}", color=(0,0.8,0.8))
                if var('tune1'):
                    gs('dingSmallHigh').play()
            return
            
        if "شعر" in m:
            if var('state') and not s.update_spam_tracker(sender_id, f):
                poem = random.choice(s.poems)
                send_in_char_chunks(poem + s.B)
                if var('tune0'):
                    push(f"Built-in poem response! To: {f}", color=(0.8,0.8,0))
                if var('tune1'):
                    gs('dingSmallHigh').play()
            return
            
        if "تاریخ" in m:
            if var('state') and not s.update_spam_tracker(sender_id, f):
                now = DT.now()
                miladi_date = now.strftime("%Y/%m/%d")
                jy, jm, jd = gregorian_to_jalali(now.year, now.month, now.day)
                jalali_str = f"{jy}/{jm:02d}/{jd:02d}"
                response = f"📅 تاریخ: شمسی {jalali_str} | میلادی {miladi_date}"
                    
                send_in_char_chunks(response + s.B)
                if var('tune0'):
                    push(f"Built-in date response! To: {f}", color=(0.8,0.8,0))
                if var('tune1'):
                    gs('dingSmallHigh').play()
            return
            
        if hasattr(s, 'truth_game_active') and s.truth_game_active and m.strip() == "بعدی":
            if not s.update_spam_tracker(sender_id, f):
                s.next_truth_question()
            return
            
        k = s.me()
        my_full_id = s.get_full_identifier(k)
        
        if var('tune3'): 
            l = var('l')
            message_to_match = m
        else: 
            message_to_match = m.lower()
            l = var('lc')
            
        if l and var('state') and var('auto_response_enabled'):
            if message_to_match in l:
                responses = l[message_to_match]
                if not responses:
                    return
                    
                response_index_dict = var('response_index') or {}
                current_index = response_index_dict.get(message_to_match, 0)
                
                response_data = responses[current_index]
                response_str = response_data[0]
                
                new_index = (current_index + 1) % len(responses)
                response_index_dict[message_to_match] = new_index
                var('response_index', response_index_dict)
                
                if s.update_spam_tracker(sender_id, f):
                    return
                s.S(response_str, f, 0)
                return
            
            elif var('combined_response'):
                words = message_to_match.split()
                combined_response = []
                response_index_dict = var('response_index') or {}
                found = False
                
                for word in words:
                    if word in l:
                        responses = l[word]
                        if not responses:
                            continue
                            
                        current_index = response_index_dict.get(word, 0)
                        response_data = responses[current_index]
                        response_str = response_data[0]
                        
                        combined_response.append(response_str)
                        
                        new_index = (current_index + 1) % len(responses)
                        response_index_dict[word] = new_index
                        found = True
                
                if found:
                    var('response_index', response_index_dict)
                    full_response = " ".join(combined_response)
                    
                    if not s.update_spam_tracker(sender_id, f):
                        s.S(full_response, f, 1)
                    return
            
            for trigger in l:
                responses = l[trigger]
                if not responses:
                    continue
                    
                response_data = responses[0]  
                wildcard_flag = response_data[2]
                if wildcard_flag and trigger in message_to_match:
                    response_index_dict = var('response_index') or {}
                    current_index = response_index_dict.get(trigger, 0)
                    
                    response_data = responses[current_index]
                    response_str = response_data[0]
                    
                    new_index = (current_index + 1) % len(responses)
                    response_index_dict[trigger] = new_index
                    var('response_index', response_index_dict)
                    
                    if s.update_spam_tracker(sender_id, f):
                        return
                    s.S(response_str, f, 1)
                    break
                
        if var('swear_mode'):
            swear_words = list(var('swear_words') or [])
            if swear_words:
                for word in swear_words:
                    if word.lower() in m.lower():
                        if not s.update_spam_tracker(sender_id, f):
                            s.swear_response(f)
                        return
                
    def S(s, response, sender, is_wild):
        """ارسال پاسخ خودکار با تاخیر و کاراکتر صفر"""
        parsed = AR.parse(t=response, s=sender)
        send_in_char_chunks(parsed + s.B)  
        
        if var('tune0'):
            notif_text = f"{['Exact','Wild','Combined'][is_wild]} match! To: {sender}"
            if len(notif_text) > 80:
                notif_text = notif_text[:47] + '...'
            push(notif_text, color=(10,5,0))
                
        if var('tune1'):
            gs('dingSmallHigh').play()

    def __init__(s):
        o = party.PartyWindow.__init__
        def e(s_party,*a,**k):
            r = o(s_party,*a,**k)
            b = AR.bw(
                icon=gt('achievementFlawlessVictory'),
                position=(s_party._width-650,s_party._height-150),
                parent=s_party._root_widget,
                iconscale=1,
                size=(150,70),
                label='Singl'
            )
            bw(b,on_activate_call=Call(AR,source=b))
            
            sticker_buttons = [
                ("🦉", "owl"),
                ("🤝", "handshake"),
                ("✋", "hand"),
                ("👌", "ok_hand"),
                ("☹️", "frown"),
                ("😂", "laugh"),
                ("😖", "confounded"),
                ("🥺", "pleading")
            ]
            button_width = 30
            button_height = 30
            horizontal_spacing = button_width + 5
            vertical_spacing = button_height + 5
            
            start_x = s_party._width - 15 + 10  
            start_y = s_party._height - 45 - 30 - 5
            
            row_count = 4 
            col_count = 2
            
            for row in range(row_count):
                for col in range(col_count):
                    index = row * col_count + col
                    if index >= len(sticker_buttons):
                        break
                    
                    sticker, icon = sticker_buttons[index]
                    x = start_x + col * horizontal_spacing
                    y = start_y - row * vertical_spacing
                    
                    b = bw(
                        label=sticker,
                        size=(button_width, button_height),
                        position=(x, y),
                        parent=s_party._root_widget,
                        iconscale=0.7,
                        on_activate_call=Call(CM, sticker)
                    )

                    # اضافه کردن دکمه پینگ
            s_party.ping_button = AR.bw(
                icon=gt('replayIcon'),
                position=(s_party._width-800, s_party._height-150),
                parent=s_party._root_widget,
                iconscale=0.8,
                size=(120,60),
                label=f'{current_ping}ms'
            )
            bw(s_party.ping_button, on_activate_call=Call(s.send_ping_to_chat))
        
            # شروع به روزرسانی خودکار پینگ
            s.start_ping_updates(s_party)
        
            # بقیه کدهای موجود...
            # [کدهای موجود برای استیکرها و...]
        
            return r
        party.PartyWindow.__init__ = e
        s.z = []
        teck(5,s.ear)
        teck(10, s.show_credit_once)
        
        s.spam_tracker = {}
        
        s.last_party_time = 0
        s.next_party_time = 0
        s.party_timer = None
        
        s.active_timers = {}
        
        s.truth_game_active = False
        s.last_truth_message_time = 0  
        
        s.choice_game_active = False
        s.choice_game_state = "idle"
        s.choice_category = None
        s.choice_player = None
        s.choice_questions = []
        s.current_question_index = 0
        
        s.credit_shown = False

    def show_credit_once(s):
        if not s.credit_shown:
            credit_msg = "SinglMod v5.1 | Telegram: @Amiry_11228"
            push(credit_msg, color=(0.8,0.8,1.0))
            s.credit_shown = True

    @classmethod
    def get_riddles(c):
        riddles_json = var('riddles')
        if riddles_json:
            return json.loads(riddles_json)
        return RIDDLES.copy()
    
    @classmethod
    def save_riddles(c, riddles):
        var('riddles', json.dumps(riddles))

"""Add a response"""
class Add:
    def __init__(s,t):
        w = AR.cw(
            source=t,
            size=(300,295),
            ps=AR.UIS()*0.8
        )
        a = []
        for i in range(2):
            j = ['If found','Respond with'][i]
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
                text=['After','seconds'][i],
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
            text='Search in message',
            value=s.cbv,
            on_value_change_call=Call(setattr,s,'cbv'),
            color=(0.13,0.13,0.13),
            textcolor=(1,1,1),
        )
        tw(
            parent=w,
            scale=0.5,
            position=(20,37.5),
            text=f'%m: Your v2 name \n%s: Sender name ! %t: Time\n%dsh:khorshididate | %dm: miladidate',
            maxwidth=190,
            color=(0.65,0.65,0.65)
        )
        AR.bw(
            parent=w,
            label='Add',
            size=(50,35),
            position=(230,25),
            on_activate_call=Call(s._add,a)
        )
        AR.swish()
    
    """Actually add"""
    def _add(s,a):
        z = tw(query=s.t)
        try: z = float(z)
        except: AR.err('Invalid time. Fix your input!'); return
        var('time',str(z))
        i,j = [tw(query=t).strip().replace('\n',' ') for t in a]
        if not i or not j: AR.err('Write something!'); return
        l = var('l') or {}
        lc = var('lc') or {}
        ic = i.lower()
        
        if i not in l:
            l[i] = []
        l[i].append((j, z, s.cbv))
        
        if ic not in lc:
            lc[ic] = []
        lc[ic].append((j, z, s.cbv))
        
        var('l',l)
        var('lc',lc)
        [tw(t,text='') for t in a]
        AR.ok()
    
    """Paste"""
    def paste(s,t):
        if not CIS(): AR.err('Unsupported!'); return
        if not CHT(): AR.err('Your clipboard is empty!'); return
        tw(t,text=CGT().replace('\n',' '),color=(0,1,0))
        gs('gunCocking').play()
        teck(0.3,Call(tw,t,color=(1,1,1)))
        push('Pasted!',color=(0,1,0))

"""کلاس گوه مالي """
class AntiKickSystem:
    def __init__(self):
        self.enabled = True
        self.check_interval = 5  # هر 5 ثانیه موقعیت را بررسی کند
        self.inactivity_threshold = 15  # پس از 15 ثانیه بی‌حرکتی پیام ارسال شود
        self.last_position = None
        self.last_activity_time = time.time()
        self.timer = None
        self.is_active = False
        
        # ذخیره تنظیمات
        self.save_settings()
        
        if self.enabled:
            self.start_monitoring()

    def save_settings(self):
        """ذخیره تنظیمات در فایل پیکربندی"""
        try:
            config = {
                'enabled': self.enabled,
                'check_interval': self.check_interval,
                'inactivity_threshold': self.inactivity_threshold
            }
            
            config_path = os.path.join(os.path.dirname(__file__), 'anti_kick_config.json')
            with open(config_path, 'w') as f:
                json.dump(config, f)
        except:
            pass

    def load_settings(self):
        """بارگذاری تنظیمات از فایل"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), 'anti_kick_config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    self.enabled = config.get('enabled', True)
                    self.check_interval = config.get('check_interval', 5)
                    self.inactivity_threshold = config.get('inactivity_threshold', 15)
        except:
            pass

    def start_monitoring(self):
        """شروع مانیتورینگ حرکت کاربر"""
        self.stop_monitoring()
        self.timer = teck(self.check_interval, self.check_movement)
        self.is_active = True
        self.last_activity_time = time.time()
        push('سیستم ضد اخراج فعال شد', color=(0, 1, 0))

    def stop_monitoring(self):
        """توقف مانیتورینگ"""
        if self.timer is not None:
            try:
                self.timer.delete()
            except:
                pass
            self.timer = None
        self.is_active = False
        push('سیستم ضد اخراج غیرفعال شد', color=(1, 0, 0))

    def get_player_position(self):
        """دریافت موقعیت بازیکن در بازی"""
        try:
            # دریافت فعالیت فعلی
            activity = bs.get_foreground_host_activity()
            if activity is None:
                return None
            
            # پیدا کردن بازیکن محلی
            for player in activity.players:
                if hasattr(player, 'sessionplayer') and player.sessionplayer.inputdevice == bs.app.device:
                    if hasattr(player, 'actor') and player.actor and hasattr(player.actor, 'node'):
                        return player.actor.node.position
            return None
        except:
            return None

    def check_movement(self):
        """بررسی حرکت کاربر"""
        if not self.enabled:
            return
            
        try:
            current_position = self.get_player_position()
            
            if current_position is None:
                # اگر موقعیت در دسترس نیست، بعداً دوباره تلاش کن
                if self.enabled:
                    self.timer = teck(self.check_interval, self.check_movement)
                return
                
            if self.last_position is None:
                # اولین بار که موقعیت را می‌گیریم
                self.last_position = current_position
                self.last_activity_time = time.time()
            else:
                # بررسی تغییر موقعیت
                movement_detected = False
                for i in range(3):
                    if abs(current_position[i] - self.last_position[i]) > 0.1:
                        movement_detected = True
                        break
                
                if movement_detected:
                    # حرکت تشخیص داده شد
                    self.last_activity_time = time.time()
                    self.last_position = current_position
                else:
                    # بررسی زمان بی‌حرکتی
                    inactivity_time = time.time() - self.last_activity_time
                    if inactivity_time >= self.inactivity_threshold:
                        # ارسال پیام ضد اخراج
                        send_in_char_chunks("SinglMod:Anti kick" + SinglMod.B)
                        self.last_activity_time = time.time()  # ریست زمان
            
            self.last_position = current_position
            
            # ادامه مانیتورینگ
            if self.enabled:
                self.timer = teck(self.check_interval, self.check_movement)
                
        except Exception as e:
            # در صورت بروز خطا، بعداً دوباره تلاش کن
            if self.enabled:
                self.timer = teck(self.check_interval, self.check_movement)

    def set_enabled(self, enabled):
        """تنظیم وضعیت فعال/غیرفعال سیستم"""
        self.enabled = enabled
        self.save_settings()
        
        if enabled:
            self.start_monitoring()
        else:
            self.stop_monitoring()

    def set_check_interval(self, interval):
        """تنظیم بازه بررسی (ثانیه)"""
        self.check_interval = interval
        self.save_settings()
        
        if self.enabled:
            self.stop_monitoring()
            self.start_monitoring()

    def set_inactivity_threshold(self, threshold):
        """تنظیم آستانه بی‌حرکتی (ثانیه)"""
        self.inactivity_threshold = threshold
        self.save_settings()


class AntiKickPanel:
    def __init__(s, source):
        w = s.w = AR.cw(
            source=source,
            size=(400, 300),
            ps=AR.UIS()*0.8
        )

        tw(
            parent=w,
            text='سیستم ضد اخراج',
            scale=1.2,
            position=(200, 270),
            h_align='center',
            color=(0, 1, 1)
        )

        # ایجاد سیستم ضد اخراج
        s.anti_kick = AntiKickSystem()
        s.anti_kick.load_settings()

        # دکمه فعال/غیرفعال
        tw(
            parent=w,
            text='فعال:',
            position=(50, 230),
            scale=0.9,
            color=(1, 1, 1)
        )
        s.enabled_toggle = chk(
            parent=w,
            size=(30, 30),
            position=(150, 230),
            value=s.anti_kick.enabled,
            on_value_change_call=Call(s.set_enabled)
        )

        # فیلد بازه بررسی
        tw(
            parent=w,
            text='بازه بررسی (ثانیه):',
            position=(50, 190),
            scale=0.9,
            color=(1, 1, 1)
        )
        s.interval_input = tw(
            parent=w,
            size=(100, 30),
            editable=True,
            position=(200, 190),
            text=str(s.anti_kick.check_interval),
            color=(0.9, 0.9, 0.9)
        )

        # فیلد آستانه بی‌حرکتی
        tw(
            parent=w,
            text='آستانه بی‌حرکتی (ثانیه):',
            position=(50, 150),
            scale=0.9,
            color=(1, 1, 1)
        )
        s.threshold_input = tw(
            parent=w,
            size=(100, 30),
            editable=True,
            position=(200, 150),
            text=str(s.anti_kick.inactivity_threshold),
            color=(0.9, 0.9, 0.9)
        )

        # دکمه ذخیره تنظیمات
        AR.bw(
            parent=w,
            label='ذخیره تنظیمات',
            size=(120, 40),
            position=(140, 100),
            on_activate_call=s.save_settings
        )

        # وضعیت
        s.status_text = tw(
            parent=w,
            text='',
            position=(200, 60),
            scale=0.8,
            color=(0.8, 0.8, 1),
            h_align='center'
        )

        AR.swish()

    def set_enabled(s, value):
        s.anti_kick.set_enabled(value)

    def save_settings(s):
        try:
            check_interval = int(tw(query=s.interval_input))
            inactivity_threshold = int(tw(query=s.threshold_input))

            if check_interval < 2 or check_interval > 30:
                AR.err('بازه بررسی باید بین 2 تا 30 ثانیه باشد!')
                return

            if inactivity_threshold < 5 or inactivity_threshold > 60:
                AR.err('آستانه بی‌حرکتی باید بین 5 تا 60 ثانیه باشد!')
                return

            # اعمال تنظیمات روی سیستم
            s.anti_kick.set_check_interval(check_interval)
            s.anti_kick.set_inactivity_threshold(inactivity_threshold)

            tw(s.status_text, text='تنظیمات ذخیره شد!', color=(0, 1, 0))
            push('تنظیمات ضد اخراج ذخیره شد!', color=(0, 1, 0))
        except ValueError:
            AR.err('لطفاً اعداد معتبر وارد کنید!')


# ایجاد یک نمونه از سیستم ضد اخراج
anti_kick_system = AntiKickSystem()

"""Secret Message Encryption/Decryption System - Fixed Version"""
class SecretMessageSender:
    def __init__(s, source):
        w = s.w = AR.cw(
            source=source,
            size=(400,290),
            ps=AR.UIS()*0.8
        )
        
        tw(
            parent=w,
            text='🔒 Secret Message Sender',
            scale=1.2,
            position=(200, 260),
            h_align='center',
            color=(0, 1, 1)
        )
        
        tw(
            parent=w,
            text='Message:',
            position=(20, 220),
            scale=0.9,
            color=(1, 1, 1)
        )
        s.message_input = tw(
            parent=w,
            editable=True,
            position=(20, 190),
            size=(360, 40),
            text='',
            description='Type your secret message',
            color=(0.9, 0.9, 0.9)
        )
        
        tw(
            parent=w,
            text='Encryption Key (4 digits):',
            position=(20, 150),
            scale=0.9,
            color=(1, 1, 1)
        )
        s.key_input = tw(
            parent=w,
            editable=True,
            position=(20, 120),
            size=(200, 30),
            text='',
            description='1234',
            color=(0.9, 0.9, 0.9)
        )
        
        AR.bw(
            parent=w,
            label='Encrypt & Send',
            size=(150, 40),
            position=(125,60),
            on_activate_call=s.encrypt_and_send,
            icon=gt('file'),
            iconscale=0.8
        )
        
        s.status_text = tw(
            parent=w,
            text='Ready to encrypt',
            position=(200, 10),
            h_align='center',
            scale=0.8,
            color=(0.8, 0.8, 1)
        )
        
        AR.swish()
    
    def encrypt_and_send(s):
        message = tw(query=s.message_input).strip()
        key = tw(query=s.key_input).strip()
        
        if not message:
            AR.err('Please enter a message!')
            return
            
        if not key or len(key) != 4 or not key.isdigit():
            AR.err('Encryption key must be 4 digits!')
            return
            
        # Encrypt the message
        encrypted = s.encrypt_message(message, key)
        
        # Send to chat with prefix
        full_message = f"Singl_Secret:{encrypted}"
        send_in_char_chunks(full_message + SinglMod.B)
        
        tw(s.status_text, text='Message encrypted and sent!', color=(0, 1, 0))
        push('Secret message sent!', color=(0, 1, 0))
        
        # Clear inputs
        tw(s.message_input, text='')
        tw(s.key_input, text='')
    
    def encrypt_message(s, message, key):
        """Encrypt message using simple substitution cipher"""
        # دقیق‌ترین نگاشت فارسی به فینگلیش
        persian_to_finglish = {
            'ا': 'a', 'آ': 'a', 'أ': '2', 'إ': 'e', 'ئ': 'i',
            'ب': 'b', 'پ': 'p', 
            'ت': 't', 'ث': 'th', 
            'ج': 'j', 'چ': 'ch',
            'ح': '4', 'خ': 'kh',
            'د': 'd', 'ذ': 'dh',
            'ر': 'r', 'ز': 'z', 'ژ': 'zh',
            'س': 's', 'ش': 'sh',
            'ص': '9', 'ض': '8', 'ط': '6', 'ظ': '7',
            'ع': '3', 'غ': 'gh',
            'ف': 'f', 
            'ق': 'q', 
            'ک': 'k', 'گ': 'g',
            'ل': 'l', 
            'م': 'm', 
            'ن': 'n',
            'و': 'v', 
            'ه': 'eh', 
            'ی': 'y', 'ي': 'y',
            ' ': ' ', '؟': '?', '!': '!', '.': '.', ',': ',',
            '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
            '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'
        }
        
        # تبدیل فارسی به فینگلیش
        finglish = ''
        for char in message:
            if char in persian_to_finglish:
                finglish += persian_to_finglish[char]
            else:
                finglish += char
        
        # اعمال رمزنگاری ساده با استفاده از کلید
        encrypted = ''
        key_index = 0
        
        for char in finglish:
            if char.isalpha():
                # شیفت کاراکتر بر اساس رقم کلید (استفاده از الگوریتم ساده‌تر)
                shift = int(key[key_index % 4])
                base = ord('a') if char.islower() else ord('A')
                shifted_char = chr((ord(char) - base + shift) % 26 + base)
                encrypted += shifted_char
                key_index += 1
            else:
                encrypted += char
        
        return encrypted

class SecretMessageReceiver:
    def __init__(s, source):
        w = s.w = AR.cw(
            source=source,
            size=(450, 290),
            ps=AR.UIS()*0.8
        )
        
        tw(
            parent=w,
            text='🔓 Secret Message Receiver',
            scale=1.2,
            position=(225, 260),
            h_align='center',
            color=(0, 1, 1)
        )
        
        tw(
            parent=w,
            text='Encrypted Message:',
            position=(20, 250),
            scale=0.7,
            color=(1, 1, 1)
        )
        s.encrypted_input = tw(
            parent=w,
            editable=True,
            position=(20, 220),
            size=(410, 40),
            text='',
            description='Paste encrypted message here',
            color=(0.9, 0.9, 0.9)
        )
        
        AR.bw(
            parent=w,
            label='Paste ',
            size=(100, 30),
            position=(350, 190),
            on_activate_call=s.paste_from_chat,
            icon=gt('file'),
            iconscale=0.7
        )
        
        tw(
            parent=w,
            text='Decryption Key (4 digits):',
            position=(20, 200),
            scale=0.7,
            color=(1, 1, 1)
        )
        s.key_input = tw(
            parent=w,
            editable=True,
            position=(20, 180),
            size=(200, 30),
            text='',
            description='1234',
            color=(0.9, 0.9, 0.9)
        )
        
        AR.bw(
            parent=w,
            label='Decrypt',
            size=(100, 30),
            position=(350, 150),
            on_activate_call=s.decrypt_message,
            icon=gt('replayIcon'),
            iconscale=0.8
        )
        
        s.decrypted_text = tw(
            parent=w,
            text='Decrypted message will appear here',
            position=(210, 120),
            h_align='center',
            scale=0.8,
            color=(0.8, 1, 0.8),
            maxwidth=400
        )
        
        s.save_button = AR.bw(
            parent=w,
            label='Save Message',
            size=(120, 35),
            position=(165,10),
            on_activate_call=s.save_message,
            icon=gt('achievementMine'),
            iconscale=0.7
        )
        
        s.status_text = tw(
            parent=w,
            text='Ready to decrypt',
            position=(210, 90),
            h_align='center',
            scale=0.8,
            color=(0.8, 0.8, 1)
        )
        
        s.saved_messages = var('secret_messages') or []
        AR.swish()
    
    def paste_from_chat(s):
        if not CIS():
            AR.err('Clipboard not supported!')
            return
            
        if not CHT():
            AR.err('Clipboard is empty!')
            return
            
        clipboard_text = CGT()
        # تشخیص خودکار پیام رمزگذاری شده
        if 'Singl_Secret:' in clipboard_text:
            encrypted = clipboard_text.split('Singl_Secret:')[-1].strip()
            tw(s.encrypted_input, text=encrypted)
            push('Encrypted message pasted!', color=(0, 1, 0))
        else:
            AR.err('No encrypted message found in clipboard!')
    
    def decrypt_message(s):
        encrypted = tw(query=s.encrypted_input).strip()
        key = tw(query=s.key_input).strip()
        
        if not encrypted:
            AR.err('Please enter an encrypted message!')
            return
            
        if not key or len(key) != 4 or not key.isdigit():
            AR.err('Decryption key must be 4 digits!')
            return
        
        # حذف پیشوند اگر وجود دارد
        if 'Singl_Secret:' in encrypted:
            encrypted = encrypted.split('Singl_Secret:')[-1].strip()
        
        # رمزگشایی پیام
        try:
            decrypted = s.decrypt_text(encrypted, key)
            tw(s.decrypted_text, text=decrypted, color=(0, 1, 0))
            tw(s.status_text, text='Message decrypted successfully!', color=(0, 1, 0))
        except Exception as e:
            AR.err(f'Decryption failed: {str(e)}')
    
    def decrypt_text(s, encrypted, key):
        """رمزگشایی پیام با استفاده از الگوریتم ساده"""
        # معکوس کردن رمزنگاری
        decrypted_finglish = ''
        key_index = 0
        
        for char in encrypted:
            if char.isalpha():
                # معکوس کردن شیفت بر اساس رقم کلید
                shift = int(key[key_index % 4])
                base = ord('a') if char.islower() else ord('A')
                decrypted_char = chr((ord(char) - base - shift) % 26 + base)
                decrypted_finglish += decrypted_char
                key_index += 1
            else:
                decrypted_finglish += char
        
        # تبدیل فینگلیش به فارسی با دقت بالا
        finglish_to_persian = {
            'a': 'ا',
            'b': 'ب',
            'p': 'پ',
            't': 'ت',
            'j': 'ج',
            'ch': 'چ',
            '4': 'ح',
            'kh': 'خ',
            'd': 'د',
            'r': 'ر',
            'z': 'ز',
            'zh': 'ژ',
            's': 'س',
            'sh': 'ش',
            'gh': 'غ',
            'f': 'ف',
            'q': 'ق',
            'k': 'ک',
            'g': 'گ',
            'l': 'ل',
            'm': 'م',
            'n': 'ن',
            'v': 'و',
            'y': 'ی',
            ' ': ' ', '?': '؟', '!': '!', '.': '.', ',': ',',
            '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
            '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹',
            'th': 'ث',
            'dh': 'ذ',
            '9': 'ص',
            '8': 'ض',
            '6': 'ط',
            '7': 'ظ',
            '3': 'ع',
            'eh': 'ه',
            '2': 'أ',
            'e': 'إ',
            'i': 'ئ'
        }
        
        # تبدیل فینگلیش به فارسی
        decrypted = ''
        i = 0
        while i < len(decrypted_finglish):
            # اول دنبال دنباله‌های دو حرفی می‌گردیم
            found = False
            
            # چک کردن دنباله ۲ حرفی
            if i + 2 <= len(decrypted_finglish):
                two_chars = decrypted_finglish[i:i+2]
                if two_chars in finglish_to_persian:
                    decrypted += finglish_to_persian[two_chars]
                    i += 2
                    found = True
            
            # اگر دنباله دو حرفی پیدا نکردیم، تک حرف را بررسی می‌کنیم
            if not found and i < len(decrypted_finglish):
                single_char = decrypted_finglish[i]
                if single_char in finglish_to_persian:
                    decrypted += finglish_to_persian[single_char]
                else:
                    decrypted += single_char
                i += 1
        
        return decrypted
    
    def save_message(s):
        decrypted = tw(query=s.decrypted_text)
        if not decrypted or decrypted == 'Decrypted message will appear here':
            AR.err('No decrypted message to save!')
            return
            
        # ذخیره در پیام‌های ذخیره شده
        s.saved_messages.append(decrypted)
        var('secret_messages', s.saved_messages)
        
        tw(s.status_text, text='Message saved to history!', color=(0, 1, 0))
        push('Secret message saved!', color=(0, 1, 0))

class SecretMessageHistory:
    def __init__(s, source):
        messages = var('secret_messages') or []
        if not messages:
            AR.err('No secret messages saved!')
            return
            
        w = s.w = AR.cw(
            source=source,
            size=(500, 290),
            ps=AR.UIS()*0.8
        )
        
        tw(
            parent=w,
            text='📜 Secret Message History',
            scale=1.2,
            position=(250, 260),
            h_align='center',
            color=(0, 1, 1)
        )
        
        s.scroll = sw(
            parent=w,
            size=(480, 190),
            position=(10, 60)
        )
        
        s.container = cw(
            parent=s.scroll,
            size=(460, len(messages) * 50),
            background=False
        )
        
        y_pos = len(messages) * 50 - 25
        for i, message in enumerate(messages):
            # پس‌زمینه پیام
            bw(
                parent=s.container,
                label='',
                size=(450, 40),
                position=(5, y_pos),
                color=(0.2, 0.2, 0.3),
                enable_sound=False
            )
            
            # متن پیام
            tw(
                parent=s.container,
                text=message,
                position=(10, y_pos + 5),
                scale=0.7,
                maxwidth=400,
                color=(1, 1, 1),
                h_align='left'
            )
            
            # دکمه کپی
            AR.bw(
                parent=s.container,
                label='Copy',
                size=(60, 25),
                position=(390, y_pos),
                on_activate_call=Call(s.copy_message, message),
                text_scale=0.6
            )
            
            y_pos -= 50
        
        AR.bw(
            parent=w,
            label='Clear All',
            size=(100, 35),
            position=(200, 15),
            on_activate_call=s.clear_all,
            icon=gt('backIcon'),
            iconscale=0.7
        )
        
        AR.swish()
    
    def copy_message(s, message):
        if CIS():
            from babase import clipboard_set_text
            clipboard_set_text(message)
            push('Message copied!', color=(0, 1, 0))
        else:
            AR.err('Clipboard not supported!')
    
    def clear_all(s):
        var('secret_messages', [])
        push('All secret messages cleared!', color=(1, 0.5, 0))
        cw(s.w, transition='out_scale')

"""Add a code command"""
class AddCode:
    def __init__(s,t):
        w = AR.cw(
            source=t,
            size=(350,280),
            ps=AR.UIS()*0.8
        )
        
        tw(
            parent=w,
            text='Add New Code Command:',
            position=(170,260),
            h_align='center',
            scale=0.7,
            color=(0.5,1,0.5))
        
        tw(
            parent=w,
            text='Trigger Code:',
            position=(20,230),
            scale=0.8
        )
        s.trigger = tw(
            parent=w,
            size=(100,30),
            editable=True,
            position=(20,200),
            color=(0.75,0.75,0.75),
            allow_clear_button=False
        )
        
        tw(
            parent=w,
            text='Response Code:',
            position=(20,170),
            scale=0.8
        )
        s.response = tw(
            parent=w,
            size=(100,30),
            editable=True,
            position=(20,140),
            color=(0.75,0.75,0.75),
            allow_clear_button=False
        )
        
        tw(
            parent=w,
            text='Delay (seconds):',
            position=(20,110),
            scale=0.8
        )
        s.delay = tw(
            parent=w,
            size=(50,30),
            editable=True,
            position=(20,70),
            color=(0.75,0.75,0.75),
            text="0.3"
        )
        
        AR.bw(
            parent=w,
            label='Add',
            size=(80,30),
            position=(130,20),
            on_activate_call=s.save_code,
            icon=gt('achievementStayinAlive'),
            iconscale=0.8
        )
        
        s.status = tw(
            parent=w,
            text='',
            position=(175,50),
            h_align='center',
            scale=0.8,
            color=(0,1,0)
        )
    
    """Save code command"""
    def save_code(s):
        trigger = tw(query=s.trigger).strip().lower()
        response = tw(query=s.response).strip()
        delay_str = tw(query=s.delay).strip()
        
        if not trigger or not response:
            tw(s.status, text='Both fields are required!', color=(1,0,0))
            return
            
        try:
            delay_val = float(delay_str)
            if delay_val < 0 or delay_val > 5.0:
                tw(s.status, text='Delay: 0.1-5.0 seconds', color=(1,0,0))
                return
        except:
            tw(s.status, text='Invalid delay value!', color=(1,0,0))
            return
            
        code_commands = var('code_commands') or {}
        if trigger in code_commands:
            tw(s.status, text='Trigger already exists!', color=(1,0,0))
            return
            
        code_commands[trigger] = (response, delay_val)
        var('code_commands', code_commands)
        
        tw(s.trigger, text='')
        tw(s.response, text='')
        tw(s.status, text='Code command added!', color=(0,1,0))
        push(f"New code command: {trigger} → {response}", color=(0,1,0))

"""Nuke a response or code command - Improved Version"""
class Nuke:
    def __init__(s, t):
        w = s.w = AR.cw(
            source=t,
            size=(400, 350), 
            stack_offset=(0, 0)
        )
        
        tw(
            parent=w,
            text="Delete Triggers",
            position=(200,330),
            h_align='center',
            scale=1.2,
            color=(1,0.5,0.5)
        )
        
        tabs_container = cw(
            parent=w,
            size=(380,40),
            position=(10,295),
            background=False
        )
        
        s.auto_button = bw(
            parent=tabs_container,
            size=(180,35),
            position=(10,2.5),
            label='Auto Responses',
            color=(0.3,0.5,0.8),
            textcolor=(1,1,1),
            on_activate_call=Call(s.set_mode, 'auto')
        )
        
        s.code_button = bw(
            parent=tabs_container,
            size=(180,35),
            position=(200,2.5),
            label='Code Commands',
            color=(0.8,0.5,0.3),
            textcolor=(1,1,1),
            on_activate_call=Call(s.set_mode, 'code')
        )
        
        s.scroll = sw(
            parent=w,
            size=(380,230),
            position=(10,50)
        )
        
        s.container = cw(
            parent=s.scroll,
            size=(360,0),
            background=False
        )
        
        s.delete_button = bw(
            parent=w,
            size=(180,35),
            position=(140,10),
            label='DELETE SELECTED',
            color=(1,0.2,0.2),
            textcolor=(1,1,1),
            on_activate_call=s.delete_selected
        )
        
        s.mode = 'auto'
        s.selected_item = None
        s.fresh()
        AR.swish()
    
    def set_mode(s, mode):
        s.mode = mode
        s.selected_item = None
        s.fresh()
        if mode == 'auto':
            bw(s.auto_button, color=(0.2,0.6,1))
            bw(s.code_button, color=(0.8,0.5,0.3))
        else:
            bw(s.auto_button, color=(0.3,0.5,0.8))
            bw(s.code_button, color=(1,0.7,0.4))
    
    def fresh(s):
        for child in s.container.get_children():
            child.delete()
        
        if s.mode == 'auto':
            data = var('l') or {}
            items = []
            for trigger, responses in data.items():
                for idx, response in enumerate(responses):
                    items.append((trigger, response, idx))
        else:
            data = var('code_commands') or {}
            items = list(data.items())
            
        if not items:
            tw(
                parent=s.container,
                text="No items found!",
                position=(160,120),
                h_align='center',
                scale=2.0,
                color=(1,0.5,0.5)
            )
            cw(s.container, size=(360,230))
            return
            
        height = len(items) * 70  
        if height < 270: height = 270
        cw(s.container, size=(360,height))
        
        for i, item in enumerate(items):
            item_container = cw(
                parent=s.container,
                size=(340,60),  
                position=(10,height - 70*(i+1) + 10), 
                color=(0.25,0.25,0.25),  
                background=True
            )
            
            if s.mode == 'auto':
                trigger, response_tuple, idx = item
                response, delay, wildcard = response_tuple
                text = f"Trigger: {trigger}\nResponse: {response}\nWildcard: {'Yes' if wildcard else 'No'}"
            else:
                trigger, (response, delay) = item
                text = f"Trigger: {trigger}\nCommand: {response}\nDelay: {delay}s"
                
            t = tw(
                text=text,
                parent=item_container,
                size=(320,50),
                selectable=True,
                click_activate=True,
                position=(10,5),
                on_activate_call=Call(s.select_item, i),
                maxwidth=310,
                scale=0.8,
                color=(1,1,1)  
            )
            
            if s.selected_item == i:
                cw(item_container, color=(0.3,0.3,0.5)) 
    
    def select_item(s,i):
        s.selected_item = i
    
    def delete_selected(s):
        if s.selected_item is None:
            AR.err('Please select an item first!')
            return
            
        if s.mode == 'auto':
            data = var('l') or {}
            lc = var('lc') or {}
            items = []
            for trigger, responses in data.items():
                for idx, response in enumerate(responses):
                    items.append((trigger, response, idx))
            
            if s.selected_item < len(items):
                trigger, response_tuple, idx = items[s.selected_item]
                
                if trigger in data:
                    if idx < len(data[trigger]):
                        del data[trigger][idx]
                        if not data[trigger]:
                            del data[trigger]
                
                trigger_lower = trigger.lower()
                if trigger_lower in lc:
                    new_list = [r for r in lc[trigger_lower] if r != response_tuple]
                    if new_list:
                        lc[trigger_lower] = new_list
                    else:
                        del lc[trigger_lower]
                
                var('l', data)
                var('lc', lc)
                push(f"Deleted response: {trigger}", color=(1,0.5,0))
        else:
            data = var('code_commands') or {}
            items = list(data.items())
            if s.selected_item < len(items):
                key, value = items[s.selected_item]
                del data[key]
                var('code_commands', data)
                push(f"Deleted code command: {key}", color=(1,0.5,0))
        
        s.selected_item = None
        s.fresh()
        AR.ok()

"""Blocked accounts"""
class Blocked:
    def __init__(s,t):
        accounts = list(var('ignore_accounts') or [])
        if not accounts: 
            AR.err('No blocked accounts!')
            return
            
        w = AR.cw(
            source=t,
            size=(350,250),
            ps=AR.UIS()*0.5
        )
        
        tw(
            parent=w,
            text='Blocked Accounts:',
            position=(20,220),
            scale=0.9,
            color=(1,0,0))
        
        a = sw(
            parent=w,
            size=(310,180),
            position=(20,30)
        )
        s.c = cw(
            parent=a,
            size=(310,0),
            background=False
        )
        s.kids = []
        s.fresh()
        AR.swish()
    
    """Refresh"""
    def fresh(s):
        [k.delete() for k in s.kids]
        s.kids.clear()
        
        items = list(var('ignore_accounts') or [])
        height = (len(items) + 1) * 25
        
        header = cw(
            parent=s.c,
            size=(310,25),
            position=(0,25*len(items))
        )
        tw(
            text="Account ID",
            parent=header,
            size=(200,25),
            position=(10,0),
            h_align='left',
            v_align='center',
            color=(1,1,0.5),
            scale=0.8
        )
        tw(
            text="Action",
            parent=header,
            size=(100,25),
            position=(220,0),
            h_align='center',
            v_align='center',
            color=(1,1,0.5),
            scale=0.8
        )
        s.kids.append(header)
        
        for i,account_id in enumerate(items):
            c = cw(
                parent=s.c,
                size=(310,25),
                position=(0,25*(len(items)-i-1))
            )
            tw(
                text=account_id,
                parent=c,
                size=(200,25),
                position=(10,0),
                h_align='left',
                v_align='center',
                color=(0.8,0.5,0.5),
                scale=0.7
            )
            AR.bw(
                parent=c,
                label='Unblock',
                size=(60,20),
                position=(240,2.5),
                text_scale=0.6,
                on_activate_call=Call(s.unblock,account_id)
            )
            s.kids.append(c)
            
        cw(s.c,size=(310,height))
    
    """Unblock"""
    def unblock(s,account_id):
        accounts = list(var('ignore_accounts') or [])
        if account_id in accounts:
            accounts.remove(account_id)
            var('ignore_accounts',accounts)
                
        s.fresh()
        AR.ok()
        push(f"Unblocked: {account_id}", color=(0,1,0))

"""Whitelisted accounts"""
class Whitelisted:
    def __init__(s,t):
        accounts = list(var('whitelist_accounts') or [])
        w = AR.cw(
            source=t,
            size=(350,280),
            ps=AR.UIS()*0.5
        )
        
        tw(
            parent=w,
            text='Whitelisted Accounts:',
            position=(20,250),
            scale=0.9,
            color=(0,1,0))
        
        a = sw(
            parent=w,
            size=(310,200),
            position=(20,30)
        )
        s.c = cw(
            parent=a,
            size=(310,(len(accounts)+1)*25),
            background=False
        )
        s.kids = []
        
        tw(
            parent=w,
            text='Add Account ID:',
            position=(20,220),
            scale=0.7
        )
        s.new_acc = tw(
            parent=w,
            size=(200,25),
            editable=True,
            position=(20,220),
            color=(0.75,0.75,0.75),
            allow_clear_button=False
        )
        AR.bw(
            parent=w,
            label='Add',
            size=(50,25),
            position=(280,220),
            on_activate_call=s.add_account,
            text_scale=0.7
        )
        
        s.fresh()
        AR.swish()
    
    """Refresh"""
    def fresh(s):
        [k.delete() for k in s.kids]
        s.kids.clear()
        
        items = list(var('whitelist_accounts') or [])
        
        header = cw(
            parent=s.c,
            size=(310,25),
            position=(0,25*len(items))
        )
        tw(
            text="Account ID",
            parent=header,
            size=(200,25),
            position=(10,0),
            h_align='left',
            v_align='center',
            color=(0.5,1,0.5),
            scale=0.8
        )
        tw(
            text="Action",
            parent=header,
            size=(100,25),
            position=(220,0),
            h_align='center',
            v_align='center',
            color=(0.5,1,0.5),
            scale=0.8
        )
        s.kids.append(header)
        
        for i,account_id in enumerate(items):
            c = cw(
                parent=s.c,
                size=(310,25),
                position=(0,25*(len(items)-i-1))
            )
            tw(
                text=account_id,
                parent=c,
                size=(200,25),
                position=(10,0),
                h_align='left',
                v_align='center',
                color=(0.7,1,0.7),
                scale=0.7
            )
            AR.bw(
                parent=c,
                label='Remove',
                size=(60,20),
                position=(240,2.5),
                text_scale=0.6,
                on_activate_call=Call(s.remove,account_id)
            )
            s.kids.append(c)
            
        cw(s.c,size=(310,(len(items)+1)*25))
    
    """Add account"""
    def add_account(s):
        account_id = tw(query=s.new_acc).strip()
        if not account_id:
            AR.err('Enter account ID!')
            return
            
        whitelist = list(var('whitelist_accounts') or [])
        if account_id in whitelist:
            AR.err('Already whitelisted!')
            return
            
        whitelist.append(account_id)
        var('whitelist_accounts',whitelist)
        tw(s.new_acc,text='')
        s.fresh()
        AR.ok()
        push(f"Added to whitelist: {account_id}",color=(0,1,0))
    
    """Remove account"""
    def remove(s,account_id):
        whitelist = list(var('whitelist_accounts') or [])
        if account_id in whitelist:
            whitelist.remove(account_id)
            var('whitelist_accounts',whitelist)
                
        s.fresh()
        AR.ok()
        push(f"Removed from whitelist: {account_id}",color=(1,0.5,0))

"""Advanced blocking settings"""
class BlockSettings:
    def __init__(s,t):
        w = AR.cw(
            source=t,
            size=(350,200),
            ps=AR.UIS()*0.8
        )
        AR.swish()
        
        tw(
            parent=w,
            text='Spam Detection Settings:',
            position=(20,160),
            scale=0.9,
            color=(1,0.5,0))
        
        for i in range(2):
            text = ['Messages threshold:', 'Time window (sec):'][i]
            tw(
                parent=w,
                text=text,
                position=(20,130-40*i),
                scale=0.6
            )
            
        s.threshold = tw(
            parent=w,
            text=str(var('spam_threshold') or 10),
            size=(50,25),
            editable=True,
            position=(170,130),
            color=(0.75,0.75,0.75)
        )
        
        s.time_window = tw(
            parent=w,
            text=str(var('spam_time_window') or 15),
            size=(50,25),
            editable=True,
            position=(170,90),
            color=(0.75,0.75,0.75)
        )
        
        AR.bw(
            parent=w,
            label='Save',
            size=(60,30),
            position=(270,40),
            on_activate_call=s.save_settings
        )
    
    """Save settings"""
    def save_settings(s):
        try:
            threshold = int(tw(query=s.threshold))
            time_window = int(tw(query=s.time_window))
            
            if threshold < 5 or threshold > 30:
                AR.err('Threshold: 5-30')
                return
            if time_window < 5 or time_window > 60:
                AR.err('Time window: 5-60')
                return
                
            var('spam_threshold',threshold)
            var('spam_time_window',time_window)
            AR.ok()
            push('Settings saved!',color=(0,1,0))
        except:
            AR.err('Invalid values!')

"""The settings"""
class Tune:
    def __init__(s, t):
        w = AR.cw(
            source=t,
            size=(350, 250),
            ps=AR.UIS()*0.7
        )
        
        scroll_widget = sw(
            parent=w,
            size=(330, 180),
            position=(10, 40)
        )
        
        container = cw(
            parent=scroll_widget,
            size=(310, 300),
            background=False
        )
        
        settings = [
            ('Notify', 'tune0'),
            ('Sound', 'tune1'),
            ('Self-response', 'tune2'),
            ('Case sensitive', 'tune3'),
            ('Block All', 'block_all_mode'),
            ('Auto-response', 'auto_response_enabled'),
            ('Combined resp', 'combined_response'),
            ('Split messages', 'enable_splitting'),
            ('Notifications', 'show_notifications'),
            ('Stickers', 'enable_stickers'),
            ('Swear Mode', 'swear_mode')  
        ]
        
        y_pos = 280 
        for i, (label, config_key) in enumerate(settings):
            chk(
                text=label,
                parent=container,
                size=(300, 20), 
                position=(5, y_pos - 30*i),
                textcolor=(1,1,1),
                value=var(config_key),
                color=(0.13,0.13,0.13),
                on_value_change_call=Call(s.set_setting, config_key),
                scale=0.6
            )
        
        tw(
            parent=w,
            text='Settings',
            position=(175,225),
            h_align='center',
            scale=0.8,
            color=(0.8,0.8,1)
        )
        
        AR.bw(
            parent=w,
            label='Save',
            size=(70,25),
            position=(70,5),
            on_activate_call=Call(s.save_all, w),
            icon=gt('startButton'),
            iconscale=0.6,
            text_scale=0.6
        )
        
        close_btn = AR.bw(
            parent=w,
            label='Close',
            size=(70,25),
            position=(200,5),
            on_activate_call=Call(cw, w, transition='out_scale'),
            icon=gt('crossOut'),
            iconscale=0.6,
            text_scale=0.6
        )
        bw(close_btn, color=(0.8,0.2,0.2))
        
        AR.swish()
    
    def set_setting(s, config_key, value):
        var(config_key, value)
        
        if config_key in ['auto_response_enabled', 'block_all_mode']:
            status = "ON" if value else "OFF"
            push(f"{config_key} {status}", color=(0,1,0) if value else (1,0.5,0))
    
    def save_all(s, window):
        push("Saved!", color=(0,1,0))
        gs('dingSmall').play()
        teck(0.3, Call(cw, window, transition='out_scale'))

"""List responses and code commands"""
class List:
    def __init__(s, t):
        w = s.w = AR.cw(
            source=t,
            size=(500, 290),
            ps=AR.UIS()*0.7
        )
        
        tw(
            parent=w,
            text='List Manager',
            scale=1.2,
            position=(225, 260),
            h_align='center',
            color=(1, 1, 0.5)
        )
        
        s.tab1 = bw(
            parent=w,
            position=(120, 225),
            size=(120, 30),
            label='Auto Responses',
            on_activate_call=Call(s.set_mode, 'auto'),
            color=(0.3, 0.5, 0.8),
            text_scale=0.7
        )
        
        s.tab2 = bw(
            parent=w,
            position=(310, 225),
            size=(120, 30),
            label='Code Commands',
            on_activate_call=Call(s.set_mode, 'code'),
            color=(0.8, 0.5, 0.3),
            text_scale=0.7
        )
        
        s.scroll = sw(
            parent=w,
            position=(25, 25),
            size=(470, 180)
        )
        
        s.container = cw(
            parent=s.scroll,
            size=(380, 0),  
            background=False
        )
        
        s.mode = 'auto'
        s.selected_item = None
        
        s.fresh()
        AR.swish()
    
    def set_mode(s, mode):
        s.mode = mode
        if mode == 'auto':
            bw(s.tab1, color=(0.2, 0.6, 1))
            bw(s.tab2, color=(0.8, 0.5, 0.3))
        else:
            bw(s.tab1, color=(0.3, 0.5, 0.8))
            bw(s.tab2, color=(1, 0.7, 0.4))
        s.selected_item = None
        s.fresh()
    
    def fresh(s):
        for child in s.container.get_children():
            child.delete()
        
        if s.mode == 'auto':
            data = var('l') or {}
            items = []
            for trigger, responses in data.items():
                for idx, response in enumerate(responses):
                    items.append((trigger, response, idx))
        else:
            data = var('code_commands') or {}
            items = list(data.items())
            
        if not items:
            tw(
                parent=s.container,
                text="No items found!",
                position=(240, 145),
                h_align='center',
                scale=1.2,
                color=(1, 0.5, 0.5)
            )
            cw(s.container, size=(420, 180))
            return
            
        total_height = 0
        for i, item in enumerate(items):
            item_height = 35
            
            if s.selected_item == i:
                if s.mode == 'auto':
                    _, response_tuple, _ = item
                    response, delay, wildcard = response_tuple
                    response_lines = max(1, (len(response) + 20) // 35) 
                    item_height += 15 + (response_lines * 12)  
                else:
                    _, (response, delay) = item
                    response_lines = max(1, (len(response) + 20) // 35)
                    item_height += 15 + (response_lines * 12)
            
            total_height += item_height + 5  
        
        cw(s.container, size=(480, max(290, total_height)))
        
        y_pos = max(290, total_height) - 15 
        
        for i, item in enumerate(items):
            if s.mode == 'auto':
                trigger, response_tuple, idx = item
                response, delay, wildcard = response_tuple
                display_text = trigger[:25] + "..." if len(trigger) > 25 else trigger
            else:
                trigger, (response, delay) = item
                display_text = trigger[:25] + "..." if len(trigger) > 25 else trigger
            
            item_height = 35
            if s.selected_item == i:
                response_lines = max(1, (len(response) + 20) // 35)
                item_height += 15 + (response_lines * 12)
            
            item_container = cw(
                parent=s.container,
                size=(460, item_height),
                position=(10, y_pos - item_height),
                background=False
            )
            
            item_btn = bw(
                parent=item_container,
                label=display_text,
                size=(440, 35),
                position=(0, item_height - 35),
                on_activate_call=Call(s.toggle_item, i, item),
                text_scale=0.65  
            )
            
            if s.selected_item == i:
                bw(item_btn, color=(0.3, 0.5, 0.8))
                
                detail_y = item_height - 50
                
                if s.mode == 'auto':
                    delay_text = f"Delay: {delay}s | Wildcard: {'Yes' if wildcard else 'No'}"
                    tw(
                        parent=item_container,
                        text=delay_text,
                        position=(10, detail_y),
                        scale=0.55,  
                        color=(0.8, 0.8, 1)
                    )
                else:
                    delay_text = f"Delay: {delay}s"
                    tw(
                        parent=item_container,
                        text=delay_text,
                        position=(10, detail_y),
                        scale=0.55,  
                        color=(0.8, 0.8, 1)
                    )
                
                response_y = detail_y - 12
                truncated_response = response[:60] + "..." if len(response) > 60 else response
                tw(
                    parent=item_container,
                    text=f"Response: {truncated_response}",
                    position=(10, response_y),
                    scale=0.55,  
                    maxwidth=440,
                    color=(1, 1, 1)
                )
            
            y_pos -= item_height + 5  
    
    def toggle_item(s, index, item):
        if s.selected_item == index:
            s.selected_item = None
        else:
            s.selected_item = index
        
        s.fresh()
        
"""Backup and Restore Settings"""
class BackupRestore:
    def __init__(self, t):
        w = self.w = AR.cw(
            source=t,
            size=(400, 250),
            ps=AR.UIS()*0.8
        )
        
        tw(
            parent=w,
            text='Backup & Restore',
            scale=1.2,
            position=(200, 220),
            h_align='center',
            color=(0.5, 1, 0.5)
        )
        
        tw(
            parent=w,
            text='Filename:',
            position=(20, 180),
            scale=0.8
        )
        self.filename = tw(
            parent=w,
            text=f"singlmod_backup_{time.strftime('%Y%m%d_%H%M%S')}",
            size=(250, 30),
            editable=True,
            position=(100, 175),
            color=(0.9, 0.9, 0.9)
        )
        
        AR.bw(
            parent=w,
            label='Backup',
            size=(120, 40),
            position=(50, 120),
            on_activate_call=self.create_backup,
            icon=gt('file'),
            iconscale=0.8
        )
        
        AR.bw(
            parent=w,
            label='Restore',
            size=(120, 40),
            position=(230, 120),
            on_activate_call=self.restore_backup,
            icon=gt('replayIcon'),
            iconscale=0.8
        )
        
        self.status = tw(
            parent=w,
            text='',
            position=(200, 70),
            h_align='center',
            scale=0.8,
            color=(0.8, 0.8, 1)
        )
        
        AR.bw(
            parent=w,
            label='List Backups',
            size=(150, 35),
            position=(125, 30),
            on_activate_call=self.list_backups,
            icon=gt('folder'),
            iconscale=0.7
        )
        
        AR.swish()
    
    def create_backup(self):
        """ایجاد پشتیبان از تنظیمات"""
        filename = tw(query=self.filename).strip()
        if not filename:
            tw(self.status, text='Please enter filename!', color=(1, 0, 0))
            return
            
        if not filename.endswith('.json'):
            filename += '.json'
            
        try:
            # جمع‌آوری تمام تنظیمات پلاگین
            backup_data = {}
            cfg = APP.config
            for key in cfg:
                if key.startswith(pr):
                    backup_data[key] = cfg[key]
            
            script_dir = os.path.dirname(os.path.abspath(__file__))
            backup_path = os.path.join(script_dir, 'backups')
            
            if not os.path.exists(backup_path):
                os.makedirs(backup_path)
                print(f"Created backup directory: {backup_path}")
                
            full_path = os.path.join(backup_path, filename)
            
            counter = 1
            original_filename = filename
            while os.path.exists(full_path):
                name, ext = os.path.splitext(original_filename)
                filename = f"{name}_{counter}{ext}"
                full_path = os.path.join(backup_path, filename)
                counter += 1
            
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2)
                
            print(f"Backup created successfully: {full_path}")
            tw(self.status, text=f'Backup created: {filename}', color=(0, 1, 0))
            push(f'Backup saved: {filename}', color=(0, 1, 0))
            gs('dingSmallHigh').play()
            
            tw(self.filename, text=filename.replace('.json', ''))
            
        except Exception as e:
            error_msg = f'Backup failed: {str(e)}'
            print(error_msg)
            tw(self.status, text=error_msg, color=(1, 0, 0))
            AR.err(error_msg)
    
    def restore_backup(self):
        """بازیابی تنظیمات از پشتیبان"""
        filename = tw(query=self.filename).strip()
        if not filename:
            tw(self.status, text='Please enter filename!', color=(1, 0, 0))
            return
            
        if not filename.endswith('.json'):
            filename += '.json'
            
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            backup_path = os.path.join(script_dir, 'backups')
            full_path = os.path.join(backup_path, filename)
            
            print(f"Attempting to restore from: {full_path}")
            
            if not os.path.exists(full_path):
                error_msg = f'Backup file not found: {filename}'
                print(error_msg)
                tw(self.status, text=error_msg, color=(1, 0, 0))
                return
                
            with open(full_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            cfg = APP.config
            for key, value in backup_data.items():
                cfg[key] = value
            cfg.commit()
            
            print(f"Settings restored successfully from: {filename}")
            tw(self.status, text='Settings restored successfully!', color=(0, 1, 0))
            push(f'Settings restored from: {filename}', color=(0, 1, 0))
            gs('dingSmallHigh').play()
            
            if hasattr(SinglMod, 'party_timer') and SinglMod.party_timer:
                try:
                    SinglMod.party_timer.delete()
                except:
                    pass
                SinglMod.party_timer = None
                
            if hasattr(SinglMod, 'active_timers'):
                SinglMod.active_timers = {}
                
            if var('party_mode'):
                SinglMod().start_party_loop()
                
        except Exception as e:
            error_msg = f'Restore failed: {str(e)}'
            print(error_msg)
            tw(self.status, text=error_msg, color=(1, 0, 0))
            AR.err(error_msg)
    
    def list_backups(self):
        """نمایش لیست پشتیبان‌های موجود"""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            backup_path = os.path.join(script_dir, 'backups')
            
            print(f"Looking for backups in: {backup_path}")
            
            if not os.path.exists(backup_path):
                error_msg = 'Backup directory does not exist!'
                print(error_msg)
                tw(self.status, text=error_msg, color=(1, 0.5, 0))
                return
                
            backups = [f for f in os.listdir(backup_path) if f.endswith('.json')]
            
            backups.sort(key=lambda x: os.path.getmtime(os.path.join(backup_path, x)), reverse=True)
            
            if not backups:
                error_msg = 'No backup files found!'
                print(error_msg)
                tw(self.status, text=error_msg, color=(1, 0.5, 0))
                return
                
            print(f"Found {len(backups)} backup files")
                
            w = AR.cw(
                source=self.w,
                size=(450, 400),
                ps=AR.UIS()*0.7
            )
            
            tw(
                parent=w,
                text="Available Backups",
                scale=1.1,
                position=(225, 370),
                h_align='center',
                color=(1, 1, 0.5)
            )
            
            scroll = sw(
                parent=w,
                size=(430, 300),
                position=(10, 60)
            )
            
            container_height = max(400, len(backups) * 50)
            container = cw(
                parent=scroll,
                size=(410, container_height),
                background=False
            )
            
            for i, backup in enumerate(backups):
                y_pos = container_height - (i * 50) - 40
                
                file_path = os.path.join(backup_path, backup)
                mod_time = time.strftime('%Y-%m-%d %H:%M:%S', 
                                       time.localtime(os.path.getmtime(file_path)))
                
                tw(
                    parent=container,
                    text=backup,
                    position=(10, y_pos),
                    scale=0.7,
                    maxwidth=300,
                    color=(0.8, 0.8, 1)
                )
                
                tw(
                    parent=container,
                    text=mod_time,
                    position=(10, y_pos-15),
                    scale=0.5,
                    maxwidth=300,
                    color=(0.6, 0.6, 0.8)
                )
                
                AR.bw(
                    parent=container,
                    label='Select',
                    size=(80, 30),
                    position=(340, y_pos-10),
                    on_activate_call=Call(self.select_backup, backup, w),
                    text_scale=0.6
                )
                
            AR.swish()
            
        except Exception as e:
            error_msg = f'Error listing backups: {str(e)}'
            print(error_msg)
            AR.err(error_msg)
    
    def select_backup(self, filename, window):
        """انتخاب یک پشتیبان از لیست"""
        tw(self.filename, text=filename.replace('.json', ''))
        cw(window, transition='out_scale')
        tw(self.status, text=f'Selected: {filename}', color=(0, 1, 0))
        print(f"Selected backup: {filename}")

"""Error Log Viewer"""
class ErrorLog:
    def __init__(s, t):
        w = s.w = AR.cw(
            source=t,
            size=(500, 290),
            ps=AR.UIS()*0.7
        )
        
        tw(
            parent=w,
            text='Error Log',
            scale=1.2,
            position=(250, 260),
            h_align='center',
            color=(1, 0.5, 0.5)
        )
        
        s.status_text = tw(
            parent=w,
            text='Select an error to view details',
            position=(250,235),
            scale=0.7,
            color=(0.8, 0.8, 1),
            h_align='center'
        )
        
        s.scroll = sw(
            parent=w,
            size=(480, 160),
            position=(10, 65)
        )
        
        s.container = cw(
            parent=s.scroll,
            size=(460, 0),
            background=False
        )
        
        AR.bw(
            parent=w,
            label='Refresh',
            size=(80, 30),
            position=(50, 25),
            on_activate_call=s.load_errors,
            icon=gt('replayIcon'),
            iconscale=0.7
        )
        
        AR.bw(
            parent=w,
            label='Clear All',
            size=(80, 30),
            position=(370, 25),
            on_activate_call=s.clear_errors,
            icon=gt('crossOut'),
            iconscale=0.7
        )
        
        s.selected_error = None
        s.load_errors()
        AR.swish()
    
    def load_errors(s):
        """Load errors from storage"""
        s.errors = var('error_log') or []
        
        for child in s.container.get_children():
            child.delete()
        
        if not s.errors:
            tw(
                parent=s.container,
                text='No errors logged yet!',
                position=(230, 100),
                h_align='center',
                scale=1.2,
                color=(0.8, 0.8, 0.8)
            )
            cw(s.container, size=(460, 200))
            tw(s.status_text, text='No errors found')
            return
        
        height = len(s.errors) * 40
        cw(s.container, size=(460, height))
        
        for i, error in enumerate(s.errors):
            y_pos = height - i * 40 - 20
            
            btn = bw(
                parent=s.container,
                size=(450, 35),
                position=(5, y_pos),
                label='',
                color=(0.25, 0.25, 0.3),
                on_activate_call=Call(s.show_error_details, i)
            )
            
            section, message, timestamp = error
            time_str = time.strftime("%H:%M:%S", time.localtime(timestamp))
            
            tw(
                parent=s.container,
                text=f"{section} - {time_str}",
                position=(15, y_pos + 5),
                scale=0.7,
                color=(1, 1, 1),
                maxwidth=300,
                h_align='left'
            )
            
            preview = message[:30] + "..." if len(message) > 30 else message
            tw(
                parent=s.container,
                text=preview,
                position=(15, y_pos - 10),
                scale=0.6,
                color=(1, 0.5, 0.5),
                maxwidth=300,
                h_align='left'
            )
        
        tw(s.status_text, text=f'{len(s.errors)} errors found')
    
    def show_error_details(s, index):
        """Show detailed view of a specific error"""
        if index >= len(s.errors):
            return
            
        s.selected_error = index
        section, message, timestamp = s.errors[index]
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        
        detail_w = AR.cw(
            source=s.w,
            size=(450, 280),
            ps=AR.UIS()*0.6
        )
        
        tw(
            parent=detail_w,
            text='Error Details',
            scale=1.1,
            position=(225, 250),
            h_align='center',
            color=(1, 0.5, 0.5)
        )
        
        tw(
            parent=detail_w,
            text=f'Section: {section}',
            position=(20, 220),
            scale=0.8,
            color=(1, 1, 1)
        )
        
        tw(
            parent=detail_w,
            text=f'Time: {time_str}',
            position=(20, 200),
            scale=0.7,
            color=(0.8, 0.8, 1)
        )
        
        message_scroll = sw(
            parent=detail_w,
            size=(430, 120),
            position=(10, 70)
        )
        
        message_container = cw(
            parent=message_scroll,
            size=(410, 0),
            background=False
        )
        
        lines = message.split('\n')
        line_height = 20
        total_height = len(lines) * line_height
        
        cw(message_container, size=(410, total_height))
        
        y_pos = total_height - line_height
        for line in lines:
            tw(
                parent=message_container,
                text=line,
                position=(5, y_pos),
                scale=0.7,
                color=(1, 1, 1),
                maxwidth=400,
                h_align='left'
            )
            y_pos -= line_height
        
        AR.bw(
            parent=detail_w,
            label='Copy Error',
            size=(120, 30),
            position=(165, 30),
            on_activate_call=Call(s.copy_error, message),
            icon=gt('fileIcon'),
            iconscale=0.7
        )
    
    def copy_error(s, error_message):
        """Copy error to clipboard"""
        try:
            if CIS():
                from babase import clipboard_set_text
                clipboard_set_text(error_message)
                push('Error copied to clipboard!', color=(0, 1, 0))
                gs('dingSmall').play()
            else:
                AR.err('Clipboard not supported!')
        except Exception as e:
            AR.err(f'Copy error: {str(e)}')
    
    def clear_errors(s):
        """Clear all errors"""
        var('error_log', [])
        s.load_errors()
        push('All errors cleared!', color=(1, 0.5, 0))
        
"""Riddle Management Panel - Compact Version"""
class Riddles:
    def __init__(s, source):
        w = s.w = AR.cw(
            source=source,
            size=(500, 290),
            ps=AR.UIS() * 0.8
        )
        
        tw(
            parent=w,
            text='Riddle Management',
            position=(250, 260),
            h_align='center',
            scale=1.0,
            color=(0.8, 0.5, 0.8)
        )
        
        tw(
            parent=w,
            text='Question:',
            position=(20, 230),
            scale=0.8
        )
        s.question_input = tw(
            parent=w,
            size=(460, 30),
            editable=True,
            position=(20, 200),
            color=(0.9, 0.9, 0.9),
            description="Enter riddle question..."
        )
        
        tw(
            parent=w,
            text='Answer:',
            position=(20, 170),
            scale=0.8
        )
        s.answer_input = tw(
            parent=w,
            size=(460, 30),
            editable=True,
            position=(20, 140),
            color=(0.9, 0.9, 0.9),
            description="Enter riddle answer..."
        )
        
        s.add_button = AR.bw(
            parent=w,
            label='Add Riddle',
            size=(150, 30),
            position=(20, 100),
            on_activate_call=s.add_riddle,
            icon=gt('addGameWindow'),
            iconscale=0.7
        )
        
        s.del_button = AR.bw(
            parent=w,
            label='Delete Selected',
            size=(150, 30),
            position=(180, 100),
            on_activate_call=s.delete_selected,
            icon=gt('trash'),
            iconscale=0.7
        )
        bw(s.del_button, color=(1, 0.2, 0.2))
        
        s.status_text = tw(
            parent=w,
            text='Select a riddle...',
            position=(350, 100),
            scale=0.7,
            color=(0.8, 0.8, 1)
        )
        
        s.scroll = sw(
            parent=w,
            size=(480, 80),
            position=(10, 10)
        )
        
        s.container = cw(
            parent=s.scroll,
            size=(460, 0),
            background=False
        )
        
        s.selected_riddle = None
        s.item_widgets = []
        s.fresh()
        AR.swish()
    
    def fresh(s):
        for widget in s.item_widgets:
            widget.delete()
        s.item_widgets = []
        
        riddles = SinglMod.get_riddles()
        height = max(80, len(riddles) * 30)
        
        # Recreate the container with the proper height
        if hasattr(s, 'container') and s.container:
            s.container.delete()
        s.container = cw(
            parent=s.scroll,
            size=(460, height),
            background=False
        )
        
        y_pos = height - 15
        for i, (question, answer) in enumerate(riddles):
            item_button = AR.bw(
                parent=s.container,
                size=(440, 25),
                position=(0, y_pos),
                label='',  
                on_activate_call=Call(s.select_riddle, i),
                enable_sound=False
            )
            bw(item_button, color=(0.2, 0.2, 0.3) if i != s.selected_riddle else (0, 0.5, 0))
            
            tw(
                parent=s.container,
                text=f"پرسش: {question[:40]}{'...' if len(question) > 40 else ''}",
                position=(10, y_pos + 15),
                scale=0.7,
                maxwidth=300,
                color=(1, 1, 1)
            )
            
            tw(
                parent=s.container,
                text=f"جواب: {answer}",
                position=(10, y_pos + 5),
                scale=0.6,
                maxwidth=300,
                color=(0.7, 0.7, 1)
            )
            
            s.item_widgets.append(item_button)
            y_pos -= 30
    
    def select_riddle(s, index):
        s.selected_riddle = index
        riddles = SinglMod.get_riddles()
        
        if index < len(riddles):
            question, answer = riddles[index]
            tw(s.status_text, text=f"انتخاب شده: {question[:30]}{'...' if len(question) > 30 else ''}")
            
            for i, button in enumerate(s.item_widgets):
                color = (0, 0.5, 0) if i == index else (0.2, 0.2, 0.3)
                bw(button, color=color)
    
    def add_riddle(s):
        question = tw(query=s.question_input).strip()
        answer = tw(query=s.answer_input).strip()
        
        if not question or not answer:
            AR.err('لطفاً هم پرسش و هم جواب را وارد کنید!')
            return
        
        riddles = SinglMod.get_riddles()
        riddles.append((question, answer))
        SinglMod.save_riddles(riddles)
        
        tw(s.question_input, text='')
        tw(s.answer_input, text='')
        s.fresh()
        AR.ok()
        push('چیستان اضافه شد!', color=(0, 1, 0))
    
    def delete_selected(s):
        if s.selected_riddle is None:
            AR.err('لطفاً یک چیستان را انتخاب کنید!')
            return
        
        riddles = SinglMod.get_riddles()
        if s.selected_riddle < len(riddles):
            question, answer = riddles[s.selected_riddle]
            del riddles[s.selected_riddle]
            SinglMod.save_riddles(riddles)
            
            tw(s.status_text, text='هیچ چیستان انتخاب نشده')
            s.selected_riddle = None
            s.fresh()
            AR.ok()
            push(f'چیستان "{question[:20]}..." حذف شد!', color=(1, 0.5, 0))

"""Party Color Settings Panel"""
class PartyColors:
    def __init__(s,t):
        w = AR.cw(
            source=t,
            size=(400,290),
            ps=AR.UIS()*0.8
        )
        s.w = w
        
        tw(
            parent=w,
            text='Party Color Settings',
            position=(180,250),
            h_align='center',
            scale=1.0,
            color=(0.8,0.5,0.8))
        
        AR.bw(
            parent=w,
            label='Toggle All',
            size=(100,35),
            position=(50,210),
            on_activate_call=s.toggle_all,
            icon=gt('uiAtlas'),
            iconscale=0.8
        )
        
        AR.bw(
            parent=w,
            label='Save',
            size=(80,35),
            position=(270,210),
            on_activate_call=s.save_settings,
            icon=gt('startButton'),
            iconscale=0.8
        )
        
        scroll_widget = sw(
            parent=w,
            size=(380,190),
            position=(10,20)
        )
        s.container = cw(
            parent=scroll_widget,
            size=(360,len(PARTY_COLORS)*40),
            background=False
        )
        
        s.color_widgets = []
        s.fresh()
        AR.swish()
    
    """Refresh color list"""
    def fresh(s):
        for widget in s.color_widgets:
            widget.delete()
        s.color_widgets = []
        
        enabled_colors = var('party_colors_enabled') or [True]*len(PARTY_COLORS)
        
        for i,(name,color) in enumerate(PARTY_COLORS):
            y_pos = len(PARTY_COLORS)*40 - i*40 - 30
            
            preview = bw(
                parent=s.container,
                size=(35,35),
                position=(10,y_pos),
                color=color,
                texture=None,
                enable_sound=False
            )
            s.color_widgets.append(preview)
            
            name_widget = tw(
                parent=s.container,
                text=name,
                position=(55,y_pos+10),
                scale=0.8,
                color=(1,1,1),
                h_align='left'
            )
            s.color_widgets.append(name_widget)
            
            checkbox = chk(
                parent=s.container,
                size=(35,35),
                position=(350,y_pos),
                value=enabled_colors[i],
                on_value_change_call=Call(s.toggle_color,i)
            )
            s.color_widgets.append(checkbox)
    
    """Toggle all colors"""
    def toggle_all(s):
        enabled_colors = var('party_colors_enabled') or [True]*len(PARTY_COLORS)
        new_state = not all(enabled_colors)
        enabled_colors = [new_state]*len(enabled_colors)
        var('party_colors_enabled',enabled_colors)
        s.fresh()
    
    """Toggle a single color"""
    def toggle_color(s,index,value):
        enabled_colors = var('party_colors_enabled') or [True]*len(PARTY_COLORS)
        enabled_colors[index] = value
        var('party_colors_enabled',enabled_colors)
    
    """Save settings"""
    def save_settings(s):
        AR.ok()
        push('Color settings saved!',color=(0,1,0))

"""Message Splitting Settings"""
class SplitSettings:
    def __init__(s,t):
        w = AR.cw(
            source=t,
            size=(350,200),
            ps=AR.UIS()*0.8
        )
        AR.swish()
        
        tw(
            parent=w,
            text='Message Splitting Settings',
            position=(165,170),
            h_align='center',
            scale=0.8,
            color=(0.5,0.8,1))
        
        s.enable_checkbox = chk(
            text='Enable Message Splitting',
            parent=w,
            size=(320,30),
            position=(15,140),
            textcolor=(1,1,1),
            value=var('enable_splitting',True),
            on_value_change_call=Call(var,'enable_splitting'),
            color=(0.13,0.13,0.13)
        )
        
        tw(
            parent=w,
            text='Max Characters per Chunk:',
            position=(20,100),
            scale=0.8
        )
        s.max_chars = tw(
            parent=w,
            text=str(var('max_chars') or 50),
            size=(60,25),
            editable=True,
            position=(280,100),
            color=(0.75,0.75,0.75)
        )
        
        tw(
            parent=w,
            text='Delay Between Chunks (sec):',
            position=(20,60),
            scale=0.8
        )
        s.delay = tw(
            parent=w,
            text=str(var('split_delay') or 1.0),
            size=(60,25),
            editable=True,
            position=(280,60),
            color=(0.75,0.75,0.75)
        )
        
        AR.bw(
            parent=w,
            label='Save',
            size=(80,30),
            position=(135,20),
            on_activate_call=s.save_settings
        )
    
    """Save settings"""
    def save_settings(s):
        try:
            max_chars = int(tw(query=s.max_chars))
            if max_chars < 10 or max_chars > 200:
                AR.err('Max chars: 10-200')
                return
                
            delay = float(tw(query=s.delay))
            if delay < 0.1 or delay > 2.0:
                AR.err('Delay: 0.1-2.0 seconds')
                return
                
            var('max_chars',max_chars)
            var('split_delay',delay)
            AR.ok()
            push('Splitting settings saved!',color=(0,1,0))
        except:
            AR.err('Invalid values!')

"""Player List Management Panel - Improved Version"""
class PlayerList:
    def __init__(s,t):
        w = AR.cw(
            source=t,
            size=(350,350),
            ps=AR.UIS()*0.5
        )
        s.w = w
        
        tw(
            parent=w,
            text='Players for Truth Game:',
            position=(175,330),
            h_align='center',
            scale=1.0,
            color=(0.8,0.5,0.8))
        
        tw(
            parent=w,
            text='Add Player Name:',
            position=(20,300),
            scale=0.7
        )
        s.new_player = tw(
            parent=w,
            size=(200,25),
            editable=True,
            position=(20,270),
            color=(0.75,0.75,0.75),
            allow_clear_button=False
        )
        AR.bw(
            parent=w,
            label='Add',
            size=(50,25),
            position=(230,270),
            on_activate_call=s.add_player,
            text_scale=0.7
        )
        
        AR.bw(
            parent=w,
            label='Show Players',
            size=(110,30),
            position=(50,220),
            on_activate_call=s.show_players,
            icon=gt('usersButton'),
            iconscale=0.7
        )
        
        AR.bw(
            parent=w,
            label='Delete All',
            size=(110,30),
            position=(190,220),
            on_activate_call=s.delete_all,
            icon=gt('trash'),
            iconscale=0.7,
            color=(1,0.2,0.2)
        )
        
        a = sw(
            parent=w,
            size=(310,180),
            position=(20,30)
        )
        s.c = cw(
            parent=a,
            size=(310,0),
            background=False
        )
        s.kids = []
        s.fresh()
        AR.swish()
    
    """Refresh player list"""
    def fresh(s):
        [k.delete() for k in s.kids]
        s.kids.clear()
        
        players = list(var('truth_players') or [])
        height = (len(players)+1)*25
        
        header = cw(
            parent=s.c,
            size=(310,25),
            position=(0,25*len(players))
        )
        tw(
            text="Player Name",
            parent=header,
            size=(200,25),
            position=(10,0),
            h_align='left',
            v_align='center',
            color=(1,1,0.5),
            scale=0.8
        )
        tw(
            text="Action",
            parent=header,
            size=(100,25),
            position=(220,0),
            h_align='center',
            v_align='center',
            color=(1,1,0.5),
            scale=0.8
        )
        s.kids.append(header)
        
        for i,player in enumerate(players):
            c = cw(
                parent=s.c,
                size=(310,25),
                position=(0,25*(len(players)-i-1))
            )
            tw(
                text=player,
                parent=c,
                size=(200,25),
                position=(10,0),
                h_align='left',
                v_align='center',
                color=(0.8,0.5,1),
                scale=0.7
            )
            AR.bw(
                parent=c,
                label='Delete',
                size=(60,20),
                position=(240,2.5),
                text_scale=0.6,
                on_activate_call=Call(s.delete_player,player),
                color=(1,0,0)
            )
            s.kids.append(c)
            
        cw(s.c,size=(310,height))
    
    """Add a player"""
    def add_player(s):
        player_name = tw(query=s.new_player).strip()
        if not player_name:
            AR.err('Enter player name!')
            return
            
        players = list(var('truth_players') or [])
        if player_name in players:
            AR.err('Player already exists!')
            return
            
        players.append(player_name)
        var('truth_players',players)
        tw(s.new_player,text='')
        s.fresh()
        AR.ok()
        push(f"Player '{player_name}' added",color=(0,1,0))
    
    """Delete a player"""
    def delete_player(s,player):
        players = list(var('truth_players') or [])
        if player in players:
            players.remove(player)
            var('truth_players',players)
            s.fresh()
            AR.ok()
            push(f"Player '{player}' deleted",color=(1,0.5,0))
    
    """Delete all players"""
    def delete_all(s):
        players = list(var('truth_players') or [])
        if not players:
            AR.err('Player list is already empty!')
            return
            
        var('truth_players',[])
        s.fresh()
        AR.ok()
        push('All players deleted!',color=(1,0.5,0))
    
    """Show players in chat"""
    def show_players(s):
        players = list(var('truth_players') or [])
        if not players:
            push('No players in the list!',color=(1,0,0))
            return
            
        player_list = " | ".join(players)
        send_in_char_chunks(f"لیست بازیکنان:\n{player_list}" + SinglMod.B)

"""Ear Processing Speed Settings"""
class EarSpeedSettings:
    def __init__(s,t):
        w = AR.cw(
            source=t,
            size=(350,200),
            ps=AR.UIS()*0.8
        )
        AR.swish()
        
        tw(
            parent=w,
            text='Ear Processing Speed:',
            position=(150,165),
            h_align='center',
            scale=0.8,
            color=(0.5,0.8,1))
        
        tw(
            parent=w,
            text='Speed (s):',
            position=(20,130),
            scale=0.7
        )
        s.speed_entry = tw(
            parent=w,
            text=str(var('ear_processing_speed') or 0.01),
            size=(80,30),
            editable=True,
            position=(150,130),
            color=(0.75,0.75,0.75)
        )
        
        AR.bw(
            parent=w,
            label='Save',
            size=(80,30),
            position=(135,70),
            on_activate_call=s.save_settings
        )
    
    """Save settings"""
    def save_settings(s):
        try:
            speed = float(tw(query=s.speed_entry))
            if speed < 0.001 or speed > 1.0:
                AR.err('Speed must be between 0.001 and 1.0 seconds!')
                return
            var('ear_processing_speed', speed)
            AR.ok()
            push('Ear speed saved!',color=(0,1,0))
        except:
            AR.err('Invalid value!')


"""کلاس اتصال مجدد"""
class Reconnect:
    def __init__(s, t):
        w = s.w = AR.cw(
            source=t,
            size=(350, 200),
            ps=AR.UIS()*0.8
        )
        
        tw(
            parent=w,
            text='اتصال مجدد',
            scale=1.2,
            position=(160, 170),
            h_align='center',
            color=(0, 1, 1)
        )
        
        s.server_info = tw(
            parent=w,
            text=f'اطلاعات سرور:\nآیپی: {server_ip}\nپورت: {server_port}',
            position=(155, 140),
            scale=0.8,
            color=(1, 1, 1),
            h_align='center',
            maxwidth=300
        )
        
        s.reconnect_btn = bw(
            parent=w,
            label='اتصال مجدد',
            size=(120, 50),
            position=(20, 15),
            on_activate_call=s.do_reconnect,
            color=(0, 0.6, 0)
        )
        
        s.disconnect_btn = bw(
            parent=w,
            label='قطع اتصال',
            size=(120, 50),
            position=(200, 15),
            on_activate_call=s.do_disconnect,
            color=(0.8, 0.2, 0.2)
        )
        
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
        
        teck(1.0, s.update_info)
    
    def do_reconnect(s):
        """انجام اتصال مجدد"""
        try:
            if server_ip != "127.0.0.1" and server_port != 43210:
                conn_info = get_connection_info()
                if conn_info:
                    original_disconnect()
                    push('در حال قطع اتصال...', color=(1, 0.5, 0))
                    time.sleep(1)
                
                push(f'در حال اتصال به {server_ip}:{server_port}...', color=(0, 1, 0))
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

"""Server Information"""
class ServerInfo:
    def __init__(s, t):
        w = s.w = AR.cw(
            source=t,
            size=(400, 350),
            ps=AR.UIS()*0.8
        )
        
        tw(
            parent=w,
            text='Server Information',
            scale=1.2,
            position=(180, 280),
            h_align='center',
            color=(0, 1, 1)
        )
        
        global server_ip, server_port, current_ping
        
        conn_info = get_connection_info()
        if conn_info:
            server_name = conn_info.name
            server_status = "Connected"
        else:
            server_name = "Local Server"
            server_status = "Local"
        
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
            tw(
                parent=w,
                text=label,
                position=(30, y_pos),
                scale=0.8,
                color=(1, 1, 0.8),
                h_align='left'
            )
            value_x = 230
            
            value_widget = tw(
                parent=w,
                text="",  
                position=(value_x, y_pos),
                scale=0.8,
                color=(1, 1, 1),
                h_align='left'
            )
            s.info_widgets.append(value_widget)
            y_pos -= 30
        
        s.update_server_info()
        
        copy_buttons = [
            ('IP copy', server_ip, (20, 70)),
            ('Port copy', str(server_port), (150, 70)),
            ('copy all', f"{server_ip}:{server_port}", (280, 70))
        ]
        
        for label, data, pos in copy_buttons:
            AR.bw(
                parent=w,
                label=label,
                size=(100, 35),
                position=pos,
                on_activate_call=Call(s.copy_to_clipboard, data)
            )

        s.timer = teck(1.0, s.update_server_info)
        AR.swish()
    
    def update_server_info(s):
        """بروزرسانی اطلاعات سرور"""
        if not hasattr(s, 'w') or not s.w.exists():
            return
        
        conn_info = get_connection_info()
        
        if conn_info:
            server_name = conn_info.name
            server_status = "Connected"
        else:
            server_name = "Local Server"
            server_status = "Local"
        
        values = [
            server_ip,
            str(server_port),
            server_name,
            f"{current_ping} ms",
            server_status
        ]
        
        for i, value in enumerate(values):
            if i < len(s.info_widgets) and s.info_widgets[i].exists():
                tw(s.info_widgets[i], text=value)
        
        if 3 < len(s.info_widgets) and s.info_widgets[3].exists():
            ping_color = (0, 1, 0) if current_ping < 100 else (1, 1, 0) if current_ping < 300 else (1, 0, 0)
            tw(s.info_widgets[3], color=ping_color)
        
        if 4 < len(s.info_widgets) and s.info_widgets[4].exists():
            status_color = (0, 1, 0) if server_status == "Connected" else (1, 1, 0) if server_status == "Local" else (1, 0, 0)
            tw(s.info_widgets[4], color=status_color)
        
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
    active_instance = None

    def __init__(s, source):
        Spam.active_instance = s

        w = s.w = AR.cw(
            source=source,
            size=(400, 350),
            ps=AR.UIS()*0.8
        )

        tw(
            parent=w,
            text='SPAM SYSTEM',
            scale=1.2,
            position=(200, 280),
            h_align='center',
            color=(1, 0.5, 0)
        )

        tw(parent=w, text='YUOR TEXT:', position=(30, 250), scale=0.9, color=(1, 1, 1))
        s.message_widget = tw(parent=w, position=(30, 220), size=(340, 30), editable=True,
                              text='', color=(0.9, 0.9, 0.9))

        tw(parent=w, text='NUMBER:', position=(30, 180), scale=0.9, color=(1, 1, 1))
        s.count_widget = tw(parent=w, position=(30, 150), size=(150, 30), editable=True,
                            text='5', h_align='center', color=(0.9, 0.9, 0.9))

        tw(parent=w, text='DELAY (S) :', position=(200, 180), scale=0.9, color=(1, 1, 1))
        s.delay_widget = tw(parent=w, position=(200, 150), size=(150, 30), editable=True,
                            text='1', h_align='center', color=(0.9, 0.9, 0.9))

        s.status_text = tw(parent=w, text='READY', position=(30, 110), scale=0.8, color=(0.8, 0.8, 1))

        s.start_btn = bw(parent=w, label='START', size=(120, 40), position=(20, 60),
                         on_activate_call=Call(s.start_spam), color=(0, 0.6, 0), textcolor=(1, 1, 1))

        s.stop_btn = bw(parent=w, label='STOP', size=(120, 40), position=(160, 60),
                        on_activate_call=Call(s.stop_spam), color=(0.6, 0, 0), textcolor=(1, 1, 1))

        s.spamming = False
        s.spam_timer = None
        s.remaining_count = 0
        s.sent_count = 0  
        AR.swish()

    @staticmethod
    def start_spam():
        s = Spam.active_instance
        try:
            message = tw(query=s.message_widget).strip()
            count = int(tw(query=s.count_widget))
            delay = float(tw(query=s.delay_widget))

            if not message:
                AR.err('Please enter a TEXT!')
                return

            if count <= 0 or delay <= 0 :
                AR.err('Delay ​​must be greater than 1!')
                return

            s.spamming = True
            s.remaining_count = count
            s.spam_message = message
            s.spam_delay = delay
            s.sent_count = 1  

            tw(s.status_text, text=f'Spaming: {s.remaining_count} remaining', color=(0, 1, 0))

            s.do_spam()

            push(f'START SPAMING: {count} TEXT WITH A DELAY OF{delay} SECENDS', color=(0, 1, 0))

        except ValueError:
            AR.err('Please enter valid numbers!')
        except Exception as e:
            AR.err(f'Error: {str(e)}')

    @staticmethod
    def stop_spam():
        s = Spam.active_instance
        if not s.spamming:
            return  

        s.spamming = False

        if s.spam_timer:
            try:
                s.spam_timer.cancel()
            except:
                pass
            s.spam_timer = None

        tw(s.status_text, text='⛔ SPAM STOPED', color=(1, 0.5, 0))
        push('⛔ SINGL MOD: ((spam stoped))', color=(1, 0.5, 0))

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
            tw(s.status_text, text='✅ SINGLMOD: ((Spam is over))', color=(0, 1, 0))
            push('✅ SINGLMOD:((Spam is over))', color=(0, 1, 0))
            return

        try:
            s.sent_count += 1

            message_to_send = s.spam_message
            if s.sent_count % 2 == 0:
                message_to_send += "."
                
            CM(message_to_send)
            s.remaining_count -= 1

            if s.w.exists():
                tw(s.status_text, text=f'SPAMING: {s.remaining_count} remaining')

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
                tw(s.status_text, text='✅ SINGLMOD: Spam is over', color=(0, 1, 0))
                push('✅ SINGLMOD: Spam is over', color=(0, 1, 0))

        except Exception as e:
            AR.err(f'Error: {str(e)}')
            Spam.stop_spam()
            
"""Theme Settings Panel - Compact Version"""
class ThemeSettings:
    def __init__(s,t):
        w = s.w = AR.cw(
            source=t,
            size=(300,250),
            ps=AR.UIS()*0.8
        )
        
        tw(
            parent=w,
            text='Theme Settings',
            position=(130,230),
            h_align='center',
            scale=1,
            color=(0.8,0.5,0.8))
        
        themes = [
            ("Classic", "classic"),
            ("Beautiful", "beautiful"),
            ("Modern", "modern"),
            ("Custom", "custom")
        ]
        
        y_pos = 190
        for i, (label, theme_name) in enumerate(themes):
            b = bw(
                parent=w,
                label=label,
                size=(100,35),
                position=(20, y_pos - i*45), 
                on_activate_call=Call(s.set_theme, theme_name)
            )
            if theme_name == "classic":
                bw(b, color=(0.1,0.1,0.1))
            elif theme_name == "beautiful":
                bw(b, color=(0.7,0.5,0.1))
            elif theme_name == "modern":
                bw(b, color=(0.2,0.5,0.8))

                themes = [
            ("Gigari", "gig"),
            ("Zard", "zr"),
            ("Sorati", "sr")
        ]
        
        y_pos = 190
        for i, (label, theme_name) in enumerate(themes):
            b = bw(
                parent=w,
                label=label,
                size=(100,35),
                position=(180, y_pos - i*45), 
                on_activate_call=Call(s.set_theme, theme_name)
            )
            if theme_name == "gig":
                bw(b, color=(0.7,0.0,0.3))
            elif theme_name == "zr":
                bw(b, color=(0.9,0.9,0.0))
            elif theme_name == "sr":
                bw(b, color=(0.9,0.4,0.7))
                
        AR.bw(
            parent=w,
            label='Save Theme',
            size=(120,35),
            position=(90,20),
            on_activate_call=s.save_theme,
            icon=gt('gameCenterIcon'),
            iconscale=0.7
        )
        
        AR.swish()
    
    def set_theme(s, theme_name):
        s.selected_theme = theme_name
        if theme_name == "custom":
            CustomThemeSettings(s.w)
    
    def save_theme(s):
        if hasattr(s, 'selected_theme'):
            var('theme', s.selected_theme)
            push(f"Theme changed to {s.selected_theme}!", color=(0,1,0))
            cw(s.w, transition='out_scale')
        else:
            AR.err('Please select a theme first!')

"""Custom Theme Settings - Compact Version"""
class CustomThemeSettings:
    def __init__(s, parent_window):
        w = s.w = AR.cw(
            source=parent_window,
            size=(300,250),
            ps=AR.UIS()*0.7
        )
        
        tw(
            parent=w,
            text='Custom Theme Settings',
            position=(150,230),
            h_align='center',
            scale=1.1,
            color=(0.8,0.5,0.8))
        
        tw(
            parent=w,
            text='Panel Color (RGB):',
            position=(20,200),
            scale=0.8
        )
        s.panel_r = tw(parent=w, text='0.18', size=(70,25), editable=True, position=(20,170), color=(0.75,0.75,0.75))
        s.panel_g = tw(parent=w, text='0.18', size=(70,25), editable=True, position=(100,170), color=(0.75,0.75,0.75))
        s.panel_b = tw(parent=w, text='0.18', size=(70,25), editable=True, position=(180,170), color=(0.75,0.75,0.75))
        
        tw(
            parent=w,
            text='Button Color (RGB):',
            position=(20,140),
            scale=0.8
        )
        s.button_r = tw(parent=w, text='0.18', size=(70,25), editable=True, position=(20,110), color=(0.75,0.75,0.75))
        s.button_g = tw(parent=w, text='0.18', size=(70,25), editable=True, position=(100,110), color=(0.75,0.75,0.75))
        s.button_b = tw(parent=w, text='0.18', size=(70,25), editable=True, position=(180,110), color=(0.75,0.75,0.75))
        
        panel_color = var('custom_panel_color') or (0.18,0.18,0.18)
        button_color = var('custom_button_color') or (0.18,0.18,0.18)
        tw(s.panel_r, text=str(panel_color[0]))
        tw(s.panel_g, text=str(panel_color[1]))
        tw(s.panel_b, text=str(panel_color[2]))
        tw(s.button_r, text=str(button_color[0]))
        tw(s.button_g, text=str(button_color[1]))
        tw(s.button_b, text=str(button_color[2]))
        
        AR.bw(
            parent=w,
            label='Save Custom Theme',
            size=(150,35),
            position=(75,50),
            on_activate_call=s.save_settings,
            icon=gt('save'),
            iconscale=0.7
        )
    
    def save_settings(s):
        try:
            panel_r = float(tw(query=s.panel_r))
            panel_g = float(tw(query=s.panel_g))
            panel_b = float(tw(query=s.panel_b))
            button_r = float(tw(query=s.button_r))
            button_g = float(tw(query=s.button_g))
            button_b = float(tw(query=s.button_b))
            
            for val in [panel_r, panel_g, panel_b, button_r, button_g, button_b]:
                if val < 0.0 or val > 1.0:
                    AR.err('RGB values must be between 0.0 and 1.0!')
                    return
            
            panel_color = (panel_r, panel_g, panel_b)
            button_color = (button_r, button_g, button_b)
            
            var('custom_panel_color', panel_color)
            var('custom_button_color', button_color)
            var('theme', 'custom')
            
            AR.ok()
            push('Custom theme saved!', color=(0,1,0))
            cw(s.w, transition='out_scale')
        except:
            AR.err('Invalid values!')

"""Performance Mode Settings Panel"""
class PerformancePanel:
    def __init__(s, t):
        w = AR.cw(
            source=t,
            size=(350, 300),
            ps=AR.UIS()*0.8
        )
        
        tw(
            parent=w,
            text='Performance Mode ',
            position=(175, 280),
            h_align='center',
            scale=1.2,
            color=(0.5, 0.8, 1)
        )
        
        s.modes = [
            ("Normal Mode", "normal", (0.2, 0.8, 0.2)),
            ("Performance Mode", "performance", (0.8, 0.8, 0.2)),
            ("Ultra Performance", "ultra", (0.8, 0.2, 0.2))
        ]
        
        y_pos = 240
        for i, (label, mode_name, color) in enumerate(s.modes):
            b = bw(
                parent=w,
                label=label,
                size=(320, 40),
                position=(15, y_pos - i*50),
                color=color,
                textcolor=(1, 1, 1),
                on_activate_call=Call(s.set_mode, mode_name)
            )
        
        AR.bw(
            parent=w,
            label='Save Settings',
            size=(150, 40),
            position=(100, 30),
            on_activate_call=s.save_settings,
            icon=gt('lock'),
            iconscale=0.8
        )
    
    def set_mode(s, mode_name):
        s.selected_mode = mode_name
    
    def save_settings(s):
        if not hasattr(s, 'selected_mode'):
            AR.err('Please select a performance mode first!')
            return
        
        if s.selected_mode == "normal":
            var('auto_response_enabled', True)
            var('swear_mode', True)
            var('party_mode', False)
            var('riddle_mode', False)
            var('truth_game_active', False)
            var('choice_game_active', False)
            var('enable_splitting', True)
            var('ear_processing_speed', 0.01)
            var('state', 1) 
            push("Normal mode activated! All features enabled.", color=(0, 1, 0))
        
        elif s.selected_mode == "performance":
            var('auto_response_enabled', False)
            var('swear_mode', False)
            var('party_mode', False)
            var('riddle_mode', False)
            var('truth_game_active', False)
            var('choice_game_active', False)
            var('enable_splitting', False)
            var('ear_processing_speed', 0.3)
            var('state', 1) 
            push("Performance mode activated! Heavy features disabled.", color=(1, 1, 0))
        
        elif s.selected_mode == "ultra":
            var('state', 0) 
            
            if hasattr(SinglMod, 'party_timer') and SinglMod.party_timer:
                try:
                    SinglMod.party_timer.delete()
                except:
                    pass
                SinglMod.party_timer = None
            
            if hasattr(SinglMod, 'active_timers'):
                for timer_id in list(SinglMod.active_timers.keys()):
                    del SinglMod.active_timers[timer_id]
            
            var('party_mode', False)
            var('riddle_mode', False)
            var('truth_game_active', False)
            var('choice_game_active', False)
            push("Ultra Performance mode activated! Plugin completely disabled.", color=(1, 0.5, 0))
        
        var('performance_mode', s.selected_mode)
        AR.ok()
        push("Performance settings saved!", color=(0, 1, 0))

"""The AutoRespond base"""
class AR:
    @classmethod
    def UIS(c=0):
        i = APP.ui_v1.uiscale
        return [1.5,1.1,0.8][0 if i == uis.SMALL else 1 if i == uis.MEDIUM else 2]
    
    @classmethod
    def parse(c=0,t=0,s=None):
        me = SinglMod.me()
        now = DT.now()
        
        jy, jm, jd = gregorian_to_jalali(now.year, now.month, now.day)
        jalali_str = f"{jy}/{jm:02d}/{jd:02d}"

        bet = random.randint(1, 6)
                
        gregorian_date = now.strftime("%Y/%m/%d")

        # جایگزینی تاس تصادفی
        if '%dice' in t:
            t = t.replace('%dice', random.choice(DICE))
        #جایگزینی آیپی سرور واقعی
        if '%ip' in t:
            t = t.replace('%ip', f"IP : {server_ip} Port : {server_port}")
        if '%p' in t:
            t = t.replace('%p', f"{current_ping} ms")
            
        replacements = {
            '%t': now.strftime("%H:%M:%S"),
            '%s': s or SinglMod.v2 + 'Singl',
            '%m': me,
            '%dsh': jalali_str,
            '%dm': gregorian_date
        }
        
        for key,value in replacements.items():
            t = t.replace(key,value)
            
        return t

    @classmethod
    def bw(c,**k):
        theme = var('theme') or 'classic'
        if theme == 'classic':
            color = (0.0,0.0,0.)
        elif theme == 'beautiful':
            color = (0.7,0.5,0.1)
        elif theme == 'modern':
            color = (0.2,0.5,0.8)
        elif theme == 'gig':
            color = (0.7,0.0,0.3)
        elif theme == 'zr':
            color = (0.9,0.9,0.0)
        elif theme == 'sr':
            color = (0.9,0.4,0.7)
        elif theme == 'custom':
            color = var('custom_button_color') or (0.18,0.18,0.18)
        else:
            color = (0.18,0.18,0.18)
            
        return bw(
            **k,
            textcolor=(1,1,1),
            enable_sound=False,
            button_type='square',
            color=color
        )
    
    @classmethod
    def cw(c,source,ps=0,**k):
        theme = var('theme') or 'classic'
        if theme == 'classic':
            color = (0.18,0.18,0.18)
        elif theme == 'beautiful':
            color = (0.18,0.18,0.18) 
        elif theme == 'modern':
            color = (0.9,0.9,0.9)
        elif theme == 'custom':
            color = var('custom_panel_color') or (0.18,0.18,0.18)
        else:
            color = (0.0,0.0,0.0)
        
        o = source.get_screen_space_center() if source else None
        r = cw(
            **k,
            scale=c.UIS()+ps,
            transition='in_scale',
            color=color,
            parent=gsw('overlay_stack'),
            scale_origin_stack_offset=o
        )
        cw(r,on_outside_click_call=Call(c.swish,t=r))
        return r
    
    swish = lambda c=0,t=0: (gs('swish').play(),cw(t,transition='out_scale') if t else t)
    err = lambda t: (gs('block').play(),push(t,color=(1,1,0)))
    ok = lambda: (gs('dingSmallHigh').play(),push('Okay!',color=(0,1,0)))
    bye = lambda: (gs('laser').play(),push('Bye!',color=(0,1,0)))
    
    def __init__(s, source: bw = None) -> None:
        w = s.w = s.cw(
            source=source,
            size=(400,500)
        )
        
        tw(
            parent=w,
            scale=1.5,
            text='SinglMod v5.1',
            h_align='center',
            position=(200,450),
            color=(1,1,0.5))

         # اضافه کردن آمار و اطلاعات (با پینگ واقعی)
        s.stats_text = tw(
            parent=w,
            text=f"📊 آمار:\n"
                 f"• {len(var('l') or {})} ماشه فعال\n"
                 f"• وضعیت: {'فعال' if var('state') else 'غیرفعال'}\n"
                 f"• پینگ: {current_ping} ms\n"
                 f"• سرور: {server_ip}:{server_port}",
            position=(400, 270),
            scale=0.65,
            color=(0.8, 1, 0.8),
            maxwidth=160,
            h_align='left'
        )

        teck(1.0, s.update_stats)

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
        
        scroll_area = sw(
            parent=w,
            size=(380,370),
            position=(10,70),
            capture_arrows=True
        )
        
        s.button_container = cw(
            parent=scroll_area,
            size=(360,0),
            background=False
        )
        mem = globals()
        
        buttons = [
            ('Add', 'achievementStayinAlive'),
            ('AddCode', 'achievementSuperPunch'),
            ('Nuke', 'textClearButton'),
            ('AntiKickPanel', 'shield'),
            ('Tune', 'settingsIcon'),
            ('List', 'logIcon'),
            ('Blocked', 'spinner11'),
            ('Whitelisted', 'star'),
            ('BlockSettings', 'playerLineup'),
            ('Riddles', 'wizardIcon'),
            ('PartyColors', 'achievementSharingIsCaring'),
            ('SplitSettings', 'uiAtlas'),
            ('PlayerList', 'achievementFreeLoader'),
            ('EarSpeedSettings', 'advancedIcon'),
            ('Spam','cursor'),
            ('ServerInfo', 'replayIcon'),
            ('Reconnect', 'replayIcon'),
            ('ThemeSettings', 'storeIcon'),
            ('FontMaker','chTitleChar1'),
            ('PlayerInfo','discordServer'),
            ('ChatLog','rightButton'),
            ('PerformancePanel', 'tv'),
            ('BackupRestore', 'upButton'),
            ('SecretMessageSender', 'lock'),
            ('SecretMessageReceiver', 'achievementFootballShutout'),
            ('SecretMessageHistory', 'file'),
            ('ErrorLog', 'cuteSpaz')
            ]
        s.buttons = []
        for i, (label, texture_name) in enumerate(buttons):
            b = s.bw(
                label=label,
                parent=s.button_container,
                size=(350,40),
                position=(5,40*(len(buttons)-i-1)+10),
                icon=gt(texture_name) if gt(texture_name) else None,
                iconscale=0.9,
                text_scale=0.8
                )
            bw(b,on_activate_call=Call(mem[label],b))
            s.buttons.append(b)
        
        button_height = len(buttons)*40
        cw(s.button_container,size=(360,button_height))
        
        s.b = bw(
            parent=w,
            size=(80,35),
            position=(160,25),
            enable_sound=False,
            button_type='square',
            on_activate_call=s.but
        )
        s.but(1)
        s.swish()
        
    def update_stats(s):
        """بروزرسانی آمار شامل پینگ واقعی"""
        if hasattr(s, 'stats_text') and s.stats_text.exists():
            conn_info = get_connection_info()
            server_status = f"{server_ip}:{server_port}" if server_ip != "127.0.0.1" else "محلی"
            
            tw(s.stats_text, 
               text=f"📊 آمار:\n"
                    f"• {len(var('l') or {})} ماشه فعال\n"
                    f"• وضعیت: {'فعال' if var('state') else 'غیرفعال'}\n"
                    f"• پینگ: {current_ping} ms\n"
                    f"• سرور: {server_status}")
        teck(1.0, s.update_stats)
    
    def but(s,dry=0):
        v = var('state')
        if not dry:
            v = [1,0][v]
            var('state',v)
            gs('deek').play()
            
            if v:
                message = "SinglMod روشن شد.(.:"
            else:
                message = "SinglMod خاموش شد.).:"
            send_in_char_chunks(message + SinglMod.B)
            
        bw(
            s.b,
            label=['OFF','ON'][v],
            color=[(0.35,0,0),(0,0.45,0)][v],
            textcolor=[(0.5,0,0),(0,0.6,0)][v]
        )

pr = 'ar3_'
def var(s,v=None):
    c = APP.config
    s = pr+s
    if v is None: return c.get(s,v)
    c[s] = v
    c.commit()
def reset_conf(): 
    cfg = APP.config
    for c in list(cfg.keys()):
        if c.startswith(pr):
            cfg.pop(c)
    cfg.commit()

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

# راه‌اندازی اولیه
setup_connection_overrides()

if var('enable_splitting') is None:
    var('enable_splitting', True)

if var('max_chars') is None:
    var('max_chars', 200)

if var('split_delay') is None:
    var('split_delay', 0.7)

if var('code_commands') is None:
    var('code_commands', {})

if var('truth_players') is None:
    var('truth_players', [])

if var('block_all_mode') is None:
    var('block_all_mode', False)

if var('response_index') is None:
    var('response_index', {})

if var('ear_processing_speed') is None:
    var('ear_processing_speed', 0.01)

if var('theme') is None:
    var('theme', 'classic')

if var('custom_panel_color') is None:
    var('custom_panel_color', (0.18,0.18,0.18))

if var('custom_button_color') is None:
    var('custom_button_color', (0.18,0.18,0.18))

if var('swear_words') is None:
    var('swear_words', [])

if var('swear_mode') is None:
    var('swear_mode', True)

if var('performance_mode') is None:
    var('performance_mode', 'normal')

for i in range(4): 
    j = f'tune{i}'
    v = var(j)
    if v is None: 
        var(j,i<3)

if var('state') is None:
    var('state',1)

if var('time') is None:
    var('time','0.5')

if var('l') is None:
    var('l',{})

if var('lc') is None:
    var('lc',{})

if var('ignore_accounts') is None:
    var('ignore_accounts',[])

if var('party_mode') is None:
    var('party_mode', False)

if var('party_speed') is None:
    var('party_speed', 1.0)

if var('whitelist_accounts') is None:
    var('whitelist_accounts', [])

if var('spam_threshold') is None:
    var('spam_threshold', 10)

if var('spam_time_window') is None:
    var('spam_time_window', 15)

if var('riddle_mode') is None:
    var('riddle_mode', False)

if var('current_riddle_index') is None:
    var('current_riddle_index', 0)

if var('party_colors_enabled') is None:
    var('party_colors_enabled', [True] * len(PARTY_COLORS))

if var('code_mode') is None:
    var('code_mode', True)

if var('truth_game_active') is None:
    var('truth_game_active', False)

if var('auto_response_enabled') is None:
    var('auto_response_enabled', True)

if var('combined_response') is None:
    var('combined_response', True)

if var('anti_kick_enabled') is None:
    var('anti_kick_enabled', True)

if var('anti_kick_interval') is None:
    var('anti_kick_interval', 30)

if var('anti_kick_threshold') is None:
    var('anti_kick_threshold', 10)
