# Telegram Event & Points Bot

Telegram bot for community event management: registration, event creation, check-ins, points, rankings, announcements, and scheduled reminders.

## Features

- User registration through Telegram commands and buttons
- Admin flows for creating and managing events
- Participant check-ins with automatic points
- Personal history and global ranking views
- Broadcast announcements
- Scheduled event reminders
- CSV-based persistence for simple deployment and backups

## Tech Stack

- Python
- Aiogram 3
- APScheduler
- CSV storage

## Getting Started

```bash
git clone https://github.com/RazerTag/kibiki_bot.git
cd kibiki_bot

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file:

```dotenv
BOT_TOKEN=your_telegram_bot_token
ADMIN_ID=comma_separated_admin_user_ids
```

Run the bot:

```bash
python main.py
```

## Project Structure

```text
kibiki_bot/
├── handlers/
│   ├── admin.py
│   ├── announcements.py
│   ├── checkin.py
│   ├── events.py
│   ├── ranking.py
│   └── registration.py
├── middlewares/
├── csv_utils.py
├── keyboards.py
├── main.py
├── scheduler_tasks.py
└── states.py
```

## Portfolio Context

This project shows practical Telegram automation: FSM-based user flows, admin workflows, scheduled jobs, and simple persistence. It is a small community-management system rather than a production SaaS backend.

## License

MIT
