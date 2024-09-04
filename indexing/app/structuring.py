import app
from app import SITEMAP_FILE,  TRANSFORMED_DATA_DIR, STRUCTURED_DATA_DIR
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

# prompt_template = Template(
#     """
#     다음 HTML을 보고 [ 페이지 전체 요약과 각 서브 주제별 요약 ] 형식으로 정보를 구조화하여 json 파일을 만들어주세요.
#     모든 p 태그는 반드시 개행문자로 변경하여 표현해주세요.
#     모든 이미지 링크는 반드시 추출되어야 합니다.
#     !![중요]이미지 링크는 속해있는 주제 영역에 포함되어야 합니다.
#     !![중요]이미지 링크는 필요시 각 주제 영역에 중복으로 포함될수 있습니다.

#     전체 요약에서는 페이지 전체를 요약해서 간단한 문장과 주요 검색 키워드를 정리합니다.
#     - title : 전체 페이지 제목
#     - content : 전체 페이지를 요약하는 짧은 문장
#     - links : a href, iframe src와 img src 속성을 참고하여 설명 및 유형 정보와 함께, 다음 가이드에 따라 links 속성에 넣을 것
#     . type은 img, doc, video, link 4가지
#     . 헤더에 포함된 이미지는 전체 요약의 links에 포함시켜줘

#     서브 주제는 반드시 h2 태그내의 내용을 기준으로 구분되어야 하며 다음 요소를 추출하여 구성합니다
#     - title : 서브 주제 제목 (h2 태그내의 내용)
#     - source: 서브 주제에 해당하는 앵커 링크 (h2 태그의 내부 a 태그의 href 속성)
#     - content : 해당 내용을 기반으로 질문에 충분히 답변할 수 있는 형태의 문장 (단계별/열거형 설명은 반드시 모든 단계/열거를 포함하고, 열거 형식으로 표현할 것)
#     - links : a href, iframe src와 img src 속성을 참고하여 설명 및 유형 정보와 함께, 다음 가이드에 따라 links 속성에 넣을 것
#     . type은 img, doc, video, link 4가지
#     - nexts : a 태그의 href 속성이 '${DATA_GITBOOK_SITE}' 로 시작하는 a 태그 텍스트와 링크를 표시할 것
    
#     [주의]결과는 다음 예시와 같은 형식입니다.
#     ```
#         {{
#             "page" : {{
#                 "title":"서비스 소개 및 장점", 
#                 "content" : "처음 시작하시는 분들을 위해  '통계 데이터 확인 방법'을 영상으로 설명드릴게요. 주요기능은 다음과 같습니다.", 
#                 "links"=[
#                         {{"link":"main.jpg","desc":"서비스 소개 및 장점", "type":"img"}},                                     
#                         ],                
#                 "subjects" : ["서비스 소개","서비스 장점"],                                    
#             }},
#             "subjects" : [
#                 {{
#                     "source":"#undefined"
#                     "title":"서비스 소개", 
#                     "content" : "분석을 위해 사이트 소스에 적용해야 하는 자바스크립트로 만들어진 태그입니다.", 
#                     "links"=[
#                         {{"link":"test.jpg","desc":"서비스 주요기능", "type":"img"}},                                     
#                         ],
#                     "nexts"=[
#                         {{"question":"주요기능","href":"${DATA_GITBOOK_SITE}/sub/crm/mall/step-1"}},         
#                         {{"question":"가격정보","href":"${DATA_GITBOOK_SITE}/sub/crm/mall/step-1"}},                             
#                     ],                                  
#                 }},
#             ]
#         }}
#     ```
                 
#     HTML: 
#     {data}
                                     
#     JSON:                                          
#     """
# )

