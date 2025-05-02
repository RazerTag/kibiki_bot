import os
from aiogram import Router, types
from aiogram.filters import Command
from keyboards import main_menu, admin_menu
from csv_utils import get_user_group

router = Router()

# Parse ADMIN_IDs from environment
_admin_ids = os.getenv("ADMIN_ID", "")
ADMIN_IDS = {int(uid) for uid in _admin_ids.split(',') if uid.strip().isdigit()}

@router.message(Command("start"))
async def start_handler(message: types.Message):
    """
    Handle /start command: greet the user and show appropriate menu.
    """
    welcome_text = (
        "👋 Добро пожаловать в Kibiki Bot!\n"
        "Этот бот предназначен для учёта и управления вашими Кибиками.\n"
        "Отмечайтесь на события, получайте Кибики и следите за своим балансом."
    )
    user_id = message.from_user.id
    # Show group if set
    group = get_user_group(user_id)
    if group:
        welcome_text += f"\n👥 Ваша группа: {group}"
    kb = admin_menu if user_id in ADMIN_IDS else main_menu
    await message.answer(welcome_text, reply_markup=kb)

@router.message(Command("help"))
async def help_handler(message: types.Message):
    """
    Handle /help command: show available commands and appropriate menu.
    """
    help_text = (
        "Используйте кнопки меню или команды:\n"
        "/start — Начать работу\n"
        "/menu — Показать меню\n"
        "/events — Список событий\n"
        "/checkin — Отметиться на событии\n"
        "/balance — Показать ваш баланс\n"
        "/history — Ваша история чек-инов\n"
        "/cancel — Отменить текущее действие"
    )
    user_id = message.from_user.id
    # Show group if set
    group = get_user_group(user_id)
    if group:
        help_text += f"\n👥 Ваша группа: {group}"
    kb = admin_menu if user_id in ADMIN_IDS else main_menu
    await message.answer(help_text, reply_markup=kb)
