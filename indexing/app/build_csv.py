
from pathlib import Path

import json

from llama_index.core import Document
from llama_index.core.schema import TextNode

import app, hashlib
from app import STRUCTURED_DATA_DIR, INDEXED_DATA_DIR, SITEMAP_FILE

from pandas import DataFrame, concat

class CSVBuilder(app.BaseTask): 

    def __init__(self, save_directory: str=".", base_url:str =None,**kwargs):
        super().__init__(save_directory, base_url)
        self.src_path = self.root_path/STRUCTURED_DATA_DIR
        self.target_path = self.root_path/INDEXED_DATA_DIR
        
        if not self.target_path.exists():
            # 디렉토리가 존재하지 않으면 생성
            self.target_path.mkdir(parents=False, exist_ok=True)
        

    def do_task(self):    
        documents = self._load_documents()   
        df_pages = DataFrame(documents)
        df_pages.reset_index(drop=True, inplace=True)
        df_pages.loc[:, ["content"]]\
            .to_csv(self.target_path/"content.tsv", sep="\t", index=True, header=False)
        df_pages.loc[:, ["section", "source", "links", "nexts"]]\
            .to_csv(self.target_path/"metadata.csv", sep=";", index=True, header=True)

    def _load_documents(self):
        with open(self.src_path/SITEMAP_FILE, 'r', encoding='utf-8') as json_file:
            sitemap = json.load(json_file)   

        
        list_chunks = []
        for page in sitemap:
            file_path = self.src_path/page.get("filename")

            try:
                with file_path.open(mode='r', encoding='utf-8') as file:
                    data = json.load(file)
                    page = data.get("page",{})
                    image_map = data.get("image_map",{})
                    subjects = data.get("subjects",[])   
                    for subject in subjects:

                        keywords = subject.get("keywords",[]) + page.get("keywords",[])
                        _links = subject.get("links",[])
                        _nexts = subject.get("nexts",[])
                        for _link in _links:
                            if _link.get("type","") == "img":
                                _link["link"] = image_map.get(_link["link"],"UNKNOWN")  


                        documents = []
                        documents.append(subject.get("content"))


                        items = data.get("items",[])   
                        
                        for item in items:
                            documents.append(item.get("title",""))
                            documents.append(item.get("content"))


                            _item_links = item.get("links",[])
                            for _item_link in _item_links:
                                if _item_link.get("type","") == "img":
                                    _item_link["link"] = image_map(_link["link"])

                            _item_nexts = item.get("nexts",[])

                            _links = _links + _item_links
                            _nexts = _nexts + _item_nexts

                        list_chunks.append({"section": page.get("title","") + " > " +  subject.get("title",""),
                                            "content": subject.get("content"),
                                            "source" : page.get("source",""),
                                            "links": json.dumps(_links, ensure_ascii=False, indent=4),
                                            "nexts": json.dumps(_nexts, ensure_ascii=False, indent=4)
                                        })                                      
            except FileNotFoundError:
                print(f"The file {file_path} does not exist.")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from file {json_file}: {e}")                
            except Exception as e:
                print(f"An error occurred: {e}")             

        return list_chunks


if __name__ == "__main__":
    indexing = CSVBuilder("data", "https://socialbiz.gitbook.io")

    indexing.do_task()       