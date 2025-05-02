from aiogram import BaseMiddleware
from aiogram.types import Message, Update

from csv_utils import is_user_registered, add_user

class RegistrationMiddleware(BaseMiddleware):
    """
    Middleware for automatic user registration on first interaction.
    If the user is not registered in CSV, add them.
    """
    async def __call__(self, handler, event: Update, data: dict):
        # Extract message object
        message = None
        if isinstance(event, Update) and event.message:
            message = event.message
        elif isinstance(event, Message):
            message = event

        if message:
            user = message.from_user
            if not is_user_registered(user.id):
                add_user(
                    user.id,
                    user.username or "",
                    user.first_name or "",
                    user.last_name or ""
                )
        # Continue to handler
        return await handler(event, data)
