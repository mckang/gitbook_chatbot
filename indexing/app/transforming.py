import app
from app import SITEMAP_FILE,  CLENSING_DIR, TRANSFORMED_DATA_DIR
from app import Menu, SiteMap, StructuredSiteMap
from app.llm import LLM
from llama_index.core import PromptTemplate


import tiktoken

from bs4 import BeautifulSoup

import os, json, hashlib
from pathlib import Path
from typing import List, Any
from json import JSONDecodeError
from string import Template

from tqdm import tqdm
import warnings  



def count_tokens(text, model_name='cl100k_base'):
    # 모델 이름에 맞는 토크나이저 가져오기
    tokenizer = tiktoken.get_encoding(model_name)
    
    # 텍스트를 토크나이즈
    tokens = tokenizer.encode(text)
    
    # 토큰 개수 출력
    num_tokens = len(tokens)
    return num_tokens       


prompt_template = Template(
    """
Please convert the following HTML content into Markdown format. Adhere to the following guidelines during the conversion:

1. **Headers:**
   - Convert `<h1>` to `<h6>` tags to Markdown headers using `#` symbols.
   - Example: `<h1>Title</h1>` → `# Title`

2. **Images:**
   - Convert `<img>` tags to the `![Alt Text](Image URL)` format.
   - If the `alt` attribute is missing, use a descriptive text for the Alt Text.
   - Example: `<img src="image.jpg" alt="Description">` → `![Description](image.jpg)`

3. **Links:**
   - Convert `<a href="URL">Link Text</a>` to the `[Link Text](URL)` format.
   - Example: `<a href="https://example.com">Example</a>` → `[Example](https://example.com)`

4. **Emphasis:**
   - Convert `<strong>` or `<b>` tags to `**text**`.
   - Convert `<em>` or `<i>` tags to `*text*`.

5. **Blockquotes:**
   - Convert `<blockquote>` tags using the `>` syntax.
   - Example: `<blockquote><p>Quote</p></blockquote>` → `> Quote`

6. **Lists:**
   - Unordered lists (`<ul>`) should be converted using `-` or `*`.
   - Ordered lists (`<ol>`) should use numbers followed by periods.
   - Example:
     ```html
     <ul>
       <li>First item</li>
       <li>Second item</li>
     </ul>
     ```
     → 
     ```markdown
     - First item
     - Second item
     ```

7. **Code Blocks:**
   - Convert `<pre><code>` blocks using triple backticks (```) for Markdown.
   - Example:
     ```html
     <pre><code>Code content</code></pre>
     ```
     → 
     ```markdown
     ```
     Code content
     ```
     ```

8. **Other HTML Elements:**
   - Tags like `<span>`, `<div>`, `<p>`, etc., should be converted using appropriate Markdown syntax or removed if unnecessary.
   - Remove unnecessary tags and retain only the content.

9. **Line Breaks:**
   - Use empty lines to represent paragraph breaks.
   - For line breaks within lists or blockquotes, add two spaces at the end of the line before pressing Enter.

10. **Additional Formatting:**
    - Utilize other Markdown features such as tables or horizontal rules as needed to reflect the structure of the HTML.

!![Important] All structured content must be generated in the korean language.

**Original HTML:**
{data}
                                       
"""
)

prompt = prompt_template.substitute(os.environ)
 

class DataTransformer(app.BaseMultiTask):  
    def __init__(self, save_directory: str=".", base_url:str =None, llm: LLM = None, **kwargs):
        super().__init__(save_directory, base_url)
        self.llm = llm
        self.src_path = self.root_path/CLENSING_DIR
        self.target_path = self.root_path/TRANSFORMED_DATA_DIR
        DataTransformer.delete_all_in_directory(self.target_path) 

    def _get_targets(self) -> List[SiteMap]:  
        with open(self.src_path/"sitemap.json", 'r', encoding='utf-8') as json_file:
            pages = json.load(json_file)   
        return pages         
    
    def _get_results_container(self) -> List[SiteMap]:  
        return []        
    
    def _finalize(self, results_container : List[SiteMap]):  
        sitemap_path = self.target_path/app.SITEMAP_FILE
        sitemap_path.write_text(json.dumps(results_container, ensure_ascii=False, indent=4))   

    def _worker(self, pages, queue ):
        warnings.filterwarnings("ignore", category=Warning, module='bs4')
        site_infos = []
        for page in pages:
            file_path = self.src_path/page.get("filename")
            try:
                with file_path.open(mode='r', encoding='utf-8') as file:
                    document = file.read()
                    page_info = self._transform_document(document)
                    
                    filename = os.path.splitext(os.path.basename(file.name))[0]+".md"
                    self._save_document(filename, page_info.get("content",""))
                    queue.put([{"filename": filename, 
                                "url": page.get("url"), 
                                "uri": page.get("uri"), 
                                "menu" :  page.get("menu"), 
                                "error": False, 
                                "image_map": page_info.get("image_map",[])}])      
            except FileNotFoundError:
                print(f"The file {file_path} does not exist.")
                site_infos.append({"filename": filename, "url": page.get("url"), "uri": page.get("uri"), "menu" :  page.get("menu"), "error": True, "image_map":[]}) 
            except Exception as e:
                print(file_path, ":",page.get("menu"),":",f"An error occurred: {e}") 
                site_infos.append({"filename": filename, "url": page.get("url"), "uri": page.get("uri"), "menu" :  page.get("menu"), "error": True, "image_map":[]}) 
        queue.put(site_infos)

    def _transform_document(self, document:str):
        image_map ={}

        soup = BeautifulSoup(document, 'html.parser')
        for tag in soup.findAll(True):         
            if ( tag.name == 'img' or tag.name == 'iframe' ):
                hash_object = hashlib.md5(tag.attrs["src"].encode('utf-8'))
                hash_hex = hash_object.hexdigest()
                image_map[hash_hex]=tag.attrs["src"]
                tag.attrs = {"src" : hash_hex}
            elif tag.name == 'a':
                tag.attrs = {"href" : tag.attrs["href"]}
            elif not tag.contents or all(str(child).strip() == "" for child in tag.contents):
                tag.decompose()
            else:
                tag.attrs = {}      

        num_tokens = count_tokens(str(soup))
        if(num_tokens > 10*1024 ):
            print("!important. 과다한 토큰 사용으로 img tag를 제거합니다.")
            imgs = soup.find_all("img")
            for img in imgs:
                img.decompose()
            # _template=md(str(template))

        data = str(soup)

        prompt_template = PromptTemplate(prompt)
        page_info_str = self.llm.complete(prompt_template.format(data=data))
        page_info = {}
        try:
            page_info["content"] = page_info_str.replace("```markdown\n","").replace("\n```","")
        except JSONDecodeError as e:
            print("*"*100)
            print(page_info_str)
            print("*"*100)
            print(e)
            print("*"*100)

        page_info["image_map"] = image_map
        return page_info        

    def _save_document(self, file_name:str, content:str):
        file_path = self.target_path/file_name
        file_path.write_text(content)  

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()

    DATA_TASK_MODEL = os.getenv('DATA_TASK_MODEL')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') 
    structurer = DataTransformer(base_url="https://socialbiz.gitbook.io", save_directory="data", llm=LLM(temperature=0, model=DATA_TASK_MODEL, api_key=OPENAI_API_KEY))

    structurer.do_task()

  
               