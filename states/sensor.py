from aiogram.fsm.state import StatesGroup, State


class SensorStates(StatesGroup):
    choosing_sensor = State()
    choosing_day = State()
    choosing_start_date = State()
    choosing_end_date = State()
