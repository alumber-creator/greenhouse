from aiogram.filters.callback_data import CallbackData


class DateModeCallback(CallbackData, prefix="date_mode"):
    action: str  # "single" или "period"


class DateSelectionCallback(CallbackData, prefix="date_sel"):
    action: str  # "select", "confirm"
    year: int
    month: int
    day: int
