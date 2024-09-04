# flake8: noqa: E402
from dotenv import load_dotenv

from app.config import DATA_DIR

load_dotenv()

import logging
import os

import uvicorn
from app.api.routers.chat import chat_router
from app.api.routers.chat_config import config_router
# from app.api.routers.upload import file_upload_router
from app.observability import init_observability
from app.settings import init_settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

init_observability()
init_settings()

environment = os.getenv("ENVIRONMENT", "dev")  # Default to 'development' if not set
logger = logging.getLogger("uvicorn")

if environment == "dev":
    logger.warning("Running in development mode - allowing CORS for all origins")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Redirect to documentation page when accessing base URL
    @app.get("/")
    async def redirect_to_docs():
        return RedirectResponse(url="/docs")


app.include_router(chat_router, prefix="/api/chat")
app.include_router(config_router, prefix="/api/chat/config")
# app.include_router(file_upload_router, prefix="/api/chat/upload")

if __name__ == "__main__":
    app_host = os.getenv("APP_HOST", "0.0.0.0")
    app_port = int(os.getenv("APP_PORT", "8000"))
    reload = True if environment == "dev" else False
    print("app_port: ", app_port)
    uvicorn.run(app="main:app", host=app_host, port=app_port, reload=reload)
