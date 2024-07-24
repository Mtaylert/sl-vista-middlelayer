from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


class SalesAchievement(BaseModel):
    category: str
    achieved: bool


class RecommendationAchievement(BaseModel):
    prediction_label: str
    recommendation_instruction: Optional[Union[str, List[str]]]


class RecommendationInput(BaseModel):
    recommendation_checklist: Optional[RecommendationAchievement]
    sales_checklist: Optional[SalesAchievement]


class RecommendationResponse(BaseModel):
    status: str = "received"


class RecommendationMessaging(BaseModel):
    label: str
    message: str
    timestamp: str


class RecommendationOutput(BaseModel):
    current_recommendations: Optional[List[RecommendationMessaging]] = None
    sales_checklist: Optional[Dict[str, bool]] = None
