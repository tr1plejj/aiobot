from aiogram.fsm.state import StatesGroup, State


class Offer(StatesGroup):
    id = State()
    address = State()
    is_confirmed = State()
