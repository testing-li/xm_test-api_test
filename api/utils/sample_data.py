import json
import random
import requests

# 首次请求  具体需要替换
from datetime import datetime
import random
import datetime as datetimetools

# b2


pp_and_chexing = [
    "大众-朗逸",
    "大众-速腾",
    "东风日产-轩逸",
    "五菱-宏光MINIEV",
    "别克-英朗",
    "丰田-卡罗拉",
    "本田-本田CRV",
    "宝马-宝马3系",
    "奥迪-奥迪Q5L",
    "奔驰-奔驰GLC",
]
obj = random.choice(pp_and_chexing)
pp, xinghao = obj.split("-")

from json import dumps, loads


# question-list-content


# 一道题 必须多个选数据结构 ["tid":{ row选项：{item选项：剩余个数} ， 选项：剩余个数    }]
# 一道题 可以之选一个数据结构 【{“tid”:{item选项：剩余个数} }】


def begin(host, sig, project, dev_id, deliver_id):
    url = f"{host}/api/survey/b/{project}?source=2"
    data = {
        "allParams": {
            "source": "2",
            "code": "",
            "scenes": "1",
            "org_code": "auto",
            "deliver_id": deliver_id,
            "sig": sig,
        },
        "source": "2",
        "dev_id": dev_id,
    }
    Authorization = "Bearer null"
    print(f"first:{data}")
    reg = requests.post(url, json=data, headers={"Authorization": Authorization})
    jwt_token = reg.json()["data"]["jwt_token"]
    seq = reg.json()["data"]["seq"]
    version = reg.json()["data"]["version"]
    return jwt_token, seq, version


