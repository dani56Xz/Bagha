import telebot, json, os, time, datetime
from telebot import types

bot = telebot.TeleBot('7459857250:AAHpb_NliuOiM7-cTmFSrospKdoKMnAFiew')
admin_id = 5542927340
channel = 'bagha_game'
tron_address = 'TJ4xrwKJzKjk6FgKfuuqwah3Az5Ur22kJb'

# سوالات بازی (لیست کامل)
questions = [
    {
        "q": "تو داخل یه جنگل تاریک گیر کردی. برای روشن کردن راهت باید چی کنی؟",
        "o": ["الف) آتش روشن کنم", "ب) فریاد بزنم", "ج) بی‌حرکت بمونم", "د) دنبال نور ماه بگردم"],
        "a": "الف) آتش روشن کنم",
        "d": "برای روشن کردن راه، بهتره آتش روشن کنی."
    },
    {
        "q": "بعد از روشن کردن آتش، ناگهان صدایی از پشت درخت‌ها میاد. چه کاری انجام میدی؟",
        "o": ["الف) فرار کنم", "ب) فریاد بزنم", "ج) آماده مبارزه شم", "د) آروم بمونم"],
        "a": "د) آروم بمونم",
        "d": "آرامش حفظ کن و موقعیت رو بررسی کن."
    },
    {
        "q": "برای پیدا کردن آب در طبیعت، بهتره کجا رو جستجو کنی؟",
        "o": ["الف) پایین دره", "ب) بالای کوه", "ج) وسط جنگل", "د) روی صخره‌ها"],
        "a": "الف) پایین دره",
        "d": "آب معمولا در پایین دره‌ها جمع میشه."
    },
    {
        "q": "اگر زخمی شدی، چه کاری باید انجام بدی؟",
        "o": ["الف) زخم رو با آب تمیز بشورم", "ب) زخم رو نادیده بگیرم", "ج) از گیاهان دارویی استفاده کنم", "د) سریع حرکت کنم"],
        "a": "ج) از گیاهان دارویی استفاده کنم",
        "d": "استفاده از گیاهان دارویی به درمان کمک می‌کنه."
    },
    {
        "q": "وقتی هوا تاریک میشه، بهترین مکان برای خوابیدن کجاست؟",
        "o": ["الف) کنار آتش", "ب) زیر درخت", "ج) کنار رودخانه", "د) وسط جنگل"],
        "a": "الف) کنار آتش",
        "d": "آتش گرما و امنیت بیشتری فراهم می‌کنه."
    }
]

def load():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

def save(data):
    with open('users.json', 'w') as f:
        json.dump(data, f)

@bot.message_handler(commands=['start'])
def start(m):
    data = load()
    uid = str(m.from_user.id)
    if uid not in data:
        data[uid] = {
            "name": "",
            "coins": 0,
            "score": 0,
            "life": 3,
            "step": 0,
            "last_daily": "",
            "waiting_receipt": False,
            "in_game": False
        }
        save(data)
    check_sub(m)

def check_sub(msg):
    try:
        status = bot.get_chat_member(f"@{channel}", msg.from_user.id).status
    except Exception:
        status = "left"
    if status in ["member", "administrator", "creator"]:
        ask_name(msg)
    else:
        link = f"https://t.me/{channel}"
        btn = types.InlineKeyboardMarkup()
        btn.add(types.InlineKeyboardButton("عضویت در کانال 📢", url=link))
        btn.add(types.InlineKeyboardButton("عضو شدم ✅", callback_data="check"))
        bot.send_message(msg.chat.id, "برای ادامه، لطفا عضو کانال شو:", reply_markup=btn)

@bot.callback_query_handler(func=lambda c: True)
def callback(c):
    uid = str(c.from_user.id)
    data = load()
    if c.data == "check":
        try:
            status = bot.get_chat_member(f"@{channel}", c.from_user.id).status
        except Exception:
            status = "left"
        if status in ["member", "administrator", "creator"]:
            ask_name(c.message)
        else:
            bot.answer_callback_query(c.id, "⛔ هنوز عضو کانال نشدی!", show_alert=True)

    elif c.data == "buy_life":
        if data[uid]["coins"] >= 100:
            data[uid]["coins"] -= 100
            data[uid]["life"] += 1
            save(data)
            bot.edit_message_text("✅ جان خریداری شد!", c.message.chat.id, c.message.message_id)
        else:
            bot.answer_callback_query(c.id, "سکه کافی نداری!", show_alert=True)

    elif c.data.startswith('admin_'):
        if str(c.from_user.id) != str(admin_id):
            bot.answer_callback_query(c.id, "شما ادمین نیستید!", show_alert=True)
            return

        parts = c.data.split('_')
        action = parts[1]
        user_id = parts[2]

        if action == 'approve':
            data[user_id]['coins'] += 100
            save(data)
            bot.send_message(user_id, "✅ پرداخت شما تایید شد! 100 سکه به حساب شما اضافه شد.")
            bot.edit_message_reply_markup(c.message.chat.id, c.message.message_id, reply_markup=None)
            bot.answer_callback_query(c.id, "تایید شد!")

        elif action == 'reject':
            bot.send_message(user_id, "❌ پرداخت شما رد شد!")
            bot.edit_message_reply_markup(c.message.chat.id, c.message.message_id, reply_markup=None)
            bot.answer_callback_query(c.id, "رد شد!")

