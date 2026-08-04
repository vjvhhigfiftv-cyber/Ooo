#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بوت الأرقام الوهمية - Virtual Numbers Bot
OnlineSim.io + أرقام مخصصة - 151,000 رقم
"""

import os, sys, json, random, threading, time, logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Dict, List

import telebot
from telebot import types
import requests

# ======================== logging ========================
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# ======================== أعلام الدول ========================
FLAGS = {
    "af":"🇦🇫","al":"🇦🇱","dz":"🇩🇿","ar":"🇦🇷","am":"🇦🇲","au":"🇦🇺","at":"🇦🇹","az":"🇦🇿",
    "bh":"🇧🇭","bd":"🇧🇩","by":"🇧🇾","be":"🇧🇪","bo":"🇧🇴","ba":"🇧🇦","br":"🇧🇷","bg":"🇧🇬",
    "kh":"🇰🇭","cm":"🇨🇲","ca":"🇨🇦","cl":"🇨🇱","cn":"🇨🇳","co":"🇨🇴","cr":"🇨🇷","hr":"🇭🇷",
    "cu":"🇨🇺","cy":"🇨🇾","cz":"🇨🇿","cd":"🇨🇩","dk":"🇩🇰","do":"🇩🇴","ec":"🇪🇨","eg":"🇪🇬",
    "sv":"🇸🇻","ee":"🇪🇪","et":"🇪🇹","fi":"🇫🇮","fr":"🇫🇷","ge":"🇬🇪","de":"🇩🇪","gh":"🇬🇭",
    "gr":"🇬🇷","gt":"🇬🇹","hn":"🇭🇳","hu":"🇭🇺","is":"🇮🇸","in":"🇮🇳","id":"🇮🇩","ir":"🇮🇷",
    "iq":"🇮🇶","ie":"🇮🇪","il":"🇮🇱","it":"🇮🇹","jm":"🇯🇲","jp":"🇯🇵","jo":"🇯🇴","kz":"🇰🇿",
    "ke":"🇰🇪","kw":"🇰🇼","kg":"🇰🇬","la":"🇱🇦","lv":"🇱🇻","lb":"🇱🇧","ly":"🇱🇾","lt":"🇱🇹",
    "lu":"🇱🇺","my":"🇲🇾","mx":"🇲🇽","md":"🇲🇩","mn":"🇲🇳","me":"🇲🇪","ma":"🇲🇦","mm":"🇲🇲",
    "nl":"🇳🇱","nz":"🇳🇿","ng":"🇳🇬","kp":"🇰🇵","no":"🇳🇴","om":"🇴🇲","pk":"🇵🇰","ps":"🇵🇸",
    "pa":"🇵🇦","py":"🇵🇾","pe":"🇵🇪","ph":"🇵🇭","pl":"🇵🇱","pt":"🇵🇹","qa":"🇶🇦","ro":"🇷🇴",
    "ru":"🇷🇺","sa":"🇸🇦","rs":"🇷🇸","sg":"🇸🇬","sk":"🇸🇰","si":"🇸🇮","za":"🇿🇦","kr":"🇰🇷",
    "es":"🇪🇸","lk":"🇱🇰","sd":"🇸🇩","se":"🇸🇪","ch":"🇨🇭","sy":"🇸🇾","tw":"🇹🇼","tj":"🇹🇯",
    "tz":"🇹🇿","th":"🇹🇭","tn":"🇹🇳","tr":"🇹🇷","tm":"🇹🇲","ug":"🇺🇬","ua":"🇺🇦","ae":"🇦🇪",
    "gb":"🇬🇧","us":"🇺🇸","uy":"🇺🇾","uz":"🇺🇿","ve":"🇻🇪","vn":"🇻🇳","ye":"🇾🇪","zw":"🇿🇼",
    "hk":"🇭🇰","mo":"🇲🇴","pr":"🇵🇷","xk":"🇽🇰",
}

# كود الدولة -> علم
CC_TO_FLAG = {
    1: "🇺🇸", 7: "🇷🇺", 20: "🇪🇬", 27: "🇿🇦", 30: "🇬🇷", 31: "🇳🇱", 32: "🇧🇪",
    33: "🇫🇷", 34: "🇪🇸", 36: "🇭🇺", 39: "🇮🇹", 40: "🇷🇴", 41: "🇨🇭", 43: "🇦🇹",
    44: "🇬🇧", 45: "🇩🇰", 46: "🇸🇪", 47: "🇳🇴", 48: "🇵🇱", 49: "🇩🇪", 51: "🇵🇪",
    52: "🇲🇽", 53: "🇨🇺", 54: "🇦🇷", 55: "🇧🇷", 56: "🇨🇱", 57: "🇨🇴", 58: "🇻🇪",
    60: "🇲🇾", 61: "🇦🇺", 62: "🇮🇩", 63: "🇵🇭", 64: "🇳🇿", 65: "🇸🇬", 66: "🇹🇭",
    81: "🇯🇵", 82: "🇰🇷", 84: "🇻🇳", 86: "🇨🇳", 90: "🇹🇷", 91: "🇮🇳", 92: "🇵🇰",
    93: "🇦🇫", 94: "🇱🇰", 95: "🇲🇲", 98: "🇮🇷", 212: "🇲🇦", 213: "🇩🇿", 216: "🇹🇳",
    218: "🇱🇾", 220: "🇬🇲", 221: "🇸🇳", 222: "🇲🇷", 223: "🇲🇱", 224: "🇬🇳",
    225: "🇨🇮", 226: "🇧🇫", 227: "🇳🇪", 228: "🇹🇬", 229: "🇧🇯", 230: "🇲🇺",
    231: "🇱🇷", 232: "🇸🇱", 233: "🇬🇭", 234: "🇳🇬", 235: "🇹🇩", 236: "🇨🇫",
    237: "🇨🇲", 238: "🇨🇻", 239: "🇸🇹", 240: "🇬🇶", 241: "🇬🇦", 242: "🇨🇬",
    243: "🇨🇩", 244: "🇦🇴", 245: "🇬🇼", 246: "🇩🇬", 247: "🇦🇨", 248: "🇸🇨",
    249: "🇸🇩", 250: "🇷🇼", 251: "🇪🇹", 252: "🇸🇴", 253: "🇩🇯", 254: "🇰🇪",
    255: "🇹🇿", 256: "🇺🇬", 257: "🇧🇮", 258: "🇲🇿", 260: "🇿🇲", 261: "🇲🇬",
    262: "🇷🇪", 263: "🇿🇼", 264: "🇳🇦", 265: "🇲🇼", 266: "🇱🇸", 267: "🇧🇼",
    268: "🇸🇿", 269: "🇰🇲", 290: "🇸🇭", 291: "🇪🇷", 297: "🇦🇼", 298: "🇫🇴",
    299: "🇬🇱", 350: "🇬🇮", 351: "🇵🇹", 352: "🇱🇺", 353: "🇮🇪", 354: "🇮🇸",
    355: "🇦🇱", 356: "🇲🇹", 357: "🇨🇾", 358: "🇫🇮", 359: "🇧🇬", 370: "🇱🇹",
    371: "🇱🇻", 372: "🇪🇪", 373: "🇲🇩", 374: "🇦🇲", 375: "🇧🇾", 376: "🇦🇩",
    377: "🇲🇨", 378: "🇸🇲", 379: "🇻🇦", 380: "🇺🇦", 381: "🇷🇸", 382: "🇲🇪",
    383: "🇽🇰", 385: "🇭🇷", 386: "🇸🇮", 387: "🇧🇦", 389: "🇲🇰", 420: "🇨🇿",
    421: "🇸🇰", 423: "🇱🇮", 500: "🇫🇰", 501: "🇧🇿", 502: "🇬🇹", 503: "🇸🇻",
    504: "🇭🇳", 505: "🇳🇮", 506: "🇨🇷", 507: "🇵🇦", 508: "🇵🇲", 509: "🇭🇹",
    590: "🇬🇵", 591: "🇧🇴", 592: "🇬🇾", 593: "🇪🇨", 594: "🇬🇫", 595: "🇵🇾",
    596: "🇲🇶", 597: "🇸🇷", 598: "🇺🇾", 599: "🇧🇶", 670: "🇹🇱", 672: "🇦🇶",
    673: "🇧🇳", 674: "🇳🇷", 675: "🇵🇬", 676: "🇹🇴", 677: "🇸🇧", 678: "🇻🇺",
    679: "🇫🇯", 680: "🇵🇼", 681: "🇼🇫", 682: "🇨🇰", 683: "🇳🇺", 685: "🇼🇸",
    686: "🇰🇮", 687: "🇳🇨", 688: "🇹🇻", 689: "🇵🇫", 690: "🇹🇰", 691: "🇫🇲",
    692: "🇲🇭", 850: "🇰🇵", 852: "🇭🇰", 853: "🇲🇴", 855: "🇰🇭", 856: "🇱🇦",
    880: "🇧🇩", 886: "🇹🇼", 960: "🇲🇻", 961: "🇱🇧", 962: "🇯🇴", 963: "🇸🇾",
    964: "🇮🇶", 965: "🇰🇼", 966: "🇸🇦", 967: "🇾🇪", 968: "🇴🇲", 970: "🇵🇸",
    971: "🇦🇪", 972: "🇮🇱", 973: "🇧🇭", 974: "🇶🇦", 975: "🇧🇹", 976: "🇲🇳",
    977: "🇳🇵", 992: "🇹🇯", 993: "🇹🇲", 994: "🇦🇿", 995: "🇬🇪", 996: "🇰🇬",
    998: "🇺🇿",
}

# ======================== تحليل الأرقام ========================
def parse_num(num_str: str) -> dict:
    """تحليل رقم الهاتف بدون مكتبات خارجية"""
    n = num_str.lstrip("+")
    info = {"full": n, "cc": "", "flag": "🌍", "national": n}

    # نبحث عن كود الدولة
    for length in [3, 2, 1]:
        prefix = n[:length]
        cc = int(prefix) if prefix.isdigit() else 0
        if cc in CC_TO_FLAG:
            info["cc"] = str(cc)
            info["flag"] = CC_TO_FLAG[cc]
            info["national"] = n[length:]
            return info
    return info

# ======================== الإعدادات ========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# التوكن من ملف أو من متغير البيئة
def get_token():
    # أولاً: متغير البيئة
    tok = os.environ.get("BOT_TOKEN", "")
    if tok:
        return tok
    # ثانياً: ملف token.txt
    for p in [os.path.join(BASE_DIR, "token.txt"), os.path.join(BASE_DIR, "src", "token.txt")]:
        if os.path.exists(p):
            with open(p) as f:
                return f.read().strip()
    raise SystemExit("❌ التوكن غير موجود! ضع BOT_TOKEN كمتغير بيئة أو أنشئ token.txt")

TOKEN = get_token()
bot = telebot.TeleBot(TOKEN)
user_state: Dict[int, str] = {}

# OnlineSim API
API = "https://onlinesim.io/api/v1/free_numbers_content"

# الملفات المخصصة
CUSTOM = {
    "ألمانيا 🇩🇪": "5_6309591581011747290.txt",
    "الجزائر 🇩🇿": "5_6309591581011747291.txt",
    "الكونغو 🇨🇩": "5_6309591581011747292.txt",
    "قطر واتساب 🇶🇦": "Qatar WhatsApp.txt",
}

# ======================== تحميل الأرقام ========================
def load_nums(fname: str) -> List[str]:
    for d in [os.path.join(BASE_DIR, "numbers"), os.path.join(BASE_DIR, "src")]:
        fp = os.path.join(d, fname)
        if os.path.exists(fp):
            with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                return [l.strip() for l in f if l.strip() and l.strip().isdigit()]
    return []

# ======================== OnlineSim ========================
def api_countries():
    try:
        r = requests.get(f"{API}/countries", timeout=10).json()
        if r.get("response") == "1":
            return [c for c in r.get("counties", []) if c.get("online")]
    except Exception as e:
        log.error(f"OnlineSim countries: {e}")
    return []

def api_numbers(country):
    try:
        r = requests.get(f"{API}/countries/{country}?lang=en", timeout=10).json()
        if r.get("response") == "1":
            return [{"time": n["data_humans"], "num": n["full_number"]} for n in r.get("numbers", [])]
    except:
        pass
    return []

def api_inbox(country, number):
    try:
        r = requests.get(f"{API}/countries/{country}/{number}?lang=en", timeout=10).json()
        if r.get("response") == "1" and r.get("online"):
            return [{"time": m["data_humans"], "text": m["text"]} for m in r.get("messages", {}).get("data", [])]
    except:
        pass
    return []

# ======================== لوحة المفاتيح ========================
def main_kb():
    m = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.add("📱 رقم وهمي جديد", "🔄 تجديد الرقم")
    m.add("🇶🇦 واتساب قطر", "📂 أرقام مخصصة")
    m.add("📥 صندوق الرسائل", "ℹ️ مساعدة")
    return m

def custom_kb():
    m = types.InlineKeyboardMarkup(row_width=1)
    for name in CUSTOM:
        m.add(types.InlineKeyboardButton(name, callback_data=f"c_{name}"))
    m.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back"))
    return m

# ======================== الأوامر ========================
@bot.message_handler(commands=["start", "restart"])
def cmd_start(m):
    name = m.from_user.first_name or m.from_user.username or "مستخدم"
    text = f"""
