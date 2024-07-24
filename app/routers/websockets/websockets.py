from datetime import datetime
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.cache_manager import CacheManager
from app.routers.websockets.schemas import (
    RecommendationInput,
    RecommendationOutput,
    RecommendationResponse,
)

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


def format_recommendation(recommendation_checklist, formatted_timestamp):
    if isinstance(recommendation_checklist.recommendation_instruction, list):
        instruction_html = (
            "<ul>"
            + "".join(
                f"<li>{item}</li>"
                for item in recommendation_checklist.recommendation_instruction
            )
            + "</ul>"
        )
    else:
        instruction_html = recommendation_checklist.recommendation_instruction

    input_data = {
        "label": recommendation_checklist.prediction_label.title(),
        "message": instruction_html,
        "timestamp": formatted_timestamp,
    }
    return input_data


def format_sales(sales_checklist):
    map = {"active listening": "active_listening", "matt": "build_rapport"}
    category = map.get(sales_checklist.category, sales_checklist.category)
    return {category: True}


@router.post("/create-response-recommendation")
async def find_recommendation(recommendation: RecommendationInput):
    formatted_timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    recommendation_input = None
    sales_input = None
    if recommendation.recommendation_checklist:
        recommendation_input = format_recommendation(
            recommendation_checklist=recommendation.recommendation_checklist,
            formatted_timestamp=formatted_timestamp,
        )

    if recommendation.sales_checklist:
        sales_input = format_sales(sales_checklist=recommendation.sales_checklist)
    CacheManager.add_to_cache(
        input_data=recommendation_input, sales_checklist=sales_input
    )
    # Trigger WebSocket message
    await websocket_manager.send_message("Event Received")
    return RecommendationResponse(status="received")


@router.get("/fetch-recommendations")
async def fetch_recommendation():
    recommendation = CacheManager.fetch_from_cache()

    return RecommendationOutput(
        current_recommendations=recommendation["recommendation"],
        sales_checklist=recommendation["sales_checklist"],
    )


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
