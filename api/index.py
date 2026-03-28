import os
import base64
import json
import asyncio
from http.server import BaseHTTPRequestHandler
from aiogram import Bot, Dispatcher, types

# ======================================
# CONFIGURATION
# ======================================
TOKEN = "8488302808:AAGwWZ6EUDF9p9t_kNVbuSCjCPh59WylRwY"
ADMIN_IDS = [5556909453]

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# ========================================
# KEYBOARDS & UTILS
# ========================================
def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton("🔐 PHP Encryption"))
    keyboard.row(types.KeyboardButton("👤 My Profile"), types.KeyboardButton("ℹ️ Info"))
    return keyboard

def encrypt_php_code(original_code):
    clean_code = original_code.strip()
    if clean_code.startswith("<?php"):
        clean_code = clean_code[5:].strip()
    if clean_code.endswith("?>"):
        clean_code = clean_code[:-2].strip()

    encoded_string = base64.b64encode(clean_code.encode('utf-8')).decode('utf-8')

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
    
    try:
        file_info = await bot.get_file(message.document.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        content = downloaded_file.read().decode('utf-8')

        encrypted_code = encrypt_php_code(content)
        new_filename = f"Encrypted_{message.document.file_name}"
        
        # Vercel-এর /tmp ফোল্ডারে ফাইল সেভ করতে হয়
        temp_path = f"/tmp/{new_filename}"
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(encrypted_code)

        with open(temp_path, "rb") as doc:
            caption = (
                "✅ *𝗘𝗡𝗖𝗥𝗬𝗣𝗧𝗜𝗢𝗡 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗!* ✅\n\n"
                f"📦 *File:* `{new_filename}`\n"
                "🛡️ *Security:* 𝟲𝟰-𝗕𝗶𝘁 𝗕𝗮𝘀𝗲𝟲𝟰\n"
                "⚡ *Status:* 𝟭𝟬𝟬% 𝗪𝗼𝗿𝗸𝗶𝗻𝗴\n\n"
                "⚡ *Created By:* @sakib01994"
            )
            await bot.send_document(message.chat.id, doc, caption=caption, parse_mode="Markdown")
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
    except Exception as e:
        await message.answer(f"❌ Error: {str(e)}")
    finally:
        await bot.delete_message(message.chat.id, proc.message_id)

@dp.message_handler(lambda message: message.text == "ℹ️ Info")
async def info(message: types.Message):
    await message.answer("📌 This bot helps developers protect their PHP source code using Base64 obfuscation.")

# ========================================
# VERCEL WEBHOOK HANDLER
# ========================================
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            update_dict = json.loads(post_data.decode('utf-8'))
            update = types.Update.to_object(update_dict)
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(dp.process_update(update))
            loop.close()

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK")
        except Exception as e:
            self.send_response(500)
            self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"PHP Encryptor Bot is Running!")
