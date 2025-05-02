from aiogram import Router, types
from aiogram.filters import Command
from csv_utils import get_all_events
from datetime import datetime

router = Router()

@router.message(Command("events"))
async def list_events(message: types.Message):
    """
    Handle /events command: list all upcoming events.
    """
    events = get_all_events()
    if not events:
        await message.answer("🚫 No events available at the moment.")
        return

    # Parse dates and sort events chronologically
    parsed = []
    for ev in events:
        try:
            ev_dt = datetime.fromisoformat(ev['date'])
        except Exception:
            ev_dt = None
        parsed.append((ev_dt, ev))
    # Keep original order for unparsable dates
    parsed_sorted = sorted(parsed, key=lambda x: x[0] or datetime.max)

    # Build response
    lines = ["📅 *Upcoming Events:*\n"]
    for ev_dt, ev in parsed_sorted:
        date_str = ev['date']
        name = ev['name']
        location = ev['location']
        points = ev['points']
        ev_id = ev['event_id']
        lines.append(f"*{ev_id}.* {name} — {date_str} UTC — {location} — {points} pts")

    text = "\n".join(lines)
    await message.answer(text, parse_mode="Markdown")
