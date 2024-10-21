import logging, uuid, json

from fastapi import APIRouter
from app.api.routers.models import ScoreRequest, ScoreResponse

score_router = r = APIRouter()

logger = logging.getLogger("uvicorn")


@r.post("")
async def chat_score(data: ScoreRequest) -> ScoreResponse:
    from app.observability import langfuse
    
    if langfuse:
        traceId=str(uuid.uuid4())
        langfuse.trace(id=traceId, input=data.question, output=data.answer)
        langfuse.score(trace_id=traceId,name='user_feedback', value=data.score, comment=data.comment)

    return ScoreResponse(message='Feedback received')
