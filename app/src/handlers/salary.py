from aiogram import Router
from aiogram.types import Message

from models.filters import TextFilter

router: Router = Router()

@router.message(TextFilter())
async def aggregate_salary(message: Message):

    await message.answer(text=message.text)