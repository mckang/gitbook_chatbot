
from pathlib import Path
import shutil

from app.structuring import DataStructurer
import json, tqdm

from llama_index.core import Document
from llama_index.core.schema import TextNode

import app, hashlib
from app import STRUCTURED_DATA_DIR, INDEXED_DATA_DIR, SITEMAP_FILE

from llama_index.core.schema import NodeRelationship, RelatedNodeInfo
class VectorstoreIndexer(app.BaseTask): 

    def __init__(self, save_directory: str=".", base_url:str =None, do_index = None , refresh_index = True, **kwargs):
        super().__init__(save_directory, base_url)
        self.do_index = do_index
        self.src_path = self.root_path/STRUCTURED_DATA_DIR
        self.target_path = self.root_path/INDEXED_DATA_DIR
          
        if refresh_index:
            VectorstoreIndexer.delete_all_in_directory(self.target_path)   
        

    def do_task(self):    
        documents = self._load_documents()   
        if (self.do_index):
            self.do_index(documents, self.target_path)

    def _load_documents(self):
        with open(self.src_path/SITEMAP_FILE, 'r', encoding='utf-8') as json_file:
            sitemap = json.load(json_file)   

        documents = []
        for page in sitemap:
            file_path = self.src_path/page.get("filename")

            try:
                with file_path.open(mode='r', encoding='utf-8') as file:
                    data = json.load(file)
                    page = data.get("page",{})
                    image_map = data.get("image_map",{})
                    subjects = data.get("subjects",[])   

                    links = page.get("links",[])
                    for link in links:
                        if link.get("type","") == "img":
                            if image_map.get(link["link"]):
                                link["link"] = image_map.get(link["link"],"UNKNOWN")  
                            else: 
                                links.remove(link)

                    document = Document(
                            id_ = hashlib.md5(page.get("title","").encode('utf-8')).hexdigest(),
                            # text="Title: " + page.get("title","") + "\n"
                            #      "Body: " + page.get("content"),
                            text= page.get("title","") + "\n" + page.get("content"),                           
                            metadata={
                                "body" : "",
                                "source" : page.get("source",""),
                                "links": json.dumps(links, ensure_ascii=False, indent=4),
                                "nexts": json.dumps([ page.get("title","") + " > " + subject for subject in page.get("subjects",[])], ensure_ascii=False, indent=4)
                            },
                            excluded_llm_metadata_keys=["nexts","links" ],
                            excluded_embed_metadata_keys = [ "links","nexts","source","body"],
                            metadata_template="{key}=>{value}",
                            text_template="Content:\n{content}\n-----\nMetadata:\n{metadata_str}\n=====\n",                            
                    )
                    print("indexing : ", page.get("title",""))
                    documents.append(document)    
                    _prev_id = None
                    _prev_document = None                      
                    for subject in subjects:
                        _id = hashlib.md5((page.get("title","") + "_" +  subject.get("title","")).encode('utf-8')).hexdigest()
                        _relationships = {NodeRelationship.SOURCE: RelatedNodeInfo(node_id=document.id_)}
                        if (_prev_id) :
                            _relationships[NodeRelationship.PREVIOUS] = RelatedNodeInfo(node_id=_prev_id)
                        if (_prev_document) :
                            _prev_document.relationships[NodeRelationship.NEXT] = RelatedNodeInfo(node_id=_id)   

                        _links = subject.get("links",[])
                        for _link in _links:
                            if _link.get("type","") == "img":
                                if image_map.get(_link["link"]):
                                    _link["link"] = image_map.get(_link["link"])  
                                else: 
                                    _links.remove(link)

                        _document = Document(
                                id_ = _id,
                                # text="Title: " + page.get("title","") + " > " +  subject.get("title",""),
                                # text= page.get("title","") + "\n" +  subject.get("title",""),
                                text = document.text  + "\n\n" +  subject.get("title","")+ "\n" +  subject.get("summary",""),
                                metadata={
                                    "body" : subject.get("content"),
                                    "source" : page.get("source","") + subject.get("source",""),
                                    "links": json.dumps(_links, ensure_ascii=False, indent=4),
                                    "nexts": json.dumps([ page.get("title","") + " > " +  subject.get("title","") + " > " + next.get("desc","") for next in page.get("nexts",[])], ensure_ascii=False, indent=4)
                                },
                                embedding=document.embedding,
                                excluded_embed_metadata_keys=document.excluded_embed_metadata_keys,
                                excluded_llm_metadata_keys=document.excluded_llm_metadata_keys,
                                metadata_seperator=document.metadata_seperator,
                                metadata_template=document.metadata_template,
                                text_template=document.text_template,
                                relationships=_relationships,                           
                        )
                        print("indexing : ", page.get("title","") + " > " +  subject.get("title",""))
                        documents.append(_document)
                        _prev_id, _prev_document = _id, _document 
                                       
            except FileNotFoundError:
                print(f"The file {file_path} does not exist.")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from file {json_file}: {e}")                
            except Exception as e:
                print(f"An error occurred: {e}")             

        return documents