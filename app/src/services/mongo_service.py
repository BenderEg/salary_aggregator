import asyncio

from datetime import datetime, timedelta
from json import dumps, loads, JSONDecodeError
from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import ValidationError
from pymongo.collection import Collection

from exeptions.base import WrongDataError
from models.schemas import InputData


class MongoService:
    def __init__(self, client: AsyncIOMotorClient) -> None:  # type: ignore
        self.client = client
        self.db = self.client["dump"]
        self.sample: Collection = self.db["sample_collection"]

    async def get_avarage_salary(self, msg: str) -> str:
        try:
            data = InputData(**loads(msg))
        except (ValidationError, JSONDecodeError):
            raise WrongDataError()
        dt_from, dt_upto = data.dt_from, data.dt_upto
        match data.group_type:
            case "month":
                diff = dt_upto.month - dt_from.month
                dates = [(dt_from.replace(day=1)+timedelta(days=31*n)).replace(day=1) \
                         for n in range(diff+2)]
            case "day":
                diff = (dt_upto - dt_from).days
                dates = [dt_from.replace(hour=0, minute=0)+timedelta(days=n) for n in range(diff+2)]
            case "hour":
                prep = dt_upto.replace(minute=0) - dt_from.replace(minute=0)
                diff = prep.days*24+prep.seconds//(60*60)
                dates = [dt_from.replace(minute=0)+timedelta(hours=n) for n in range(diff+2)]
        dates[0] = dt_from
        dates[-1] = dt_upto
        tasks = []
        for i in range(1, len(dates)):
            end = dates[i]
            start = dates[i-1]
            tasks.append(asyncio.create_task(self.aggregate(start, end)))
        dataset = await asyncio.gather(*tasks)
        return dumps({
            "dataset": dataset,
            "labels": [ele.isoformat() for ele in dates[:-1]]
        })

    async def aggregate(self, dt_from: datetime, dt_upto: datetime) -> int:
        cursor = self.sample.aggregate([
                {"$match":
                {
                    "dt": {"$gte": dt_from, "$lt": dt_upto}
                }
                },
                {
                    "$group": {
                        "_id": {"$dateToString": {"format": "%Y-%m", "date": "$dt" } },
                        "total_salary": {"$sum": "$value"}
                    }
                },
            ]
            )
        try:
            document: dict = await cursor.next()
            return document.get("total_salary")
        except StopAsyncIteration:
            return 0

@lru_cache()
def get_mongo_service(client: AsyncIOMotorClient) -> MongoService: # type: ignore
    return MongoService(client)