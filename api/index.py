import os
import base64
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

# ======================================
# CONFIGURATION
# ======================================
TOKEN = "8488302808:AAGwWZ6EUDF9p9t_kNVbuSCjCPh59WylRwY"
ADMIN_IDS = [5556909453]

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# ========================================
# KEYBOARDS
# ========================================
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton("🔐 PHP Encryption"))
    keyboard.row(KeyboardButton("👤 My Profile"), KeyboardButton("ℹ️ Info"))
    return keyboard

# ========================================
# ENCRYPTION ENGINE
# ========================================
def encrypt_php_code(original_code):
    # কোড থেকে <?php ট্যাগ সরিয়ে ফেলা (যদি থাকে)
    clean_code = original_code.strip()
    if clean_code.startswith("<?php"):
        clean_code = clean_code[5:].strip()
    if clean_code.endswith("?>"):
        clean_code = clean_code[:-2].strip()

    # Base64 এনকোডিং
    encoded_bytes = base64.b64encode(clean_code.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')

    # প্রিমিয়াম এনক্রিপ্টেড ফরম্যাট
    encrypted_template = f"""<?php
/* * ==========================================
 * 🔐 ENCRYPTED BY SB SAKIB CHOWDHURY
 * ⚡ Premium 64-Bit Security Applied
 * ==========================================
 */
eval(base64_decode("{encoded_string}"));
?>"""
    return encrypted_template

# ========================================
# HANDLERS
# ========================================

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    welcome = (
        "🔥 *𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗣𝗛𝗣 𝗘𝗡𝗖𝗥𝗬𝗣𝗧𝗢𝗥* 🔥\n\n"
        "🤖 I can encrypt your PHP source code into 64-bit format.\n"
        "🛡️ Your code will be 100% functional after encryption.\n\n"
        "⚡ *Powered By:* @sakib01994"
    )
    await message.answer(welcome, parse_mode="Markdown", reply_markup=get_main_keyboard())

@dp.message_handler(lambda message: message.text == "🔐 PHP Encryption")
async def enc_info(message: types.Message):
    await message.answer(
        "📂 *𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝗲𝗻𝗱 𝘆𝗼𝘂𝗿 .𝗽𝗵𝗽 𝗳𝗶𝗹𝗲 𝗻𝗼𝘄*\n\n"
        "I will encrypt the content and send back a protected version.",
        parse_mode="Markdown"
    )

@dp.message_handler(content_types=['document'])
async def handle_docs(message: types.Message):
    if not message.document.file_name.endswith('.php'):
        return await message.answer("❌ *Please send a valid .php file!*", parse_mode="Markdown")

    proc = await message.answer("🔐 *𝗘𝗡𝗖𝗥𝗬𝗣𝗧𝗜𝗡𝗚 𝗬𝗢𝗨𝗥 𝗖𝗢𝗗𝗘...*")

    # ফাইল ডাউনলোড করা
    file_info = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    content = downloaded_file.read().decode('utf-8')

    # এনক্রিপ্ট করা
    encrypted_code = encrypt_php_code(content)

    # নতুন ফাইল তৈরি
    new_filename = f"Encrypted_{message.document.file_name}"
    with open(new_filename, "w", encoding="utf-8") as f:
        f.write(encrypted_code)

    # ফাইল পাঠানো
    with open(new_filename, "rb") as doc:
        caption = (
            "✅ *𝗘𝗡𝗖𝗥𝗬𝗣𝗧𝗜𝗢𝗡 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗!* ✅\n\n"
            f"📦 *File:* `{new_filename}`\n"
            "🛡️ *Security:* 𝟲𝟰-𝗕𝗶𝘁 𝗕𝗮𝘀𝗲𝟲𝟰\n"
            "⚡ *Status:* 𝟭𝟬𝟬% 𝗪𝗼𝗿𝗸𝗶𝗻𝗴\n\n"
            "⚡ *Created By:* @sakib01994"
        )
        await bot.send_document(message.chat.id, doc, caption=caption, parse_mode="Markdown")

    # ক্লিনআপ
    os.remove(new_filename)
    await bot.delete_message(message.chat.id, proc.message_id)

@dp.message_handler(lambda message: message.text == "ℹ️ Info")
async def info(message: types.Message):
    await message.answer("📌 This bot helps developers protect their PHP source code using Base64 obfuscation.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
