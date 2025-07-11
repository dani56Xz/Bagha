 import telebot, json, os, time, datetime
from telebot import types

bot = telebot.TeleBot('7459857250:AAHpb_NliuOiM7-cTmFSrospKdoKMnAFiew')
admin_id = 5542927340
channel = 'bagha_game'
tron_address = 'TJ4xrwKJzKjk6FgKfuuqwah3Az5Ur22kJb'

def load():
    return json.load(open('users.json', 'r')) if os.path.exists('users.json') else {}

def save(data):
    json.dump(data, open('users.json', 'w'))

questions = [
    {"q": "در یک شب تاریک در جنگل گم شده‌ای. صدای زوزه گرگ‌ها میاد. چکار می‌کنی؟", 
     "o": ["آتش روشن می‌کنم", "پنهان می‌شم", "به راهم ادامه میدم", "منو 🔙"], 
     "a": "آتش روشن می‌کنم", 
     "d": "گرگ‌ها از آتش می‌ترسند!"},
     
    {"q": "یه کلبه قدیمی می‌بینی. داخلش یه چراغ نفتی روشنه. وارد میشی؟", 
     "o": ["بله، شاید کسی اونجاست", "نه، خطرناکه", "اول محیط رو بررسی می‌کنم", "منو 🔙"], 
     "a": "اول محیط رو بررسی می‌کنم", 
     "d": "داخل کلبه دام بود!"},
     
    {"q": "توی کلبه یه نقشه قدیمی پیدا می‌کنی که مسیر گنج رو نشون میده. دنبالش میری؟", 
     "o": ["آره، بلافاصله", "نه، احتمالا دامه", "اول تحقیق می‌کنم", "منو 🔙"], 
     "a": "اول تحقیق می‌کنم", 
     "d": "نقشه تقلبی بود!"},
     
    {"q": "سر راهت یه رودخانه خروشان میبینی. چطور ازش عبور می‌کنی؟", 
     "o": ["شنا می‌کنم", "پل چوبی میسازم", "دنبال نقطه امن میگردم", "منو 🔙"], 
     "a": "دنبال نقطه امن میگردم", 
     "d": "جریان آب تو رو با خودش برد!"},
     
    {"q": "یه غریبه بهت پیشنهاد کمک میده. چکار می‌کنی؟", 
     "o": ["پذیرش می‌کنم", "رد می‌کنم", "اول هویتش رو میپرسم", "منو 🔙"], 
     "a": "اول هویتش رو میپرسم", 
     "d": "غریبه دزد بود!"},
     
    {"q": "تو مسیر یه مار سمی میبینی. چطور از کنارش رد میشی؟", 
     "o": ["فرار می‌کنم", "آروم دور میشم", "با چوب میزنمش", "منو 🔙"], 
     "a": "آروم دور میشم", 
     "d": "مار بهت حمله کرد!"},
     
    {"q": "یه صندوقچه طلایی تو آبشار پیدا می‌کنی. چکار می‌کنی؟", 
     "o": ["بازش می‌کنم", "ولش می‌کنم", "اول بررسی می‌کنم", "منو 🔙"], 
     "a": "اول بررسی می‌کنم", 
     "d": "صندوقچه تله بود!"},
     
    {"q": "یه درخت عجیب با میوه‌های نورانی میبینی. میچینی؟", 
     "o": ["آره، شاید خاص باشه", "نه، خطرناکه", "اول تست می‌کنم", "منو 🔙"], 
     "a": "اول تست می‌کنم", 
     "d": "میوه سمی بود!"},
     
    {"q": "تو تاریکی شب چراغ قوه‌ات تموم میشه. چکار می‌کنی؟", 
     "o": ["همونجا میمونم", "در تاریکی راه میرم", "آتش روشن می‌کنم", "منو 🔙"], 
     "a": "آتش روشن می‌کنم", 
     "d": "توی تاریکی گم شدی!"},
     
    {"q": "یه معبد قدیمی پیدا می‌کنی. داخلش سه در هست. کدوم رو انتخاب می‌کنی؟", 
     "o": ["در سمت چپ", "در سمت راست", "در وسط", "منو 🔙"], 
     "a": "در وسط", 
     "d": "درها تله بودند!"},
     
    {"q": "توی معبد یه سری نوشته رمزآلود روی دیواره. چکار می‌کنی؟", 
     "o": ["نادیده میگیرم", "سعی می‌کنم رمزگشایی کنم", "عکس میگیرم", "منو 🔙"], 
     "a": "عکس میگیرم", 
     "d": "نوشته‌ها طلسم بودند!"},
     
    {"q": "یه زخمی تو راه میبینی. چکار می‌کنی؟", 
     "o": ["کمکش می‌کنم", "نادیده میگیرم", "اول وضعیت رو بررسی می‌کنم", "منو 🔙"], 
     "a": "اول وضعیت رو بررسی می‌کنم", 
     "d": "دشمن بود!"},
     
    {"q": "یه پل قدیمی و پوسیده میبینی. چطور ازش رد میشی؟", 
     "o": ["با سرعت میدوم", "آروم رد میشم", "راه دیگه‌ای پیدا می‌کنم", "منو 🔙"], 
     "a": "راه دیگه‌ای پیدا می‌کنم", 
     "d": "پل فرو ریخت!"},
     
    {"q": "یه غار تاریک میبینی. داخلش میری؟", 
     "o": ["آره، شاید گنج باشه", "نه، خطرناکه", "اول روشنایی فراهم می‌کنم", "منو 🔙"], 
     "a": "اول روشنایی فراهم می‌کنم", 
     "d": "توی تاریکی گم شدی!"},
     
    {"q": "توی غار یه خفاش حمله می‌کنه. چکار می‌کنی؟", 
     "o": ["فرار می‌کنم", "میجنگم", "آروم میمونم", "منو 🔙"], 
     "a": "آروم میمونم", 
     "d": "خفاش‌ها بیشتر شدند!"},
     
    {"q": "یه گنج واقعی پیدا می‌کنی. چکار می‌کنی؟", 
     "o": ["برمیدارمش", "ولش می‌کنم", "اول بررسی می‌کنم", "منو 🔙"], 
     "a": "اول بررسی می‌کنم", 
     "d": "گنج طلسم شده بود!"},{"q": "یه آینه جادویی میبینی که آینده رو نشون میده. نگاه می‌کنی؟", 
     "o": ["آره", "نه", "اول فکر می‌کنم", "منو 🔙"], 
     "a": "اول فکر می‌کنم", 
     "d": "آینه روح تو رو دزدید!"},
     
    {"q": "یه چشمه آب حیات پیدا می‌کنی. ازش میخوری؟", 
     "o": ["آره", "نه", "اول تست می‌کنم", "منو 🔙"], 
     "a": "اول تست می‌کنم", 
     "d": "آب سمی بود!"},
     
    {"q": "یه هیولا نگهبان گنج رو میبینی. چکار می‌کنی؟", 
     "o": ["میجنگم", "فرار می‌کنم", "حیله می‌زنم", "منو 🔙"], 
     "a": "حیله می‌زنم", 
     "d": "هیولا تو رو خورد!"},
     
    {"q": "بالاخره به گنج رسیدی. چکار می‌کنی؟", 
     "o": ["برمیدارمش", "ولش می‌کنم", "بخشی رو برمیدارم", "منو 🔙"], 
     "a": "بخشی رو برمیدارم", 
     "d": "طمع کارت کرد!"}
]

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
    link = f"https://t.me/{channel}"
    btn = types.InlineKeyboardMarkup()
    btn.add(types.InlineKeyboardButton("عضویت در کانال 📢", url=link))
    btn.add(types.InlineKeyboardButton("عضو شدم ✅", callback_data="check"))
    bot.send_message(msg.chat.id, "برای ادامه، عضو کانال شو:", reply_markup=btn)

