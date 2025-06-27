import requests,json
from nonebot import get_driver
config = get_driver().config
def bsql(input:str,op:str):
    try:
        sk = config.sk 
    except:
        return "令牌不存在"
    try:
        query = _build(input,sk,op)
    except:
        try: query = _build(input,sk,op)
        except: query = "未知原因，生成失败"
    return query

def _build(input:str,sk:str,op:str):
    url = "https://api.siliconflow.cn/v1/chat/completions"

    payload = {
        "model": "Qwen/QwQ-32B",
        "messages": [
            {
                "role": "system",
                "content": f"""你是个sql语句生成器，你生成的sql语句都会在被用户确认过后才会执行，不用再向用户确认是否执行,以下是已有的数据表说明
                类的名字是表名，变量的值是项的名字
                class user:
                    #永久数据
                    uid:int = 'uid'#qq号
                    white:int = 'white'#白名单，1是好人，0是拉黑，2是管理员
                    love:int = 'love'#好感度
                    name:str = 'name'#自定义昵称
                    prename:str = 'prename'#未审核的昵称
                    nametime:int = 'nametime'#改名cd
                    meet:int = 'meet'#相遇的日子
                    everytea:int = 'etea'#所有喝茶的日子(为什么不叫alltea呢，因为我觉得每个tea的瞬间更浪漫)
                    everygreet:int = 'egreet'#所有问好的日子(同上)
                    #临时数据
                    teatime:int = 'teatime'#上次泡茉莉的时间
                    greetime:int = 'greetime'#上次问好的时间
                    ifgreet:int = 'ifgreet'#问好时间段100000000表示都没问，问了0变1，采用二进制转十进制的方式存储
                    #对于uid为1的数据来说
                    #everytea是所有人当天的喝茶次数
                    #其它的也可以类推哦，uid1可以记录下茉莉自己的数据
                class auth:
                    uid:int = 'uid'#qq号，如果uid为1则为审核群，为2则为主群
                    gid:int = 'gid'#群号
                    time:int = 'time'#授权时间
                    
                额外提示：当前操作员的qq号为{op}"""
            },
            {
                "role": "user",
                "content": input
            }
        ],
        "stream": False,
        "max_tokens": 512,
        "thinking_budget": 4096,
        "min_p": 0.05,
        "stop": None,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "frequency_penalty": 0.5,
        "n": 1,
        "response_format": {"type": "text"},
        "tools": [
            {
                "type": "function",
                "function": {
                    "description": "执行sql语句",
                    "name": "exsql",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "要执行的sql语句",
                            },
                        },
                        "required": [
                            "query"
                        ],
                    },
                    "strict": True
                }
            }
        ]
    }
    headers = {
        "Authorization": f"Bearer {sk}",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    d = json.loads(response.text)["choices"][0]["message"]
    for i in d["tool_calls"]:
        f = i['function']
        if f["name"] == "exsql":
            arg = json.loads(f["arguments"])
            query=arg["query"]
            return query