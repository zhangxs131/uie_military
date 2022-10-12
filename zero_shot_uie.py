from paddlenlp import Taskflow
from pprint import pprint
from show import read_file,template_class,show_list
import argparse

import logging
logging.basicConfig(level=logging.WARNING)

import warnings
warnings.filterwarnings("ignore")


def load_task(schema,model_path='uie-base'):

    """
    uie schema
    实体抽取 ["人名","地名"]

    关系抽取 {"活动名":["主办方","承办方","举办次数"]}

    事件抽取 {
        xx触发词:['时间','位置','内容','结果']
    }

    model 可选择 uie-base,uie-mini,uie-m-large,uie-m-base

    其他参数，fp32，use_faster

    """
    ie=Taskflow('information_extraction',schema=schema,task_path=model_path)

    return ie

def choose_schema(choice_id=1):
    if choice_id==1:
        #演习
        
        schema=['国家','时间',
                    {'演习触发词':['国家','地点','部队','内容','时间']},
                    {'打击触发词':['装备名','打击行为','打击目标']},
                    {'装备':['名字','数量','动作','目标']},
                    {'武器':[['名字','数量','动作','目标']},
                    {'部队':['数量','行为']},
                    {'演习':['意义','目的','影响']}
        ]
    elif choice_id==2:
        #DARPA项目
        
        schema=['国家','时间','技术',
                    {'项目触发词':['公司','名称','目的','用途','阶段','时长']},
                    {'开发触发词':['时间','内容','目的']},
                    {'技术触发词':['名称','学科','领域','创新内容']},
                    {'研制':['意义','目的','影响']}
        ]
    elif choice_id==3:
        #装备研制
        
        schema=['国家','时间',
                    {'研制触发词':['机构','内容','时间']},
                    {'试验触发词':['机构','内容','时间']},
                    {'装备':['特点','性能','计划']},
                    {'研制':['意义','目的','影响']}
        ]
    else:
        schema=[]

    return schema

def generate_text(json_item,choice_id):
    schema=choose_schema(choice_id)
    ie=load_task(schema)
    
    show_list([json_item],['title_cn','content_cn'])

    input_text=json_item['content_cn']
    result=ie(input_text)
    
    #xm_text="{}\n {},{},".format()
    pprint(result)
    gen_text=template_ch_text(result,json_item,choice_id)
    
    print(gen_text)
    print('=======================================================================')
    
def get_args():
    parser=argparse.ArgumentParser(description='ner args')
    parser.add_argument('--template_type',type=int,default=1,help='使用模板类型，1，演习，2项目，3，装备研制')
    parser.add_argument('--predict_file',type=str,default='./data/2022-09-26_guowai_dongtai_06775without_tran_8000_content.json',help='抽取源文件')
    parser.add_argument('--learning_rate',type=float,default=3e-5,help='learning_rate')
    parser.add_argument('--batch_size',type=int,default=32,help='batch_SIZE')
    parser.add_argument('--gpu',type=int,default=0,help='使用的GPU序号')
    
    
    return parser.parse_args()
    
def template_ch_text(result,json_item,choice_id):
    
    
    sen=[]
    
    if choice_id==1:
        #结果解析，去重
        for i in result:
            zb_name=[]
            
            if k,v in i.items():
                if k=='国家'：
                    countries=[]
                    for j in v:
                        countries.append(j['text'])
                
                elif k=='时间':
                    time=v[0]['text']
                
                elif k=='武器':
                    for j in v:
                        zb_name.append(j['text'])
                    
                elif k=='装备':
                    for j in v:
                        zb_name.append(j['text'])
                    
                elif k=='部队':
                    army_names=[]
                    for j in v:
                        army_names.append(j['text'])
                    
                elif k=='演习':
                    
        
        
        
        #填充模板
        sen.append(json_item['title_cn'])
        sen.append("{},{}在{}举行{}演习".format(time,(',').join(countries),place,yx_name))
        second_sen="演习的重点在于"
        for i in aims:
            second_sen=second_sen+i+','
        sen.append(second_sen)

        sen.append('{}的{}参加了演习。'.format(country,(',').join(army_names)))
        
        t_sen='参演装备包括'
        for i in zb_name:
            t_sen=t_sen+i+','
        t_sen=t_sen+'等。'
        
        sen.append(t_sen)
        
        t_sen='参演中,'
        for i in zip(zb_name,zb_move,zb_target):
            t_sen=t_sen+i[0]+i[1]+i[2]+','
        t_sen=t_sen+'等。'
        
        sen.append(t_sen)
        
        last_sen='此次演习{}'.format('meaning')
        sen.append(last_sen)
        
        sen.append('({} {})'.format(json_item['site'],json_item['date']))
        sen.append(json_item['url'])
        
            
    elif choice_id==2:
        #DARPA项目
        
        schema=['国家','时间','技术',
                    {'项目触发词':['公司','名称','目的','用途','阶段','时长']},
                    {'开发触发词':['时间','内容','目的']},
                    {'技术触发词':['名称','学科','领域','创新内容']},
                    {'研制':['意义','目的','影响']}
        ]
    elif choice_id==3:
        #装备研制
        
        schema=['国家','时间',
                    {'研制触发词':['机构','内容','时间']},
                    {'试验触发词':['机构','内容','时间']},
                    {'装备':['特点','性能','计划']},
                    {'研制':['意义','目的','影响']}
        ]
    else:
        sen=[]

    return sen

    

def main():
    args=get_args()
    
    json_list=read_file(args.predict_file)
    class_list=template_class(json_list,args.template_type)
    for i in class_list[8:12]:
        generate_text(i,choice_id=args.template_type)

def add_sum(a,b):
    
    if  a==
    
    #    
if __name__=='__main__':
    main()
    #
