from aiogram import types
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from handlers.menu import cmd_start
from keyboards.order_keyboard import cancel_menu
from keyboards import for_menu
from filters.chat_filter import ChatTypeFilter
from states import CreateOrder
from filters.order_filter import UrlFilter
from service import functions, requests

router = Router()

router.message.filter(
    ChatTypeFilter(chat_type=['private'])
)


@router.message(StateFilter(None), F.text.lower() == '🛒 сделать заказ')
async def make_order(message: types.Message, state: FSMContext):
    """ Выбор сделать заказ """

    await message.answer('💬 Пришлите URL ссылку на товар который желаете преобрести', reply_markup=cancel_menu())
    await state.set_state(CreateOrder.send_url)


@router.message(CreateOrder.send_url, UrlFilter())
async def get_url(message: types.Message, state: FSMContext):
    """ Функция для обработки URL и передачи заказа в БД """

    user = message.from_user

    # Собираем URL
    url = await functions.get_url(message.text)

    # Передаем заказ в БД
    await requests.create_order(user, url, message)

    await state.clear()


@router.message(CreateOrder.send_url)
async def less_send(message: types.Message):
    await message.answer(text='❌ Не верно передан URL повторите отправку')
