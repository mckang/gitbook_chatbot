## Getting Started

### poetry 환경설정하기

```
poetry install
poetry shell
```

### .env 파일 만들기
```
LANGFUSE_PUBLIC_KEY=
LANGFUSE_SECRET_KEY=
LANGFUSE_HOST=

# The provider for the AI models to use.
MODEL_PROVIDER=openai

# The name of LLM model to use.
MODEL=gpt-4o-mini

# Name of the embedding model to use.
EMBEDDING_MODEL=text-embedding-ada-002

# Dimension of the embedding model to use.
# EMBEDDING_DIM=1536

# The questions to help users get started (multi-line).
CONVERSATION_STARTERS='소셜비즈가 뭔가요?
Socialbiz를 통해 자동화할 수 있는 메시지 유형은 뭔가요?
소셜비즈로 활용 가능한 시나리오를 알려주세요
소셜비즈의 이용 요금은 어떻게 되나요?
'

# The OpenAI API key to use.
OPENAI_API_KEY=

# Temperature for sampling from the model.
LLM_TEMPERATURE=0

# Maximum number of tokens to generate.
LLM_MAX_TOKENS=5120

# The number of similar embeddings to return when retrieving documents.
TOP_K=20

# The time in milliseconds to wait for the stream to return a response.
STREAM_TIMEOUT=60000

# The name of the collection in your Chroma database
CHROMA_COLLECTION=my_chroma_store

# The API endpoint for your Chroma database
CHROMA_HOST=127.0.0.1

# The port for your Chroma database
CHROMA_PORT=8001


# The address to start the backend app.
APP_HOST=0.0.0.0

# The port to start the backend app.
APP_PORT=8989
```

### Docker 이미지 만들기
```
docker build -t socialbiz_chatbot_backend_v1 .
```

### Backend 인스턴스 실행하기
```
docker run --name socialbiz_chatbot_backend \
--rm -d -p 8989:8989 \
--network=socialbiz \
-e CHROMA_HOST='chromadb' \
-e CHROMA_PORT='8000' \
socialbiz_chatbot_backend_v1

참고 : 운영환경 -e ENVIRONMENT='prod'
```

### 브라우져 열기
```
[오픈API](http://127.0.0.1:8989/docs)
```