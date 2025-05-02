from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главное меню для всех пользователей
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔍 События")],
        [KeyboardButton(text="✅ Отметиться")],
        [
            KeyboardButton(text="📊 Мой баланс"),
            KeyboardButton(text="📜 Моя история")
        ],
        [
            KeyboardButton(text="📢 Объявления"),
            KeyboardButton(text="❔ Помощь")
        ],
    ],
    resize_keyboard=True
)

# Меню администратора
admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕ Добавить событие"),
            KeyboardButton(text="✏️ Редактировать событие")
        ],
        [
            KeyboardButton(text="🗑 Удалить событие"),
            KeyboardButton(text="✉️ Новое объявление")
        ],
        [
            KeyboardButton(text="📊 Баланс"),
            KeyboardButton(text="📜 История")
        ],
        [
            KeyboardButton(text="📢 Объявления"),
            KeyboardButton(text="❔ Помощь")
        ],
        [
            KeyboardButton(text="🧑‍🎓 Добавить участника"),
            KeyboardButton(text="🚫 Удалить участника")
        ],
        [
            KeyboardButton(text="📋 Список участников")
        ],
    ],
    resize_keyboard=True
)
