
from llama_index.core import Document
from pathlib import Path
from app import EMBEDDING_MODE, EMBEDDING_MODEL, DATA_SAVE_DIR, DATA_GITBOOK_SITE, DATA_SEED_URI, DATA_TASK, DATA_TASK_MODEL, OPENAI_API_KEY, INDEXED_DATA_DIR
from app.llm import LLM
from app.blog.crawling import CustomPageDownloader
from app.blog.cleansing import CustomPageCleanser
from app.blog.structuring import CustomDataStructurer
from app.blog.indexing import CustomVectorstoreIndexer
from app.blog.transforming import CustomDataTransformer

from app.blog import build_index, DEFAULT_CONF_DIR, __main__
import os, yaml

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

def load_site_config(directory:str):
    site_configs = {"sitemap":[]}
    for filename in os.listdir(directory):
        if filename.endswith('.yaml') or filename.endswith('.yml'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    site_config = yaml.safe_load(file)
                    site_configs["sitemap"].extend(site_config.get("sitemap", []))
                except yaml.YAMLError as exc:
                    print(f"{filename} 파일을 로드하는 중 오류 발생: {exc}")        
    return site_configs
        
def main():

    import argparse

    parser = argparse.ArgumentParser(description="사이트를 Chroma Vector DB 인덱스화합니다.")
    parser.add_argument('-s', '--save', type=str, default=DATA_SAVE_DIR, help="저장 디렉토리")
    parser.add_argument('-c', '--config', type=str, default=DEFAULT_CONF_DIR, help="사이트 Config")
    parser.add_argument('-t', '--task', type=str, default=DATA_TASK, help="Task Name")


    args = parser.parse_args()

    __main__.INDEX_STORE_PATH = args.save+"/"+INDEXED_DATA_DIR

    site_config = load_site_config(args.config)

    # print(site_config)
    # print([ site['url']+uri for site in site_config['sitemap'] for uri in site['pages'].keys()] )

    req_task_string = args.task.lower()
    req_tasks = [part.strip() for part in req_task_string.split(",")]

    tasks=[]
    if '*' in req_tasks:
        tasks.append(CustomPageDownloader)
        tasks.append(CustomPageCleanser)
        tasks.append(CustomDataTransformer)
        tasks.append(CustomDataStructurer)
        tasks.append(CustomVectorstoreIndexer)
    else:
        if 'download' in req_tasks:
            tasks.append(CustomPageDownloader)
        if 'clean' in req_tasks:
            tasks.append(CustomPageCleanser)
        if 'struct' in req_tasks:
            tasks.append(CustomDataStructurer)
        if 'index' in req_tasks:
            tasks.append(CustomVectorstoreIndexer)
        if 'transform' in req_tasks:
            tasks.append(CustomDataTransformer)                

    build_index(save_directory=args.save+"/blog",llm=LLM(temperature=0, model=DATA_TASK_MODEL, api_key=OPENAI_API_KEY), site_config=site_config, tasks=tasks, do_index=do_chroma_index)   

if __name__ == "__main__":
    main()