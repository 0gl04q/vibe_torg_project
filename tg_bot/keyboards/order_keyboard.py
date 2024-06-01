from aiogram import types

import functools

CANCEL_BUTTON = [types.KeyboardButton(text="🔄 Отмена")]


def standard_keyboard(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        kb = func(*args, **kwargs)
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True
        )
        return keyboard

    return wrapper


@standard_keyboard
def cancel_menu():
    return [CANCEL_BUTTON]


@standard_keyboard
def list_keyboard(order_list):
    return [[types.KeyboardButton(text=order)] for order in order_list] + [CANCEL_BUTTON]


@standard_keyboard
def yes_no_keyboard():
    return [[types.KeyboardButton(text='✅ Да'), types.KeyboardButton(text='❌ Нет')], CANCEL_BUTTON]
