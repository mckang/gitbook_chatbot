from app.cleansing import HtmlCleanser
from bs4 import BeautifulSoup, Comment
from app import SITEMAP_FILE
import json, os

def remove_empty_tags(soup):
    # 모든 태그를 역순으로 순회 (자식부터 처리)
    for tag in soup.find_all(recursive=False):
        # 자식 태그가 있으면 재귀적으로 함수 호출
        if tag.find_all(recursive=False):
            remove_empty_tags(tag)
        # 태그의 문자열이 없고 자식 태그도 없으면 제거
        if not tag.get_text(strip=True) and not tag.find_all():
            if tag.name == 'img':
                continue  # img 태그는 삭제하지 않음            
            tag.decompose()

class CustomPageCleanser(HtmlCleanser): 
    def __init__(self, save_directory: str=".", base_url:str =None, site_config:dict = None, **kwargs):
        super().__init__(save_directory, "https://dummy.url")
        self.site_config=site_config


    def do_task(self):
        with open(self.src_path/SITEMAP_FILE, 'r', encoding='utf-8') as json_file:
            sitemap = json.load(json_file)   

        site_infos = []
        for page in sitemap:
            file_path = self.src_path/page.get("filename")

            
            try:
                with file_path.open(mode='r', encoding='utf-8') as file:
                    document = file.read()
                    document = self._transform_document_w_expression(page, document)
                    self._save_document(os.path.basename(file.name), document)
                    site_infos.append({"filename": page.get("filename"), "url": page.get("url"), "menu" :  page.get("menu")})      
            except FileNotFoundError:
                print(f"The file {file_path} does not exist.")
            except Exception as e:
                print(file_path, ":",page.get("menu"),":",f"An error occurred: {e}") 
        sitemap_name = "sitemap.json"
        sitemap_path = self.target_path/sitemap_name
        sitemap_path.write_text(json.dumps(site_infos, ensure_ascii=False, indent=4))                  

    def _transform_document(self, document:str):
        pass

    def _transform_document_w_expression(self, page:dict, document:str):
        # 기본 HTML 구조 생성
        template = BeautifulSoup('<main><head></head><body></body></main>', 'html.parser')
        
        # 문서 파싱
        soup = BeautifulSoup(document, 'html.parser')
        soup = soup.find('div', id='SITE_PAGES')
        if soup is None:
            raise ValueError("id가 'SITE_PAGES'인 <div> 태그를 찾을 수 없습니다.")
        
        # 주석 제거
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()
        
        # <style> 태그 제거
        for style_tag in soup.find_all('style'):
            style_tag.decompose()
        
        # 최상위 태그의 속성 제거
        if soup.contents:
            if hasattr(soup.contents[0], 'attrs'):
                soup.contents[0].attrs = {}
        wow_images = soup.find_all('wow-image')
        for tag in wow_images:
            # if tag.get('data-motion-part') == 'BG_IMG':
            tag.decompose()  # 태그 제거
        # 태그의 속성 처리
        for tag in soup.find_all(True):
            if tag.name in ['img', 'iframe']:
                src = tag.get('src')
                if src:
                    tag.attrs = {'src': src}
                else:
                    tag.decompose()
            elif tag.name == 'a':
                href = tag.get('href')
                if href:
                    if "mailto:" in href:
                        tag.decompose()
                        continue                      
                    tag.attrs = {'href': href}
                else:
                    tag.decompose()
            elif not tag.find_all(text=True, recursive=False) and not tag.find_all(recursive=False):
                tag.decompose()
            else:
                tag.attrs = {}
        # remove_empty_tags(soup)
        
        site_nodes = [ site for site in self.site_config["sitemap"] if site["url"] == page.get("base_url", None)]
        if not site_nodes:
            return ""
        expression = site_nodes[0].get("expressions",{}).get("clean")
        page_expression = site_nodes[0].get("pages").get(page.get("uri")).get("expressions",{}).get("clean", None)
        if page_expression:
            expression = page_expression
        
        local_namespace = {'soup':soup, 'template':template}
        exec(expression, globals(), local_namespace)
        # print(local_namespace)
        # custom_function = local_namespace['do_task']
        # template = custom_function(template, soup)
        return template.prettify()


           