import os
from aiogram import Router, types
from aiogram.filters import Command
from keyboards import user_menu, admin_menu

# Initialize router
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
        "👋 Welcome!\n"
        "This bot helps you register for events, check in, and track your points.\n"
        "Use the menu below to get started."
    )
    user_id = message.from_user.id
    # Choose menu based on admin status
    if user_id in ADMIN_IDS:
        await message.answer(welcome_text, reply_markup=admin_menu)
    else:
        await message.answer(welcome_text, reply_markup=user_menu)

@router.message(Command("help"))
async def help_handler(message: types.Message):
    """
    Handle /help command: show available commands.
    """
    help_text = (
        "/start - Start interaction with the bot\n"
        "/events - List upcoming events\n"
        "/checkin - Check in to an event\n"
        "/balance - Show your current points\n"
        "/history - Show your event check-in history\n"
        "/cancel - Cancel current action"
    )
    await message.answer(help_text)
