import logging
import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from middlewares.registration_middleware import RegistrationMiddleware
from csv_utils import init_csv_files
from scheduler_tasks import send_upcoming_events

from handlers.registration import router as registration_router
from handlers.checkin import router as checkin_router
from handlers.events import router as events_router
from handlers.ranking import router as ranking_router
from handlers.admin import router as admin_router
from handlers.common import router as common_router
from handlers.announcements import router as announcements_router
from handlers.buttons import router as buttons_router

async def setup_bot_commands(bot: Bot):
    """
    Register commands shown by Telegram when the user opens the "/" menu.
    """
    commands = [
        BotCommand(command="start", description="Начать регистрацию"),
        BotCommand(command="help", description="Помощь / меню команд"),
        BotCommand(command="events", description="Список мероприятий"),
        BotCommand(command="checkin", description="Отметиться на мероприятии"),
        BotCommand(command="balance", description="Показать ваши баллы"),
        BotCommand(command="history", description="Ваша история чек-инов"),
        BotCommand(command="addevent", description="Добавить событие (админ)"),
        BotCommand(command="deleteevent", description="Удалить событие (админ)"),
        BotCommand(command="editevent", description="Изменить событие (админ)"),
        BotCommand(command="adduser", description="Добавить пользователя (админ)"),
        BotCommand(command="removeuser", description="Удалить пользователя (админ)"),
        BotCommand(command="listusers", description="Список пользователей (админ)"),
        BotCommand(command="setpoints", description="Установить очки (админ)"),
        BotCommand(command="announce", description="Создать объявление (админ)"),
        BotCommand(command="announcements", description="Показать объявления"),
        BotCommand(command="cancel", description="Отменить текущее действие"),
    ]
    await bot.set_my_commands(commands)

async def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не найден в .env")
        return

    init_csv_files()

    bot = Bot(token=BOT_TOKEN, parse_mode=None)
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(RegistrationMiddleware())

    dp.include_router(registration_router)
    dp.include_router(checkin_router)
    dp.include_router(events_router)
    dp.include_router(ranking_router)
    dp.include_router(admin_router)
    dp.include_router(announcements_router)
    dp.include_router(buttons_router)   
    dp.include_router(common_router)

    await setup_bot_commands(bot)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_upcoming_events, "interval", hours=1)
    scheduler.start()

    logger.info("Бот запущен. Нажмите Ctrl+C для остановки.")

    # Запуск polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
