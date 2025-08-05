import asyncio
import logging
import sqlite3
import re
from datetime import datetime, timedelta, timezone
from contextlib import closing

from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ContentType, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardRemove
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramBadRequest

from config import BOT_TOKEN, ADMIN_ID, CARD_NUMBER, DB_PATH
from translations import get_text

# FSM State-lər
class RegisterForm(StatesGroup):
    selecting_language = State()
    entering_name = State()
    entering_phone = State()
    awaiting_screenshot = State()

# Yoxlamalar
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN boş ola bilməz.")
if not ADMIN_ID:
    raise ValueError("ADMIN_ID təyin olunmayıb.")
if not DB_PATH:
    raise ValueError("DB_PATH tapılmadı.")

CHANNEL_ID = -1002299496126

# Bot və Dispatcher
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

# DB bağlantısı
def get_db_connection():
    return sqlite3.connect(DB_PATH)

# --- /start ilə dil seçimi ---
@router.message(F.text == "/start")
async def start_register(message: Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="AZ🇦🇿", callback_data="lang_az"),
                InlineKeyboardButton(text="RU🇷🇺", callback_data="lang_ru"),
                InlineKeyboardButton(text="EN🇬🇧", callback_data="lang_en"),
                InlineKeyboardButton(text="TR🇹🇷", callback_data="lang_tr")
            ]
        ]
    )
    await message.answer(get_text("choose_language"), reply_markup=keyboard)
    await state.set_state(RegisterForm.selecting_language)

# --- Inline dil seçimi cavablandırılır ---
@router.callback_query(RegisterForm.selecting_language, F.data.startswith("lang_"))
async def process_language_selection(callback: CallbackQuery, state: FSMContext):
    if callback.data is not None:
        lang = callback.data.split("_")[1]
        await state.update_data(lang=lang)
    else:
        await callback.answer("❗ Xəta: Dil seçimi məlumatı tapılmadı.")
        return
    if callback.message is not None:
        await bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=None
        )
    if callback.message is not None:
        await callback.message.answer(get_text("language_selected", lang))
        await callback.message.answer(get_text("start", lang))
        await callback.message.answer(get_text("enter_name", lang))
    await state.set_state(RegisterForm.entering_name)

# --- Ad və soyad alınır ---
@router.message(RegisterForm.entering_name)
async def get_name(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "az")

    name = message.text.strip() if message.text is not None else ""
    await state.update_data(name=name)
    await message.answer(get_text("enter_phone", lang))
    await state.set_state(RegisterForm.entering_phone)

# --- Telefon nömrəsi alınır ---
@router.message(RegisterForm.entering_phone)
async def get_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "az")
    phone = message.text.strip() if message.text is not None else ""

    if not re.match(r"^\+994\d{9}$", phone):
        await message.answer(get_text("invalid_phone", lang))
        return

    await state.update_data(phone=phone)
    await message.answer(f"{get_text('payment_info', lang)}\n\n"
        f"💳 Kart nömrəsi: <b>{CARD_NUMBER}</b>\n\n"
        "✅ Ödənişi tamamladıqdan sonra screenshot/qəbzi bu çatda paylaşın.")
    await state.set_state(RegisterForm.awaiting_screenshot)

# --- Screenshot prosesi ---
@router.message(RegisterForm.awaiting_screenshot)
async def process_payment_proof(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "az")

    if message.content_type != ContentType.PHOTO or not message.photo:
        await message.answer("❗ Zəhmət olmasa, yalnız ödəniş qəbzinin şəklini göndərin.")
        return

    user = message.from_user
    if user is None:
        await message.answer("❗ Xəta: istifadəçi məlumatı tapılmadı.")
        return
    user_id = user.id
    username = getattr(user, "username", None) or "Yoxdur"
    username_line = f"🔗 Username: @{username}" if username != "Yoxdur" else "🔗 Username: Yoxdur"

    caption = (
        f"✅ Yeni qeydiyyat və ödəniş screenshotu:\n"
        f"👤 Ad, Soyad: {data['name']}\n"
        f"📞 Telefon: {data['phone']}\n"
        f"🆔 Telegram ID: {user_id}\n"
        f"{username_line}"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Təsdiqlə", callback_data=f"approve_{user_id}")]
    ])

    await bot.send_photo(chat_id=ADMIN_ID, photo=message.photo[-1].file_id, caption=caption, reply_markup=keyboard)

    with get_db_connection() as conn:
        with conn:
            conn.execute(
                "INSERT INTO users (user_id, name, phone, username) VALUES (?, ?, ?, ?)",
                (user_id, data['name'], data['phone'], username)
            )

    await message.answer("✅ Qeydiyyat tamamlandı. Məlumat adminə göndərildi.")
    await message.answer("📨 Təsdiqdən sonra sizə bir istifadəçi üçün nəzərdə tutulmuş və 24 saat ərzində keçərli olan giriş linki təqdim olunacaq.")
    await state.clear()

# --- Admin təsdiqləmə ---
@router.callback_query(F.data.startswith("approve_"))
async def approve_user(callback: CallbackQuery):
    if callback.data is None:
        await callback.answer("❗ Xəta: callback data tapılmadı.")
        return

    user_id = int(callback.data.split("_")[1])

    try:
        invite_link = await bot.create_chat_invite_link(
            chat_id=CHANNEL_ID,
            expire_date=datetime.now(timezone.utc) + timedelta(days=1),
            member_limit=1
        )
        await bot.send_message(chat_id=user_id, text=f"✅ Giriş linkiniz: {invite_link.invite_link}")

        if callback.message:
            await bot.edit_message_reply_markup(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                reply_markup=None
            )

        await callback.answer("İstifadəçiyə link göndərildi.")
    except TelegramBadRequest as e:
        await callback.answer(f"❗ Xəta: {e}")

# --- Ping komandası ---
@router.message(F.text == "/ping")
async def ping(message: Message):
    await message.answer("✅ Bot işləyir.")

# --- Kanal ID almaq üçün test ---
@router.message(F.text == "/get_channel_id")
async def get_chat_id(message: Message):
    await message.answer(f"<b>Chat ID:</b> <code>{message.chat.id}</code>")
    print(f"CHAT ID: {message.chat.id}")

# --- DB yaradılması ---
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

# --- Botun başlatılması ---
async def main():
    logging.basicConfig(level=logging.INFO)
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
