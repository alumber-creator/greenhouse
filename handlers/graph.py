from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery

import config.keyboards
from callbacks.graph import DateModeCallback, DateSelectionCallback
from states.graph import GraphStates
from utils.calendar_kb import GraphMenu
from utils.plot import PlotGenerator as pg
from datetime import datetime
from config.keyboards import Keyboard as kb

dp = Router()


@dp.callback_query(F.data == "agro.graph")
async def graph(callback: types.CallbackQuery, state: FSMContext):
    """Обработчик входа в систему графиков"""
    await state.set_state(GraphStates.sensor_selected)
    await callback.message.edit_text(
        "📈 Выберите сенсор для построения графика:",
        reply_markup=await GraphMenu.sensors_menu()
    )
    await callback.answer()


@dp.callback_query(
    GraphStates.sensor_selected,
    F.data.startswith("sensor_")
)
async def handle_sensor_selected(callback: types.CallbackQuery, state: FSMContext):
    sensor_id = callback.data.split("_")[1]
    await state.update_data(sensor_id=sensor_id)
    await state.set_state(GraphStates.date_mode_selected)

    await callback.message.edit_text(
        f"✅ Выбран сенсор: {sensor_id}\n"
        "📊 Выберите тип графика:",
        reply_markup=GraphMenu.date_mode_menu()
    )
    await callback.answer()


@dp.callback_query(DateModeCallback.filter(F.action == "single"))
async def handle_single_date_mode(
        callback: CallbackQuery,
        state: FSMContext
):
    await state.set_state(GraphStates.single_date_selected)
    await callback.message.edit_text(
        "Выберите дату:",
        reply_markup=GraphMenu.calendar_menu(datetime.now().year, datetime.now().month)
    )


@dp.callback_query(DateModeCallback.filter(F.action == "period"))
async def handle_period_date_mode(
        callback: CallbackQuery,
        state: FSMContext
):
    await state.set_state(GraphStates.period_start_selected)
    await state.update_data(period_start=None, period_end=None)
    await callback.message.edit_text(
        "Выберите начало периода:",
        reply_markup=GraphMenu.calendar_menu(datetime.now().year, datetime.now().month)
    )


@dp.callback_query(
    DateSelectionCallback.filter(F.action == "select"),
    GraphStates.single_date_selected
)
async def handle_daily_selection(
        callback: CallbackQuery,
        callback_data: DateSelectionCallback,
        state: FSMContext
):
    data = datetime(
        callback_data.year,
        callback_data.month,
        callback_data.day
    )
    start_date = data.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date.replace(hour=23, minute=59, second=59)

    if end_date < start_date:
        end_date, start_date = start_date, end_date

    await state.update_data(period_end={
        "year": callback_data.year,
        "month": callback_data.month,
        "day": callback_data.day
    })
    await callback.message.edit_text(text="Идёт генерация графика...")
    # Генерация графика
    sensor_data = await state.get_data()
    plot = await pg.generate_plot(
        sensor_id=sensor_data['sensor_id'],
        start_date=start_date,
        end_date=end_date
    )
    await callback.message.delete()
    if plot:
        await callback.message.answer_photo(
            BufferedInputFile(plot.getvalue(), "graph.png")
        )
    else:
        await callback.message.answer("Нет данных за выбранный период")

    await state.clear()


@dp.callback_query(
    DateSelectionCallback.filter(F.action == "select"),
    GraphStates.period_start_selected
)
async def handle_period_start_selection(
        callback: CallbackQuery,
        callback_data: DateSelectionCallback,
        state: FSMContext
):
    await state.update_data(period_start={
        "year": callback_data.year,
        "month": callback_data.month,
        "day": callback_data.day
    })
    await state.set_state(GraphStates.period_end_selected)
    await callback.message.edit_text(
        "Выберите конец периода:",
        reply_markup=GraphMenu.calendar_menu(callback_data.year, callback_data.month)
    )


@dp.callback_query(
    DateSelectionCallback.filter(F.action == "select"),
    GraphStates.period_end_selected
)
async def handle_period_end_selection(
        callback: CallbackQuery,
        callback_data: DateSelectionCallback,
        state: FSMContext
):
    data = await state.get_data()
    start_date = datetime(
        data['period_start']['year'],
        data['period_start']['month'],
        data['period_start']['day']
    )
    end_date = datetime(
        callback_data.year,
        callback_data.month,
        callback_data.day
    )

    if end_date < start_date:
        end_date, start_date = start_date, end_date

    await state.update_data(period_end={
        "year": callback_data.year,
        "month": callback_data.month,
        "day": callback_data.day
    })

    # Генерация графика
    sensor_data = await state.get_data()
    await callback.message.edit_text(text="Идёт генерация графика...")
    plot = await pg.generate_plot(
        sensor_id=sensor_data['sensor_id'],
        start_date=start_date,
        end_date=end_date
    )
    await callback.message.delete()
    if plot:
        await callback.message.answer_photo(
            BufferedInputFile(plot.getvalue(), "graph.png")
        )
    else:
        await callback.message.answer("Нет данных за выбранный период")

    await state.clear()


@dp.callback_query(DateSelectionCallback.filter(F.action == "change_month"))
async def handle_month_change(
        callback: CallbackQuery,
        callback_data: DateSelectionCallback
):
    await callback.message.edit_reply_markup(
        reply_markup=GraphMenu.calendar_menu(
            callback_data.year,
            callback_data.month
        )
    )