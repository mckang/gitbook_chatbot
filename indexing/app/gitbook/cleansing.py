from app.cleansing import HtmlCleanser
from bs4 import BeautifulSoup, Comment


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

class GitbookHtmlCleanser(HtmlCleanser): 
                
    def _transform_document(self, document:str):
        template = BeautifulSoup('<main></main>', 'html.parser')
        soup = BeautifulSoup(document, 'html.parser')
        soup = soup.body.main      
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()
        soup.attrs = {}    
        for tag in soup.findAll(True):         
            if ( tag.name == 'img' or tag.name == 'iframe' ):
                tag.attrs = {"src" : tag.attrs["src"]}
            elif tag.name == 'a':
                if "mailto:" in tag.attrs["href"] :
                    tag.decompose()
                    continue
                tag.attrs = {"href" : tag.attrs["href"]}
            elif not tag.contents or all(str(child).strip() == "" for child in tag.contents):
                tag.decompose()
            else:
                tag.attrs = {}      

        # remove_empty_tags(soup)
        header = soup.header
        body = soup.div

        template.main.append(header)
        template.main.append(body)     
        return str(template)

           