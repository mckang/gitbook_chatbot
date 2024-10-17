from llama_index.core import set_global_handler
from llama_index.core import Settings
from langfuse import Langfuse
import os

langfuse = None
def init_observability():
    global langfuse 
    if os.getenv('LANGFUSE_HOST'):
        set_global_handler("langfuse",
            public_key=os.getenv('LANGFUSE_PUBLIC_KEY'),
            secret_key=os.getenv('LANGFUSE_SECRET_KEY'),
            host=os.getenv('LANGFUSE_HOST')
        )
    if os.getenv('SCORE_LANGFUSE_HOST'):        
        langfuse = Langfuse(
            public_key=os.getenv('SCORE_LANGFUSE_PUBLIC_KEY'),
            secret_key=os.getenv('SCORE_LANGFUSE_SECRET_KEY'),
            host=os.getenv('SCORE_LANGFUSE_HOST')
        );  
    # Settings.callback_manager = CallbackManager()
