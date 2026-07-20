from pydantic import BaseModel


class EntityRequest(BaseModel):
    document_id: str

class EntityResponse(BaseModel):
    message: str
    entities: dict[str, list[str]]