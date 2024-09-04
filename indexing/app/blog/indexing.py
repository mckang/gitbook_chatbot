from app.indexing import VectorstoreIndexer
class CustomVectorstoreIndexer(VectorstoreIndexer):
    def __init__(self, save_directory: str=".", base_url:str =None, do_index = None , refresh_index = True, **kwargs):
        super().__init__(save_directory, "https://dummy.url", do_index,False, **kwargs)