prompt_template = Template(
    """
You are an expert in parsing Markdown documents and structuring information in the format of [Overall Page Summary and Each Subtopic Summary] and converting it into JSON format. Please follow the instructions below to convert the given Markdown into JSON format.

[[Instructions]]    
    In the overall summary, summarize the entire page into a simple sentence and list the main search keywords.
    - title: The title of the entire page
    - content: A short sentence summarizing the entire page
    - links: Refer to the a href, iframe src, and img src attributes to include description and type information in the links attribute according to the following guide
        . type can be one of img, doc, video, link
        . Images included in the header should be included in the links of the overall summary

    Subtopics must be divided based on the content within the h2 tags and should be structured with the following elements:
    - title: The title of the subtopic 
    - source: The anchor link corresponding to the subtopic (href attribute)
    - summary: A sentence that can sufficiently answer questions based on the content
    - content: original content text(step-by-step/enumeration explanations must include all steps/enumerations and be expressed in an enumerated format)
    - links: Refer to the a href, iframe src, and img src attributes to include description and type information in the links attribute according to the following guide
        . type can be one of img, doc, video, link
    - nexts: Display the text and link of a tags whose href attribute starts with 'https://socialbiz.gitbook.io'

    All p tags must be converted to newline characters.
    All image links must be extracted.
    !![Important] Image links must be included in the topic area they belong to.
    !![Important] Image links may be included redundantly in each topic area if necessary.
    !![Important] All structured content must be generated in the korean language.

[Output JSON Example]
```
    {{
        "page" : {{
            "title":"Service Introduction and Benefits", 
            "content" : "For those who are starting for the first time, we will explain 'how to check statistical data' through a video. The main features are as follows.", 
            "links":[
                    {{"link":"main.jpg","desc":"Service Introduction and Benefits", "type":"img"}},                                     
                    ],                
            "subjects" : ["Service Introduction","Service Benefits"],                                    
        }},
        "subjects" : [
            {{
                "source":"#undefined"
                "title":"Service Introduction", 
                "content" : "It is a tag made of JavaScript that needs to be applied to the site source for analysis.", 
                "links":[
                    {{"link":"test.jpg","desc":"Main Features of the Service", "type":"img"}},                                     
                    ],
                "nexts":[
                    {{"desc":"Main Features","link":"https://socialbiz.gitbook.io/sub/crm/mall/step-1",  "type":"link"}},         
                    {{"desc":"Price Information","link":"https://socialbiz.gitbook.io/sub/crm/mall/step-1", "type":"link"}},                                 
                ],                                  
            }},
        ]
    }}
```
                 
Markdown: 
{data}
                                     
JSON:                                          
"""
)

prompt = prompt_template.substitute(os.environ)
 

class DataStructurer(app.BaseMultiTask):  
    def __init__(self, save_directory: str=".", base_url:str =None, llm: LLM = None, **kwargs):
        super().__init__(save_directory, base_url)
        self.llm = llm
        self.src_path = self.root_path/TRANSFORMED_DATA_DIR
        self.target_path = self.root_path/STRUCTURED_DATA_DIR
        DataStructurer.delete_all_in_directory(self.target_path) 

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
                    document = self._transform_document(document, page.get("image_map",[]))
                    document.get("page")["title"] = page.get("menu")
                    document.get("page")["source"] = page.get("url")
                    filename = os.path.splitext(os.path.basename(file.name))[0]+".json"
                    self._save_document(filename, document)
                    # site_infos.append({"filename": filename, "url": page.get("url"), "menu" :  page.get("menu"), "error": False})  
                    queue.put([{"filename": filename, "url": page.get("url"), "uri": page.get("uri"), "menu" :  page.get("menu"), "error": False}])      
            except FileNotFoundError:
                print(f"The file {file_path} does not exist.")
                site_infos.append({"filename": filename, "url": page.get("url"), "uri": page.get("uri"), "menu" :  page.get("menu"), "error": True}) 
            except Exception as e:
                print(file_path, ":",page.get("menu"),":",f"An error occurred: {e}") 
                site_infos.append({"filename": filename, "url": page.get("url"), "uri": page.get("uri"), "menu" :  page.get("menu"), "error": True}) 
        queue.put(site_infos)

    def _transform_document(self, document:str, image_map:dict):
        # image_map ={}

        # soup = BeautifulSoup(document, 'html.parser')
        # for tag in soup.findAll(True):         
        #     if ( tag.name == 'img' or tag.name == 'iframe' ):
        #         hash_object = hashlib.md5(tag.attrs["src"].encode('utf-8'))
        #         hash_hex = hash_object.hexdigest()
        #         image_map[hash_hex]=tag.attrs["src"]
        #         tag.attrs = {"src" : hash_hex}
        #     elif tag.name == 'a':
        #         tag.attrs = {"href" : tag.attrs["href"]}
        #     elif not tag.contents or all(str(child).strip() == "" for child in tag.contents):
        #         tag.decompose()
        #     else:
        #         tag.attrs = {}      

        # num_tokens = count_tokens(str(soup))
        # if(num_tokens > 10*1024 ):
        #     print("!important. 과다한 토큰 사용으로 img tag를 제거합니다.")
        #     imgs = soup.find_all("img")
        #     for img in imgs:
        #         img.decompose()
        #     # _template=md(str(template))

        # data = str(soup)

        prompt_template = PromptTemplate(prompt)
        page_info_str = self.llm.complete(prompt_template.format(data=document))
        try:
            page_info = json.loads(page_info_str.replace("```json\n","").replace("\n```",""))
        except JSONDecodeError as e:
            print("*"*100)
            print(page_info_str)
            print("*"*100)
            print(e)
            print("*"*100)

        page_info["image_map"]=image_map
        return page_info        
        # return str(soup)

    def _save_document(self, file_name:str, document:dict):
        file_path = self.target_path/file_name
        file_path.write_text(json.dumps(document, ensure_ascii=False, indent=4))  

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()

    DATA_TASK_MODEL = os.getenv('DATA_TASK_MODEL')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') 
    structurer = DataStructurer(base_url="https://socialbiz.gitbook.io", save_directory="data", llm=LLM(temperature=0, model=DATA_TASK_MODEL, api_key=OPENAI_API_KEY))

    structurer.do_task()

  
               