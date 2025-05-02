from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import os

from states import AddEventStates
from csv_utils import save_event, set_user_points, delete_event, edit_event

router = Router()

# Проверка прав администратора через переменную окружения
def is_admin(user_id: int) -> bool:
    admin_env = os.getenv("ADMIN_ID", "")
    ADMIN_IDS = {int(uid) for uid in admin_env.split(',') if uid.strip().isdigit()}
    return user_id in ADMIN_IDS

@router.message(Command("addevent"))
async def addevent_start(message: types.Message, state: FSMContext):
    """
    Запуск FSM-флоу создания события.
    """
    if not is_admin(message.from_user.id):
        await message.answer("🚫 У вас нет прав администратора.")
        return
    await state.set_state(AddEventStates.name)
    await message.answer("✏️ Пожалуйста, введите *название события*:", parse_mode="Markdown")

@router.message(AddEventStates.name)
async def addevent_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddEventStates.date)
    await message.answer(
        "📅 Введите *дату события* в формате ISO (YYYY-MM-DDTHH:MM:SS):",
        parse_mode="Markdown"
    )

@router.message(AddEventStates.date)
async def addevent_date(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text)
    await state.set_state(AddEventStates.location)
    await message.answer("📍 Введите *локацию* события:", parse_mode="Markdown")

@router.message(AddEventStates.location)
async def addevent_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)
    await state.set_state(AddEventStates.points)
    await message.answer("🏅 Введите *количество баллов* за событие:", parse_mode="Markdown")

@router.message(AddEventStates.points)
async def addevent_points(message: types.Message, state: FSMContext):
    pts_text = message.text.strip()
    if not pts_text.isdigit():
        await message.answer(
            "⚠️ Баллы должны быть числом. Пожалуйста, введите *баллы*:",
            parse_mode="Markdown"
        )
        return

# --- Удаление события ---
@router.message(Command("deleteevent"))
async def deleteevent_handler(message: types.Message):
    """
    Удалить событие админом.
    Использование: /deleteevent <event_id>
    """
    if not is_admin(message.from_user.id):
        return await message.answer("🚫 У вас нет прав администратора.")
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        return await message.answer("Использование: /deleteevent <event_id>")
    eid = int(parts[1])
    if delete_event(eid):
        await message.answer(f"✅ Событие #{eid} удалено.")
    else:
        await message.answer(f"⚠️ Событие #{eid} не найдено.")

# --- Редактирование события ---
@router.message(Command("editevent"))
async def editevent_handler(message: types.Message):
    """
    Редактирование полей события. 
    Использование: /editevent <event_id> <name|date|location|points> <new_value>
    """
    if not is_admin(message.from_user.id):
        return await message.answer("🚫 У вас нет прав администратора.")
    parts = message.text.split(maxsplit=3)
    if len(parts) != 4 or not parts[1].isdigit():
        return await message.answer(
            "Использование: /editevent <event_id> "
            "<name|date|location|points> <новое значение>"
        )
    eid = int(parts[1])
    field = parts[2].lower()
    new = parts[3].strip()

    kwargs = {}
    if field == "name":
        kwargs["name"] = new
    elif field == "date":
        kwargs["date"] = new
    elif field == "location":
        kwargs["location"] = new
    elif field == "points" and new.isdigit():
        kwargs["points"] = int(new)
    else:
        return await message.answer(
            "Поле должно быть одним из: name, date, location, points."
        )

    if edit_event(eid, **kwargs):
        await message.answer(f"✅ Событие #{eid} обновлено: {field} → {new}")
    else:
        await message.answer(f"⚠️ Событие #{eid} не найдено или не изменилось.")

    data = await state.get_data()
    name = data["name"]
    date = data["date"]
    location = data["location"]
    points = int(pts_text)

    event_id = save_event(name=name, date=date, location=location, points=points)
    await message.answer(
        f"✅ Событие *{name}* (ID: {event_id}) успешно создано!",
        parse_mode="Markdown"
    )
    await state.clear()

@router.message(Command("setpoints"))
async def setpoints_handler(message: types.Message):
    """
    Установка баллов пользователю администратором.
    Использование: /setpoints <user_id> <points>
    """
    if not is_admin(message.from_user.id):
        await message.answer("🚫 У вас нет прав администратора.")
        return

    parts = message.text.split()
    if len(parts) != 3 or not parts[1].isdigit() or not parts[2].isdigit():
        await message.answer("Использование: /setpoints <user_id> <points>")
        return

    user_id = int(parts[1])
    points = int(parts[2])
    set_user_points(user_id, points)
    await message.answer(
        f"✅ Баллы пользователя `{user_id}` установлены в *{points}*.",
        parse_mode="Markdown"
    )