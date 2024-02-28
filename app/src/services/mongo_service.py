from datetime import datetime, timedelta
from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection


class MongoService:
    def __init__(self, client: AsyncIOMotorClient) -> None:  # type: ignore
        self.client = client
        self.db = self.client["dump"]
        self.sample: Collection = self.db["sample_collection"]

    async def get_avarage_salary(self,
                                 dt_from: datetime,
                                 dt_upto: datetime,
                                 group_type: str
                                 ) -> str:
        match group_type:
            case "month":
                diff = dt_upto.month - dt_from.month
                dates = [(dt_from.replace(day=1)+timedelta(days=31*n)).replace(day=1) \
                         for n in range(diff+2)]
        dataset = []
        for i in range(1, len(dates)):
            end = dates[i]
            start = dates[i-1]
            cursor = self.sample.aggregate([
                {"$match":
                {
                    "dt": {"$gte": start, "$lt": end}
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
                dataset.append(document.get("total_salary"))
            except StopAsyncIteration:
                dataset.append(0)
        print(dataset)

@lru_cache()
def get_mongo_service(client: AsyncIOMotorClient) -> MongoService: # type: ignore
    return MongoService(client)