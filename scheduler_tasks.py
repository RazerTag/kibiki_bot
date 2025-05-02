import os
import logging
from datetime import datetime, timedelta

from aiogram import Bot
from csv_utils import get_all_events, get_all_users

# Configure logging
logger = logging.getLogger(__name__)

async def send_upcoming_events():
    """
    Send reminders about events happening within the next 24 hours to all registered users.
    """
    try:
        token = os.getenv("BOT_TOKEN")
        if not token:
            logger.error("BOT_TOKEN is not set in environment variables.")
            return

        bot = Bot(token=token)
        now = datetime.utcnow()
        threshold = now + timedelta(hours=24)

        events = get_all_events()
        # Filter events occurring in the next 24 hours
        upcoming = []
        for ev in events:
            try:
                # Expecting ISO format in 'date' field
                ev_dt = datetime.fromisoformat(ev['date'])
            except Exception as e:
                logger.warning(f"Невозможно проанализировать дату '{ev['date']}' для события {ev['event_id']}: {e}")
                continue
            if now < ev_dt <= threshold:
                upcoming.append(ev)

        if not upcoming:
            await bot.session.close()
            return

        users = get_all_users()
        for user in users:
            try:
                chat_id = int(user['user_id'])
                for ev in upcoming:
                    text = (
                        f"📢 Напоминание: Предстоящее событие *{ev['name']}*\n"
                        f"📅 Когда: {ev['date']} UTC\n"
                        f"📍 Где: {ev['location']}\n"
                        f"🏅 Кибики: {ev['points']}"
                    )
                    await bot.send_message(chat_id, text, parse_mode="Markdown")
            except Exception as e:
                logger.error(f"Не удалось отправить напоминание пользователю {user['user_id']}: {e}")

        await bot.session.close()
    except Exception as e:
        logger.exception(f"Ошибка в send_upcoming_events: {e}")
