from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from csv_utils import get_all_events, add_history, increment_user_points

router = Router()

@router.message(Command("checkin"))
async def checkin_start(message: types.Message):
    """
    Start check-in flow: show list of upcoming events to the user.
    """
    events = get_all_events()
    if not events:
        await message.answer("🚫 На данный момент нет доступных событий.")
        return

    builder = InlineKeyboardBuilder()
    for ev in events:
        btn_text = f"{ev['name']} — {ev['date']}"
        callback_data = f"checkin:{ev['event_id']}"
        builder.button(text=btn_text, callback_data=callback_data)
    builder.adjust(1)

    await message.answer("📌 Выберите событие для регистрации:", reply_markup=builder.as_markup())

@router.callback_query(lambda c: c.data and c.data.startswith("checkin:"))
async def process_checkin(call: types.CallbackQuery):
    """
    Handle user's selection and record check-in + points.
    """
    event_id = int(call.data.split(":")[1])
    user_id = call.from_user.id

    # Record history
    add_history(user_id, event_id)

    # Award points for the event
    events = get_all_events()
    points_awarded = 0
    selected_event = None
    for ev in events:
        if int(ev['event_id']) == event_id:
            selected_event = ev
            points_awarded = int(ev['points'])
            break
    if selected_event is None:
        await call.answer("Event not found.", show_alert=True)
        return
    increment_user_points(user_id, points_awarded)

    # Acknowledge and remove buttons
    await call.message.edit_reply_markup(None)
    await call.message.answer(
        f"✅ Вы отметились в *{selected_event['name']}* и заработали *{points_awarded}* баллов!",
        parse_mode="Markdown"
    )
    await call.answer()
