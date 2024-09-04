## Getting Started
Gitbook Site를 크롤링하여 Chromadb index를 생성하고 S3 Object Storage에 저장한다.
S3 Object Storage에 저장된 Chromadb index를 기반으로 Chromadb Docker Instance를 실행한다.

### .env 파일 만들기
```
DATA_SAVE_DIR=data
DATA_GITBOOK_SITE=
DATA_SEED_URI=/
DATA_TASK=*
DATA_TASK_MODEL=gpt-4o

# The OpenAI API key to use.
OPENAI_API_KEY=
# text_search, similarity
EMBEDDING_MODE=text_search
# text-embedding-ada-002, text-embedding-3-large, text-embedding-3-small
EMBEDDING_MODEL=text-embedding-ada-002
MODEL=gpt-4o-mini

LANGFUSE_PUBLIC_KEY=pk-lf-2e4d0012-5569-4b82-9915-bcf08362e894
LANGFUSE_SECRET_KEY=sk-lf-c6f83f6f-f737-46af-b651-4221593039f4
LANGFUSE_HOST=

INDEX_COLLECTION_NAME=my_chroma_store


AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=ap-northeast-2
S3_BUCKET=
UPLOAD_S3=true
```

### All-in-One
```
DATA_GITBOOK_SITE={gitbook site 주소} docker-compose up --build
```

이미 만들어진 인덱스를 기반으로 Chromadb 실행하기
```
DATA_GITBOOK_SITE={gitbook site 주소} DATA_TASK=skip docker-compose up --build
```

### 사이트 크롤링 및 인덱스 저장
```
docker build -t gitbook_indexing_task_v1  -f Dockerfile-indexing .
docker run --name indexing --rm --cpus 3  --env-file .env  gitbook_indexing_task_v1
```

#### Docker 이미지 만들기
```
docker build -t gitbook_chromadb_v1  -f Dockerfile-chromadb .
docker run --name chromadb --rm -d -p 8000:8000 --env-file .env gitbook_chromadb_v1
```


#### Test용 Shell 실행하기
```
poetry install
poetry shell
python rag_console.py
```

