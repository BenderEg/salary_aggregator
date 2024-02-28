from aiogram.filters import BaseFilter
from aiogram.types import Message

class TextFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text:
            return {'msg': message.text}
        return False