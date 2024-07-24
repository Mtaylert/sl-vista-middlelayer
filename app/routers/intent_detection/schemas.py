from pydantic import BaseModel


class IntentClassification(BaseModel):
    input_chunk: str


class IntentResponse(BaseModel):
    intent_class: str
