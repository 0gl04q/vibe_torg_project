from aiogram.fsm.state import State, StatesGroup

'''
    Файл для установки стадий разных конечных автоматов
'''


class Menu(StatesGroup):
    main = State()


class CreateOrder(StatesGroup):
    send_url = State()


class CheckOrder(StatesGroup):
    select_order = State()
    confirm_order = State()
