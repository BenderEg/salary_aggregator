from aiogram import Bot, Dispatcher
from dependency_injector import containers, providers

from core.config import Settings
from db.mongo import get_mongo_client
from services.mongo_service import MongoService


class Container(containers.DeclarativeContainer):
    settings: providers.Singleton[Settings] = providers.Singleton(Settings)
    bot: providers.Singleton[Bot] = providers.Singleton(Bot, settings().token)
    dp: providers.Singleton[Dispatcher] = providers.Singleton(Dispatcher)
    mongo_client = providers.Resource(get_mongo_client,
                                     settings().mongo.connection
                                     )
    mongo_service: providers.Singleton[MongoService] = providers.Singleton(
        MongoService, mongo_client)