╭━━━━━━━━━━━━━━━━━━╮
║  📱 بوت الأرقـام الـوهـمـيـة  ║
╰━━━━━━━━━━━━━━━━━━╯

👋 أهلاً {name}!

✅ واتساب | تيليجرام | فيسبوك | انستغرام | تيك توك
📌 أرقام حية تستقبل أكواد SMS
📌 من OnlineSim + 151,000 رقم مخصص

استخدم الأزرار 👇
"""
    bot.send_message(m.chat.id, text, reply_markup=main_kb())

@bot.message_handler(commands=["help"])
def cmd_help(m):
    bot.send_message(m.chat.id, """
📚 طريقة الاستخدام:
1️⃣ رقم وهمي جديد → رقم نشط
2️⃣ استخدمه في التطبيق
3️⃣ صندوق الرسائل → كود التفعيل
4️⃣ تجديد → رقم جديد

📌 واتساب قطر → أرقام قطرية خاصة
📌 أرقام مخصصة → 151,000 رقم
""", reply_markup=main_kb())

@bot.message_handler(commands=["number"])
def cmd_num(m):
    get_number(m)

# ======================== أزرار ========================
@bot.message_handler(func=lambda m: m.text == "📱 رقم وهمي جديد")
def btn_new(m):
    get_number(m)

@bot.message_handler(func=lambda m: m.text == "🔄 تجديد الرقم")
def btn_renew(m):
    get_number(m)

@bot.message_handler(func=lambda m: m.text == "📂 أرقام مخصصة")
def btn_custom(m):
    bot.send_message(m.chat.id, "📂 اختر الدولة:", reply_markup=custom_kb())

@bot.message_handler(func=lambda m: m.text == "🇶🇦 واتساب قطر")
def btn_qatar(m):
    nums = load_nums("Qatar WhatsApp.txt")
    if not nums:
        bot.send_message(m.chat.id, "❌ لا توجد أرقام")
        return
    num = random.choice(nums)
    info = parse_num(num)
    text = f"📱 **رقم واتساب قطري**\n\n{info['flag']} +{info['full']}"
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("🔄 رقم آخر", callback_data="c_قطر واتساب 🇶🇦"))
    bot.send_message(m.chat.id, text, parse_mode="Markdown", reply_markup=mk)

@bot.message_handler(func=lambda m: m.text == "📥 صندوق الرسائل")
def btn_inbox(m):
    user_state[m.chat.id] = "inbox"
    bot.send_message(m.chat.id, "📥 أرسل الرقم كاملاً:\nمثال: `4915510287697`", parse_mode="Markdown", reply_markup=types.ForceReply(selective=True))

@bot.message_handler(func=lambda m: m.text == "ℹ️ مساعدة")
def btn_help(m):
    cmd_help(m)

# ======================== رقم جديد ========================
def get_number(m):
    p = bot.send_message(m.chat.id, "🔍 جاري البحث عن رقم نشط...")
    cid, mid = m.chat.id, p.message_id

    countries = api_countries()
    if not countries:
        bot.edit_message_text("⚠️ OnlineSim غير متاح\n🔍 الأرقام المخصصة...", cid, mid)
        custom_num(m, cid, mid)
        return

    random.shuffle(countries)
    bot.edit_message_text(f"🔍 {len(countries)} دولة\n🔄 اختبار الأرقام...", cid, mid)

    for c in countries:
        nums = api_numbers(c["name"])
        cname = c["name"].replace("_", " ").title()
        for nd in nums:
            n = nd["num"]
            info = parse_num(n)
            bot.edit_message_text(f"🔍 {cname} ({info['national']})", cid, mid)
            if api_inbox(c["name"], n) is not False:
                text = f"""
