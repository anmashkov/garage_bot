import datetime
import itertools
import re
from math import ceil

import pymorphy3

from src.conifg import required_fields, CAR_LIST_ONPAGE


def valid_year(input_year):
    year_pattern = r"^(19\d{2}|20[0-1]\d|202[0-4])$"
    return bool(re.match(year_pattern, input_year))


def valid_car_number(input_number):
    car_number_pattern = r"[АВЕКМНОРСТУХ]\d{3}(?<!000)[АВЕКМНОРСТУХ]{2}"
    return bool(re.match(car_number_pattern, input_number))


def valid_string(input_string):
    string_pattern = r"^[a-zA-Zа-яА-ЯёЁ-]+$"
    return bool(re.match(string_pattern, input_string))


def get_car_info_message(car_data):
    text = (
        "\n"
        f"Марка: \t{car_data.get('mark', 'Строка не должна содержать цифр и быть не длиннее 30 символов')}\n"
        f"Модель: \t{car_data.get('model', 'Строка не должна быть длиннее 10 символов')}\n"
        f"Номер: \t{car_data.get('number', 'В номере допускаются только буквы русского алфавита')}\n"
        f"Год выпуска: \t{car_data.get('year', 'Допустим год от 1900 до 2024')}\n"
        f"Цвет: \t{car_data.get('color', 'Строка не должна содержать цифр  и быть не длиннее 30 символов')}\n"
        f"Пробег: \t{car_data.get('mileage', 'Допустимы только числовые значения')}\n"
        f"Дата выезда: \t{car_data.get('date_exit', 'Допустимы только числовые значения')}\n"
    )

    if car_data.get('date_enter', False):
        text += f"Добавлена: \t{car_data.get('date_enter', '')}"

    return text


def get_car_lsit_message(car_list):
    res = 'Список машин:\n'
    for car in car_list:
        res += f"{car_list[car]['mark']} {car_list[car]['number']}\n"
    return res


def valid_field(name, value):
    match name:
        case 'mileage':
            return value.isnumeric()
        case 'date_exit':
            return len(value) > 0
        case 'year':
            return valid_year(value)
        case 'number':
            return valid_car_number(value)
        case 'model':
            return len(value) < 10
        case _:
            return valid_string(value) and len(value) < 30


def get_car_info(car_data):
    car_info = {}

    for name, title in required_fields.items():
        value = parse_field_value(name, title, car_data)

        if value is not None:
            car_info[name] = value

    return car_info


def parse_field_value(name, title, car_data):
    print(name, title, car_data)
    p = re.compile(fr'{title}:?\s+(?P<{name}>[\wа-яА-Я- ]+)', re.IGNORECASE)
    m = p.search(car_data)

    if m is not None:
        value = m.group(name)

        return parse_value(name, value)


def parse_value(name, value):
    if value is not None:

        if name == 'color':
            value = morf_color(value)

        if name == 'date_exit':
            value = parse_date(value)

        return value.strip()


def morf_color(word):
    word = word.replace(' ', '-')
    morph = pymorphy3.MorphAnalyzer()

    p = morph.parse(word)[0]
    return p.normal_form


def parse_date(date):
    p = re.compile(r'^(?P<num>[0-9]){1,2}\s?(?P<period>[dw])$', re.IGNORECASE)
    m = p.search(date)

    if not bool(m):
        return ''

    num = int(m.group('num'))
    period = m.group('period')

    match period:
        case 'd':
            today = datetime.date.today()
            exit_day = today + datetime.timedelta(days=num)
        case 'w':
            today = datetime.date.today()
            exit_day = today + datetime.timedelta(weeks=num)
        case _:
            exit_day = ''

    return str(exit_day)


def valid_car_info(car_data):
    errors = {}
    for name, value in car_data.items():
        if not valid_field(name, value):
            errors[name] = value

    return errors


async def update_car_info(state, car_info):
    data = await state.get_data()

    car_data = data.get('car_info', {})
    car_data = car_data | car_info

    await state.update_data(car_info=car_data)

    return car_data


async def get_car_list(state, page=1):
    data = await state.get_data()
    car_list = data.get('car_list', {})

    if not car_list:
        return car_list, ceil(len(car_list) // CAR_LIST_ONPAGE)

    list_slice = dict(itertools.islice(car_list.items(), (page - 1) * CAR_LIST_ONPAGE, page * CAR_LIST_ONPAGE))

    return list_slice, ceil(len(car_list) / CAR_LIST_ONPAGE)
