from aiogram.fsm.state import StatesGroup, State

class AddEventStates(StatesGroup):
    name = State()
    date = State()
    location = State()
    points = State()