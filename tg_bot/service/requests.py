import aiohttp
import json
import logging
from aiogram import types
from keyboards import for_menu

logger = logging.getLogger(__name__)


async def create_buyer(user: types.User) -> bool:
    """ Функция для создания покупателя в базе данных """

    async with aiohttp.ClientSession() as session:
        async with session.post(url=f'http://127.0.0.1:8000/api/buyer/create/',
                                data={'tg_id': user.id, 'nickname': f'@{user.username}'}) as response:
            return response.status == 201


async def create_order(user: types.User, url: str, message: types.Message) -> None:
    """ Функция передачи заказа в БД по запросу """
    async with aiohttp.ClientSession() as session:

        data = {'buyer': user.id, 'link': url}

        async with session.post(url='http://127.0.0.1:8000/api/order/create/', data=data) as response:
            if response.status == 201:
                await message.answer(
                    text='Спасибо!🌟 Мы зафиксировали ваш заказ и начали его обрабатывать. '
                         'В ближайшее время с вами свяжутся!📦',
                    reply_markup=for_menu.keyboard_menu())
            else:
                await message.answer(
                    text='❌ Упс! Обнаружена ошибка, фиксируем для исправления. Обратитесь в наш сервис позже.',
                    reply_markup=for_menu.keyboard_menu())
                logger.error(f'{user.id}, data: {data}')

            logger.info(f'{user.id}, status: {response.status}, url: {url}')


async def list_orders(user: types.User) -> list | bool:
    """ Функция получения активных заказов пользователя из БД по запросу """

    async with aiohttp.ClientSession() as session:
        async with session.get(url=f'http://127.0.0.1:8000/api/order/{user.id}/') as response:
            if response.status == 200:
                text = await response.text()
                logger.info(f'{user.id}, status: {response.status}, list: {text}')
                return json.loads(text)
            else:
                logger.error(f'{user.id}, status: {response.status}')
                return False


async def get_order(user: types.User, order_id: str) -> dict | bool:
    """ Функция получения заказа пользователя из БД по запросу """

    async with aiohttp.ClientSession() as session:
        async with session.get(url=f'http://127.0.0.1:8000/api/order/{user.id}/{order_id}/') as response:
            if response.status == 200:
                text = await response.text()
                logger.info(f'{user.id}, status: {response.status}, order: {text}')
                return json.loads(text)
            else:
                logger.error(f'{user.id}, status: {response.status}')
                return False


async def update_order(user: types.User, order_id: str, key: str, value: str) -> bool:
    """ Функция для изменения параметров заказа"""

    async with aiohttp.ClientSession() as session:
        async with session.patch(url=f'http://127.0.0.1:8000/api/order/{user.id}/{order_id}/',
                                 data={key: value}) as response:
            return response.status == 200
