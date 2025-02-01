import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatMemberUpdated
from aiogram.filters import ChatMemberUpdatedFilter
from fastapi import FastAPI
import uvicorn
import os

# متغیرهای اصلی
TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")  # 🔹 از متغیر محیطی بگیر
CHAT_ID = int(os.getenv("CHAT_ID", "-1001234567890"))  # 🔹 آیدی کانال
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://your-vercel-app.vercel.app/webhook")  # 🔹 لینک وبهوک

# ایجاد بات و دیسپچر
bot = Bot(token=TOKEN)
dp = Dispatcher()
app = FastAPI()

# تنظیمات لاگینگ
logging.basicConfig(level=logging.INFO)

# هندلر برای جلوگیری از جوین شدن اعضا
@dp.chat_member(ChatMemberUpdatedFilter(member_status_changed=True))
async def handle_new_members(update: ChatMemberUpdated):
    if update.chat.id == CHAT_ID and update.new_chat_member.status == "member":
        user_id = update.new_chat_member.user.id
        try:
            await bot.ban_chat_member(CHAT_ID, user_id)  # 🚫 کاربر را بن کن
            await asyncio.sleep(5)  # ⏳ بعد از ۵ ثانیه آنبن کن
            await bot.unban_chat_member(CHAT_ID, user_id, only_if_banned=True)
            logging.info(f"🚫 کاربر {user_id} بن شد و بعد از ۵ ثانیه آنبن شد.")
        except Exception as e:
            logging.error(f"⚠️ خطا در بن کردن کاربر: {e}")

# مسیر FastAPI برای وبهوک
@app.post("/webhook")
async def webhook(update: dict):
    update = types.Update(**update)
    await dp.feed_update(bot, update)
    return {"status": "ok"}

# ست کردن وبهوک هنگام راه‌اندازی
@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"🚀 وبهوک روی {WEBHOOK_URL} تنظیم شد!")

# اجرای FastAPI (مخصوص Cloudflare/Vercel)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
