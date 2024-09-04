import os
from typing import Dict

from llama_index.core.settings import Settings

from app.engine.node_postprocessors import get_postprocessors
from app.engine.index import get_index

from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Dict
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.indices.vector_store.base import VectorStoreIndex
from dotenv import dotenv_values


@dataclass
class _Settings:
    """Settings for the ChatEngine, lazily initialized."""
    # lazy initialization
    _node_postprocessors: Optional[List[BaseNodePostprocessor]] = None
    _vectorstore_index: Optional[VectorStoreIndex] = None
    _envs: Optional[Dict[str,str]] = None

    @property
    def envs(self) -> Dict[str,str]:
        """Get the envs."""
        if self._envs is None:
            self._envs = dotenv_values()
        return self._envs
    
    @property
    def node_postprocessors(self) -> List[BaseNodePostprocessor]:
        """Get the node_postprocessors."""
        if self._node_postprocessors is None:
            self._node_postprocessors = get_postprocessors()
        return self._node_postprocessors

    @node_postprocessors.setter
    def node_postprocessors(self, node_postprocessors: List[BaseNodePostprocessor]) -> None:
        """Set the node_postprocessors."""
        self._node_postprocessors = node_postprocessors

    @property
    def vectorstore_index(self) -> VectorStoreIndex:
        """Get the vectorstore_index."""
        if self._vectorstore_index is None:
            self._vectorstore_index = get_index()    

        return self._vectorstore_index

    @vectorstore_index.setter
    def vectorstore_index(self, vectorstore_index: VectorStoreIndex) -> None:
        """Set the vectorstore_index."""
        self._llm = vectorstore_index        

AppSettings = _Settings()

def init_settings():
    model_provider = os.getenv("MODEL_PROVIDER")
    match model_provider:
        case "openai":
            init_openai()
        case "t-systems":
            from .llmhub import init_llmhub

            init_llmhub()
        case _:
            raise ValueError(f"Invalid model provider: {model_provider}")

    Settings.chunk_size = int(os.getenv("CHUNK_SIZE", "1024"))
    Settings.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "0"))

    AppSettings.node_postprocessors = get_postprocessors()
    AppSettings.vectorstore_index = get_index()    

def refresh_index():
    AppSettings.vectorstore_index = get_index()


def init_openai():
    from llama_index.core.constants import DEFAULT_TEMPERATURE
    from llama_index.embeddings.openai import OpenAIEmbedding
    from llama_index.llms.openai import OpenAI

    max_tokens = os.getenv("LLM_MAX_TOKENS")
    config = {
        "model": os.getenv("MODEL"),
        "temperature": float(os.getenv("LLM_TEMPERATURE", DEFAULT_TEMPERATURE)),
        "max_tokens": int(max_tokens) if max_tokens is not None else None,
    }
    Settings.llm = OpenAI(**config)

    dimensions = os.getenv("EMBEDDING_DIM")
    config = {
        "model": os.getenv("EMBEDDING_MODEL"),
        "dimensions": int(dimensions) if dimensions is not None else None,
    }
    Settings.embed_model = OpenAIEmbedding(**config)


