from apscheduler.schedulers.blocking import BlockingScheduler
from do_attendance import Attendance

sched = BlockingScheduler()


@sched.scheduled_job('cron', minute='*/20')
def main():
    a = Attendance()
    try:
        result1 = a.health_info_attendance()
        result2 = a.do_daily_attendance()
        print(result1['info'])
        print(result2['info'])
    except:
        print('提交失败了哦QAQ')


sched.start()
