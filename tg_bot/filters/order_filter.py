from aiogram.filters import BaseFilter
from aiogram.types import Message
from service import functions


class UrlFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        url = await functions.check_url(message.text)

        return True if url else False

