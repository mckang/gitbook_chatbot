
from pathlib import Path

import json

from llama_index.core import Document
from llama_index.core.schema import TextNode

import app
from app import STRUCTURED_DATA_DIR, INDEXED_DATA_DIR, SITEMAP_FILE, CLENSING_DIR

from markdownify import markdownify as md
import os

class MarkDownBuilder(app.BaseTask): 

    def __init__(self, save_directory: str=".", base_url:str =None,**kwargs):
        super().__init__(save_directory, base_url)
        self.src_path = self.root_path/CLENSING_DIR
        self.target_path = self.root_path/"markdown"
        
        MarkDownBuilder.delete_all_in_directory(self.target_path)
        

    def do_task(self):
        with open(self.src_path/SITEMAP_FILE, 'r', encoding='utf-8') as json_file:
            sitemap = json.load(json_file)   

        site_infos = []
        for page in sitemap:
            file_path = self.src_path/page.get("filename")

            
            try:
                with file_path.open(mode='r', encoding='utf-8') as file:
                    document = file.read()
                    document = self._transform_document(document)
                    self._save_document(os.path.basename(file.name), document)
                    site_infos.append({"filename": page.get("filename"), "url": page.get("url"), "uri": page.get("uri") , "menu" :  page.get("menu")})      
            except FileNotFoundError:
                print(f"The file {file_path} does not exist.")
            except Exception as e:
                print(file_path, ":",page.get("menu"),":",f"An error occurred: {e}") 
        sitemap_name = "sitemap.json"
        sitemap_path = self.target_path/sitemap_name
        sitemap_path.write_text(json.dumps(site_infos, ensure_ascii=False, indent=4))                  

    def _transform_document(self, document:str):
        return md(document)

    def _save_document(self, file_name:str, document:str):
        file_path = self.target_path/file_name
        file_path.write_text(document)  
