from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Any
from tqdm import tqdm
from multiprocessing import Pool, Manager, cpu_count   
import os
import shutil

RAW_DIR = "raw"
CLENSING_DIR = "stage"
STRUCTURED_DATA_DIR = "data"
INDEXED_DATA_DIR = "store"
TRANSFORMED_DATA_DIR = "transform"
MENU_FILE = "menus.json"
SITEMAP_FILE = "sitemap.json"

class BaseTask(ABC):

    def __init__(self, save_directory: str=".", base_url: str = None, initialize:bool = False, **kwargs):
        if(not base_url):
            raise ValueError("Invalid argument: base_url은 유효한 url 주소이어야 합니다.")
        self.save_directory = save_directory
        self.base_url = base_url
        # self.root_path = Path(self.save_directory+ "/" + self.base_url.replace("https://","").replace("http://","").replace(".","_").replace("/","__"))
        self.root_path = Path(self.save_directory)

        if initialize and self.root_path.exists(): 
            try:
                shutil.rmtree(self.root_path)
                print(f"Directory '{self.root_path}' has been removed successfully.")
            except Exception as e:
                print(f"An error occurred while deleting the directory: {e}")   

        if not self.root_path.exists():
            self.root_path.mkdir(parents=True, exist_ok=True)
            print(f"디렉토리가 생성되었습니다: {self.root_path}")        

    @abstractmethod
    def do_task(self):
        pass        

    @staticmethod
    def delete_all_in_directory(directory_path: Path):
        if not os.path.exists(directory_path):
            directory_path.mkdir(parents=False, exist_ok=True)
            return

        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')    


from typing import TypeVar, Generic
T = TypeVar('T')
R = TypeVar('R')
class BaseMultiTask(BaseTask, Generic[T,R]):

    def do_task(self):
        targets = self._get_targets()
        results_container = self._get_results_container()
        self._do_multi_task(targets, results_container)
        self._finalize(results_container)

    def _do_multi_task(self, targets : List[T], results_container: List[R]):
        # 결과를 저장할 큐
        manager = Manager()
        queue = manager.Queue()
        
        # 배치 크기 설정
        batch_size = 5
        
        # URL 리스트를 배치 단위로 나누기
        batches = [targets[i:i + batch_size] for i in range(0, len(targets), batch_size)]

        # 프로세스 풀 생성 (동시에 실행될 프로세스 개수 제한)
        # with Pool(processes=5) as pool:
        #     pool.starmap(self.worker, [(batch, queue) for batch in batches])
        # 큐에서 결과를 가져와 출력
        # while not queue.empty():
        #     site_infos.extend(queue.get()) 

        num_processes = 1 if cpu_count() <=2 else min(4, cpu_count() - 2)
        pool = Pool(processes=num_processes)
        print("num_processes", num_processes)
        with tqdm(total=len(targets)) as pbar:
            # 각 URL에 대해 worker 함수 호출
            pool.starmap_async(self._worker, [(batch, queue) for batch in batches])
            # 모든 작업이 완료될 때까지 진행 상황 업데이트
            completed_tasks = 0
            while completed_tasks < len(targets):
                results = queue.get()
                results_container.extend(results) 
                completed_tasks += len(results)
                pbar.update(len(results))
        pool.close()
        pool.join() 


    @abstractmethod
    def _get_targets(self) -> List[T]:  
        pass

    @abstractmethod
    def _get_results_container(self) -> List[R]:  
        pass    

    @abstractmethod
    def _worker(self, jobs : List[T], queue ):      
        pass

    @abstractmethod
    def _finalize(self, results_container: List[R]):  
        pass      