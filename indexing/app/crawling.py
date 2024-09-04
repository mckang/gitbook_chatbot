import requests
from bs4 import BeautifulSoup, Comment

from pathlib import Path
import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
from typing import List, Optional

import app

from multiprocessing import Pool, Manager    
from typing import List, Any
from collections import namedtuple
from app import Menu, SiteMap

import chromedriver_autoinstaller

class SiteReader:
    def __init__(self, setup_driver, base_url:str):
        self.setup_driver = setup_driver
        self.driver = self.setup_driver()
        self.base_url = base_url
    
    def clean_url(self, url):
        return url.split("#")[0]

    def restart_driver(self):
        self.driver.quit()
        self.driver = self.setup_driver()
    
    def extract_content(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        return self.driver.page_source       

    def load_data(self, pages: List[Any], callback ) -> List[str]:
        """Load data from pages URL.

        Args:
            pages (List[Any]): URL to scrap.


        Returns:
            List[str]: List of scraped documents.
        """


        for page in pages:
            if (page.get("base_url", None)):
                current_url = page.get("base_url") + page.get("url")
            else:
                current_url = self.base_url + page.get("url")
            
            # print(f"Visiting: {current_url}, {len(pages)} left")

            try:
                self.driver.get(current_url)
                page_content = self.extract_content()
                callback(page, page_content)
                time.sleep(1)

            except WebDriverException:
                print("WebDriverException encountered, restarting driver...")
                self.restart_driver()
            except Exception as e:
                print(f"An unexpected exception occurred: {e}, skipping URL...")
                continue

        self.driver.quit()




class WebPageDownloader(app.BaseMultiTask):

    def __init__(self, save_directory: str=".", base_url:str =None, **kwargs):
        super().__init__(save_directory, base_url)
        self.save_path = self.root_path/app.RAW_DIR
        # if not self.save_path.exists():
        #     self.save_path.mkdir(parents=True, exist_ok=True)        
        WebPageDownloader.delete_all_in_directory(self.save_path)
    

    # def json_to_namedtuple(self, data, name='Menu'):
    #     if isinstance(data, dict):
    #         fields = {k: self.json_to_namedtuple(v, k) for k, v in data.items()}
    #         return namedtuple(name, fields.keys())(*fields.values())
    #     elif isinstance(data, list):
    #         return [self.json_to_namedtuple(item, name) for item in data]
    #     else:
    #         return data
        
    def _get_targets(self) -> List[Menu]:  
        with open(self.root_path/app.MENU_FILE, 'r', encoding='utf-8') as json_file:
            urls = json.load(json_file)             
        return [ url for url in urls if not ( url.get("url").startswith("http://") or url.get("url").startswith("https://"))]
    
    def _get_results_container(self) -> List[SiteMap]:  
        return []        
    
    def _finalize(self, results_container : List[SiteMap]):  
        sitemap_path = self.save_path/app.SITEMAP_FILE
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
            queue.put([{"filename": file_name, "url": self.base_url + page.get("url"), "uri": page.get("url") , "menu" :  page.get("title"), "error": False}])               

        scraper.load_data(pages, callback)

        # site_infos = []
        # for page in pages:
        #     print(page + " downloads start ")
        #     # site_infos.append({"filename": page.get("url").replace("/","__")+".html", "url": self.base_url + page.get("url"), "menu" :  page.get("title")})
        #     # time.sleep(1)
        #     if not self._try_request(driver, self.base_url + page.get("url")):
        #         print("Failed to retrieve the page after multiple attempts. Refresh driver",page.get("url"))
        #         driver.quit()
        #         time.sleep(5)
        #         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        #         if not self.try_request(driver, self.base_url + page.get("url")):
        #             print("Failed to retrieve the page after multiple attempts. Skip this page",page.get("url"))
        #             site_infos.append({"filename": file_name, "url": self.base_url + page.get("url"), "menu" :  page.get("title"), "error":True})      
        #             continue
        
        #     time.sleep(5)
        #     page_content = driver.page_source    
        #     file_name = page.get("url").replace("/","__")+".html"
        #     file_path = self.save_path/file_name
        #     file_path.write_text(page_content)     
        #     site_infos.append({"filename": file_name, "url": self.base_url + page.get("url"), "menu" :  page.get("title"), "error": False})      
        #     print(page + " downloads end ")
        # queue.put(site_infos)                        
        # driver.quit() 

    # def _worker(self, pages, queue ):
    #     chrome_options = Options()
    #     chrome_options.add_argument("--headless")  # Headless 모드 설정
    #     chrome_options.add_argument("--no-sandbox")
    #     chrome_options.add_argument("--disable-dev-shm-usage")  
    #     # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)   
    #     driver = webdriver.Chrome(options=chrome_options)       
    

    #     site_infos = []
    #     for page in pages:
    #         print(page + " downloads start ")
    #         # site_infos.append({"filename": page.get("url").replace("/","__")+".html", "url": self.base_url + page.get("url"), "menu" :  page.get("title")})
    #         # time.sleep(1)
    #         if not self._try_request(driver, self.base_url + page.get("url")):
    #             print("Failed to retrieve the page after multiple attempts. Refresh driver",page.get("url"))
    #             driver.quit()
    #             time.sleep(5)
    #             driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    #             if not self.try_request(driver, self.base_url + page.get("url")):
    #                 print("Failed to retrieve the page after multiple attempts. Skip this page",page.get("url"))
    #                 site_infos.append({"filename": file_name, "url": self.base_url + page.get("url"), "menu" :  page.get("title"), "error":True})      
    #                 continue
        
    #         time.sleep(5)
    #         page_content = driver.page_source    
    #         file_name = page.get("url").replace("/","__")+".html"
    #         file_path = self.save_path/file_name
    #         file_path.write_text(page_content)     
    #         site_infos.append({"filename": file_name, "url": self.base_url + page.get("url"), "menu" :  page.get("title"), "error": False})      
    #         print(page + " downloads end ")
    #     queue.put(site_infos)                        
    #     driver.quit() 

    def _try_request(self, driver, url, retries=1, delay=3):
        from selenium.common.exceptions import WebDriverException
        for attempt in range(retries):
            try:
                driver.get(url)
                return True
            except WebDriverException as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(delay)
        return False
    

if __name__ == "__main__":
    downloader = WebPageDownloader(base_url="https://socialbiz.gitbook.io", save_directory="data")
    downloader.do_task()
