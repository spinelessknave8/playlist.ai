import requests
import heapq
import models
import time

class FacebookBART:
    def __init__(self,token,url):
        self.token = token
        self.url = url
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.chunked_genres = self.make_chunks(models.sp.recommendation_genre_seeds()['genres'])
    
    #this is the function to call when you need to categorise something
    def categorise(self,input_query:str)->list:
        
        max_retries = 3
        result_heap = []
        
        for candidate_labels in self.chunked_genres:
            payload = {
                "inputs": input_query,
                "parameters": {"candidate_labels": candidate_labels},
            }
            
            retries = 0
            
            while retries < max_retries:
                response = requests.post(self.url, headers=self.headers, json=payload)

                if response.status_code == 200:
                    result = response.json()
                    for i,_ in enumerate(result['labels']):
                        if result['scores'][i] > 0.3:
                            result_heap.append( (-1*result['scores'][i], result['labels'][i]) )
                    break
                    
                elif response.status_code:
                    error_data = response.json()
                    estimated_time = error_data.get("estimated_time", 10)
                    time.sleep(estimated_time)
                    retries += 1
                    
                else:
                    print(f"Error: {response.status_code}, {response.text}")
        
        print("max retries reached") if retries == max_retries else None
        
        heapq.heapify(result_heap)
        result = []
        
        for i in range(min(len(result_heap),5)):
            genre = heapq.heappop(result_heap)
            result.append(genre[1])
        
        return result

    """below function is only to chunk the genres in sizes of 10 becauses 
    thats the current max of the hugging face api candidate_labels feature"""
    def make_chunks(self,input_list,size_chunk = 10):
        result = []
        while len(input_list) >= size_chunk:
            sublist = input_list[:10]
            result.append(sublist)
            input_list = input_list[9:]
        result.append(input_list)
        return result
