from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
from app.routers.websockets.schemas import (
    RecommendationInput,
    RecommendationResponse,
    RecommendationOutput,
)
from app.cache_manager import CacheManager
from datetime import datetime

router = APIRouter()


# WebSocket Manager to handle WebSocket connections
class WebSocketManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def send_message(self, message: str):
        for connection in self.connections:
            await connection.send_text(message)


websocket_manager = WebSocketManager()


@router.post("/create-response-recommendation")
async def find_recommendation(recommendation: RecommendationInput):
    formatted_timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    if isinstance(recommendation.recommendation_instruction, list):
        instruction_html = (
            "<ul>"
            + "".join(
                f"<li>{item}</li>" for item in recommendation.recommendation_instruction
            )
            + "</ul>"
        )
    else:
        instruction_html = recommendation.recommendation_instruction

    CacheManager.add_to_cache(
        input_data={
            "label": recommendation.prediction_label.title(),
            "message": instruction_html,
            "timestamp": formatted_timestamp,
        }
    )
    # Trigger WebSocket message
    await websocket_manager.send_message("Event Received")
    return RecommendationResponse(status="received")


@router.get("/fetch-recommendations")
async def fetch_recommendation():
    recommendation = CacheManager.fetch_from_cache()
    recommendation.reverse()
    return RecommendationOutput(current_recommendations=recommendation)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received data: {data}")
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
        print("Client disconnected")
    except Exception as e:
        print(f"An error occurred: {e}")
