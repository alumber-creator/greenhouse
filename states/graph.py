from aiogram.fsm.state import State, StatesGroup


class GraphStates(StatesGroup):
    sensor_selected = State()
    date_mode_selected = State()
    single_date_selected = State()
    period_start_selected = State()
    period_end_selected = State()