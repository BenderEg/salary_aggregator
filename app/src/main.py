import asyncio

from containers.container import Container
from handlers import salary


async def main():
    container = Container()
    container.init_resources()
    container.wire(modules=["handlers.salary"])
    container.dp().include_router(salary.router)
    await container.bot().delete_webhook(drop_pending_updates=True)
    await container.dp().start_polling(container.bot())

if __name__ == "__main__":
    asyncio.run(main())