from llama_index.core import set_global_handler
from llama_index.core import Settings
# from llama_index.core.callbacks import CallbackManager

import os

def init_observability():
    if os.getenv('LANGFUSE_HOST'):
        set_global_handler("langfuse",
            public_key=os.getenv('LANGFUSE_PUBLIC_KEY'),
            secret_key=os.getenv('LANGFUSE_SECRET_KEY'),
            host=os.getenv('LANGFUSE_HOST')
        )
    # Settings.callback_manager = CallbackManager()
