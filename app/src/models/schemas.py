from datetime import datetime
from typing import Literal

from pydantic import BaseModel, model_validator

from exeptions.base import WrongDataError

class InputData(BaseModel):

    dt_from: datetime
    dt_upto: datetime
    group_type: Literal["hour", "day", "month"]

    @model_validator(mode="after")
    def check_time(self):
        if self.dt_upto <= self.dt_from:
            raise WrongDataError()