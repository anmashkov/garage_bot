import os

from dotenv import load_dotenv

load_dotenv()

REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_PORT = os.getenv('REDIS_PORT')
TOKEN = os.getenv('TOKEN')

required_fields = {
    'mark': "марка",
    'model': "модель",
    'number': "номер",
    'year': "год выпуска",
    'color': "цвет",
    'mileage': "пробег",
    'date_exit': "дата выезда"
}

CAR_LIST_ONPAGE = 5

car_info_tpl = "\n\nМарка: Toyota\nМодель: Camry\nНомер: А123АА\nГод выпуска: 2015\nЦвет: белый\nПробег: 80000\nДата выезда: 1 d - дней, w - недель"
