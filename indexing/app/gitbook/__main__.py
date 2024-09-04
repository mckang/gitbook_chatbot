
from llama_index.core import Document
from pathlib import Path
from app.llm import LLM
from app.initializing import MenuBuilder
from app.crawling import WebPageDownloader
from app.structuring import DataStructurer
from app.indexing import VectorstoreIndexer
from app.gitbook.cleansing import GitbookHtmlCleanser
from app.transforming import DataTransformer
from app.gitbook import build_index, __main__
from app import EMBEDDING_MODE, EMBEDDING_MODEL, DATA_SAVE_DIR, DATA_GITBOOK_SITE, DATA_SEED_URI, DATA_TASK, DATA_TASK_MODEL, OPENAI_API_KEY, INDEXED_DATA_DIR
import os

INDEX_STORE_PATH = None

def do_chroma_index(documents : list[Document], target : Path):
    ##pip install chromadb
    ##pip install llama-index-vector-stores-chroma
    from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingModelType, OpenAIEmbeddingMode
    from llama_index.core import VectorStoreIndex
    from llama_index.core import Settings

    embedding  = OpenAIEmbedding(embed_batch_size=10, 
                                           mode=EMBEDDING_MODE, 
                                           model=EMBEDDING_MODEL)
    Settings.chunk_size = 2048
    Settings.chunk_overlap = 0
    Settings.embed_model =embedding   
            
    import chromadb
    from llama_index.vector_stores.chroma import ChromaVectorStore
    from llama_index.core import (
        VectorStoreIndex, SimpleDirectoryReader, StorageContext)  
    
    if __main__.INDEX_STORE_PATH:
        db = chromadb.PersistentClient(path=__main__.INDEX_STORE_PATH)
    else:
        db = chromadb.PersistentClient(path=str(target))
    chroma_collection = db.get_or_create_collection(
        os.getenv("INDEX_COLLECTION_NAME")
    )     
    vector_store = ChromaVectorStore(
        chroma_collection=chroma_collection
    )
    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )      
    VectorStoreIndex.from_documents(
        documents=documents,
        storage_context=storage_context,
        embed_model=embedding
    )

def main():
    import argparse

    parser = argparse.ArgumentParser(description="깃북 사이트를 Chroma Vector DB 인덱스화합니다.")
    parser.add_argument('-s', '--save', type=str, default=DATA_SAVE_DIR, help="저장 디렉토리")
    parser.add_argument('-u', '--url', type=str, default=DATA_GITBOOK_SITE, help="깃북 사이트")
    parser.add_argument('-m', '--menu', type=str, default=DATA_SEED_URI, help="Seed Uri")
    parser.add_argument('-t', '--task', type=str, default=DATA_TASK, help="Task Name")


    args = parser.parse_args()

    __main__.INDEX_STORE_PATH = args.save+"/"+INDEXED_DATA_DIR

    req_task_string = args.task.lower()
    req_tasks = [part.strip() for part in req_task_string.split(",")]

    tasks=[]
    if '*' in req_tasks:
        tasks.append(MenuBuilder)
        tasks.append(WebPageDownloader)
        tasks.append(GitbookHtmlCleanser)
        tasks.append(DataTransformer)
        tasks.append(DataStructurer)
        tasks.append(VectorstoreIndexer)
    else:
        if 'init' in req_tasks:
            tasks.append(MenuBuilder)
        if 'download' in req_tasks:
            tasks.append(WebPageDownloader)
        if 'clean' in req_tasks:
            tasks.append(GitbookHtmlCleanser)
        if 'struct' in req_tasks:
            tasks.append(DataStructurer)
        if 'index' in req_tasks:
            tasks.append(VectorstoreIndexer)
        if 'transform' in req_tasks:
            tasks.append(DataTransformer)            

    build_index(save_directory=args.save+"/gitbook",base_url=args.url,llm=LLM(temperature=0, model=DATA_TASK_MODEL, api_key=OPENAI_API_KEY), menu_url=args.menu, tasks=tasks, do_index=do_chroma_index)   

if __name__ == "__main__":
    main()