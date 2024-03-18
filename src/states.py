from aiogram.fsm.state import StatesGroup, State


class CarInfoCreate(StatesGroup):
    await_info = State()
    await_new_value = State()
    await_edit_fields = State()
    await_action = State()