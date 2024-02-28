from aiogram import Bot, Dispatcher
from dependency_injector import containers, providers

from core.config import Settings


class Container(containers.DeclarativeContainer):
    settings: providers.Singleton[Settings] = providers.Singleton(Settings)
    bot: providers.Singleton[Bot] = providers.Singleton(Bot, settings().token)
    dp: providers.Singleton[Dispatcher] = providers.Singleton(Dispatcher)
