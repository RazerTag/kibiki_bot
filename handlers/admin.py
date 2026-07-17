import os
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states import AddEventStates
from csv_utils import (
    save_event, set_user_points,
    delete_event, edit_event,
    add_user, delete_user, get_all_users
)

router = Router()

# Helper to check admin rights
def is_admin(user_id: int) -> bool:
    admin_env = os.getenv("ADMIN_ID", "")
    ADMIN_IDS = {int(uid) for uid in admin_env.split(',') if uid.strip().isdigit()}
    return user_id in ADMIN_IDS

# --- Event creation flow ---
@router.message(Command("addevent"))
async def addevent_start(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return await message.answer("🚫 У вас нет прав администратора.")
    await state.set_state(AddEventStates.name)
    await message.answer("✏️ Введите название события:", parse_mode="Markdown")

@router.message(AddEventStates.name)
async def addevent_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddEventStates.date)
    await message.answer("📅 Введите дату события (YYYY-MM-DDTHH:MM:SS):", parse_mode="Markdown")

@router.message(AddEventStates.date)
async def addevent_date(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text)
    await state.set_state(AddEventStates.location)
    await message.answer("📍 Введите локацию события:", parse_mode="Markdown")

@router.message(AddEventStates.location)
async def addevent_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)
    await state.set_state(AddEventStates.points)
    await message.answer("🏅 Введите количество баллов за событие:", parse_mode="Markdown")

@router.message(AddEventStates.points)
async def addevent_points(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("⚠️ Баллы должны быть числом. Введите заново:", parse_mode="Markdown")
    data = await state.get_data()
    event_id = save_event(
        name=data['name'],
        date=data['date'],
        location=data['location'],
        points=int(message.text)
    )
    await message.answer(f"✅ Событие #{event_id} успешно создано!", parse_mode="Markdown")
    await state.clear()

# --- Points management ---
@router.message(Command("setpoints"))
async def setpoints_handler(message: types.Message):
    if not is_admin(message.from_user.id):
        return await message.answer("🚫 У вас нет прав администратора.")
    parts = message.text.split()
    if len(parts) != 3 or not parts[1].isdigit() or not parts[2].isdigit():
        return await message.answer("Использование: /setpoints <user_id> <points>")
    user_id, points = int(parts[1]), int(parts[2])
    set_user_points(user_id, points)
    await message.answer(f"✅ Баллы пользователя `{user_id}` установлены в *{points}*.", parse_mode="Markdown")

# --- Event deletion and editing ---
@router.message(Command("deleteevent"))
async def deleteevent_handler(message: types.Message):
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

@router.message(Command("editevent"))
async def editevent_handler(message: types.Message):
    if not is_admin(message.from_user.id):
        return await message.answer("🚫 У вас нет прав администратора.")
    parts = message.text.split(maxsplit=3)
    if len(parts) != 4 or not parts[1].isdigit():
        return await message.answer(
            "Использование: /editevent <event_id> <name|date|location|points> <новое значение>"
        )
    eid, field, new = int(parts[1]), parts[2].lower(), parts[3].strip()
    kwargs = {}
    if field == 'name':
        kwargs['name'] = new
    elif field == 'date':
        kwargs['date'] = new
    elif field == 'location':
        kwargs['location'] = new
    elif field == 'points' and new.isdigit():
        kwargs['points'] = int(new)
    else:
        return await message.answer("Поле должно быть одним из: name, date, location, points.")
    if edit_event(eid, **kwargs):
        await message.answer(f"✅ Событие #{eid} обновлено: {field} → {new}")
    else:
        await message.answer(f"⚠️ Событие #{eid} не найдено или не изменилось.")

# --- User management ---
@router.message(Command("adduser"))
async def adduser_handler(message: types.Message):
    if not is_admin(message.from_user.id):
        return await message.answer("🚫 Нет прав администратора.")
    parts = message.text.split(maxsplit=4)
    if len(parts) != 5 or not parts[1].isdigit():
        return await message.answer("Использование: /adduser <user_id> <username> <first_name> <last_name>")
    uid = int(parts[1])
    username, fn, ln = parts[2], parts[3], parts[4]
    add_user(uid, username, fn, ln)
    await message.answer(f"✅ Пользователь `{uid}` добавлен.", parse_mode="Markdown")

@router.message(Command("removeuser"))
async def removeuser_handler(message: types.Message):
    if not is_admin(message.from_user.id):
        return await message.answer("🚫 Нет прав администратора.")
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        return await message.answer("Использование: /removeuser <user_id>")
    uid = int(parts[1])
    if delete_user(uid):
        await message.answer(f"✅ Пользователь `{uid}` удалён.", parse_mode="Markdown")
    else:
        await message.answer(f"⚠️ Пользователь `{uid}` не найден.")

@router.message(Command("listusers"))
async def listusers_handler(message: types.Message):
    if not is_admin(message.from_user.id):
        return await message.answer("🚫 Нет прав администратора.")
    users = get_all_users()
    if not users:
        return await message.answer("📋 Список пользователей пуст.")
    lines = ["📋 *Список пользователей:*"]
    for u in users:
        uid  = u['user_id']
        fn   = u['first_name']
        ln   = u['last_name']
        grp  = u.get('group', '')
        if grp:
            lines.append(f"- `{uid}`: {fn} {ln} (группа: {grp})")
        else:
            lines.append(f"- `{uid}`: {fn} {ln}")
    await message.answer("\n".join(lines), parse_mode="Markdown")
