from aiogram.filters import MagicData
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router

router = Router()
router.message.filter(MagicData(F.maintenance_mode.is_(True)))
router.callback_query.filter(MagicData(F.maintenance_mode.is_(True)))


@router.message()
async def any_message(message: Message):
    await message.answer("Бот в режиме обслуживания. Пожалуйста, подождите.")


@router.callback_query()
async def any_callback(callback: CallbackQuery):
    await callback.answer(
        text="Бот в режиме обслуживания. Пожалуйста, подождите",
        show_alert=True
    )
