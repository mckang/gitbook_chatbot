import os

# from app.engine.index import get_index
# from app.engine.node_postprocessors import NodeCitationProcessor
from fastapi import HTTPException
from llama_index.core.chat_engine import CondensePlusContextChatEngine
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core import get_response_synthesizer
from app.settings import AppSettings
from app.engine.node_postprocessors import get_postprocessors

system_prompt_default=(
    "You are a helpful assistant who helps users with their questions."
)

context_prompt=(
    "Here are the relevant documents for the context given in brackets:\n\n"
    "[{context_str}]"
    "\n\nInstructions:\n"
    "If the answer is not on the above documents, say that the information is not available and do not try to imagine an answer.\n"
    "If the answer is on the above documents, provide detail answer as possible to reply user question below.\n"
    "!![Important] Always include links to sources and titles where you can read more about the context in the footer of your answer, in a list format of '[<title>](<link>)'."
    "!![Important] The source links you provide must exist in the context."
    "!![Important] Be sure to generate output in markdown."
)

condense_prompt = """
  Given the following conversation between a user and an AI assistant and a follow up question from user,
  rephrase the follow up question to be a standalone question.
  !![ When rephrasing, the language should keep the language of the question ]

  Chat History:
  {chat_history}
  Follow Up Input: {question}
  Standalone question:"""

system_prompt = AppSettings.envs.get("SYSTEM_PROMPT", system_prompt_default)

def get_chat_engine(filters=None, params=None):
    
    # citation_prompt = AppSettings.envs.get("SYSTEM_CITATION_PROMPT", None)
    # print(citation_prompt)
    top_k = int(os.getenv("TOP_K", 0))

    # retriever = vectorstore_index.as_retriever(
    #     filters=filters, **({"similarity_top_k": top_k} if top_k != 0 else {})
    # )

    retriever = AppSettings.vectorstore_index.as_retriever(
        **({"similarity_top_k": top_k} if top_k != 0 else {})
    )

    # return CondensePlusContextChatEngine.from_defaults(
    #     system_prompt=system_prompt,
    #     retriever=retriever,
    #     node_postprocessors=rag_node_postprocessors,
    # )


    memory = ChatMemoryBuffer.from_defaults(token_limit=3500)
    chat_engine = CondensePlusContextChatEngine.from_defaults(
        retriever=retriever,
        # node_postprocessors=AppSettings.node_postprocessors,
        node_postprocessors=get_postprocessors(),
        response_synthesizer=get_response_synthesizer(
                # response_mode="tree_summarize",
                response_mode="refine",
            ),    
        memory=memory,
        system_prompt=system_prompt,
        context_prompt=context_prompt,
        condense_prompt=condense_prompt,
        streaming=True
    )

    return chat_engine 
