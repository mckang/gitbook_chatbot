## Getting Started

### next 환경설정하기

```
npm install
```

### .env 파일 만들기
```
# The backend API for chat endpoint.
NEXT_PUBLIC_CHAT_API=http://localhost:8989/api/chat
NEXT_PUBLIC_GITBOOK_URL=https://socialbiz.gitbook.io

# Let's the user change indexes in LlamaCloud projects
NEXT_PUBLIC_USE_LLAMACLOUD=false
```

### 개발서버 실행하기
```
npm run dev
```

Open [http://localhost:3010](http://localhost:3010) with your browser to see the result.



### Docker 이미지 만들기
```
docker build \
--build-arg NEXT_PUBLIC_CHAT_API=http://localhost:8989/api/chat \
--build-arg NEXT_PUBLIC_GITBOOK_URL=https://socialbiz.gitbook.io \
-t gitbook_chatbot_frontend_v1 .
```

### Backend 인스턴스 실행하기
```
docker run --name gitbook_chatbot_frontend \
--rm -d -p 3010:3010 \
--network=socialbiz \
gitbook_chatbot_frontend_v1 npm run dev

```