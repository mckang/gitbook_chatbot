from app import BaseTask
from typing import List


from app.llm import LLM

DEFAULT_CONF_DIR = "./conf"

def build_index(save_directory:str, llm:LLM,site_config:str, tasks: List[BaseTask], do_index):
    # tasks = [ DataStructurer, VectorstoreIndexer]

    params = {
        "save_directory": save_directory,
        "llm": llm,
        "site_config": site_config,
        "do_index": do_index
    }
    for cls in tasks:
        print("[Blog] Initializing ", cls.__name__, "...") 
        task = cls(**params)
        print("[Blog] Doing ", cls.__name__, " task ...") 
        task.do_task()
        print("[Blog] Done ", cls.__name__, " task ...\n\n")      



