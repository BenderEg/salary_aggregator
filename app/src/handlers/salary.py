from aiogram import Router
from aiogram.types import Message
from dependency_injector.wiring import Provide, inject

from containers.container import Container
from exeptions.base import WrongDataError
from models.filters import TextFilter
from services.mongo_service import MongoService

router: Router = Router()

@router.message(TextFilter())
@inject
async def aggregate_salary(message: Message,
                           msg: str,
                           service: MongoService = Provide[Container.mongo_service]
                           ) -> None:
    try:
        result = await service.get_avarage_salary(msg)
        await message.answer(text=result)
    except WrongDataError:
        await message.answer(text="Неверный формат данных!")