import asyncio
import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from middlewares.registration_middleware import RegistrationMiddleware
from csv_utils import init_csv_files
from scheduler_tasks import send_upcoming_events

# Подключаем роутеры (обработчики команд)
from handlers.registration import router as registration_router
from handlers.checkin import router as checkin_router
from handlers.events import router as events_router
from handlers.ranking import router as ranking_router
from handlers.admin import router as admin_router
from handlers.common import router as common_router
from handlers.announcements import router as announcements_router

async def setup_bot_commands(bot: Bot):
    """
    Устанавливаем список команд, чтобы в Telegram при вводе "/"
    отображалось меню с описаниями.
    """
    commands = [
        BotCommand(command="start", description="Начать регистрацию"),
        BotCommand(command="help", description="Помощь / меню команд"),
        BotCommand(command="events", description="Список мероприятий"),
        BotCommand(command="checkin", description="Отметиться на мероприятии"),
        BotCommand(command="balance", description="Показать ваши баллы"),
        BotCommand(command="history", description="Ваша история чек-инов"),
        BotCommand(command="addevent", description="Добавить событие (админ)"),
        BotCommand(command="setpoints", description="Установить очки (админ)"),
        BotCommand(command="announce", description="Создать объявление (админ)"),
        BotCommand(command="announcements", description="Показать объявления"),
        BotCommand(command="cancel", description="Отменить текущее действие"),
    ]
    await bot.set_my_commands(commands)

async def main():
    # Настройка логирования
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Загрузка переменных окружения
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не найден в .env")
        return

    # Инициализация CSV-файлов
    init_csv_files()

    # Создание бота и диспетчера
    bot = Bot(token=BOT_TOKEN, parse_mode=None)
    dp = Dispatcher(storage=MemoryStorage())

    # Middleware для автоматической регистрации
    dp.message.middleware(RegistrationMiddleware())

    # Регистрация роутеров
    dp.include_router(registration_router)
    dp.include_router(checkin_router)
    dp.include_router(events_router)
    dp.include_router(ranking_router)
    dp.include_router(admin_router)
    dp.include_router(common_router)
    dp.include_router(announcements_router)

    # Установка команд бота
    await setup_bot_commands(bot)

    # Настройка планировщика уведомлений
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_upcoming_events, "interval", hours=1)
    scheduler.start()

    logger.info("Бот запущен. Нажмите Ctrl+C для остановки.")

    # Запуск polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())