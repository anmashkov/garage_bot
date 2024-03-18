from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.callback_fabs import CarInfoCallbackFactory, CarListCallbackFactory


def car_info_edit(errors):
    builder = InlineKeyboardBuilder()

    for title, value in errors.items():
        builder.button(
            text=value,
            callback_data=CarInfoCallbackFactory(action='void', field=title)
        )
        builder.button(
            text="Изменить",
            callback_data=CarInfoCallbackFactory(action='edit_field', field=title)
        )

    if not errors:
        builder.button(
            text="Сохранить",
            callback_data=CarInfoCallbackFactory(action='save_car', field='')
        )
        builder.button(
            text="Редактировать поля",
            callback_data=CarInfoCallbackFactory(action='edit_fields', field='')
        )

    builder.adjust(2)

    return builder.as_markup()


def car_fields_edit(fields):
    builder = InlineKeyboardBuilder()

    for title, value in fields.items():
        builder.button(
            text=value,
            callback_data=CarInfoCallbackFactory(action='void', field=title)
        )
        builder.button(
            text="Изменить",
            callback_data=CarInfoCallbackFactory(action='edit_field', field=title)
        )

    builder.button(
        text="Назад",
        callback_data=CarInfoCallbackFactory(action='info', field='')
    )

    builder.adjust(2)

    return builder.as_markup()


def car_data_edit(car, car_hash, page):
    builder = InlineKeyboardBuilder()

    for title, value in car.items():

        if title == 'date_enter':
            continue

        builder.button(
            text=value,
            callback_data=CarListCallbackFactory(action='void', car_hash=car_hash, page=page, field='')
        )
        builder.button(
            text="Изменить",
            callback_data=CarListCallbackFactory(action='edit_field', car_hash=car_hash, page=page, field=title)
        )

    builder.button(
        text="Назад",
        callback_data=CarListCallbackFactory(action='view_car', car_hash=car_hash, page=page, field='')
    )

    builder.adjust(2)

    return builder.as_markup()


def kb_car_list(car_list, total_pages, page=1):

    builder = InlineKeyboardBuilder()

    for car in car_list:
        car_title = f"{car_list[car]['mark']} {car_list[car]['number']}\n"

        builder.button(
            text=car_title,
            callback_data=CarListCallbackFactory(action='void', car_hash=car, page=1, field='')
        )

        builder.button(
            text="Подробнее",
            callback_data=CarListCallbackFactory(action='view_car', car_hash=car, page=page, field='')
        )

        builder.button(
            text="Удалить",
            callback_data=CarListCallbackFactory(action='delete_car', car_hash=car, page=page, field='')
        )

    if page > 1:
        builder.button(
            text='Назад',
            callback_data=CarListCallbackFactory(action='prev', car_hash='', page=page, field='')
        )

    if page < total_pages:
        builder.button(
            text="Вперед",
            callback_data=CarListCallbackFactory(action='next', car_hash='', page=page, field='')
        )

    builder.button(
        text="Добавить новую машину",
        callback_data=CarListCallbackFactory(action='add_car', car_hash='', page=1, field='')
    )

    builder.adjust(3, repeat=True)

    return builder.as_markup()


def kb_car_info(car_hash, page):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Изменить",
        callback_data=CarListCallbackFactory(action='edit_fields', car_hash=car_hash, page=1, field='')
    )

    builder.button(
        text="Назад",
        callback_data=CarListCallbackFactory(action='list', car_hash='', page=page, field='')
    )

    builder.adjust(2)

    return builder.as_markup()


def start_menu():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Добавить новую машину",
        callback_data=CarListCallbackFactory(action='add_car', car_hash='', page=1, field='')
    )

    builder.button(
        text="Список машин",
        callback_data=CarListCallbackFactory(action='list', car_hash='', page=1, field='')
    )

    builder.adjust(2)

    return builder.as_markup()


def delete_car(car_hash, page):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Да, удалить",
        callback_data=CarListCallbackFactory(action='confirm_delete', car_hash=car_hash, page=1, field='')
    )

    builder.button(
        text="Отмена",
        callback_data=CarListCallbackFactory(action='list', car_hash='', page=page, field='')
    )

    builder.adjust(2)

    return builder.as_markup()