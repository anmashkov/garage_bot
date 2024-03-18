from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.conifg import car_info_tpl
from src.keyboards import car_info_edit, kb_car_list, start_menu, car_data_edit, kb_car_info
from src.service import get_car_info, get_car_info_message, update_car_info, get_car_list, \
    valid_car_info, valid_field, parse_value
from src.states import CarInfoCreate

router = Router()

cached_info = {}


@router.message(Command(commands=["reset"]))
async def cmd_reset(message: Message, state: FSMContext):
    await state.set_state(CarInfoCreate.await_action)


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.update_data(car_info={})
    car_list, total_pages = await get_car_list(state)

    if not car_list:
        await message.answer(
            text="В базе Гаража пока отсутствует информация о машинах\n"
                 "Введите информацию о машине",
        )
        await message.answer(f"Шаблон данных:")
        await message.answer(car_info_tpl)
        await state.set_state(CarInfoCreate.await_info)
    else:
        await state.set_state(CarInfoCreate.await_action)
        await message.answer('Гараж:', reply_markup=start_menu())


@router.message(CarInfoCreate.await_info)
async def append_car_info(message: Message, state: FSMContext):
    car_info = get_car_info(message.text)
    print(car_info)
    car_data = await update_car_info(state, car_info)
    text_message = f"Данные о машине:\n{get_car_info_message(car_data)}"

    errors = valid_car_info(car_data)

    if errors:
        text_message += f"\n\nНеобхоимо корректно запонить поля:\n{'\n'.join(errors.values())}"
    else:
        await state.set_state(CarInfoCreate.await_info)

    await message.answer(text_message, reply_markup=car_info_edit(errors))


@router.message(CarInfoCreate.await_new_value)
async def choosing_char_name(message: Message, state: FSMContext):
    data = await state.get_data()
    car_info = data.get('car_info', {})
    field = data.get('await_field', None)

    if field:
        if valid_field(field, message.text):
            car_info[field] = parse_value(field, message.text)
            car_data = await update_car_info(state, car_info)
            text_message = f"Данные о машине:\n{get_car_info_message(car_data)}"
            errors = valid_car_info(car_data)
            await message.answer(text_message, reply_markup=car_info_edit(errors))
            await state.set_state(CarInfoCreate.await_info)

        else:
            await message.answer('Введены не корректные данные')


@router.message(CarInfoCreate.await_new_data)
async def choosing_char_name(message: Message, state: FSMContext):
    data = await state.get_data()
    field = data.get('await_field', None)
    car_hash = data.get('car_hash', None)
    car_list = data.get('car_list', {})

    car_info = car_list.get(car_hash, {})

    if field:
        if valid_field(field, message.text):
            car_info[field] = parse_value(field, message.text)
            car_list[car_hash] = car_info
            await state.update_data(car_list=car_list)
            text_message = f"Ифнормация о машине:\n{get_car_info_message(car_info)}"
            await message.answer(text_message, reply_markup=car_data_edit(car_info, car_hash, 1))
            await state.set_state(CarInfoCreate.await_action)
        else:
            await message.answer('Введены не корректные данные')


@router.message(CarInfoCreate.await_info)
async def confirm_car_info(message: Message, state: FSMContext):
    car_info, errors = get_car_info(message.text)

    car_data = await update_car_info(state, car_info)

    text_message = f"Данные о машине:\n{get_car_info_message(car_data)}"

    if errors:
        text_message += f"\n\nНеобхоимо корректно запонить поля:\n{'\n'.join(errors)}"

    await message.answer(text_message)


@router.message(Command(commands=["clear"]))
async def cmd_clear(message: Message, state: FSMContext):
    await state.clear()


@router.message(Command(commands=["list"]))
async def cmd_list(message: Message, state: FSMContext):
    car_list, total_pages = await get_car_list(state)

    await message.answer('Список машин:', reply_markup=kb_car_list(car_list, total_pages=total_pages))


