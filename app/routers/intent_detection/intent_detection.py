from fastapi import APIRouter

from app.routers.intent_detection.schemas import IntentClassification, IntentResponse

router = APIRouter()


def classify(input_chunk):
    prediction = "GENERAL"
    if "pricing" in input_chunk:
        prediction = "PRICE"
    return prediction


@router.post("/chunk-intent-detection")
async def chunk_detection(input_chunk: IntentClassification):
    classification = classify(input_chunk=input_chunk.input_chunk)
    return IntentResponse(intent_class=classification)
