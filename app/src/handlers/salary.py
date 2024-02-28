from datetime import datetime

from aiogram import Router
from aiogram.types import Message
from dependency_injector.wiring import Provide, inject

from containers.container import Container
from models.filters import TextFilter
from services.mongo_service import MongoService

router: Router = Router()

@router.message(TextFilter())
@inject
async def aggregate_salary(message: Message,
                           msg: str,
                           service: MongoService = Provide[Container.mongo_service]
                           ):
    result = await service.get_avarage_salary(
            datetime.fromisoformat("2022-02-01T00:00:00"),
            datetime.fromisoformat("2022-02-02T00:00:00"),
            "hour"
        )
    await message.answer(text=result)