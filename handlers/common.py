from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

router = Router()

@router.message(Command("cancel"))
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Handle /cancel command: clear any ongoing state and notify the user.
    """
    await state.clear()
    await message.answer(
        "⏹ Operation canceled.",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message()
async def fallback_handler(message: types.Message):
    """
    Catch-all handler for unrecognized messages.
    """
    await message.answer(
        "❓ I didn't understand that. Use /help to see available commands."
    )
