import os
import json
import re



class DataProcessor(object):

    def __init__(self,file_name):
        super().__init__()
        self.file_name=file_name
        if type(self.file_name)!=str or not os.path.exists(file_name):
            print('error ,no {}'.format(file_name))
        
        self._load_file(file_name)
        self._clean_data()


    def _load_file(self,file_name):
        with open(file_name,'r',encoding='gbk') as f:
            json_list=json.loads(f.read())

        self.data=json_list

    def _clean_data(self):

        #content_cn为空的去除
        data=[]
        for i in self.data:
            if len(i['content_cn'])<3:
                continue
            i['content_cn']=i['content_cn'].replace(' ','')

            # pattern = re.compile("[^\u4e00-\u9fa5^,^.^!^a-z^A-Z^0-9]")  #只保留中英文、数字和符号，去掉其他东西
            # #若只保留中英文和数字，则替换为[^\u4e00-\u9fa5^a-z^A-Z^0-9]
            # line=re.sub(pattern,'',i['content_cn'])  #把文本中匹配到的字符替换成空字符
            # i['content_cn']=''.join(line.split())
    
            #过滤非法字符，去除空格。
            data.append(i)


        self.data=data
    
    def select_text(self,query):

        result=[]
        for i in self.data:
            if query in i['title_cn']:
                result.append(i)
        return result

    def save_txt_line(self,json_list,query):

        save_file_name='{}_txt_line.txt'.format(query)
        data=[]

        for i in json_list:
            t=i['content_cn'].split('。')
            for j in t:
                if query in j:
                    data.append(j)
        
        with open(save_file_name,'w',encoding='utf-8') as f:
            f.writelines([i+'。\n' for i in data])


    def show_list(self,json_list,attr=None):

        for i in json_list:
            for k,v in i.items():
                if attr==None:
                    print(k,":",v)
                    print()
                else:
                    for j in attr:
                        if k==j:
                            print(k,":",v)
            print()
            print('==============================================')

if __name__=='__main__':
    dataset=DataProcessor('../data/sample_8000.json')
    yx_list=dataset.select_text('演习')
    dataset.show_list(yx_list,['content_cn'])
    dataset.save_txt_line(yx_list,'演习')



    
        



    
