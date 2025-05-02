from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Меню для пользователя
user_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("📊 Мой баланс"), KeyboardButton("📜 Моя история")],
        [KeyboardButton("📢 Объявления")],
    ],
    resize_keyboard=True
)

# Меню для администратора
admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("➕ Начислить Кибики"), KeyboardButton("➖ Списать Кибики")],
        [KeyboardButton("🔍 Баланс студента"), KeyboardButton("🗃 История студента")],
        [KeyboardButton("🧑‍🎓 Добавить студента"), KeyboardButton("❌ Удалить студента")],
        [KeyboardButton("📢 Новое объявление"), KeyboardButton("🧹 Удалить объявление")],
        [KeyboardButton("📊 Мой баланс"), KeyboardButton("📜 Моя история"), KeyboardButton("📢 Объявления")],
    ],
    resize_keyboard=True
)
