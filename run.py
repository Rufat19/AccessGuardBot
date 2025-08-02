import asyncio
import logging
import sqlite3
from contextlib import closing

from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ContentType
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN, ADMIN_ID, CARD_NUMBER, DB_PATH

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

def get_db_connection():
    return sqlite3.connect(DB_PATH)

class RegisterForm(StatesGroup):
    entering_name = State()
    entering_phone = State()
    awaiting_screenshot = State()

@router.message(F.text == "/start")
async def start_register(message: Message, state: FSMContext):
    await message.answer(
        "🛡️ <b>SOSİAL MÜHİT</b> Telegram kanalına qoşulmaq üçün aşağıdakı məlumatları diqqətlə və düzgün şəkildə təqdim etməyiniz xahiş olunur.\n\n"
        "📌 <b>Vacib qeydlər:</b> Əgər təqdim etdiyiniz məlumatlar natamam və ya səhv olarsa, administrator tərəfindən kanal üzvlüyünüz <u>rədd edilə bilər</u>.\n\n"
        "✍️ Zəhmət olmasa, <b>ad və soyadınızı</b> tam şəkildə daxil edin:"
    )
    await state.set_state(RegisterForm.entering_name)

@router.message(RegisterForm.entering_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer(
        "📞 <b>Zəhmət olmasa, qoşulacağınız mobil nömrəni düzgün və tam şəkildə daxil edin.</b>\n\n"
        "Bu nömrə administrator tərəfindən müraciətiniz təsdiqləndikdən sonra "
        "<u>kanala giriş linkinin göndərilməsi</u> və sizinlə əlaqə yaradılması üçün istifadə olunacaq.\n\n"
        "🔒 Diqqət: Nömrəni düzgün təqdim etməyiniz, qeydiyyat prosesinin uğurla başa çatması üçün vacibdir."
    )
    await state.set_state(RegisterForm.entering_phone)

@router.message(RegisterForm.entering_phone)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    await message.answer(
        f"💳 <b>Kanala qoşulmaq üçün 9 AZN məbləğində ödəniş tələb olunur.</b>\n\n"
        f"Ödənişi aşağıdakı ödəniş kartına köçürün:\n"
        f"<b>{CARD_NUMBER}</b>\n\n"
        "✅ Ödənişi tamamladıqdan dərhal sonra, zəhmət olmasa, təsdiq sənədini (screenshot/qəbz şəkli) bu çatda paylaşın.\n\n"
        "ℹ️ Qeyd: Bütün ödənişlər sistemimizdə qeyd olunur və birbaşa administrator tərəfindən yoxlanılır. Ödənişlərin itməsi ehtimalı yoxdur."
    )
    await state.set_state(RegisterForm.awaiting_screenshot)

@router.message(RegisterForm.awaiting_screenshot)
async def process_payment_proof(message: Message, state: FSMContext):
    if message.content_type != ContentType.PHOTO:
        await message.answer(
            "❗ Zəhmət olmasa, yalnız ödəniş qəbzinin şəklini göndərin.\n"
            "Digər mesajlara cavab verilmir."
        )
        return

    data = await state.get_data()
    user_id = message.from_user.id
    username = message.from_user.username or "Yoxdur"
    username_line = f"🔗 Username: @{username}" if username != "Yoxdur" else "🔗 Username: Yoxdur"

    caption = (
        f"✅ Yeni qeydiyyat və ödəniş screenshotu:\n"
        f"👤 Ad, Soyad: {data['name']}\n"
        f"📞 Telefon: {data['phone']}\n"
        f"🆔 Telegram ID: {user_id}\n"
        f"{username_line}"
    )

    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=message.photo[-1].file_id,
        caption=caption
    )

    await message.answer(
        "✅ Qeydiyyat üçün müraciətiniz uğurla admin heyətinə göndərildi.\n\n"
        "⏳ Hazırda müraciətlərin sayında artım müşahidə olunur. Bu səbəbdən cavab müddəti bir qədər uzana bilər. Zəhmət olmasa, səbirli olun.\n\n"
        "ℹ️ Əgər qeydiyyat prosesində hər hansı çətinliklə qarşılaşsanız, xahiş edirik @Rufat19 istifadəçi adı ilə bizimlə əlaqə saxlayın.\n\n"
        "Təşəkkür edirik və uğurlar arzulayırıq! 🎉"
    )

    with get_db_connection() as conn:
        conn.execute(
            "INSERT INTO users (user_id, name, phone, username) VALUES (?, ?, ?, ?)",
            (user_id, data['name'], data['phone'], username)
        )
        conn.commit()

    await state.clear()

def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    name TEXT,
                    phone TEXT,
                    username TEXT
                )
            """)

async def main():
    logging.basicConfig(level=logging.INFO)
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
