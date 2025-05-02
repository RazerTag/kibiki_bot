<!-- README for bot_mirea -->

<!-- Badges -->

[![Python](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)
[![Aiogram](https://img.shields.io/badge/aiogram-3.0-brightgreen.svg)](https://docs.aiogram.dev/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

\section\*{Telegram Event & Points Bot}

# Telegram Event & Points Bot

A **powerful** and **flexible** Telegram bot built with Python and [Aiogram 3](https://docs.aiogram.dev/), designed to help communities:

* Organize events
* Manage participant registrations
* Track points and leaderboards
* Broadcast announcements

---

\subsection\*{Key Features}

## Key Features

* 🎉 **User Registration**: Easy self-registration via command or button.
* 📅 **Event Management**: FSM-powered flows for admins to create, schedule, and edit events.
* ✅ **Check-In System**: Participants check in and earn points automatically.
* 🏆 **Points & Ranking**: View personal history and global leaderboards.
* 📢 **Announcements**: Broadcast messages to all users or targeted groups.
* 🔄 **Interactive Keyboards**: Intuitive inline and reply keyboards for seamless navigation.
* 💾 **Persistent Storage**: CSV storage for portability and easy backups.
* ⏰ **Scheduled Notifications**: APScheduler integration for reminders and summaries.
* 🔒 **Admin Panel**: Secure admin commands for event and point management.

---

\subsection\*{Getting Started}

## Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/bot_mirea.git
   cd bot_mirea
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file in the project root:

   ```dotenv
   BOT_TOKEN=your_telegram_bot_token
   ADMIN_ID=comma_separated_admin_user_ids
   ```

4. **Run the bot**

   ```bash
   python main.py
   ```

---

\subsection\*{Project Structure}

## Project Structure

```
bot_mirea/
├── main.py         # Entry point: bot, dispatcher, routers, scheduler
├── admin.py        # Admin commands (add events, set points)
├── keyboards.py    # Inline & reply keyboards
├── handlers/       # (Optional) Modular handlers
├── middlewares/    # Custom middleware (e.g., registration checks)
├── utils/          # CSV, scheduling helpers
├── requirements.txt
├── .env            # Environment variables
└── LICENSE
```

---


\subsection\*{License}

## License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.
