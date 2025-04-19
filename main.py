import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUsers, KeyboardButtonRequestChat
from config import BOT_TOKEN

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Define the types mapping for shared peers
types = {
    1: 'User',
    2: 'Private Channel',
    3: 'Public Channel',
    4: 'Private Group',
    5: 'Public Group',
    6: 'Bot',
    7: 'Premium User'
}

# Define the custom keyboard buttons
button_user = KeyboardButton(
    text="👤 User",
    request_users=KeyboardButtonRequestUsers(request_id=1, user_is_bot=False)
)
button_private_channel = KeyboardButton(
    text="🔒 Private Channel",
    request_chat=KeyboardButtonRequestChat(request_id=2, chat_is_channel=True, chat_has_username=False)
)
button_public_channel = KeyboardButton(
    text="🌐 Public Channel",
    request_chat=KeyboardButtonRequestChat(request_id=3, chat_is_channel=True, chat_has_username=True)
)
button_private_group = KeyboardButton(
    text="🔒 Private Group",
    request_chat=KeyboardButtonRequestChat(request_id=4, chat_is_channel=False, chat_has_username=False)
)
button_public_group = KeyboardButton(
    text="🌐 Public Group",
    request_chat=KeyboardButtonRequestChat(request_id=5, chat_is_channel=False, chat_has_username=True)
)
button_bot = KeyboardButton(
    text="🤖 Bot",
    request_users=KeyboardButtonRequestUsers(request_id=6, user_is_bot=True)
)
button_premium = KeyboardButton(
    text="Premium 🌟",
    request_users=KeyboardButtonRequestUsers(request_id=7, user_is_premium=True)
)

# Create the reply keyboard markup
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [button_user],
        [button_private_channel, button_public_channel],
        [button_private_group, button_public_group],
        [button_bot, button_premium]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

# Welcome message text
welcome_text = (
    "👋 <b>Welcome to Chat ID Finder Bot!</b> 🆔\n\n"
    "✅ <b>Fetch Any Chat ID Instantly!</b>\n\n"
    "🔧 <b>How to Use?</b>\n"
    "1️⃣ Click the buttons below to share a chat or user.\n"
    "2️⃣ Receive the unique ID instantly.\n\n"
    "💎 <b>Features:</b>\n"
    "✅ Supports users, bots, groups & channels\n"
    "⚡ Fast and reliable\n\n"
    "<blockquote>🛠 Made with ❤️ by @TheSmartDev</blockquote>"
)

# Handler for the /start command
@dp.message(Command("start"))
async def start_command(message: Message):
    logging.info("Processing /start command")
    await message.answer(welcome_text, parse_mode="HTML", reply_markup=keyboard)
    logging.info("Sent welcome message with keyboard")

# Handler for shared users (e.g., User, Bot, Premium User)
@dp.message(lambda message: message.users_shared is not None)
async def handle_users_shared(message: Message):
    users_shared = message.users_shared
    request_id = users_shared.request_id
    type_ = types.get(request_id, 'Unknown')
    user_ids = [user.user_id for user in users_shared.users]
    response = f"👤 <b>Shared {type_} Info</b>\n"
    for user_id in user_ids:
        response += f"🆔 ID: <code>{user_id}</code>\n"
    await message.answer(response, parse_mode="HTML")
    logging.info(f"Sent response: {response}")

# Handler for shared chats (e.g., Channels, Groups)
@dp.message(lambda message: message.chat_shared is not None)
async def handle_chat_shared(message: Message):
    chat_shared = message.chat_shared
    request_id = chat_shared.request_id
    type_ = types.get(request_id, 'Unknown')
    chat_id = chat_shared.chat_id
    response = f"💬 <b>Shared {type_} Info</b>\n🆔 ID: <code>{chat_id}</code>"
    await message.answer(response, parse_mode="HTML")
    logging.info(f"Sent response: {response}")

# Handler for forwarded messages
@dp.message(lambda message: message.forward_date is not None)
async def handle_forwarded_message(message: Message):
    logging.info(f"Received forwarded message: {message}")
    if message.forward_from:
        # Forwarded from a user
        user_id = message.forward_from.id
        user_name = message.forward_from.first_name or "User"
        response = (
            f"<b>Forward Message Detected</b>\n"
            f"<b>Chat Name</b> {user_name}\n"
            f"<b>ChatID</b> <code>{user_id}</code>"
        )
    elif message.forward_from_chat:
        # Forwarded from a chat (group or channel)
        chat_id = message.forward_from_chat.id
        chat_name = message.forward_from_chat.title
        response = (
            f"<b>Forward Message Detected</b>\n"
            f"<b>Chat Name</b> {chat_name}\n"
            f"<b>ChatID</b> <code>{chat_id}</code>"
        )
    else:
        response = "<b>Sorry Bro, Forward Method Not Support For Private Things</b>"

    await message.answer(response, parse_mode="HTML")
    logging.info(f"Sent response: {response}")

# Main function to start the bot
async def main():
    print("✅Bot Is Up And Running On Aiogram")
    logging.info("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())