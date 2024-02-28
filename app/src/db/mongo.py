from typing import Generator, Any

from motor.motor_asyncio import AsyncIOMotorClient


def get_mongo_client(connection: str) -> Generator[Any, Any, AsyncIOMotorClient]:  # type: ignore
    mongo_client = AsyncIOMotorClient(connection)
    yield mongo_client
    mongo_client.close()