def gendata():
    datas = []
    gen_data = {
        "2": {dumps([3]): 1000},
        "12": {dumps([13]): 1000},
        "19": {dumps({"20": ["品牌"], "21": ["型号"]}): 1000},
        "22": {
            dumps([23]): 170,
            dumps([24]): 250,
            dumps([25]): 580,
        },
        "37": {
            dumps({"38": 1, "39": 2, "40": 3, "41": 4, "42": 5}): 230,
            dumps({"38": 2, "39": 1, "40": 3, "41": 4, "42": 5}): 180,
            dumps({"38": 3, "39": 2, "40": 1, "41": 4, "42": 5}): 140,
            dumps({"38": 3, "39": 2, "40": 4, "41": 1, "42": 5}): 260,
            dumps({"38": 3, "39": 2, "40": 4, "41": 5, "42": 1}): 190,
        },
        "43": {
            dumps({"44": [1, "", ""]}): 10,
            dumps({"44": [2, "", ""]}): 10,
            dumps({"44": [3, "", ""]}): 10,
            dumps({"44": [4, "", ""]}): 20,
            dumps({"44": [5, "", ""]}): 20,
            dumps({"44": [6, "", ""]}): 30,
            dumps({"44": [7, "", ""]}): 60,
            dumps({"44": [8, "", ""]}): 160,
            dumps({"44": [9, "", ""]}): 290,
            dumps({"44": [10, "", ""]}): 390,
        },
        "45": {
            dumps({"46": [1, "", ""]}): 10,
            dumps({"46": [2, "", ""]}): 10,
            dumps({"46": [3, "", ""]}): 10,
            dumps({"46": [4, "", ""]}): 20,
            dumps({"46": [5, "", ""]}): 20,
            dumps({"46": [6, "", ""]}): 160,
            dumps({"46": [7, "", ""]}): 170,
            dumps({"46": [8, "", ""]}): 170,
            dumps({"46": [9, "", ""]}): 230,
            dumps({"46": [10, "", ""]}): 200,
        },
        # 请问您在购车前通过网站或手机APP获取了哪些信息？【多选】
        "47": {
            dumps([[48]]): 630,
            dumps([[49]]): 350,
            dumps([[50]]): 370,
            dumps([[64]]): 540,
            dumps([[63]]): 230,
            dumps([[62]]): 250,
            dumps([[61]]): 130,
            dumps([[60]]): 660,
            dumps([[59]]): 580,
            dumps([[58]]): 420,
            dumps([[57]]): 110,
            dumps([[56]]): 60,
            dumps([[55]]): 170,
            dumps([[54]]): 70,
            dumps([[53]]): 60,
        },
        "76": {
            dumps({"77": [3, "", ""]}): 30,
            dumps({"77": [4, "", ""]}): 90,
            dumps({"77": [5, "", ""]}): 170,
            dumps({"77": [6, "", ""]}): 210,
            dumps({"77": [7, "", ""]}): 230,
            dumps({"77": [8, "", ""]}): 150,
            dumps({"77": [9, "", ""]}): 100,
            dumps({"77": [10, "", ""]}): 20,
        },
        "93": {dumps(""): 1000},
        "95": {dumps(""): 1000},
        "96": {dumps(""): 1000},
        "97": {dumps(""): 1000},
        # 在第一次去您买车的4S店前，这家店在您留了联系方式后多久主动联系您？*
        "98": {
            dumps([99]): 50,
            dumps([100]): 110,
            dumps([101]): 160,
            dumps([105]): 250,
            dumps([104]): 340,
            dumps([103]): 90,
        },
        # ，您与您买车的这家4S店沟通了什么信息？
        "109": {
            dumps([[110]]): 670,
            dumps([[118]]): 50,
            dumps([[117]]): 120,
            dumps([[116]]): 210,  # ？？？？
            dumps([[115]]): 90,
            dumps([[114]]): 70,
            dumps([[113]]): 180,
            dumps([[112]]): 220,
            dumps([[111]]): 160,
            dumps([[123]]): 90,
        },
        "124": {
            dumps([125]): 33,
            dumps([128]): 57,
            dumps([127]): 101,
            dumps([126]): 18,
        },
        # 入店前，您与这家4S店的沟通得到的信息是否有用？【单选】
        "129": {
            dumps([130]): 40,
            dumps([133]): 89,
            dumps([132]): 48,
            dumps([131]): 53,
        },
        "166": {dumps(""): 1000},
        # 您第一次进入这家4S店时，等候了多久才有工作人员来接待您？【单选】
        "167": {
            dumps([168]): 350,
            dumps([171]): 180,
            dumps([170]): 460,
            dumps([169]): 10,
        },
        # 给入店前和您购车的4S店的沟通体验打分 矩阵题
        "177": {
            "180": {
                dumps({"180": [183]}): 17,
                dumps({"180": [184]}): 33,
                dumps({"180": [185]}): 59,
                dumps({"180": [186]}): 69,
                dumps({"180": [187]}): 76,
                dumps({"180": [188]}): 46,
                dumps({"180": [189]}): 23,
                dumps({"180": [190]}): 7,
            },
            "181": {
                dumps({"181": [183]}): 7,
                dumps({"181": [184]}): 17,
                dumps({"181": [185]}): 26,
                dumps({"181": [186]}): 36,
                dumps({"181": [187]}): 43,
                dumps({"181": [188]}): 56,
                dumps({"181": [189]}): 76,
                dumps({"181": [190]}): 69,
            },
            "182": {
                dumps({"182": [183]}): 10,
                dumps({"182": [184]}): 23,
                dumps({"182": [185]}): 36,
                dumps({"182": [186]}): 69,
                dumps({"182": [187]}): 76,
                dumps({"182": [188]}): 50,
                dumps({"182": [189]}): 33,
                dumps({"182": [190]}): 33,
            },
        },
        "191": {
            "194": {
                dumps({"194": [192]}): 10,
                dumps({"194": [193]}): 10,
                dumps({"194": [198]}): 10,
                dumps({"194": [199]}): 20,
                dumps({"194": [200]}): 20,
                dumps({"194": [201]}): 30,
                dumps({"194": [202]}): 30,
                dumps({"194": [203]}): 190,
                dumps({"194": [204]}): 320,
                dumps({"194": [205]}): 360,
            },
            "195": {
                dumps({"195": [192]}): 10,
                dumps({"195": [193]}): 10,
                dumps({"195": [198]}): 10,
                dumps({"195": [199]}): 20,
                dumps({"195": [200]}): 20,
                dumps({"195": [201]}): 30,
                dumps({"195": [202]}): 130,
                dumps({"195": [203]}): 160,
                dumps({"195": [204]}): 270,
                dumps({"195": [205]}): 340,
            },
            "196": {
                dumps({"196": [192]}): 10,
                dumps({"196": [193]}): 10,
                dumps({"196": [198]}): 10,
                dumps({"196": [199]}): 20,
                dumps({"196": [200]}): 20,
                dumps({"196": [201]}): 30,
                dumps({"196": [202]}): 180,
                dumps({"196": [203]}): 150,
                dumps({"196": [204]}): 260,
                dumps({"196": [205]}): 310,
            },
            "197": {
                dumps({"197": [192]}): 10,
                dumps({"197": [193]}): 10,
                dumps({"197": [198]}): 10,
                dumps({"197": [199]}): 20,
                dumps({"197": [200]}): 20,
                dumps({"197": [201]}): 30,
                dumps({"197": [202]}): 100,
                dumps({"197": [203]}): 160,
                dumps({"197": [204]}): 290,
                dumps({"197": [205]}): 350,
            },
        },
        "206": {dumps(""): 1000},
        "207": {dumps([208]): 530, dumps([209]): 250, dumps([210]): 220},  # #  #
        # 销售人员询问了哪些信息？
        "214": {
            dumps([[215]]): 670,
            dumps([[225]]): 445,  # ???
            dumps([[224]]): 374,
            dumps([[223]]): 296,
            dumps([[222]]): 491,
            dumps([[221]]): 328,
            dumps([[220]]): 203,
            dumps([[219]]): 133,
            dumps([[218]]): 101,
            dumps([[217]]): 47,
            dumps([[216]]): 8,
        },
        # 销售人员询问了哪些信息？
        "226": {
            "229": {
                dumps({"229": [227]}): 10,
                dumps({"229": [228]}): 10,
                dumps({"229": [231]}): 10,
                dumps({"229": [232]}): 20,
                dumps({"229": [233]}): 30,
                dumps({"229": [234]}): 50,
                dumps({"229": [235]}): 100,
                dumps({"229": [236]}): 160,
                dumps({"229": [237]}): 230,
                dumps({"229": [238]}): 380,
            },
            "230": {
                dumps({"230": [227]}): 0,
                dumps({"230": [228]}): 0,
                dumps({"230": [231]}): 0,
                dumps({"230": [232]}): 10,
                dumps({"230": [233]}): 20,
                dumps({"230": [234]}): 20,
                dumps({"230": [235]}): 20,
                dumps({"230": [236]}): 30,
                dumps({"230": [237]}): 40,
                dumps({"230": [238]}): 860,
            },
            "239": {
                dumps({"239": [227]}): 10,
                dumps({"239": [228]}): 10,
                dumps({"239": [231]}): 10,
                dumps({"239": [232]}): 20,
                dumps({"239": [233]}): 30,
                dumps({"239": [234]}): 50,
                dumps({"239": [235]}): 90,
                dumps({"239": [236]}): 170,
                dumps({"239": [237]}): 240,
                dumps({"239": [238]}): 370,
            },
            "240": {
                dumps({"240": [227]}): 0,
                dumps({"240": [228]}): 0,
                dumps({"240": [231]}): 20,
                dumps({"240": [232]}): 50,
                dumps({"240": [233]}): 80,
                dumps({"240": [234]}): 110,
                dumps({"240": [235]}): 130,
                dumps({"240": [236]}): 170,
                dumps({"240": [237]}): 230,
                dumps({"240": [238]}): 210,
            },
            "241": {
                dumps({"241": [227]}): 10,
                dumps({"241": [228]}): 10,
                dumps({"241": [231]}): 10,
                dumps({"241": [232]}): 20,
                dumps({"241": [233]}): 20,
                dumps({"241": [234]}): 30,
                dumps({"241": [235]}): 60,
                dumps({"241": [236]}): 160,
                dumps({"241": [237]}): 290,
                dumps({"241": [238]}): 390,
            },
            "242": {
                dumps({"242": [227]}): 0,
                dumps({"242": [228]}): 0,
                dumps({"242": [231]}): 10,
                dumps({"242": [232]}): 10,
                dumps({"242": [233]}): 10,
                dumps({"242": [234]}): 20,
                dumps({"242": [235]}): 40,
                dumps({"242": [236]}): 130,
                dumps({"242": [237]}): 360,
                dumps({"242": [238]}): 400,
            },
        },
        "243": {dumps(""): 1000},
        "244": {
            dumps([245]): 180,
            dumps([249]): 420,
            dumps([248]): 170,
            dumps([247]): 160,
            dumps([246]): 70,
        },
        "250": {
            dumps(["10"]): 60,
            dumps(["15"]): 120,
            dumps(["20"]): 120,
            dumps(["25"]): 120,
            dumps(["30"]): 120,
            dumps(["40"]): 60,
        },
        "251": {
            dumps([[252]]): 222,
            dumps([[253]]): 0,
            dumps([[254]]): 366,
            dumps([[255]]): 336,
            dumps([[256]]): 258,
        },
        # Q17. 您如何评价试乘试驾时销售人员对车辆的讲解
        "257": {
            dumps([258]): 48,  #
            dumps([259]): 288,  #
            dumps([260]): 210,  #
            dumps([261]): 54,  #
        },
        # ，请不要被某个好的或坏的经历影响你评价其它问题
        "262": {
            "265": {
                dumps({"265": [263]}): 0,
                dumps({"265": [264]}): 0,
                dumps({"265": [267]}): 18,
                dumps({"265": [268]}): 42,
                dumps({"265": [269]}): 66,
                dumps({"265": [270]}): 126,
                dumps({"265": [271]}): 138,
                dumps({"265": [272]}): 90,
                dumps({"265": [273]}): 60,
                dumps({"265": [274]}): 60,
            },
            "266": {
                dumps({"266": [263]}): 0,
                dumps({"266": [264]}): 0,
                dumps({"266": [267]}): 12,
                dumps({"266": [268]}): 18,
                dumps({"266": [269]}): 48,
                dumps({"266": [270]}): 96,
                dumps({"266": [271]}): 132,
                dumps({"266": [272]}): 114,
                dumps({"266": [273]}): 96,
                dumps({"266": [274]}): 84,
            },
            "275": {
                dumps({"275": [263]}): 0,
                dumps({"275": [264]}): 0,
                dumps({"275": [267]}): 12,
                dumps({"275": [268]}): 18,
                dumps({"275": [269]}): 48,
                dumps({"275": [270]}): 84,
                dumps({"275": [271]}): 132,
                dumps({"275": [272]}): 114,
                dumps({"275": [273]}): 102,
                dumps({"275": [274]}): 90,
            },
            "276": {
                dumps({"276": [263]}): 0,
                dumps({"276": [264]}): 0,
                dumps({"276": [267]}): 18,
                dumps({"276": [268]}): 30,
                dumps({"276": [269]}): 54,
                dumps({"276": [270]}): 102,
                dumps({"276": [271]}): 126,
                dumps({"276": [272]}): 108,
                dumps({"276": [273]}): 84,
                dumps({"276": [274]}): 78,
            },
        },
        "277": {dumps(""): 1000},
        "278": {
            dumps([[279]]): 720,  #
            dumps([[286]]): 60,  #
            dumps([[285]]): 90,  #
            dumps([[284]]): 360,  #
            dumps([[283]]): 20,  #
            dumps([[282]]): 20,  #
        },
        "287": {
            "290": {
                dumps({"290": [288]}): 850,
                dumps({"290": [289]}): 150,
                dumps({"290": [292]}): 0,
            },
            "291": {
                dumps({"291": [288]}): 780,
                dumps({"291": [289]}): 220,
                dumps({"291": [292]}): 0,
            },
            "293": {
                dumps({"293": [288]}): 890,
                dumps({"293": [289]}): 110,
                dumps({"293": [292]}): 0,
            },
            "294": {
                dumps({"294": [288]}): 760,
                dumps({"294": [289]}): 240,
                dumps({"294": [292]}): 0,
            },
            "295": {
                dumps({"295": [288]}): 760,
                dumps({"295": [289]}): 240,
                dumps({"295": [292]}): 0,
            },
        },
        "296": {
            dumps([[297]]): 260,  #
            dumps([[298]]): 60,  #
            dumps([[305]]): 150,  #
            dumps([[304]]): 480,  #
            dumps([[303]]): 530,  #
            dumps([[302]]): 360,  #
            dumps([[301]]): 160,  #
        },
        "306": {
            dumps([[316]]): 680,  #
            dumps([[307]]): 70,  #
            dumps([[308]]): 40,  #
            dumps([[315]]): 80,  #
            dumps([[314]]): 120,  #
            dumps([[313]]): 160,  #
            dumps([[312]]): 80,  #
            dumps([[311]]): 190,  #
            dumps([[310]]): 40,  #
            dumps([[309]]): 90,  #
        },
        "317": {
            "320": {dumps({"320": [318]}): 860, dumps({"320": [319]}): 140},
            "321": {dumps({"321": [318]}): 790, dumps({"321": [319]}): 210},
            "322": {dumps({"322": [318]}): 650, dumps({"322": [319]}): 350},
        },
        # TODO :数据最后伪造
        "323": {
            "326": {
                dumps({"326": [324]}): 0,
                dumps({"326": [325]}): 0,
                dumps({"326": [328]}): 20,
                dumps({"326": [329]}): 30,
                dumps({"326": [330]}): 80,
                dumps({"326": [331]}): 110,
                dumps({"326": [332]}): 130,
                dumps({"326": [333]}): 170,
                dumps({"326": [334]}): 230,
                dumps({"326": [335]}): 230,
            },
            "327": {
                dumps({"327": [324]}): 0,
                dumps({"327": [325]}): 0,
                dumps({"327": [328]}): 20,
                dumps({"327": [329]}): 20,
                dumps({"327": [330]}): 20,
                dumps({"327": [331]}): 30,
                dumps({"327": [332]}): 20,
                dumps({"327": [333]}): 30,
                dumps({"327": [334]}): 40,
                dumps({"327": [335]}): 840,
            },
            "336": {
                dumps({"336": [324]}): 0,
                dumps({"336": [325]}): 10,
                dumps({"336": [328]}): 10,
                dumps({"336": [329]}): 20,
                dumps({"336": [330]}): 20,
                dumps({"336": [331]}): 30,
                dumps({"336": [332]}): 30,
                dumps({"336": [333]}): 40,
                dumps({"336": [334]}): 40,
                dumps({"336": [335]}): 800,
            },
            "337": {
                dumps({"337": [324]}): 10,
                dumps({"337": [325]}): 10,
                dumps({"337": [328]}): 20,
                dumps({"337": [329]}): 20,
                dumps({"337": [330]}): 30,
                dumps({"337": [331]}): 40,
                dumps({"337": [332]}): 40,
                dumps({"337": [333]}): 50,
                dumps({"337": [334]}): 50,
                dumps({"337": [335]}): 730,
            },
            "338": {
                dumps({"338": [324]}): 10,
                dumps({"338": [325]}): 10,
                dumps({"338": [328]}): 10,
                dumps({"338": [329]}): 20,
                dumps({"338": [330]}): 20,
                dumps({"338": [331]}): 30,
                dumps({"338": [332]}): 30,
                dumps({"338": [333]}): 40,
                dumps({"338": [334]}): 50,
                dumps({"338": [335]}): 780,
            },
        },
        "339": {dumps(""): 1000},
        "340": {
            dumps(["7"]): 180,
            dumps(["10"]): 220,
            dumps(["15"]): 280,
            dumps(["20"]): 320,
        },
        "341": {
            dumps([342]): 740,
            dumps([343]): 230,
            dumps([344]): 20,
            dumps([345]): 10,
        },
        "346": {dumps([347]): 650, dumps([348]): 350},
        "349": {
            dumps([[350]]): 720,
            dumps([[356]]): 0,
            dumps([[355]]): 0,
            dumps([[354]]): 0,
            dumps([[353]]): 0,
            dumps([[352]]): 280,
        },
        "357": {
            dumps([[358]]): 210,
            dumps([[365]]): 130,
            dumps([[442]]): 150,
            dumps([[364]]): 180,
            dumps([[366]]): 220,
            dumps([[363]]): 220,
            dumps([[362]]): 460,
            dumps([[361]]): 180,
            dumps([[360]]): 130,
            dumps([[359]]): 60,
        },
        "367": {
            dumps([[368]]): 80,
            dumps([[369]]): 90,
            dumps([[374]]): 50,
            dumps([[371]]): 680,
            dumps([[372]]): 150,
            dumps([[373]]): 210,
        },
        "375": {
            dumps([376]): 740,
            dumps([379]): 180,
            dumps([378]): 30,
            dumps([377]): 50,
        },
        "380": {dumps([381]): 980, dumps([385]): 10, dumps([384]): 10},
        "386": {dumps([387]): 380, dumps([388]): 530, dumps([389]): 90},
        "390": {
            "393": {
                dumps({"393": [391]}): 0,
                dumps({"393": [392]}): 0,
                dumps({"393": [395]}): 20,
                dumps({"393": [396]}): 30,
                dumps({"393": [397]}): 60,
                dumps({"393": [398]}): 160,
                dumps({"393": [399]}): 220,
                dumps({"393": [400]}): 210,
                dumps({"393": [401]}): 150,
                dumps({"393": [402]}): 150,
            },
            "394": {
                dumps({"394": [391]}): 10,
                dumps({"394": [392]}): 10,
                dumps({"394": [395]}): 20,
                dumps({"394": [396]}): 20,
                dumps({"394": [397]}): 30,
                dumps({"394": [398]}): 40,
                dumps({"394": [399]}): 40,
                dumps({"394": [400]}): 50,
                dumps({"394": [401]}): 50,
                dumps({"394": [402]}): 730,
            },
            "403": {
                dumps({"403": [391]}): 0,
                dumps({"403": [392]}): 0,
                dumps({"403": [395]}): 0,
                dumps({"403": [396]}): 10,
                dumps({"403": [397]}): 20,
                dumps({"403": [398]}): 20,
                dumps({"403": [399]}): 20,
                dumps({"403": [400]}): 30,
                dumps({"403": [401]}): 40,
                dumps({"403": [402]}): 860,
            },
            "404": {
                dumps({"404": [391]}): 0,
                dumps({"404": [392]}): 10,
                dumps({"404": [395]}): 20,
                dumps({"404": [396]}): 20,
                dumps({"404": [397]}): 20,
                dumps({"404": [398]}): 30,
                dumps({"404": [399]}): 40,
                dumps({"404": [400]}): 40,
                dumps({"404": [401]}): 50,
                dumps({"404": [402]}): 770,
            },
        },
        "405": {dumps(""): 1000},
        "406": {
            dumps({"407": [2, "", ""]}): 10,
            dumps({"407": [3, "", ""]}): 20,
            dumps({"407": [4, "", ""]}): 20,
            dumps({"407": [5, "", ""]}): 30,
            dumps({"407": [6, "", ""]}): 30,
            dumps({"407": [7, "", ""]}): 60,
            dumps({"407": [8, "", ""]}): 150,
            dumps({"407": [9, "", ""]}): 270,
            dumps({"407": [10, "", ""]}): 400,
        },
        "412": {dumps([413]): 740, dumps([414]): 260},
        "415": {
            dumps([416]): 0,
            dumps([417]): 310,
            dumps([418]): 220,
            dumps([419]): 100,
            dumps([420]): 370,
            dumps([421]): 0,
            dumps([422]): 0,
        },
        "423": {
            dumps([424]): 10,
            dumps([425]): 20,
            dumps([426]): 30,
            dumps([427]): 140,
            dumps([428]): 620,
            dumps([429]): 180,
        },
    }

    for i in range(1000):
        # 一个用户
        the_user_data = {}
        for cid, qiddic in gen_data.items():  # 循环所有题目
            for json_item, shengyu in qiddic.items():  # 循环 所有可选项目
                # 可以单选
                if isinstance(shengyu, int) and shengyu != 0:
                    item = loads(json_item)
                    the_user_data[cid] = item
                    qiddic[json_item] -= 1
                    break  # 选择一个
                elif isinstance(shengyu, int) and shengyu == 0:
                    continue  # 选择完了 换一个选项
                else:
                    # 多选 例如举行
                    the_user_data.setdefault(cid, {})
                    for xuanxiang, shengyu2 in shengyu.items():  # {}
                        if isinstance(shengyu2, int) and shengyu2 != 0:
                            shengyu[xuanxiang] -= 1
                            xuanxiang = loads(xuanxiang)
                            the_user_data[cid].update(xuanxiang)
                            break
                        else:
                            continue
            # 这个选项没了
            # 全部没得选
            else:
                pass
        datas.append(the_user_data)
        print("the_user_data", the_user_data)
    return datas, gen_data


