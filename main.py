import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUsers, KeyboardButtonRequestChat
from config import BOT_TOKEN

# Mapping of request IDs to types and effect IDs
TYPES = {
    1: {'name': 'User', 'effect_id': '5107584321108051014'},  # 👍 Thumbs Up
    2: {'name': 'Private Channel', 'effect_id': '5046589136895476101'},  # 💩 Poop
    3: {'name': 'Public Channel', 'effect_id': '5104841245755180586'},  # 🔥 Fire
    4: {'name': 'Private Group', 'effect_id': '5104858069142078462'},  # 👎 Thumbs Down
    5: {'name': 'Public Group', 'effect_id': '5046509860389126442'},  # 🎉 Confetti
    6: {'name': 'Bot', 'effect_id': '5046509860389126442'},  # 🎉 Confetti
    7: {'name': 'Premium User', 'effect_id': '5046509860389126442'}  # 🎉 Confetti
}

# Message effect ID for the /start command
START_EFFECT_ID = "5104841245755180586"  # 🔥 Fire

# Effect ID for forwarded messages
FORWARD_EFFECT_ID = "5046509860389126442"  # 🎉 Confetti

# Set up logging to console and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('error.log'),
        logging.StreamHandler()
    ]
)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

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
    try:
        await message.answer(
            welcome_text,
            parse_mode="HTML",
            reply_markup=keyboard,
            disable_web_page_preview=True,
            message_effect_id=START_EFFECT_ID
        )
        logging.info("Sent welcome message with keyboard and fire effect")
    except Exception as e:
        logging.error(f"Failed to send welcome message: {str(e)}")
        # Retry without effect
        await message.answer(
            welcome_text,
            parse_mode="HTML",
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
        logging.info("Retried welcome message without effect")

# Handler for shared users (e.g., User, Bot, Premium User)
@dp.message(lambda message: message.users_shared is not None)
async def handle_users_shared(message: Message):
    users_shared = message.users_shared
    request_id = users_shared.request_id
    type_info = TYPES.get(request_id, {'name': 'Unknown', 'effect_id': None})
    type_ = type_info['name']
    effect_id = type_info['effect_id']
    user_ids = [user.user_id for user in users_shared.users]
    if not user_ids:
        response = f"⚠️ <b>Error:</b> No {type_} ID received."
        await message.answer(response, parse_mode="HTML")
        logging.error(f"No user IDs in users_shared: {users_shared}")
        return
    response = f"👤 <b>Shared {type_} Info</b>\n"
    for user_id in user_ids:
        response += f"🆔 ID: <code>{user_id}</code>\n"
    try:
        await message.answer(
            response,
            parse_mode="HTML",
            message_effect_id=effect_id
        )
        logging.info(f"Sent response: {response}")
    except Exception as e:
        logging.error(f"Failed to send user shared response: {str(e)}")
        # Retry without effect
        await message.answer(
            response,
            parse_mode="HTML"
        )
        logging.info(f"Retried user shared response without effect: {response}")

# Handler for shared chats (e.g., Channels, Groups)
@dp.message(lambda message: message.chat_shared is not None)
async def handle_chat_shared(message: Message):
    chat_shared = message.chat_shared
    request_id = chat_shared.request_id
    type_info = TYPES.get(request_id, {'name': 'Unknown', 'effect_id': None})
    type_ = type_info['name']
    effect_id = type_info['effect_id']
    chat_id = chat_shared.chat_id
    response = f"💬 <b>Shared {type_} Info</b>\n🆔 ID: <code>{chat_id}</code>"
    try:
        await message.answer(
            response,
            parse_mode="HTML",
            message_effect_id=effect_id
        )
        logging.info(f"Sent response: {response}")
    except Exception as e:
        logging.error(f"Failed to send chat shared response: {str(e)}")
        # Retry without effect
        await message.answer(
            response,
            parse_mode="HTML"
        )
        logging.info(f"Retried chat shared response without effect: {response}")

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

    try:
        await message.answer(
            response,
            parse_mode="HTML",
            message_effect_id=FORWARD_EFFECT_ID
        )
        logging.info(f"Sent response: {response}")
    except Exception as e:
        logging.error(f"Failed to send forwarded message response: {str(e)}")
        # Retry without effect
        await message.answer(
            response,
            parse_mode="HTML"
        )
        logging.info(f"Retried forwarded message response without effect: {response}")

# Main function to start the bot
async def main():
    print("✅Bot Is Up And Running On Aiogram")
    logging.info("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
