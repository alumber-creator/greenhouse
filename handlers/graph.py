from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BufferedInputFile

from states.graph import GraphStates
from utils.calendar_kb import GraphMenu
from utils.plot import PlotGenerator as pg
from datetime import datetime

dp = Router()

@dp.message(Command("graph"))
async def cmd_graph(message: types.Message, state: FSMContext):
    await state.set_state(GraphStates.SENSOR_SELECT)
    await message.answer("Select sensor:", reply_markup=await GraphMenu.sensors_menu())


@dp.callback_query(F.data == "back", GraphStates.SENSOR_SELECT)
async def back_to_start(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()


@dp.callback_query(GraphStates.SENSOR_SELECT)
async def sensor_selected(callback: types.CallbackQuery, state: FSMContext):
    sensor_id = callback.data.split(":")[1]
    await state.update_data(sensor_id=sensor_id)
    await state.set_state(GraphStates.YEAR_SELECT)
    await callback.message.edit_text(
        "Select year:",
        reply_markup=await GraphMenu.years_menu()
    )


@dp.callback_query(GraphStates.YEAR_SELECT)
async def year_selected(callback: types.CallbackQuery, state: FSMContext):
    year = int(callback.data.split(":")[1])
    await state.update_data(year=year)
    await state.set_state(GraphStates.MONTH_SELECT)
    await callback.message.edit_text(
        "Select month:",
        reply_markup=await GraphMenu.months_menu(year)
    )


@dp.callback_query(GraphStates.MONTH_SELECT)
async def month_selected(callback: types.CallbackQuery, state: FSMContext):
    month = int(callback.data.split(":")[1])
    data = await state.get_data()
    await state.update_data(month=month)
    await state.set_state(GraphStates.DAY_SELECT)
    await callback.message.edit_text(
        "Select day:",
        reply_markup=await GraphMenu.days_menu(data['year'], month)
    )


@dp.callback_query(GraphStates.DAY_SELECT)
async def day_selected(callback: types.CallbackQuery, state: FSMContext):
    day = int(callback.data.split(":")[1])
    data = await state.get_data()

    try:
        selected_date = datetime(data['year'], data['month'], day)
        plot_buf = await pg.generate_plot(data['sensor_id'], selected_date)

        if plot_buf:
            # Конвертируем BytesIO в BufferedInputFile
            photo = BufferedInputFile(
                file=plot_buf.getvalue(),
                filename=f"graph_{data['sensor_id']}.png"
            )
            await callback.message.answer_photo(photo)
            plot_buf.close()
        else:
            await callback.message.answer("⚠️ No data available for selected date")

    except ValueError as e:
        await callback.message.answer(f"Error: {str(e)}")

    await state.clear()


# Добавляем обработчики для кнопок "Назад"
@dp.callback_query(F.data == "back", GraphStates.YEAR_SELECT)
async def back_to_sensors(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(GraphStates.SENSOR_SELECT)
    await callback.message.edit_text(
        "Select sensor:",
        reply_markup=await GraphMenu.sensors_menu()
    )


@dp.callback_query(F.data == "back", GraphStates.MONTH_SELECT)
async def back_to_years(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(GraphStates.YEAR_SELECT)
    await callback.message.edit_text(
        "Select year:",
        reply_markup=await GraphMenu.years_menu()
    )


@dp.callback_query(F.data == "back", GraphStates.DAY_SELECT)
async def back_to_months(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(GraphStates.MONTH_SELECT)
    data = await state.get_data()
    await callback.message.edit_text(
        "Select month:",
        reply_markup=await GraphMenu.months_menu(data['year'])
    )