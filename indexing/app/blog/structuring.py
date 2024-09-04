from app.structuring import DataStructurer
from app.llm import LLM 

class CustomDataStructurer(DataStructurer):  
    def __init__(self, save_directory: str=".", base_url:str =None, llm: LLM = None, site_config:dict = None, **kwargs):
        super().__init__(save_directory, "https://dummy.url", llm)
        self.site_config=site_config
