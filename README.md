# Chat ID Echo Bot

![Chat ID Echo Bot](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)  
A simple and efficient Telegram bot that helps you fetch chat IDs for users, groups, channels, and bots instantly.

## 📖 Overview

The **Chat ID Bot Aiogram** is a Telegram bot built with Python and the Telethon library. It allows users to quickly retrieve the unique IDs of Telegram entities (users, groups, channels, and bots) by sharing them through a user-friendly keyboard interface. Whether you're a developer needing chat IDs for Telegram API interactions or a user managing groups and channels, this bot makes the process seamless.

This project is maintained by [abirxdhack](https://github.com/abirxdhack) and hosted at [Chat-ID-Bot-Aio](https://github.com/abirxdhack/Chat-ID-Bot-Aio).

## ✨ Features

- **Fetch Chat IDs Instantly**: Retrieve IDs for users, bots, private/public groups, and private/public channels.
- **User-Friendly Interface**: Interactive keyboard with buttons to share different types of Telegram entities.
- **Reliable and Fast**: Built with Telethon for efficient Telegram API interactions.
- **Logging Support**: Includes detailed logging for debugging and monitoring.
- **Open Source**: Feel free to contribute or customize the bot for your needs!

## 📋 Prerequisites

Before setting up the bot, ensure you have the following:

- **Python 3.9+**: The bot is written in Python.
- **Bot Token**: Create a bot via [BotFather](https://t.me/BotFather) on Telegram to get a `BOT_TOKEN`.
- **Aiogram Library**: The bot uses Aiogram to interact with Telegram’s API.

## 🛠 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/abirxdhack/Chat-ID-Bot-Aio.git
   cd Chat-ID-Bot-Aio
   ```

2. **Install Dependencies**:
   Install the required Python packages using `pip`:
   ```bash
   pip install aiogram
   ```

3. **Set Up Your Credentials**:
   Open `quickinfo.py` and replace the placeholder credentials with your own:
   ```python
   BOT_TOKEN = "800xxxxwowmU"  # Replace this BOT_TOKEN
   ```

## 🚀 Usage

1. **Run the Bot**:
   Start the bot by running the script:
   ```bash
   python3 main.py
   ```
   You should see:
   ```
   ✅Bot Is Up And Running On Aiogram
   ```

2. **Interact with the Bot**:
   - Open Telegram and start a chat with your bot (find it using the username you set via BotFather).
   - Send the `/start` command to see the welcome message and keyboard.
   - Click a button (e.g., "👤 User", "🔒 Private Group", or "🌐 Public Channel") and share the requested entity.
   - The bot will reply with the chat ID, e.g.:
     ```
     👤 Shared User Info
     🆔 ID: 5857628904
     ```

## 📜 Code Structure

- **`quickinfo.py`**: The main script containing the bot logic, including the event handlers for `/start` and peer sharing.
- **Logging**: The bot uses Python’s `logging` module to log events, making it easy to debug issues.

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features or improvements, feel free to:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit them (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📧 Contact

For questions, suggestions, or support, reach out to [abirxdhack](https://github.com/abirxdhack) via GitHub Issues or Telegram (@TheSmartDev).