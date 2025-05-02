from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import os

from csv_utils import save_announcement, get_all_announcements, get_all_users
from states import AnnounceStates

router = Router()

@router.message(Command("announce"))
async def announce_start(message: types.Message, state: FSMContext):
    admin_env = os.getenv("ADMIN_ID", "")
    ADMIN_IDS = {int(uid) for uid in admin_env.split(',') if uid.strip().isdigit()}
    if message.from_user.id not in ADMIN_IDS:
        return await message.answer("🚫 У вас нет прав администратора.")
    await state.set_state(AnnounceStates.text)
    await message.answer("✏️ Введите текст объявления:", parse_mode="Markdown")

@router.message(AnnounceStates.text)
async def announce_text(message: types.Message, state: FSMContext):
    text = message.text.strip()
    ann_id = save_announcement(text)
    users = get_all_users()
    for u in users:
        try:
            await message.bot.send_message(
                int(u["user_id"]),
                f"📢 *Announcement #{ann_id}:*\n{text}",
                parse_mode="Markdown"
            )
        except:
            pass
    await message.answer(f"✅ Объявление #{ann_id} отправлено всем.")
    await state.clear()

@router.message(Command("announcements"))
async def view_announcements(message: types.Message):
    anns = get_all_announcements()
    if not anns:
        return await message.answer("📭 Пока нет объявлений.")
    lines = ["📢 *Последние объявления:*\n"]
    for row in sorted(anns, key=lambda x: int(x["announcement_id"]), reverse=True)[:5]:
        lines.append(f"#{row['announcement_id']} at `{row['timestamp']}`\n{row['text']}\n")
    await message.answer("\n".join(lines), parse_mode="Markdown")