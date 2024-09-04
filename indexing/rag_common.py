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
from rag_prompt import choice_select_prompt

from llama_index.core import set_global_handler

from typing import Dict, List, Optional, Tuple
import os,re


if os.getenv('LANGFUSE_HOST'):
    set_global_handler("langfuse",
        public_key=os.getenv('LANGFUSE_PUBLIC_KEY'),
        secret_key=os.getenv('LANGFUSE_SECRET_KEY'),
        host=os.getenv('LANGFUSE_HOST')
    )

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

    # db = chromadb.PersistentClient("./data/store")


    db = chromadb.HttpClient(  host="http://127.0.0.1:8000",
                                # settings=Settings(
                                #     chroma_client_auth_provider="chromadb.auth.token.TokenAuthClientProvider",
                                #     chroma_client_auth_credentials="<your_chroma_token>"
                                # )
                            )

    # db = chromadb.PersistentClient(path=index_dir)
    chroma_collection = db.get_or_create_collection(os.getenv("INDEX_COLLECTION_NAME","my_chroma_store"))
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

def parse_choice_select_answer_fn(
    answer: str, num_choices: int, raise_error: bool = False
) -> Tuple[List[int], List[float]]:
    """Default parse choice select answer function."""
    # print(">>>>>>>>>>",answer)
    if not answer.startswith("Answer:") and not answer.startswith("Doc:"): 
        # print("EEEEEEEE",answer)
        return [],[]
    

    answer_lines = answer.split("\n")
    answer_nums = []
    answer_relevances = []
    for answer_line in answer_lines:
        line_tokens = answer_line.split(",")
        if len(line_tokens) != 2:
            if not raise_error:
                continue
            else:
                raise ValueError(
                    f"Invalid answer line: {answer_line}. "
                    "Answer line must be of the form: "
                    "answer_num: <int>, answer_relevance: <float>"
                )
        if line_tokens[0].find(":") == -1:
            continue
        answer_num = int(line_tokens[0].split(":")[1].strip())
        if answer_num > num_choices:
            continue
        answer_nums.append(answer_num)
        # extract just the first digits after the colon.
        _answer_relevance = re.findall(r"\d+", line_tokens[1].split(":")[1].strip())[0]
        answer_relevances.append(float(_answer_relevance))
    return answer_nums, answer_relevances

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
                choice_select_prompt=choice_select_prompt,
                parse_choice_select_answer_fn=parse_choice_select_answer_fn,
                choice_batch_size=10
            )
        ]
    
    return node_postprocessors

