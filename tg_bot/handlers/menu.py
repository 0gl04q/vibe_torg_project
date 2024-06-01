from aiogram import types
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from service import requests
from keyboards import for_menu
from filters.chat_filter import ChatTypeFilter

router = Router()

router.message.filter(
    ChatTypeFilter(chat_type=['private'])
)


@router.message(StateFilter(None), Command("start"))
async def cmd_start(message: types.Message):
    """ Запуск основного меню """

    await requests.create_buyer(message.from_user)

    await message.answer("""
Добро пожаловать в наш магазин! 🛍️

Чем могу помочь?
        
🛒 Сделать заказ
📦 Проверить заказы
        
Если у вас возникли вопросы или нужна помощь, обратитесь к команде поддержки.
        
Желаем приятных покупок! 🌟""", reply_markup=for_menu.keyboard_menu())


@router.message(Command("cancel"))
@router.message(F.text.lower() == '🔄 отмена')
async def cmd_cancel(message: types.Message, state: FSMContext):
    await message.answer(
        text="❌ Действие отменено",
        reply_markup=for_menu.keyboard_menu()
    )

    await state.clear()
    