
from pprint import pprint 
from paddlenlp import Taskflow
from paddlenlp.transformers import AutoModel
import warnings
import os
import json

warnings.filterwarnings("ignore")


class UIE():
    def __init__(self,schema):

        if type(schema)==str:
            if os.path.exists(schema):
                self.schema=self._load_schema(schema)
        
            else:
                print('cant find schema file in {}'.format(schema))
        else:
            self.schema=schema

        self.ie=Taskflow('information_extraction',schema=schema,model='uie-base',cache_dir='./uie-base')

    def extraction_text(self,text):
        result=self.ie(text)

        return result

    def _load_schema(self,json_file):
        with open(json_file,'r',encoding='utf-8') as f:
            json_file=json.loads(f.read())

        return json_file


if __name__=='__main__':
    yanxi_ie=UIE('./schema/yanxi.json')
    input_text=['美国海军基尔萨奇号（LHD 3）两栖准备群(ARG)和第22海军陆战队远征部队(MEU)正在波罗的海进行演习行动，以加强与北约关键盟友和伙伴的互操作性。']
    result=yanxi_ie.extraction_text(input_text)
    pprint(result)