@bot.callback_query_handler(func=lambda c: True)
def callback(c):
    uid = str(c.from_user.id)
    data = load()

    if c.data == "check":
        status = bot.get_chat_member(f"@{channel}", c.from_user.id).status
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
        admin_action = c.data.split('_')[1]
        user_id = c.data.split('_')[2]
        
        if str(c.from_user.id) != str(admin_id):
            bot.answer_callback_query(c.id, "شما ادمین نیستید!", show_alert=True)
            return
            
        if admin_action == 'approve':
            data[user_id]['coins'] += 100
            bot.send_message(user_id, "✅ پرداخت شما تایید شد! 100 سکه به حساب شما اضافه شد.")
            bot.edit_message_reply_markup(c.message.chat.id, c.message.message_id, reply_markup=None)
            bot.answer_callback_query(c.id, "تایید شد!")
        elif admin_action == 'reject':
            bot.send_message(user_id, "❌ پرداخت شما رد شد!")
            bot.edit_message_reply_markup(c.message.chat.id, c.message.message_id, reply_markup=None)
            bot.answer_callback_query(c.id, "رد شد!")
        
        save(data)

def ask_name(msg):
    bot.send_message(msg.chat.id, "👤 حالا اسمتو بفرست:")
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
    bot.send_message(chat_id, f"🧩 مرحله {step + 1}:\n{q['q']}", reply_markup=kb)@bot.message_handler(content_types=["text"])
