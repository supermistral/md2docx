from pydantic import BaseModel, ConfigDict


class BaseDbModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
