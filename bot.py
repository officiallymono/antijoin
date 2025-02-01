import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatMemberUpdated
from aiogram.filters import ChatMemberUpdatedFilter

# تنظیمات اولیه
TOKEN = "YOUR_BOT_TOKEN"  # 🔹 توکن ربات را جایگزین کن
CHAT_ID = -1001234567890   # 🔹 آیدی کانال را جایگزین کن (با -100 شروع می‌شود)

# ایجاد نمونه‌های ربات و دیسپچر
bot = Bot(token=TOKEN)
dp = Dispatcher()

# تنظیمات لاگینگ
logging.basicConfig(level=logging.INFO)

# هندلر برای شناسایی اعضای جدید در کانال
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

# اجرای ربات با polling
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
