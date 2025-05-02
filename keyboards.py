from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Меню для пользователя
user_menu = ReplyKeyboardMarkup(resize_keyboard=True)
user_menu.add(
    KeyboardButton("📊 Мой баланс"),
    KeyboardButton("📜 Моя история"),
)
user_menu.add(
    KeyboardButton("📢 Объявления"),
)

# Меню для администратора
admin_menu = ReplyKeyboardMarkup(resize_keyboard=True)
admin_menu.add(
    KeyboardButton("➕ Начислить Кибики"),
    KeyboardButton("➖ Списать Кибики"),
)
admin_menu.add(
    KeyboardButton("🔍 Баланс студента"),
    KeyboardButton("🗃 История студента"),
)
admin_menu.add(
    KeyboardButton("🧑‍🎓 Добавить студента"),
    KeyboardButton("❌ Удалить студента"),
)
admin_menu.add(
    KeyboardButton("📢 Новое объявление"),
    KeyboardButton("🧹 Удалить объявление"),
)
admin_menu.add(
    KeyboardButton("📊 Мой баланс"),
    KeyboardButton("📜 Моя история"),
    KeyboardButton("📢 Объявления"),
)