from apscheduler.schedulers.blocking import BlockingScheduler
from do_attendance import Attendance
from datetime import datetime

sched = BlockingScheduler()


@sched.scheduled_job('cron', minute='*/20')
def main():
    a = Attendance()
    try:
        result1 = a.health_info_attendance()
        result2 = a.do_daily_attendance()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]" + result1['info'])
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]" + result2['info'])
    except:
        print('提交失败了哦QAQ')


sched.start()
