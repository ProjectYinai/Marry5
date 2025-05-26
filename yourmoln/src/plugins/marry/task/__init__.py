from nonebot import require,get_bot

require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler

@scheduler.scheduled_job("cron", hour="22",minute="55",second="0", id="job_4")
async def run_every_4_day():
    print("SCHEDULER:job_4")
    bot = get_bot()
    msg_t="(*ﾟ∇ﾟ)店长们晚安哦——"
    await bot.send_group_msg(group_id=str(555679990),message=msg_t)

    