import asyncio
import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.client.default import DefaultBotProperties


# Admin user ID
ADMIN_ID = 6520873307

# Bot və Dispatcher
bot = Bot(token="8027784707:AAEKxUr_srk_XyE71edYPf_MqzWdukvKHLE")
dp = Dispatcher()

# 📁 Baza əlaqəsi
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    full_name TEXT,
    username TEXT,
    joined_at TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS scores (
    user_id INTEGER PRIMARY KEY,
    score INTEGER
)
""")
conn.commit()

# 📋 Baş menyu
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Özün haqqında", callback_data="help1")],
    [InlineKeyboardButton(text="Mini Test", callback_data="quiz")],
    [InlineKeyboardButton(text="Sadə Sorğu", callback_data="poll")],
    [InlineKeyboardButton(text="Fayl Al", callback_data="file")],
    [InlineKeyboardButton(text="Admin Panel", callback_data="admin")]
])

# ▶ /start
@dp.message(CommandStart())
async def start_cmd(message: Message):
    user = message.from_user
    cursor.execute("INSERT OR IGNORE INTO users (id, full_name, username, joined_at) VALUES (?, ?, ?, ?)",
                   (user.id, user.full_name, user.username, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    await message.answer(f"👋 Salam, {user.full_name}!\nMəlumat almaq üçün seçim et:", reply_markup=main_menu)

# 📌 Help cavabları
@dp.callback_query(lambda c: c.data == "help1")
async def help1(callback: CallbackQuery):
    await callback.message.answer("🤖 Mən informativ və interaktiv bir botam. Əlavə məlumat üçün seçim et.")
    await callback.answer()


# ❓ Quiz sistemi
new_quiz_questions = [
    {
        "question": "Azərbaycanın ən uzun çayı hansıdır?",
        "options": ["Araz", "Kür", "Qanıx", "Tərtər"],
        "correct": 1
    },
    {
        "question": "İnsan bədənində ən böyük orqan hansıdır?",
        "options": ["Böyrək", "Qaraciyər", "Dəri", "Ağciyər"],
        "correct": 2
    },
    {
        "question": "Nizami Gəncəvi hansı əsərləri ilə məşhurdur?",
        "options": ["Divani-Hikmət", "Sədi Şirazi", "Xəmsə", "Leyli və Məcnun"],
        "correct": 2
    },
    {
        "question": "Ay Yer ətrafında bir tam dövrü təxminən neçə günə tamamlayır?",
        "options": ["30 gün", "29.5 gün", "31 gün", "28 gün"],
        "correct": 1
    },
    {
        "question": "Dünyanın ən çox danışılan dili hansıdır?",
        "options": ["İngilis dili", "Hind dili", "İspan dili", "Çin dili (Mandarin)"],
        "correct": 3
    },
    {
        "question": "Azərbaycan 1918-ci ildə müstəqil olduqda paytaxtı haraydı?",
        "options": ["Bakı", "Gəncə", "Şuşa", "Naxçıvan"],
        "correct": 1
    },
    {
        "question": "Elektron poçtun ixtiraçısı kimdir?",
        "options": ["Elon Musk", "Ray Tomlinson", "Tim Berners-Lee", "Bill Gates"],
        "correct": 1
    },
    {
        "question": "Dünyanın ən böyük okeanı hansıdır?",
        "options": ["Atlantik", "Hind", "Sakit", "Arktik"],
        "correct": 2
    },
    {
        "question": "Bakıda yerləşən məşhur alış-veriş mərkəzi hansıdır?",
        "options": ["Nərimanov Plaza", "28 Mall", "Ticarət Evi", "Flame Mall"],
        "correct": 1
    },
    {
        "question": "Hansı heyvan heç vaxt tullana bilmir?",
        "options": ["Fil", "Tısbağa", "İlan", "Kərgədan"],
        "correct": 0
    },
    {
        "question": "İnternetin əsas protokolu hansıdır?",
        "options": ["FTP", "SMTP", "HTTP", "USB"],
        "correct": 2
    },
    {
        "question": "Azərbaycanın milli valyutası nədir?",
        "options": ["Manat", "Lari", "Rubl", "Dinar"],
        "correct": 0
    },
    {
        "question": "DNT hansı məqsədlə istifadə olunur?",
        "options": ["Əsasən enerji saxlamaq üçün", "Genetik məlumatı saxlamaq üçün", "Nəfəs alma üçün", "Protein istehsalı üçün"],
        "correct": 1
    },
    {
        "question": "Tarixdə ilk yazılı qanunlar hansı sivilizasiyaya aiddir?",
        "options": ["Misir", "Roma", "Babil", "Yunan"],
        "correct": 2
    },
    {
        "question": "Hansı maddə suya atıldıqda partlaya bilər?",
        "options": ["Qızıl", "Gümüş", "Natrium", "Mis"],
        "correct": 2
    },
    {
        "question": "İnsan bədənində neçə ədəd qabırğa var?",
        "options": ["24", "22", "26", "20"],
        "correct": 0
    },
    {
        "question": "2025-ci ildə Avropa İttifaqının neçə üzv dövləti olacaq (təxmini)?",
        "options": ["27", "28", "30", "25"],
        "correct": 0
    },
    {
        "question": "Dünyanın ən hündür binası haradadır?",
        "options": ["New York", "Dubai", "Şanxay", "Tokio"],
        "correct": 1
    },
    {
        "question": "Albert Eynşteyn hansı nəzəriyyəni irəli sürüb?",
        "options": ["Kvant nəzəriyyəsi", "Nisbi nəzəriyyə", "Elektromaqnetizm", "Termodinamika"],
        "correct": 1
    },
    {
        "question": "HTML dilində səhifə yaratmaq üçün hansı tag istifadə olunur?",
        "options": ["<head>", "<html>", "<body>", "<title>"],
        "correct": 1
    },
    {
        "question": "Şuşa şəhəri 2020-ci ildə hansı tarixdə azad olunub?",
        "options": ["8 noyabr", "10 noyabr", "27 sentyabr", "20 oktyabr"],
        "correct": 0
    },
    {
        "question": "2024 Yay Olimpiya Oyunları harada keçiriləcək?",
        "options": ["Tokyo", "Los Angeles", "Paris", "Berlin"],
        "correct": 2
    },
    {
        "question": "Bitkiler günəş işığını hansı proseslə udur?",
        "options": ["Fotosintez", "Metabolizm", "Transpirasiya", "Oksidləşmə"],
        "correct": 0
    },
    {
        "question": "Avropa çempionatında ən çox qalib gələn ölkə hansıdır? (futbol)",
        "options": ["İspaniya", "Almaniya", "Fransa", "İtaliya"],
        "correct": 1
    },
    {
        "question": "Riyaziyyatda 'π' simvolu nəyi təmsil edir?",
        "options": ["Köklü ifadə", "Ədədi sabit", "Pərimetr", "Kəsr"],
        "correct": 1
    },
    {
        "question": "Azərbaycanın ən yüksək zirvəsi hansıdır?",
        "options": ["Bazardüzü", "Şahdağ", "Tufandağ", "Kəpəz"],
        "correct": 0
    },
    {
        "question": "Hansı ixtiraçının adı elektrik cərəyan vahidinə verilib?",
        "options": ["Tesla", "Faraday", "Ohm", "Ampere"],
        "correct": 3
    },
    {
        "question": "Süni intellekt nədir?",
        "options": ["Canlı orqanizm", "Avtomobil markası", "Kompyuter sistemlərinin düşünmə qabiliyyəti", "Mobil tətbiq"],
        "correct": 2
    },
    {
        "question": "Hansı iqlim tipi Azərbaycanda geniş yayılıb?",
        "options": ["Musson", "Tropik", "Subtropik", "Ekvatrial"],
        "correct": 2
    },
    {
        "question": "‘Google’ şirkəti hansı ildə yaradılıb?",
        "options": ["1995", "1998", "2000", "2003"],
        "correct": 1
    },
    {
        "question": "Günəş sistemində neçə əsas planet var?",
        "options": ["9", "7", "8", "10"],
        "correct": 2
    },
    {
        "question": "Əlifbamızda neçə hərf var?",
        "options": ["31", "32", "33", "34"],
        "correct": 1
    },
    {
        "question": "C vitamini ən çox hansı meyvədə var?",
        "options": ["Armud", "Limon", "Ərik", "Alma"],
        "correct": 1
    },
    {
        "question": "Neft hansı maddədən yaranır?",
        "options": ["Orqanik qalıqlardan", "Səmt qazından", "Kimyəvi maddədən", "Minerallardan"],
        "correct": 0
    },
    {
        "question": "Rəqəmsal saatda 00:00 nəyi bildirir?",
        "options": ["Günorta", "Gecəyarısı", "Axşam", "Səhər tezdən"],
        "correct": 1
    },
    {
        "question": "Azərbaycan Respublikasının ilk prezidenti kim olub?",
        "options": ["Abulfəz Elçibəy", "Heydər Əliyev", "Ayaz Mütəllibov", "İsa Qəmbər"],
        "correct": 2
    },
    {
        "question": "Hansı ölkədə qütb gecəsi yaşanır?",
        "options": ["Braziliya", "Norveç", "Misir", "Türkiyə"],
        "correct": 1
    },
    {
        "question": "Ən çox Nobel mükafatı alan sahə hansıdır?",
        "options": ["Ədəbiyyat", "Sülh", "Fizika", "Tibb"],
        "correct": 3
    },
    {
        "question": "Ağ Ev hansı şəhərdə yerləşir?",
        "options": ["New York", "Los Angeles", "Washington D.C.", "Chicago"],
        "correct": 2
    },
    {
        "question": "Gmail hansı şirkətə məxsusdur?",
        "options": ["Yahoo", "Microsoft", "Apple", "Google"],
        "correct": 3
    }
]

@dp.callback_query(lambda c: c.data == "quiz")
async def quiz(callback: CallbackQuery):
    q = random.choice(new_quiz_questions)
    buttons = [
        [InlineKeyboardButton(text=opt, callback_data=f"answer_{i}_{new_quiz_questions.index(q)}")]
        for i, opt in enumerate(q['options'])
    ]
    await callback.message.answer(f"<b>{q['question']}</b>", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("answer_"))
async def answer_quiz(callback: CallbackQuery):
    parts = callback.data.split("_")
    user_answer = int(parts[1])
    question_idx = int(parts[2])
    correct = new_quiz_questions[question_idx]['correct']
    user_id = callback.from_user.id

    if user_answer == correct:
        cursor.execute("INSERT OR IGNORE INTO scores (user_id, score) VALUES (?, ?)", (user_id, 0))
        cursor.execute("UPDATE scores SET score = score + 1 WHERE user_id = ?", (user_id,))
        conn.commit()
        await callback.message.answer("✅ Düzgün cavab! +1 bal")
    else:
        await callback.message.answer("❌ Yanlış cavab.")
    await callback.answer()

# 📊 Sadə poll
@dp.callback_query(lambda c: c.data == "poll")
async def simple_poll(callback: CallbackQuery):
    poll_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Bəli", callback_data="poll_yes"),
         InlineKeyboardButton(text="Xeyr", callback_data="poll_no")]
    ])
    await callback.message.answer("📊 Sizcə bu bot faydalıdır?", reply_markup=poll_keyboard)
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("poll_"))
async def poll_answer(callback: CallbackQuery):
    response = "Təşəkkürlər! Fikrinizi bildirdiniz." if callback.data == "poll_yes" else "Rəyiniz nəzərə alınacaq."
    await callback.message.answer(f"✅ {response}")
    await callback.answer()

# 📎 Fayl göndərmə
@dp.callback_query(lambda c: c.data == "file")
async def send_file(callback: CallbackQuery):
    file_path = Path("files") / "Rufat Babayev Resume.pdf"
    if not file_path.exists():
        await callback.message.answer("❌ Fayl tapılmadı.")
    else:
        file = FSInputFile(file_path)
        await callback.message.answer_document(file, caption="📎 Müəllif haqqında")
    await callback.answer()

# 🔐 Admin panel
@dp.callback_query(lambda c: c.data == "admin")
async def admin_panel(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.message.answer("⛔ Bu bölmə yalnız admin üçündür.")
    else:
        cursor.execute("SELECT COUNT(*) FROM users")
        users_count = cursor.fetchone()[0]
        cursor.execute("SELECT score FROM scores WHERE user_id = ?", (ADMIN_ID,))
        score = cursor.fetchone()
        score = score[0] if score else 0
        top_users = cursor.execute("SELECT u.full_name, s.score FROM users u JOIN scores s ON u.id = s.user_id ORDER BY s.score DESC LIMIT 10").fetchall()
        
        top_users_text = "\n".join([f"{idx+1}. {user[0]} - {user[1]} bal" for idx, user in enumerate(top_users)])

        user_list = cursor.execute("SELECT full_name, username FROM users").fetchall()
        user_list_text = "\n".join([f"{user[0]} (@{user[1]})" for user in user_list])

        await callback.message.answer(f"👤 İstifadəçi sayı: {users_count}\n📊 Sənin balın: {score}\n\nTop 10 istifadəçi:\n{top_users_text}\n\nBütün istifadəçilər:\n{user_list_text}")
    await callback.answer()

# 🟢 Echo
@dp.message()
async def echo(message: Message):
    await message.answer("Lets go! Seçim et:", reply_markup=main_menu)

# 🚀 Başlatma
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
