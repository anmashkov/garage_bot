import datetime
import hashlib

from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from src.conifg import car_info_tpl, required_fields
from src.callback_fabs import CarInfoCallbackFactory, CarListCallbackFactory
from src.handlers import cmd_list
from src.keyboards import car_info, kb_car_list, car_fields_edit, car_info_edit, delete_car
from src.service import get_car_info_message, get_car_list
from src.states import CarInfoCreate

router = Router()


@router.callback_query(CarInfoCreate.await_info, CarInfoCallbackFactory.filter())
async def choosing_char_race_fab(
        callback: types.CallbackQuery,
        callback_data: CarInfoCallbackFactory,
        state: FSMContext
):
    match callback_data.action:
        case 'void':
            await callback.answer()
            return
        case 'info':
            data = await state.get_data()
            car = data.get('car_info', {})
            text_message = f"Данные о машине:\n{get_car_info_message(car)}"
            await callback.message.edit_text(text_message, reply_markup=car_info_edit({}))
        case 'edit_field':
            await state.set_state(CarInfoCreate.await_new_value)
            await state.update_data(await_field=callback_data.field)
            await callback.message.answer('Введите новое значение: ')
        case 'edit_fields':
            data = await state.get_data()
            car = data.get('car_info', {})
            text_message = f"Данные о машине:\n{get_car_info_message(car)}"
            await state.update_data(await_field=callback_data.field)
            await callback.message.edit_text(text_message, reply_markup=car_fields_edit(car))

        case 'save_car':
            data = await state.get_data()

            car_data = data.get('car_info', {})
            car_data['date_enter'] = str(datetime.date.today())
            car_list = data.get('car_list', {})

            if len(car_data) != (len(required_fields) + 1):
                await callback.answer('Не все поля заполненны!')
                return

            hash_object = hashlib.md5((car_data['number']).encode())

            car_list[hash_object.hexdigest()] = car_data

            await state.update_data(car_info={})
            await state.update_data(car_list=car_list)
            await state.set_state(CarInfoCreate.await_action)
            await cmd_list(callback.message, state)

    await callback.answer()


@router.callback_query(CarInfoCreate.await_action, CarListCallbackFactory.filter())
async def choosing_char_race_fab(
        callback: types.CallbackQuery,
        callback_data: CarListCallbackFactory,
        state: FSMContext
):
    match callback_data.action:
        case 'void':
            pass

        case 'next':
            car_list, total_page = await get_car_list(state, callback_data.page + 1)
            await callback.message.edit_text('Список машин:',
                                             reply_markup=kb_car_list(car_list, total_page, callback_data.page + 1))

        case 'prev':
            car_list, total_page = await get_car_list(state, callback_data.page - 1)
            await callback.message.edit_text('Список машин:',
                                             reply_markup=kb_car_list(car_list, total_page, callback_data.page - 1))

        case 'list':
            car_list, total_page = await get_car_list(state, callback_data.page)
            await callback.message.edit_text('Список машин:',
                                             reply_markup=kb_car_list(car_list, total_page, callback_data.page))

        case 'add_car':
            await state.set_state(CarInfoCreate.await_info)
            await callback.message.answer(f"Шаблон данных:")
            await callback.message.answer(car_info_tpl)
            await callback.message.answer('Введите информацию о машине: ')

        case 'view_car':
            data = await state.get_data()

            car_list = data.get('car_list', {})
            car = car_list.get(callback_data.car_hash, False)

            if not car:
                await callback.answer('Машина с данным номером не найдена в базе')
                await callback.answer()
                return

            text_message = get_car_info_message(car)

            await callback.message.edit_text(f'Ифнормация о машине: {text_message}',
                                             reply_markup=car_info(callback_data.car_hash, callback_data.page))
        case 'delete_car':
            await callback.message.edit_text(f'Вы уверены?', reply_markup=delete_car(callback_data.car_hash, callback_data.page))
        case 'confirm_delete':
            data = await state.get_data()

            car_list = data.get('car_list', {})
            car_list.pop(callback_data.car_hash, None)

            await state.update_data(car_list=car_list)

            await callback.answer(f'Машина удалена')

            car_list, total_page = await get_car_list(state, )
            await callback.message.edit_text('Список машин:',
                                             reply_markup=kb_car_list(car_list, total_page, callback_data.page))

    await callback.answer()