def ask_name(msg):
    bot.send_message(msg.chat.id, "👤 لطفا اسمت رو بفرست:")
    bot.register_next_step_handler(msg, save_name)

def save_name(m):
    data = load()
    uid = str(m.from_user.id)
    data[uid]["name"] = m.text
    save(data)
    main_menu(m.chat.id)

def main_menu(cid):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🎮 شروع بازی", "🛒 فروشگاه")
    kb.add("📊 پروفایل", "🏆 برترین‌ها", "🎁 پاداش روزانه")
    bot.send_message(cid, "از منو یکی رو انتخاب کن:", reply_markup=kb)

def send_question(chat_id, step):
    data = load()
    uid = str(chat_id)
    data[uid]["in_game"] = True
    save(data)
    q = questions[step]
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for opt in q["o"]:
        kb.add(opt)
    bot.send_message(chat_id, f"🧩 مرحله {step + 1}:\n{q['q']}", reply_markup=kb)

@bot.message_handler(content_types=["text"])
def handle_text(m):
    data = load()
    uid = str(m.from_user.id)
    if uid not in data:
        return
    u = data[uid]

    if u.get("waiting_receipt"):
        if m.text == "منو 🔙":
            u["waiting_receipt"] = False
            save(data)
            return main_menu(m.chat.id)
        else:
            bot.send_message(m.chat.id, "✅ رسیدت ارسال شد. منتظر تایید باش.")
            u["waiting_receipt"] = False
            save(data)
            txt = f"📥 رسید جدید\nنام: {u['name']}\nID: {uid}\n📝 متن: {m.text}"
            markup = types.InlineKeyboardMarkup()
            markup.row(
                types.InlineKeyboardButton("✅ تایید", callback_data=f"admin_approve_{uid}"),
                types.InlineKeyboardButton("❌ رد", callback_data=f"admin_reject_{uid}")
            )
            bot.send_message(admin_id, txt, reply_markup=markup)
            return

    if m.text == "🎮 شروع بازی":
        if u["life"] <= 0:
            bot.send_message(m.chat.id, "❤️ جان‌هات تموم شده! لطفا از فروشگاه جان بخر.")
            return
        if u["step"] >= len(questions):
            u["step"] = 0
            save(data)
        send_question(m.chat.id, u["step"])
        return

    if m.text == "منو 🔙":
        u["in_game"] = False
        save(data)
        return main_menu(m.chat.id)

    if u["in_game"] and u["step"] < len(questions) and m.text in questions[u["step"]]["o"]:
        if m.text == questions[u["step"]]["a"]:
            u["score"] += 1
            u["coins"] += 5
            bot.send_message(m.chat.id, "✅ جواب درست بود! مرحله بعدی.")
        else:
            u["life"] -= 1
            bot.send_message(m.chat.id, f"❌ جواب اشتباه بود: {questions[u['step']]['d']}")
        u["step"] += 1
        save(data)

        if u["life"] <= 0:
            bot.send_message(m.chat.id, "❤️ جان‌هات تموم شد! لطفا از فروشگاه جان بخر.")
            u["in_game"] = False
            save(data)
            return

        if u["step"] >= len(questions):
            u["step"] = 0
            save(data)
            bot.send_message(m.chat.id, "🎉 تبریک! همه مراحل رو تموم کردی. دوباره شروع کن.")

        time.sleep(1)
        send_question(m.chat.id, u["step"])
        return

    elif m.text == "📊 پروفایل":
        bot.send_message(m.chat.id, f"""🧍‍♂️ نام: {u['name']}
❤️ جان: {u['life']}
💰 سکه: {u['coins']}
🏅 امتیاز: {u['score']}""")

    elif m.text == "🎁 پاداش روزانه":
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        if u.get("last_daily") == now:
            bot.send_message(m.chat.id, "⛔ امروز پاداش گرفتی، فردا بیا.")
        else:
            u["coins"] += 10
            u["last_daily"] = now
            save(data)
            bot.send_message(m.chat.id, "🎉 پاداش روزانه ۱۰ سکه به حسابت اضافه شد!")

    elif m.text == "🛒 فروشگاه":
        u["in_game"] = False
        save(data)
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🩸 خرید جان (۱۰۰ سکه)", callback_data="buy_life"))
        kb.add(types.InlineKeyboardButton("💳 پرداخت ترون", url="https://tronscan.org"))
        bot.send_message(m.chat.id, "🛍 فروشگاه:", reply_markup=kb)

@bot.message_handler(content_types=["photo"])
def handle_photo(m):
    data = load()
    uid = str(m.from_user.id)
    u = data.get(uid)
    if not u:
        return

    if u.get("waiting_receipt"):
        bot.send_message(m.chat.id, "✅ رسیدت ارسال شد. منتظر تایید باش.")
        u["waiting_receipt"] = False
        save(data)
        txt = f"📥 رسید جدید\nنام: {u['name']}\nID: {uid}"
        if m.caption:
            txt += f"\n📝 متن: {m.caption}"
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton("✅ تایید", callback_data=f"admin_approve_{uid}"),
            types.InlineKeyboardButton("❌ رد", callback_data=f"admin_reject_{uid}")
        )
        bot.send_photo(admin_id, m.photo[-1].file_id, caption=txt, reply_markup=markup)

bot.polling()
