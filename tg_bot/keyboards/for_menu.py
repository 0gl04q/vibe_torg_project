from aiogram import types


def keyboard_menu():
    kb = [
        [types.KeyboardButton(text="🛒 Сделать заказ"),
         types.KeyboardButton(text="📦 Проверить заказы")]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите дальнейшее действие'
    )

    return keyboard
