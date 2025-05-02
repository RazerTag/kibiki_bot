from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from csv_utils import get_all_events, add_history, increment_user_points

router = Router()

@router.message(Command("checkin"))
async def checkin_start(message: types.Message):
    """
    Start check-in flow: show list of upcoming events to the user.
    """
    events = get_all_events()
    if not events:
        await message.answer("🚫 There are no events available at the moment.")
        return

    markup = InlineKeyboardMarkup(row_width=1)
    for ev in events:
        btn_text = f"{ev['name']} — {ev['date']}"
        callback_data = f"checkin:{ev['event_id']}"
        markup.add(InlineKeyboardButton(text=btn_text, callback_data=callback_data))

    await message.answer("📌 Select an event to check in:", reply_markup=markup)

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
    for ev in events:
        if int(ev['event_id']) == event_id:
            points_awarded = int(ev['points'])
            break
    increment_user_points(user_id, points_awarded)

    # Acknowledge and remove buttons
    await call.message.edit_reply_markup(None)
    await call.message.answer(
        f"✅ You have checked in to *{ev['name']}* and earned *{points_awarded}* points!", 
        parse_mode="Markdown"
    )
    await call.answer()
