### .env 파일 만들기
```
NEXT_PUBLIC_CHAT_API=http://localhost:8989/api/chat
DATA_GITBOOK_SITE=https://socialbiz.gitbook.io
DATA_TASK=*
```

### Build & Start Service
```
DATA_TASK=skip docker-compose -f docker-compose.dev.yml  up --build

DATA_TASK=skip docker-compose -f docker-compose.yml  up --build
```