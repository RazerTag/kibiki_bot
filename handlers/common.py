from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from keyboards import main_menu, admin_menu
import os


router = Router()

@router.message(Command("menu"))
async def menu_handler(message: types.Message):
    user_id = message.from_user.id
    admin_env = os.getenv("ADMIN_ID", "")
    ADMIN_IDS = {int(uid) for uid in admin_env.split(',') if uid.strip().isdigit()}
    kb = admin_menu if user_id in ADMIN_IDS else main_menu
    await message.answer("Выберите пункт меню:", reply_markup=kb)

@router.message(Command("cancel"))
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Handle /cancel command: clear any ongoing state and notify the user.
    """
    await state.clear()
    await message.answer(
        "⏹ Операция отменена.",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message()
async def fallback_handler(message: types.Message):
    """
    Catch-all handler for unrecognized messages.
    """
    await message.answer(
        "❓ Я это не понял. Используйте /help, чтобы увидеть доступные команды."
    )

@router.message(Command("setgroup"))
async def setgroup_handler(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) != 2:
        return await message.answer("Использование: /setgroup <название группы>")
    group = parts[1].strip()
    set_user_group(message.from_user.id, group)
    await message.answer(f"✅ Ваша группа установлена: {group}")