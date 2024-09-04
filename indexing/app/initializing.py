
import app
import json
import requests
from bs4 import BeautifulSoup, Comment
from llama_index.core import PromptTemplate
from app.llm import LLM


MENU_PROMPT = """
    HTML로 표시된 메뉴 구조를 보고 하기 기준을 참고하여 정보를 구조화하여 메뉴구조를 json 형태로 반환해줘                              
    - 메뉴그룹은 ul 로 묶임                                 
    - 메뉴는 메뉴 그룹하위에 li > div > a 혹은 li > div 태그로 표시 되며, 메뉴 텍스트는 a 혹은 div 태그 텍스트로 표시됨      
    - 메뉴그룹 이름은 그룹의 가장 가까운 div 형제노드로 표시됨                      
    - 현재 선택된 메뉴는 a 태그의 css속성으로 text-primary 속성을 가지고 있음
    - 상기 규칙에 어긋난 li 태그는 자신을 단일 메뉴로 포함하는 신규 메뉴그룹으로 취급할 것
    [주의]결과는 반드시 다음 예시와 같이 json 형식으로 출력합니다..
    ```
        [
            {{
                "name" : "메뉴 이름",
                "link" : "메뉴 링크, 없을 경우 공백 문자열",
                "menus" : [
                    {{
                        "name" : "서브 이름",
                        "link" : "메뉴 링크, 없을 경우 공백 문자열",
                        "menus" : [
                        ]
                    }},                                   
                ]
            }}
        ]       
    ```
                                                                    
    HTML: {data}
    출력 :                                       
"""
class MenuBuilder(app.BaseTask):


    def __init__(self,llm,menu_url, **kwargs):
        self.llm = llm
        self.menu_url = menu_url        
        super().__init__(initialize=False, **kwargs)

    

    def do_task(self):
        menus = MenuBuilder._build_gitbook_site_info(self.base_url+ self.menu_url, self.llm)

        targets = []
        for menu in menus:
            self._build_gitbook_target_link(menu, targets, "")

        with open(self.root_path/app.MENU_FILE, 'w', encoding='utf-8') as json_file:
            json.dump(targets, json_file, ensure_ascii=False, indent=4)          

    @staticmethod
    def _build_gitbook_site_info( url:str, llm: LLM = None):
        """
        [
            {
                "name": "에이스카운터",
                "link": "",
                "menus": [
                    {
                        "name": "에이스카운터 알아보기",
                        "link": "/acecounter",
                        "menus": []
                    },
                    {
                        "name": "에이스카운터 시작하기",
                        "link": "/acecounter/acecounter/start",
                        "menus": []
                    }
                ]
            },
        ]
        """
        response = requests.get(url)

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            soup = soup.find('aside')
            comments = soup.find_all(string=lambda text: isinstance(text, Comment))
            for comment in comments:
                comment.extract()
            soup.attrs = {}    
            for tag in soup.findAll(True):         
                if ( tag.name == 'img' or tag.name == 'iframe' ):
                    tag.attrs = {"src" : tag.attrs["src"]}
                elif tag.name == 'a':
                    tag.attrs = {"href" : tag.attrs["href"]}
                elif not tag.contents or all(str(child).strip() == "" for child in tag.contents):
                    tag.decompose()
                else:
                    tag.attrs = {}   
        else :
            print(response.status_code)

        data = soup
        prompt_template = PromptTemplate(MENU_PROMPT)
        # print(url)
        # print(data)
        # print(prompt_template.format(data=data))
        # print(llm)

        menu_json_str = llm.complete(prompt_template.format(data=data))

        return json.loads(menu_json_str.replace("```json\n","").replace("\n```",""))           

    @staticmethod
    def _build_gitbook_target_link(menu, targets, title):
        if(title):
            _title = title + " > " + menu.get("name")
        else:
            _title = menu.get("name")

        if menu.get("link",None):
            targets.append( {"title": _title,"url":menu.get("link",None), "include_media" : True} )

        for menu in menu.get("menus",[]):
            MenuBuilder._build_gitbook_target_link(menu, targets, _title) 

