from aiogram.fsm.state import StatesGroup, State

class AddEventStates(StatesGroup):
    """States for the /addevent FSM: name, date, location, and points steps."""
    name = State()
    date = State()
    location = State()
    points = State()

class AnnounceStates(StatesGroup):
    """States for the /announce FSM: waiting for announcement text."""
    text = State()