from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Меню для пользователя
user_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Мой баланс"), KeyboardButton(text="📜 Моя история")],
        [KeyboardButton(text="📢 Объявления")],
    ],
    resize_keyboard=True
)

# Меню для администратора
admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Начислить Кибики"), KeyboardButton(text="➖ Списать Кибики")],
        [KeyboardButton(text="🔍 Баланс студента"), KeyboardButton(text="🗃 История студента")],
        [KeyboardButton(text="🧑‍🎓 Добавить студента"), KeyboardButton(text="❌ Удалить студента")],
        [KeyboardButton(text="📢 Новое объявление"), KeyboardButton(text="🧹 Удалить объявление")],
        [KeyboardButton(text="📊 Мой баланс"), KeyboardButton(text="📜 Моя история"), KeyboardButton(text="📢 Объявления")],
    ],
    resize_keyboard=True
)
