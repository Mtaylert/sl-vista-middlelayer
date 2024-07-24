from pydantic import BaseModel

from typing import Optional, List, Union


class RecommendationInput(BaseModel):
    prediction_label: str
    recommendation_instruction: Optional[Union[str, List[str]]]


class RecommendationResponse(BaseModel):
    status: str = "received"


class RecommendationMessaging(BaseModel):
    label: str
    message: str
    timestamp: str


class RecommendationOutput(BaseModel):
    current_recommendations: List[RecommendationMessaging]