✅ **رقم نشط!**

{info['flag']} {cname}
📱 **+{info['full']}**
🕐 {nd.get('time', '')}

⚠️ استخدمه فوراً!
"""
                mk = types.InlineKeyboardMarkup(row_width=2)
                mk.add(
                    types.InlineKeyboardButton("📥 الصندوق", callback_data=f"ib_{c['name']}_{n}"),
                    types.InlineKeyboardButton("🔄 تجديد", callback_data="renew"),
                )
                mk.add(
                    types.InlineKeyboardButton("👤 بروفايل", url=f"tg://resolve?phone=+{n}"),
                )
                bot.edit_message_text(text, cid, mid, parse_mode="Markdown", reply_markup=mk)
                return

    bot.edit_message_text("⚠️ لا أرقام نشطة\n🔍 المخصصة...", cid, mid)
    custom_num(m, cid, mid)

def custom_num(m, cid=None, mid=None):
    all_n = []
    for name, fn in CUSTOM.items():
        if "قطر" in name:
            continue
        all_n.extend(load_nums(fn))

    if not all_n:
        bot.send_message(m.chat.id if not cid else cid, "❌ لا أرقام")
        return

    n = random.choice(all_n)
    info = parse_num(n)
    text = f"📱 **رقم مخصص**\n\n{info['flag']} +{info['full']}"
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("🔄 آخر", callback_data="renew"))

    if cid and mid:
        bot.edit_message_text(text, cid, mid, parse_mode="Markdown", reply_markup=mk)
    else:
        bot.send_message(m.chat.id, text, parse_mode="Markdown", reply_markup=mk)

# ======================== Callbacks ========================
@bot.callback_query_handler(func=lambda c: c.data.startswith("ib_"))
def cb_inbox(call):
    _, country, num = call.data.split("_", 2)
    bot.answer_callback_query(call.id, "🔍 جلب الرسائل...")
    msgs = api_inbox(country, num)
    if not msgs:
        bot.send_message(call.message.chat.id, f"📭 لا رسائل لـ +{num}")
        return
    for m in msgs[:5]:
        txt = m['text'].split('received from OnlineSIM.io')[0]
        bot.send_message(call.message.chat.id, f"📩 {m['time']}\n{txt}")
    bot.send_message(call.message.chat.id, f"✅ {min(len(msgs),5)} رسالة", reply_markup=main_kb())

@bot.callback_query_handler(func=lambda c: c.data == "renew")
def cb_renew(call):
    bot.answer_callback_query(call.id, "🔄")
    class FM:
        def __init__(self, cid, mid):
            self.chat = type('o', (object,), {'id': cid})
            self.message_id = mid
    get_number(FM(call.message.chat.id, call.message.message_id))

@bot.callback_query_handler(func=lambda c: c.data.startswith("c_") and c.data != "c_back")
def cb_custom(call):
    name = call.data[2:]
    if name == "back":
        return
    fn = CUSTOM.get(name)
    if not fn:
        return
    nums = load_nums(fn)
    if not nums:
        bot.answer_callback_query(call.id, "❌")
        return
    sel = random.sample(nums, min(5, len(nums)))
    text = f"📂 **{name}**\n\n" + "\n".join(f"{i}. `+{n}`" for i, n in enumerate(sel, 1))
    text += f"\n📊 {len(nums):,} رقم"
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("🔄 غير", callback_data=f"c_{name}"))
    mk.add(types.InlineKeyboardButton("🔙", callback_data="c_back"))
    bot.answer_callback_query(call.id, f"✅ {name}")
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=mk)
    except:
        pass

@bot.callback_query_handler(func=lambda c: c.data == "c_back")
def cb_cback(call):
    bot.answer_callback_query(call.id, "🔙")
    bot.edit_message_text("📂 اختر الدولة:", call.message.chat.id, call.message.message_id, reply_markup=custom_kb())

@bot.callback_query_handler(func=lambda c: c.data == "back")
def cb_back(call):
    bot.answer_callback_query(call.id, "🔙")
    bot.edit_message_text("القائمة الرئيسية 👇", call.message.chat.id, call.message.message_id)

# ======================== صندوق يدوي ========================
@bot.message_handler(func=lambda m: user_state.get(m.chat.id) == "inbox")
def handle_inbox(m):
    user_state.pop(m.chat.id, None)
    n = m.text.strip().replace("+", "").replace(" ", "")
    if not n.isdigit():
        bot.send_message(m.chat.id, "❌ رقم غير صالح", reply_markup=main_kb())
        return
    found = False
    for c in api_countries():
        for nd in api_numbers(c["name"]):
            if nd["num"] == n:
                msgs = api_inbox(c["name"], n)
                if msgs:
                    bot.send_message(m.chat.id, f"📥 +{n}:")
                    for mg in msgs[:5]:
                        bot.send_message(m.chat.id, f"{mg['time']}\n{mg['text'].split('received from OnlineSIM.io')[0]}")
                    found = True
                break
        if found:
            break
    if not found:
        bot.send_message(m.chat.id, f"📭 لا رسائل لـ +{n}", reply_markup=main_kb())
    else:
        bot.send_message(m.chat.id, "✅", reply_markup=main_kb())

# ======================== Health Check HTTP Server ========================
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, format, *args):
        pass  # صامت

def run_health_server():
    port = int(os.environ.get("PORT", "8080"))
    try:
        srv = HTTPServer(("0.0.0.0", port), HealthHandler)
        log.info(f"🏥 Health server on port {port}")
        srv.serve_forever()
    except Exception as e:
        log.error(f"Health server error: {e}")

# ======================== التشغيل ========================
def main():
    log.info(f"🤖 البوت: @{bot.get_me().username} | ID: {bot.get_me().id}")

    # OnlineSim
    try:
        cs = api_countries()
        log.info(f"✅ OnlineSim: {len(cs)} دولة" if cs else "⚠️ OnlineSim: لا دول")
    except Exception as e:
        log.warning(f"⚠️ OnlineSim: {e}")

    # أرقام مخصصة
    total = 0
    for fn in CUSTOM.values():
        total += len(load_nums(fn))
    log.info(f"✅ أرقام مخصصة: {total:,}")

    # تشغيل health check server
    threading.Thread(target=run_health_server, daemon=True).start()

    # تشغيل البوت
    log.info("🚀 البوت يعمل...")
    
    # تنظيف أي جلسة سابقة وانتظار
    try:
        bot.remove_webhook()
        bot.stop_polling()
    except:
        pass
    time.sleep(3)
    
    while True:
        try:
            bot.polling(none_stop=True, timeout=30, long_polling_timeout=15)
        except Exception as e:
            log.error(f"⚠️ خطأ: {e}")
            try:
                bot.stop_polling()
            except:
                pass
            time.sleep(10)

if __name__ == "__main__":
    main()
