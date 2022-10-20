from numpy import append
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
                    {'武器':['名字','数量','动作','目标']},
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
        
        schema=['国家','时间','地点','机构','公司',
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
    
    pprint(result)
    gen_text=template_ch_text(result,json_item,choice_id)
    
    print(('\n').join(gen_text))
    print('=======================================================================')
    
def get_args():
    parser=argparse.ArgumentParser(description='ner args')
    parser.add_argument('--template_type',type=int,default=3,help='使用模板类型，1，演习，2项目，3，装备研制')
    parser.add_argument('--predict_file',type=str,default='./data/2022-09-26_guowai_dongtai_06775without_tran_8000_content.json',help='抽取源文件')
    parser.add_argument('--learning_rate',type=float,default=3e-5,help='learning_rate')
    parser.add_argument('--batch_size',type=int,default=32,help='batch_SIZE')
    parser.add_argument('--gpu',type=int,default=0,help='使用的GPU序号')
    
    
    return parser.parse_args()
    
def template_ch_text(result,json_item,choice_id):
    
    
    sen=[]
    
    if choice_id==1:
        #结果解析，去重
        
        #装备研发
        """
        "{}".format(title)
        "{}{}于{}对{}进行实验/研发。".format(country,company,time,zb_name)
        "此实验将在{}{}举行",旨在{},".format(country,place,test_aim)
        "该装备{}将为{}实现{}".format(zb_name,country,test_meaning)
        "（{}{}{}）".format(country,website,pub_time)
        日本防卫省采办、技术与后勤局（ATLA） 将在2022年7月23日 对一款在研超燃冲压发动机 开展首次燃烧飞行试验 。
        此次试验将在日本宇宙航空研究开发机构（JAXA）的内之浦太空中心举行 ，旨在获得一个预测超燃冲压发动机在飞行过程中燃烧现象的模型，并将得到的结果与地面风洞试验获得的数据进行对比；
        此外ATLA还将建立和评估一个数值分析模型，以“修正和预测实际飞行中的数据” 。
        新型发动机将为日本包括巡航导弹在内的各种高超声速飞行器提供动力，提升其保卫远岛的能力 。
        （{}{}{}）.format(country,website,pub_time) 
        
        """
        
        for i in result:
            zb_name=[]
            for k,v in i.items():
                if k=='国家':
                    countries=[]
                    for j in v:
                        countries.append(j['text'])
                    country=('').format(countries)
                
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
                    pass

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
        
        title=json_item['title_cn']
        website=json_item['site']
        pub_time=json_item['date']
        
        #参数初始化（不一定能抽取到）
        place,country,company,time,zb_name="_","_","_","_","_"
        test_meaning=[]
        test_aim=[]
        
        
        for i in result:
            for k,v in i.items():
                if k=='国家':
                    country=v[0]['text']
                elif k=='时间':
                    time=v[0]['text']
                elif k=='公司':
                    company=v[0]['text']
                elif k=='机构':
                    company=v[0]['text']
                elif k=='装备':
                    zb_name=v[0]['text']
                    
                # elif k=='研制触发词':
                #     for t in v:
                        
                # elif k=='试验触发词':
                    
                # elif k=='研制':
                    
        
        
        
        
        sen.append("{}".format(title))
        sen.append("{}{}于{}对{}进行实验/研发。".format(country,company,time,zb_name))
        sen.append("此实验将在{}{}举行,旨在{},".format(country,place,(' ').join(test_aim)))
        sen.append("该装备{}将为{}实现{}".format(zb_name,country,(' ').join(test_meaning)))
        sen.append("（{}{}{}）".format(country,website,pub_time))
    

    return sen

def uie4text(input_text,choice_id=3):
    schema=choose_schema(choice_id)
    ie=load_task(schema)
    
    
    result=ie(input_text)
    
    pprint(result)


def main():
    # args=get_args()
    
    # json_list=read_file(args.predict_file)
    # class_list=template_class(json_list,args.template_type)
    # for i in class_list[:10]:
    #     generate_text(i,choice_id=args.template_type)
   
    text="DARPA期待“飞跃式”垂直起降无人机的辅助设备 美国国防高级研究计划局(DARPA)正计划从商业上应用创新和技术 电动垂直起降(EVTOL)扇区的下一代垂直起降无人飞机系统(UAS)。 2019022 一个名义上的附属设计的渲染。 RFI中所表达的大纲性能意图包括精确度 自主垂直起降能力，在没有基础设施的情况下从8×8英尺的区域发射和回收，最大射程为500英里， 目标是在100英里范围内24小时的续航时间，持续最大速度为150千吨，模块化有效载荷高达60磅，在游荡期间有效载荷功率超过350瓦。 9月20日将举办一个辅助的提议者日和博览会。 根据DARPA的说法，这次活动旨在帮助促进 公司之间的合作安排，为即将到来的计划提供洞察力，并提高建议书的效率 准备和评估。 预计今年10月初将进行正式的节目征集。 根据目前的计划，DARPA计划授予大约八个辅助的IA阶段合同，根据这些合同，选定的承包商将完成 贸易研究，成熟他们的设计，并完成概念设计审查，包括第一阶段的成本估计。 在这个 后续活动，持续六个月，选定的表演者将继续设计成熟，直到初步设计审查。 随后被淘汰进入IIA阶段的公司将进行进一步的设计成熟和子系统测试 一个重要的设计审查。 在IIB阶段，选定的表演者将制造、地面测试和飞行测试他们的X飞机 垂直起降无人机设计。 飞行试验演示计划在两次试验中进行。 第一个测试事件将演示无基础设施 DARPA说，风中垂直起降发射和回收，在运动中模拟甲板上自动回收，以及系统可靠性。 的 第二个测试活动将演示从悬停到巡航、巡航和游荡的整个飞行包线的转换效率， 以及从巡航到悬停的过渡。 可选的第三阶段计划集中在海上环境下的X-飞机飞行测试，以验证该系统--包括 任务有效载荷--在操作演示中。 DARPA） DARPA的先进飞机基础设施--无发射和回收(ANCillary)X型飞机计划打算开发和飞行演示 在低重量、高有效载荷、长航时垂直起降能力方面实现“飞跃”所需的关键技术。 第三阶段执行的决定将在第二阶段作出，并将 DARPA说，这取决于第二阶段的可用政府资金和成功的飞行演示。 DARPA补充说，它的辅助方案招标将导致使用原型授权的其他交易的奖项。 预计IA阶段奖项将于2023年3月中旬颁发。 评论 评论 在城市空气流动性预计增长的推动下，EVTOL行业的激增见证了新型轻量级产品的发展 近年来垂直起降飞行器的配置。 辅助方案计划采用多学科方法，将 在先进控制理论、空气动力学建模和先进推进方面的共同发展，以解决 具有挑战性的设计目标。 在陆地上，操作者能够在不依赖的条件下部署和回收高性能垂直起降无人机 基础设施将在敏感的操作中最大限度地减少人员、成本和脆弱性。 在海上，工程处希望 一种小的车辆外形因素，可以使许多空中车辆从一艘船上部署。 以及有机信息， 监督和有针对性的应用，辅助方案所展示的技术也将点对点地受益 无人物流作业。 最终的 目的：是建立一种战术无人机系统，它可以在恶劣天气下从舰船飞行甲板和小型恶劣陆地上运行 没有发射和回收设备。 在宣布启动辅助研发计划时，DARPA的战术技术办公室在9月7日说 它计划开发大型非传统商业工业基地，这推动了最近的垂直起降研究 投资和先进的控制，导致创新的车辆配置跨越大小，重量，功率和成本。 进步 在小型推进系统中，高容量低重量电池、燃料电池、材料、电子和低成本添加剂 它补充说，制造业现在可以在这个贸易空间探索新的建筑和设计。 DARPA打算辅助飞行器应该是第三组类型，重量在250到330磅（113.4到149.7千克）之间。 除了在没有基础设施的情况下发射和回收的能力，其他主要设计目标包括延长续航时间 和航程，战术规模的高有效载荷重量比，以及稳健的飞行控制和相对导航。 重量低/小 辅助设备的外形系数旨在使多架飞机能够从一艘船上储存和操作，使 打造战术超视距多智能传感器网络能力。 2020年2月，DARPA发布了支持辅助设备的信息请求(RFI)，以寻求对关键技术的投入 挑战和候选技术/配置。  "
    uie4text(text,choice_id=2)
        
    


if __name__=='__main__':
    main()