def handle_text(m):
    data = load()
    uid = str(m.from_user.id)
    if uid not in data: return
    u = data[uid]

    if u.get("waiting_receipt"):
        if m.text == "منو 🔙":
            data[uid]["waiting_receipt"] = False
            save(data)
            return main_menu(m.chat.id)
            
        if m.text in ["🛒 فروشگاه", "🎮 شروع بازی", "📊 پروفایل", "🏆 برترین‌ها", "🎁 پاداش روزانه"]:
            return handle_menu(m)
        
        bot.send_message(m.chat.id, "✅ رسیدت ارسال شد. منتظر تایید باش.")
        data[uid]["waiting_receipt"] = False
        save(data)
        
        txt = f"📥 رسید جدید\nنام: {u['name']}\nID: {uid}\n📝 متن: {m.text}"
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton("✅ تایید", callback_data=f"admin_approve_{uid}"),
            types.InlineKeyboardButton("❌ رد", callback_data=f"admin_reject_{uid}")
        )
        bot.send_message(admin_id, txt, reply_markup=markup)
        return
    
    handle_menu(m)

def handle_menu(m):
    data = load()
    uid = str(m.from_user.id)
    if uid not in data: return
    u = data[uid]

    if m.text == "🎮 شروع بازی":
        data[uid]["in_game"] = True
        save(data)
        
        if u["life"] <= 0:
            bot.send_message(m.chat.id, "❤️ تموم شده! لطفاً از فروشگاه جان بخر.")
            return
        
        if u["step"] >= len(questions):
            u["step"] = 0
            save(data)
            
        send_question(m.chat.id, u["step"])
        return

    if m.text == "منو 🔙":
        data[uid]["in_game"] = False
        save(data)
        return main_menu(m.chat.id)

    current_step = u["step"]
    if u["in_game"] and current_step < len(questions) and m.text in questions[current_step]["o"]:
        if m.text == "منو 🔙":
            data[uid]["in_game"] = False
            save(data)
            return main_menu(m.chat.id)
            
        q = questions[current_step]
        if m.text == q["a"]:
            u["score"] += 1
            u["coins"] += 5
            bot.send_message(m.chat.id, "✅ درست بود! رفتی مرحله بعد.")
        else:
            u["life"] -= 1
            bot.send_message(m.chat.id, f"❌ اشتباه بود: {q['d']}")
        
        u["step"] += 1
        save(data)
        
        if u["life"] <= 0:
            bot.send_message(m.chat.id, "❤️ جان‌هایت تمام شد! از فروشگاه می‌توانی جان بخری.")
            data[uid]["in_game"] = False
            save(data)
            return
            
        if u["step"] >= len(questions):
            u["step"] = 0
            save(data)
            bot.send_message(m.chat.id, "🔥 همه مراحل رو تموم کردی! حالا از اول شروع می‌کنیم.")
            
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
            bot.send_message(m.chat.id, "⛔ امروز پاداش گرفتی. فردا بیا!")
        else:
            u["coins"] += 10
            u["last_daily"] = now
            save(data)
            bot.send_message(m.chat.id, "🎉 پاداش روزانه دریافت شد! ۱۰ سکه به حسابت اضافه شد.")
    elif m.text == "🛒 فروشگاه":
        data[uid]["in_game"] = False
        save(data)
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🩸 خرید جان (۱۰۰ سکه)", callback_data="buy_life"))
        kb.add(types.InlineKeyboardButton("💳 پرداخت ترون", url="https://tronscan.org"))
        bot.send_message(m.chat.id, "🛍 فروشگاه:", reply_markup=kb)

@bot.message_handler(content_types=["photo"])
def handle_photo(m):
    data = load()
    uid = str(m.from_user.id)
    if uid not in data: return
    u = data[uid]if u.get("waiting_receipt"):
        bot.send_message(m.chat.id, "✅ رسیدت ارسال شد. منتظر تایید باش.")
        data[uid]["waiting_receipt"] = False
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