def send(
        host,
        surveyId,
        version,
        seq,
        answer,
        jwt_token,
        project,
        sig,
        deliver_id,
        begin_time="",
        s_finish_time="",
):
    data = {
        "surveyId": surveyId,
        "version": version,
        "source": "2",
        "code": "",
        "seq": seq,
        "status": 1,  # ???
        "data_status": 1,
        "allParams": {
            "source": "2",
            "code": "",
            "scenes": "1",
            "org_code": "auto",
            "deliver_id": deliver_id,
            "sig": sig,
        },
        "show_footer": 0,
        "auth": {},
        "custom_data_action": [],
        "publicPath": "https://rs0.bestcem.cn/prod/rs/s/",
        "city": True,
        "answer": answer,
        "rspd_status": 1,
        "rspd_token": jwt_token,
        "survey_status": 1,
        "uniq_qid_list": [],
        "s_begin_time": begin_time,
        "s_finish_time": s_finish_time,
    }
    url = f"{host}/api/survey/mock/s/{project}?source=2"
    print(f"最后一次：{data}")
    reg = requests.post(
        url,
        json=data,
        headers={"Authorization": jwt_token, "token": jwt_token.split(" ")[1]},
    )
    print(reg.text)
    print(reg.json())


if __name__ == "__main__":

    answers, gen_data = gendata()

    # 将剩余的选项分配个用户
    # 非矩形题目
    gen_data2 = {}  # 只存非矩形题目还有剩余的题目
    gen_data3 = {}  # 只存矩形题目还有剩余的题目


    def add_item2user(val, timu, xuanxiang, type=None):
        """随机选中一个用户 然后判断下有没有这个答案
        type: row 只有两个选项的 items 有三个选项的
        """
        if type == "row":
            canadduser = list(
                filter(lambda q_a: xuanxiang not in q_a[timu], answers)
            )  # 过滤出这个没有选择这个选项的用户
            random.shuffle(canadduser)  # 对用户进行随机
            # 对前val个用户进行添加
            for user in canadduser[:val]:
                user[timu].extend(loads(xuanxiang))
                gen_data[timu][xuanxiang] -= 1
        else:
            print(">>>", val, timu, xuanxiang, type, answers[0][timu])
            canadduser = list(filter(lambda q_a: xuanxiang not in q_a[timu], answers))


    def get_date_map(index=-1):
        """index 是日期区间 """

        # 01/01 ~
        s_begin_time = "2021/01/01 00:00:00"
        s_finish_time = "2021/02/20 00:00:00"
        s_begin_time = datetime.strptime(s_begin_time, "%Y/%m/%d %H:%M:%S")
        s_finish_time = datetime.strptime(s_finish_time, "%Y/%m/%d %H:%M:%S")
        current_date = s_begin_time
        dates = []
        while s_begin_time <= current_date < s_finish_time:
            current_date = current_date + datetimetools.timedelta(days=1)
            dates.append(current_date)
        # 每天20份答卷
        if index == -1:
            return dict(zip(range(len(dates)), dates))
        else:
            date_map = dict(zip(range(len(dates)), dates))
            return date_map.get(index)


    def cleaning_invalid_answer(answer):
        invalid_key = list(filter(lambda id: answer[id] == {}, answer))
        for key in invalid_key: answer[key] = ''


    def choise_bank():
        obj = random.choice(pp_and_chexing)
        pp, xinghao = obj.split("-")
        return pp, xinghao


    for cid, item in gen_data.items():
        for gid, value in item.items():
            if type(value) == int:
                if value != 0:
                    gen_data2.setdefault(cid, {})
                    gen_data2[cid][gid] = value
                    add_item2user(value, cid, gid, type="row")  # 把多余的题目选项 随机给一个用户
            else:
                for rid, shengyu_num in value.items():
                    # print(gid,shengyu_num)
                    if shengyu_num != 0:
                        gen_data3.setdefault(cid, {})
                        gen_data3[cid].setdefault(gid, {})
                        gen_data3[cid][gid][rid] = shengyu_num
                        add_item2user(shengyu_num, cid, rid, type="items")

    # answers=answers[:10]
    random.shuffle(answers)
    import time

    answers = answers[:10]
    for ind, answer in enumerate(answers):
        # 把大众随机替换成一个选项
        pp, xinghao = choise_bank()
        cleaning_invalid_answer(answer)
        answer["19"]["20"].clear()
        answer["19"]["21"].clear()
        answer["19"]["20"].append(pp)
        answer["19"]["21"].append(xinghao)
        answer = dumps(answer)
        project = "6084e2e0aace70000ae51c8e"
        surveyId = project
        sig = "616ecfc069d66e6e3003a2fba9102faf"
        deliver_id = "6084e2e5f9f4f60024a064c8"
        dev_id = "FYdpHFN5Rk8WRkzbcYB83tbJ"
        host = "https://bestcem.com"
        qujian = int(((ind - ind % 20)) / 20)
        start_date = get_date_map(index=qujian)
        start_datetime = start_date + datetimetools.timedelta(
            hours=random.randint(0, 24),
            minutes=random.randint(0, 60),
            seconds=random.randint(0, 60),
        )
        end_datetime = start_datetime + datetimetools.timedelta(
            hours=random.randint(0, 24),
            minutes=random.randint(0, 60),
            seconds=random.randint(0, 60),
        )
        start_datetime = start_datetime.strftime("%Y/%m/%d %H:%M:%S")
        end_datetime = end_datetime.strftime("%Y/%m/%d %H:%M:%S")
        print(gen_data)
        # jwt_token, seq, version = begin(
        #     host=host, sig=sig, project=project, dev_id=dev_id, deliver_id=deliver_id
        # )
        # send(
        #     host=host,
        #     surveyId=surveyId,
        #     version=version,
        #     seq=seq,
        #     answer=answer,
        #     jwt_token=jwt_token,
        #     project=project,
        #     sig=sig,
        #     deliver_id=deliver_id,
        #     begin_time=start_datetime,
        #     s_finish_time=end_datetime,
        # )
        # time.sleep(0.3)
