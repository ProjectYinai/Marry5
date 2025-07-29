
from nonebot import on_command, on_message
from nonebot.adapters import Bot, Message
from nonebot.matcher import Matcher
from nonebot.rule import is_type
from nonebot.adapters.onebot.v11 import GroupMessageEvent
import random
import data


# 自定义问答表名
QA_TABLE = 'custom_qa'


# 初始化表，每条记录一个回答
def init_qa_table():
    data.sql(f'''CREATE TABLE IF NOT EXISTS {QA_TABLE} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        creator INTEGER NOT NULL
    )''')

init_qa_table()


# 添加问答命令（仅群聊，白名单等级>=5）
add_qa = on_command('添加问答', is_type(GroupMessageEvent), priority=5, block=True)

@add_qa.handle()
async def handle_add_qa(bot: Bot, event: GroupMessageEvent, matcher: Matcher):
    uid = event.user_id
    gid = event.group_id
    white = data.getWhite(uid)
    if str(uid) in data.admin.id or white>=5:
        args = str(event.get_message()).strip().split()
        if len(args) < 3:
            await bot.send_group_msg(group_id=str(gid), message="格式错误，示例：添加问答 问题 答案")
            return
        question = args[1]
        ans = ' '.join(args[2:])
        data.sql(f"INSERT INTO {QA_TABLE} (question, answer, creator) VALUES (?, ?, ?)", (question, ans, uid))
        await bot.send_group_msg(group_id=str(gid), message=f"自定义问答已添加：{question}")


# 触发自定义问答（优先级20，仅群聊）
qa_matcher = on_message(is_type(GroupMessageEvent), priority=20, block=False)

@qa_matcher.handle()
async def handle_qa(bot: Bot, event: GroupMessageEvent, matcher: Matcher):
    gid = event.group_id
    msg = str(event.get_message()).strip()
    # 查找匹配问题的所有回答
    rows = data.sql(f"SELECT answer FROM {QA_TABLE} WHERE question=?", (msg,))
    answers = [r[0] for r in rows if r[0] and r[0].strip()]
    if answers:
        answer = random.choice(answers)
        await bot.send_group_msg(group_id=str(gid), message=answer)

# 删除指定回答命令（仅群聊，白名单等级>=5）
del_qa = on_command('删除问答', is_type(GroupMessageEvent), priority=5, block=True)

@del_qa.handle()
async def handle_del_qa(bot: Bot, event: GroupMessageEvent, matcher: Matcher):
    uid = event.user_id
    gid = event.group_id
    white = data.getWhite(uid)
    if str(uid) in data.admin.id or white>=5:
        args = str(event.get_message()).strip().split()
        if len(args) < 3:
            await bot.send_group_msg(group_id=str(gid), message="格式错误，示例：删除问答 问题 答案内容")
            return
        question = args[1]
        del_answer = ' '.join(args[2:]).strip()
        # 查找该问题下的该回答
        try:
            data.sql(f"DELETE FROM {QA_TABLE} WHERE question=? AND answer=?", (question, del_answer))
            await bot.send_group_msg(group_id=str(gid), message=f"已删除回答：{del_answer}")
        except:
            await bot.send_group_msg(group_id=str(gid), message=f"没有找到回答：{del_answer}")
