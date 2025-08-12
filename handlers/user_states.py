from aiogram.fsm.state import State, StatesGroup
class UserStates(StatesGroup):
    initial_state = State()
    choosing_frequency = State()
    choosing_source = State()
    receiving_quotes = State()