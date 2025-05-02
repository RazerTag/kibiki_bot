from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from handlers.events import list_events
from handlers.checkin import checkin_start
from handlers.ranking import balance_handler, history_handler
from handlers.announcements import view_announcements, announce_start
from handlers.admin import addevent_start
from handlers.registration import help_handler

router = Router()

# Главное меню
@router.message(F.text == "🔍 События")
async def btn_events(message: types.Message):
    await list_events(message)

@router.message(F.text == "✅ Отметиться")
async def btn_checkin(message: types.Message):
    await checkin_start(message)

@router.message(F.text == "📊 Мой баланс")
async def btn_balance(message: types.Message):
    await balance_handler(message)

@router.message(F.text == "📜 Моя история")
async def btn_history(message: types.Message):
    await history_handler(message)

@router.message(F.text == "📢 Объявления")
async def btn_announcements(message: types.Message):
    await view_announcements(message)

@router.message(F.text == "❔ Помощь")
async def btn_help(message: types.Message):
    await help_handler(message)

# Админ-меню
@router.message(F.text == "➕ Добавить событие")
async def btn_add_event(message: types.Message, state: FSMContext):
    await addevent_start(message, state)

@router.message(F.text == "🗑 Удалить событие")
async def btn_delete_event(message: types.Message):
    await message.answer(
        "❓ Введите команду `/deleteevent <event_id>` для удаления события.",
        parse_mode="Markdown"
    )

@router.message(F.text == "✏️ Редактировать событие")
async def btn_edit_event(message: types.Message):
    await message.answer(
        "❓ Введите команду `/editevent <event_id> <поле> <новое значение>` для редактирования события.",
        parse_mode="Markdown"
    )

@router.message(F.text == "✉️ Новое объявление")
async def btn_new_announce(message: types.Message, state: FSMContext):
    await announce_start(message, state)

# 🧑‍🎓 Добавить участника
@router.message(F.text == "🧑‍🎓 Добавить участника")
async def btn_add_user(message: types.Message):
    # здесь мы просто перенаправляем на командный хендлер
    from handlers.admin import adduser_handler
    await adduser_handler(message)

# 🚫 Удалить участника
@router.message(F.text == "🚫 Удалить участника")
async def btn_remove_user(message: types.Message):
    from handlers.admin import removeuser_handler
    await removeuser_handler(message)

# 📋 Список участников
@router.message(F.text == "📋 Список участников")
async def btn_list_users(message: types.Message):
    from handlers.admin import listusers_handler
    await listusers_handler(message)