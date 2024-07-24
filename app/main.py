from fastapi import FastAPI
from app.routers.search.search import router as search_router
from app.routers.intent_detection.intent_detection import router as intent_router
from app.routers.websockets.websockets import router as websocket_router
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager, contextmanager
from app.cache_manager import CacheManager
import asyncio
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    CacheManager.create_cache()
    try:
        yield
    finally:
        pass


def create_app() -> FastAPI:
    _app = FastAPI(title="sl-vista-back", lifespan=lifespan)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.include_router(search_router)
    _app.include_router(intent_router)
    _app.include_router(websocket_router)
    return _app


app = create_app()


# Healthcheck and Readiness check
@app.get("/admin/healthcheck", status_code=200, include_in_schema=False)
async def healthcheck():
    return "sl-vista-backed is ready to go!"


@app.get("/admin/readiness", status_code=400)
async def readiness():
    return {"status": "ok"}


@app.get("/")
async def hello():
    return "Hello from sl-vista-backed"


async def main():
    config = uvicorn.Config(app, host="0.0.0.0", port=5050)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
