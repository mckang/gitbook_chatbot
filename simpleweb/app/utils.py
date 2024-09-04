
from dotenv import load_dotenv
import os
load_dotenv()

from llama_index.core import set_global_handler
set_global_handler("langfuse",
    public_key=os.getenv('LANGFUSE_PUBLIC_KEY'),
    secret_key=os.getenv('LANGFUSE_SECRET_KEY'),
    host=os.getenv('LANGFUSE_HOST')
)

from llama_index.core import VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingModelType, OpenAIEmbeddingMode
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingModelType, OpenAIEmbeddingMode
from llama_index.core.callbacks import CallbackManager
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core import get_response_synthesizer
from llama_index.core import QueryBundle
from llama_index.core.schema import NodeWithScore
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.postprocessor import LLMRerank


from typing import Dict, List, Optional, cast
from . import prompts


print(os.getenv("INDEX_COLLECTION_NAME","my_chroma_store"))

Settings.llm = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY',""),
            model=os.getenv('MODEL',"gpt-4o-mini"),
            temperature=0, 
        )
Settings.embed_model = OpenAIEmbedding(
            mode=os.getenv('EMBEDDING_MODE',"text_search"),
            model=os.getenv('EMBEDDING_MODEL',"text-embedding-ada-002")
        )

def load_index(index_dir):
    import chromadb
    from llama_index.vector_stores.chroma import ChromaVectorStore
    from chromadb.config import Settings as ChromaSettings

    db = chromadb.PersistentClient(path=index_dir, settings=ChromaSettings(anonymized_telemetry=False))
    chroma_collection = db.get_collection(os.getenv("INDEX_COLLECTION_NAME","my_chroma_store"))
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(
        vector_store,
    )    
    return index 

def build_retriever(index):
    return VectorIndexRetriever(
        index=index,
        similarity_top_k=20,
    )

def build_response_synthesizer():
    return get_response_synthesizer(
        # response_mode="tree_summarize",
        response_mode="refine",
    )

def build_postprocessors():
    class SimilarityPostprocessorWithAtLeastTopN(SimilarityPostprocessor):
        """Similarity-based Node processor. Return always one result if result is empty"""

        top_n : int = 1

        @classmethod
        def class_name(cls) -> str:
            return "SimilarityPostprocessorWithAtLeastTopN"

        def _postprocess_nodes(
            self,
            nodes: List[NodeWithScore],
            query_bundle: Optional[QueryBundle] = None,
        ) -> List[NodeWithScore]:
            """Postprocess nodes."""
            # for node in nodes:
            #     print(node)
            # Call parent class's _postprocess_nodes method first
            new_nodes = super()._postprocess_nodes(nodes, query_bundle)

            if not new_nodes:  # If the result is empty
                return sorted(nodes, key=lambda x: x.score)[:self.top_n] if nodes else []

            # for node in new_nodes:
            #     print(node)
            return new_nodes
        
    node_postprocessors=[
            # This postprocessor optimizes token usage by removing sentences that are not relevant to the query (this is done using embeddings).
            # The percentile cutoff is a measure for using the top percentage of relevant sentences.
            # Used to remove nodes that are below a similarity score threshold.
            SimilarityPostprocessorWithAtLeastTopN(similarity_cutoff=0.5, top_n=10),
            # Uses a LLM to re-order nodes by asking the LLM to return the relevant documents and a score of how relevant they are. Returns the top N ranked nodes.
            LLMRerank(
                top_n=5,
                choice_select_prompt=prompts.choice_select_prompt,
                choice_batch_size=10
            )
        ]
    
    return node_postprocessors



CHROMA_INDEX_DIR = os.getenv('CHROMA_INDEX_DIR')
index = load_index(CHROMA_INDEX_DIR)

from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine import CondensePlusContextChatEngine
def build_chat_engine():

    memory = ChatMemoryBuffer.from_defaults(token_limit=3500)
    chat_engine = CondensePlusContextChatEngine.from_defaults(
        retriever=build_retriever(index),
        node_postprocessors=build_postprocessors(),
        response_synthesizer=build_response_synthesizer(),    
        memory=memory,
        system_prompt=prompts.system_prompt,
        context_prompt=prompts.context_prompt,
        condense_prompt=prompts.condense_prompt,
        streaming=True
    )

    return chat_engine 