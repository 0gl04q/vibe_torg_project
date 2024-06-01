from aiogram import types, html
from aiogram.enums import ParseMode

from aiogram.utils.formatting import (
    Text, Bold, as_list, as_marked_section, as_key_value, HashTag, TextLink
)

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from states import CheckOrder
from filters.chat_filter import ChatTypeFilter
from service import requests
from keyboards.order_keyboard import list_keyboard, yes_no_keyboard, cancel_menu
from keyboards.for_menu import keyboard_menu

STATUS = {
    "PE": "В ожидании",
    "IP": "Ждем ответ",
    "BA": "На согласовании",
    "PA": "Оплачено",
    "CO": "Выполнен",
    "CA": "Отменен"
}

router = Router()

router.message.filter(
    ChatTypeFilter(chat_type=['private'])
)


@router.message(StateFilter(None), F.text.lower() == '📦 проверить заказы')
async def check_order(message: types.Message, state: FSMContext):
    """ Функция просмотра всех заказов """

    # Получаем заказы
    data_list = await requests.list_orders(message.from_user)

    # Проверяем наличие заказов
    if data_list:
        await message.answer('📋 Ваши заказы:')

        # Печатаем заказы
        for order_dict in data_list:
            content_message = (f"📦 <b>Заказ</b> {order_dict['id'][:8]}"
                               f"\n- <b>Cтатус</b>: {STATUS[order_dict['status']]}"
                               f"\n- <b>Ссылка</b>: <a href='{order_dict['''link''']}'>Ссылка на товар</a>"
                               f"\n\n- <b>Текущя цена</b>: {order_dict['price'] if order_dict['price'] != '0.00' else 'Неизвестна'} 💵")

            await message.answer(text=content_message, parse_mode=ParseMode.HTML)

        # Передаем меню выбора заказа
        order_list_by_kb = [f'{order["id"][:8]}' for order in data_list if order['status'] == 'IP']

        if order_list_by_kb:
            await message.answer('👇 Выберите заказ в меню 👇', reply_markup=list_keyboard(order_list_by_kb))

            # Сохраняем данные и передаем стадию
            await state.set_state(CheckOrder.select_order)
            await state.update_data(order_list=data_list)
        else:
            await state.clear()
    else:
        await message.answer('😔 Список заказов пуст')


@router.message(CheckOrder.select_order, F.text)
async def select_order(message: types.Message, state: FSMContext):
    """ Функция выбора заказа """

    user_data = await state.get_data()
    order_list = user_data['order_list']

    flag = False

    for order in order_list:
        if message.text in order['id']:
            flag = True
            break

    if flag:
        # Получаем заказ
        order_dict = await requests.get_order(message.from_user, message.text)

        # Проверяем существование заказа
        if order_dict:

            # Форматируем статус
            order_status = STATUS[order_dict["status"]]

            # В случае статуса "Передан клиенту" добавляем меню оформления сделки
            if order_status is STATUS['IP']:
                await message.answer('💼 Готовы ли вы перейти к оформлению? 🤝', reply_markup=yes_no_keyboard())
                await state.set_state(CheckOrder.confirm_order)
                await state.update_data(order_dict=order_dict)
        else:
            await message.answer('Такого заказа нет')
    else:
        await message.answer('Выберите номер заказа из меню')


@router.message(CheckOrder.confirm_order, F.text.lower() == '✅ да')
async def confirm_order(message: types.Message, state: FSMContext):
    """ Функция согласия на обработку заказа """

    user_data = await state.get_data()
    order_dict = user_data['order_dict']

    is_updated = await requests.update_order(user=message.from_user,
                                             order_id=order_dict["id"],
                                             key='status',
                                             value='BA')

    if is_updated:
        await message.answer(text=f'<b>Благодарим за подтверждение заказа - {order_dict["id"][:8]}</b> 🎉\n\n'
                                  'В ближайшее время наши специалисты свяжутся с вами для оформления '
                                  'покупки и передачи товара.\n\nСпасибо за выбор нашего магазина! 🛍️',
                             reply_markup=keyboard_menu(), parse_mode=ParseMode.HTML)
        await state.clear()
    else:
        await message.answer(text=f'К сожалению сейчас ответ не дошел, '
                                  f'попробуйте ответить позже', reply_markup=keyboard_menu())
        await state.clear()


@router.message(CheckOrder.confirm_order, F.text.lower() == '❌ нет')
async def cancel_order(message: types.Message, state: FSMContext):
    """ Функция отказа от обработки заказа """

    user_data = await state.get_data()
    order_dict = user_data['order_dict']

    is_updated = await requests.update_order(user=message.from_user,
                                             order_id=order_dict["id"],
                                             key='status',
                                             value='CA')

    if is_updated:
        await message.answer(text='Заказ отменен', reply_markup=keyboard_menu())
        await state.clear()
    else:
        await message.answer(text=f'К сожалению сейчас ответ не дошел, '
                                  f'попробуйте ответить позже', reply_markup=keyboard_menu())
        await state.clear()
