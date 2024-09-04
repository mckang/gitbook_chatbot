import re
from typing import List, Optional, Tuple

from llama_index.core import QueryBundle
# from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.schema import NodeWithScore
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.postprocessor import LLMRerank
from llama_index.core import PromptTemplate

from app.api.routers.events import EventCallbackHandler

# class NodeCitationProcessor(BaseNodePostprocessor):
#     """
#     Append node_id into metadata for citation purpose.
#     Config SYSTEM_CITATION_PROMPT in your runtime environment variable to enable this feature.
#     """

#     def _postprocess_nodes(
#         self,
#         nodes: List[NodeWithScore],
#         query_bundle: Optional[QueryBundle] = None,
#     ) -> List[NodeWithScore]:
#         for node_score in nodes:
#             node_score.node.metadata["node_id"] = node_score.node.node_id
#         return nodes

choice_select_prompt = PromptTemplate(
    "A list of documents is shown below. Each document has a number next to it along with a summary of the document. "
    "A question is also provided.\n"
    "Respond with the numbers of the documents you should consult to answer the question, in order of relevance, as well as the relevance score. "
    "The relevance score is a number from 1 (low) - 10 (high) based on how relevant you think the document is to the question. Be accurate!\n"
    "Do not include any documents that are not relevant to the question or documents with a score less than 7. \n"
    "Example format: \nDocument 1:\n<summary of document 1>\n\nDocument 2:\n<summary of document 2>\n\n...\n\nDocument 10:\n<summary of document 10>\n"
    "\nQuestion: <question>\nAnswer:\nDoc: 9, Relevance: 7\nDoc: 3, Relevance: 4\nDoc: 7, Relevance: 3\n"
    "\nLet's try this now: \n"
    "{context_str}"
    "\nQuestion: {query_str}"
    "\nAnswer:\n\n"
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


def get_postprocessors():
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
            SimilarityPostprocessorWithAtLeastTopN(similarity_cutoff=0.6, top_n=10),
            # Uses a LLM to re-order nodes by asking the LLM to return the relevant documents and a score of how relevant they are. Returns the top N ranked nodes.
            LLMRerank(
                top_n=6,
                choice_select_prompt=choice_select_prompt,
                parse_choice_select_answer_fn=parse_choice_select_answer_fn,
                choice_batch_size=10
            )
        ]
    
    return node_postprocessors