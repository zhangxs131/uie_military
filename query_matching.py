from matplotlib.collections import QuadMesh
from sentence_transformers import SentenceTransformer, util
from show import read_file,template_class,show_list
import numpy as np
import torch

class Query_Matching(object):

    def __init__(self,data_file) -> None:
        self.model=SentenceTransformer('distiluse-base-multilingual-cased-v1',cache_folder='./models')
        self.load_cn_file(data_file)
        

    def query_embedding(self,input_query):

        query_embedding=self.model.encode([input_query])
        
        return query_embedding

    
    def titles_embedding(self,title_list):
        
        title_embedding=self.model.encode(title_list)
        return title_embedding
    
    def load_cn_file(self,file_path):
        self.data=read_file(file_path)
        title_list=[i['title_cn'] for i in self.data]
        self.title_embeddings=self.titles_embedding(title_list)
        
    def ranking_text(self,query,select_num=5):
        
        top_k = min(select_num, len(self.data))
        
        query_embedding=self.query_embedding(query)
        
        
        result=util.semantic_search(query_embedding, self.title_embeddings, score_function=util.dot_score)
        # cos_scores = util.cos_sim(query_embedding, self.title_embeddings)[0]
        # top_results = torch.topk(cos_scores, k=top_k)
        # # result=util.dot_score(query_embedding,self.title_embeddings)
        # # max_id=np.argmax(result, axis=1)
        # for score, idx in zip(top_results[0], top_results[1]):
        #     print(self.data[idx]['title_cn'], "(Score: {:.4f})".format(score))
        #     show_list([self.data[idx]])


if __name__=='__main__':
    qm=Query_Matching('./data/content_1000.json')
    qm.ranking_text('装备研发')
    
            
        



        
        
    
