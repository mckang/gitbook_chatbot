from app.crawling import WebPageDownloader, SiteReader
from typing import List
from app import Menu, SiteMap, MENU_FILE, SITEMAP_FILE
import json
from selenium.webdriver.chrome.options import Options
from selenium import webdriver



class CustomPageDownloader(WebPageDownloader):

    def __init__(self, save_directory: str=".", base_url:str =None, site_config:dict = None, **kwargs):
        super().__init__(save_directory, "https://dummy.url")
        self.site_config=site_config

        
    def _get_targets(self) -> List[Menu]:  
        return [ { "base_url": site['url'],"url": key, "title": value["title"]} for site in self.site_config['sitemap'] for key, value in site['pages'].items()]

    
    def _get_results_container(self) -> List[SiteMap]:  
        return []        
    
    def _finalize(self, results_container : List[SiteMap]):  
        sitemap_path = self.save_path/SITEMAP_FILE
        sitemap_path.write_text(json.dumps(results_container, ensure_ascii=False, indent=4))   
            

    def _worker(self, pages, queue ):


        def setup_driver():
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Headless 모드 설정
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")  
            chrome_options.add_argument("--start-maximized")
            # chromedriver_autoinstaller.install()
            return webdriver.Chrome(options=chrome_options)
        
        scraper = SiteReader(
            setup_driver=setup_driver,
            base_url= self.base_url
        )
    
        def callback(page, page_content):
            file_name = page.get("url").replace("/","__")+".html"
            file_path = self.save_path/file_name
            file_path.write_text(page_content)     
            queue.put([{"filename": file_name, "url": page.get("base_url") + page.get("url"), "uri": page.get("url"), "base_url": page.get("base_url") , "menu" :  page.get("title"), "error": False}])               

        scraper.load_data(pages, callback)
    