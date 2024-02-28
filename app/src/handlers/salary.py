from aiogram import Router
from aiogram.types import Message


router: Router = Router()

@router.message()
async def aggregate_salary(message: Message):

    await message.answer(text=message.text)