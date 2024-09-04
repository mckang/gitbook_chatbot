import os
from llama_index.vector_stores.chroma import ChromaVectorStore


def get_vector_store():
    collection_name = os.getenv("CHROMA_COLLECTION", "default")
    chroma_path = os.getenv("CHROMA_PATH")
    # if CHROMA_PATH is set, use a local ChromaVectorStore from the path
    # otherwise, use a remote ChromaVectorStore (ChromaDB Cloud is not supported yet)
    if chroma_path:
        # store = ChromaVectorStore.from_params(
        #     persist_dir=chroma_path, collection_name=collection_name
        # )
        import chromadb
        from chromadb.config import Settings as ChromaSettings
        db = chromadb.PersistentClient(path=chroma_path, settings=ChromaSettings(anonymized_telemetry=False))
        chroma_collection = db.get_collection(collection_name)
        store = ChromaVectorStore(chroma_collection=chroma_collection)        
    else:
        if not os.getenv("CHROMA_HOST") or not os.getenv("CHROMA_PORT"):
            raise ValueError(
                "Please provide either CHROMA_PATH or CHROMA_HOST and CHROMA_PORT"
            )
        import chromadb
        from chromadb.config import Settings as ChromaSettings        
        db = chromadb.HttpClient(host=os.getenv("CHROMA_HOST"), port=os.getenv("CHROMA_PORT"), settings=ChromaSettings(anonymized_telemetry=False))
        chroma_collection = db.get_collection(collection_name)
        store = ChromaVectorStore(chroma_collection=chroma_collection)   
        
        # store = ChromaVectorStore.from_params(
        #     host=os.getenv("CHROMA_HOST"),
        #     port=os.getenv("CHROMA_PORT"),
        #     collection_name=collection_name,
        # )
    return store
