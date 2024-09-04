from app import BaseTask
from typing import List


from app.llm import LLM
def build_index(save_directory:str,base_url:str,llm:LLM,menu_url:str, tasks: List[BaseTask], do_index):
    # tasks = [ DataStructurer, VectorstoreIndexer]

    params = {
        "save_directory": save_directory,
        "base_url": base_url,
        "llm": llm,
        "menu_url": menu_url,
        "do_index": do_index
    }
    for cls in tasks:
        print("[Gitbook] Initializing ", cls.__name__, "...") 
        task = cls(**params)
        print("[Gitbook] Doing ", cls.__name__, " task ...") 
        task.do_task()
        print("[Gitbook] Done ", cls.__name__, " task ...\n\n")      



