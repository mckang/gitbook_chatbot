### namespace 생성

```
kubectl apply -f namespace_socialbiz-chatbot.yaml
```

### chromadb-secret 생성

```
DATA_SAVE_DIR: data
DATA_GITBOOK_SITE:
INDEX_COLLECTION_NAME:
AWS_ACCESS_KEY_ID:
AWS_SECRET_ACCESS_KEY:
AWS_DEFAULT_REGION: ap-northeast-2
S3_BUCKET:
```

### be-secret 생성

```
LANGFUSE_PUBLIC_KEY:
LANGFUSE_SECRET_KEY:
LANGFUSE_HOST:
MODEL_PROVIDER:
MODEL:
EMBEDDING_MODEL:
CONVERSATION_STARTERS:
OPENAI_API_KEY:
LLM_TEMPERATURE:
LLM_MAX_TOKENS:
TOP_K:
STREAM_TIMEOUT:
CHROMA_COLLECTION:
CHROMA_HOST:
CHROMA_PORT:
APP_HOST:
APP_PORT:
```

### service 생성

```
kubectl apply -f service_socialbiz-chorma.yaml
kubectl apply -f service_socialbiz-be.yaml
```

### ingress 설정

```
kubectl apply -f ingress_socialbiz_chromadb.yaml
kubectl apply -f ingress_socialbiz_be.yaml
```

### kubenetes 환경설정 확인 명령어

```
파드확인: kubectl get pod -n socialbiz_gitbook_chatbot
```

### 문제점/조치중인 방향

```
- chromadb 서비스 파드 정상 작동, describe pod 명령어 실행 시 특이점 없으나 log 실행 시 healthcheck가 404로 확인됨
    - /health 명령이 설정되어있지 않아서 404가 출력되는것으로 확인, healthCheck를 Ingress에서 제거
- socialbiz-be (backend 서버) 가 계속 CrashLoopBackOff 오류 발생 중
    - backend서버에서 chromadb서버를 참조하지 못하는것으로 파악됨.
        - CHROMA_HOST: <ChromaDB서버의 Endpoint IP>
        - CHROMA_PORT: <ChromaDB서버의 TargetPort>
        로 설정해서 configmap지정
    - TypeError: Collection.__init__() got an unexpected keyword argument 'log_position' 오류 발생
        - Collection.__init__() 파일을 찾아보았으나 'log_position' 인자가 존재하는데 TypeError가 발생함. 해당 내용 조치방법 구상중
        - ingress에 설정한 DNS접근 시에도 502 에러발생.
        - 에러 로그 확인결과 주된 오류는 chromadb indexing에서 발생하는것으로 확인됨. 따라서 에러 원인 접근을 chromadb 서비스 연결 불량으로 인한 에러 발생으로 잡고 해결방법 구상중
```

### 조치내용

```
DNS가 적용되지 않던 현상
- AWS 콘솔의 ROUTE 53에서 주소가 등록되어있지 않은 현상 발견 및 주소 추가 : https://socialbiz-channel-talk-webhook.nhndata-bigbrother.link
- 추가 이후 정상적으로 FastAPI swagger 접속 확인
```
