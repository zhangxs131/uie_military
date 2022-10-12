import json

def read_file(filename):
    with open(filename,'r',encoding='gbk') as f:
        json_list=json.load(f)

    return json_list

def template_class(json_list,choice_id=1):
    """
    使用规则匹配方法进行简单分类,
    当前类别设置：
    1. 演习活动
    2. 项目启动
    3. 装备研制
    """

    result=[]
    yx_keyword=['演习']
    xm_keyword=['项目','DARPA']
    zb_keyword=['装备','武器']
    if choice_id==1:
        return container_word(json_list,yx_keyword)
    elif choice_id==2:
        return container_word(json_list,xm_keyword)
    elif choice_id==3:
        return container_word(json_list,zb_keyword)
    else:
        return []

def show_list(json_list,attr=None):
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


def container_word(json_list,key_word=[]):
    result=[]
    for i in range(len(json_list)):
        for k,v in json_list[i].items():
            if k=='title_cn':
                for j in key_word:
                    if j in v:
                        result.append(json_list[i])

    return result

def main():
    filename='2022-09-26_guowai_dongtai_06775without_tran_8000_content.json'
    json_list=read_file(filename)
    zb_list=template_class(json_list,3)
    show_list(zb_list,['title_cn'])

if __name__=='__main__':
    main()
