from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine import CondensePlusContextChatEngine
from llama_index.core.callbacks import CallbackManager

import rag_common
import rag_prompt

import os, re
from dotenv import load_dotenv

load_dotenv()

DATA_SAVE_DIR = os.getenv('DATA_SAVE_DIR')
DATA_GITBOOK_SITE = os.getenv('DATA_GITBOOK_SITE')

index_dir = DATA_SAVE_DIR+ "/" + DATA_GITBOOK_SITE.replace("https://","").replace("http://","").replace(".","_").replace("/","__") + "/store"

memory = ChatMemoryBuffer.from_defaults(token_limit=1024*5)

index = rag_common.load_index(index_dir)

chat_engine = CondensePlusContextChatEngine.from_defaults(
    retriever=rag_common.build_retriever(index),
    node_postprocessors=rag_common.build_postprocessors(),
    response_synthesizer=rag_common.build_response_synthesizer(),    
    memory=memory,
    system_prompt=rag_prompt.system_prompt,
    context_prompt=rag_prompt.context_prompt,
    condense_prompt=rag_prompt.condense_prompt,
    streaming=True
)

while(True):
    question = input("Q : ")
    if question == 'reset':
        chat_engine.reset()
        continue;
    if question == 'quit':
        break;
    # response = chat_engine.chat(question)
    # print(response.response)
    response_stream = chat_engine.stream_chat(question)
    response_stream.print_response_stream()
    print("\n"*3)