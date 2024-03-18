from aiogram.filters.callback_data import CallbackData


class CarInfoCallbackFactory(CallbackData, prefix="car"):
    action: str
    field: str


class CarListCallbackFactory(CallbackData, prefix="car"):
    action: str
    car_hash: str
    page: int
    field: str
