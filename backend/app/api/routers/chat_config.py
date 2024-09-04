import logging
import os

from fastapi import APIRouter

from app.api.routers.models import ChatConfig
from app.settings import AppSettings


config_router = r = APIRouter()

logger = logging.getLogger("uvicorn")


@r.get("")
async def chat_config() -> ChatConfig:
    starter_questions = None
    conversation_starters = AppSettings.envs.get("CONVERSATION_STARTERS","")
    if conversation_starters and conversation_starters.strip():
        starter_questions = conversation_starters.strip().split("\n")
    return ChatConfig(starter_questions=starter_questions)
