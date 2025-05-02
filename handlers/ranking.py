from aiogram import Router, types
from aiogram.filters import Command
from csv_utils import get_user_points, get_user_history, get_all_events
from datetime import datetime

router = Router()

@router.message(Command("balance"))
async def balance_handler(message: types.Message):
    """
    Handle /balance command: show user's current points balance.
    """
    user_id = message.from_user.id
    points = get_user_points(user_id)
    await message.answer(f"🏅 Your current balance: *{points}* points", parse_mode="Markdown")

@router.message(Command("history"))
async def history_handler(message: types.Message):
    """
    Handle /history command: show user's check-in history.
    """
    user_id = message.from_user.id
    history = get_user_history(user_id)
    if not history:
        await message.answer("📜 Your history is empty.")
        return

    # Build event lookup
    events = get_all_events()
    events_map = {ev['event_id']: ev for ev in events}

    lines = ["📜 *Your check-in history:*\n"]
    # Sort history by timestamp ascending
    parsed = []
    for record in history:
        try:
            ts = datetime.fromisoformat(record['timestamp'])
        except Exception:
            ts = None
        parsed.append((ts, record))
    parsed_sorted = sorted(parsed, key=lambda x: x[0] or datetime.min)

    for ts, record in parsed_sorted:
        ev = events_map.get(record['event_id'])
        name = ev['name'] if ev else f"Event {record['event_id']}"
        date = record['timestamp']
        lines.append(f"- *{name}* at `{date}` UTC")

    text = "\n".join(lines)
    await message.answer(text, parse_mode="Markdown")