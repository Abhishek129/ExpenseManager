from apscheduler.schedulers.background import BackgroundScheduler
from ..task import scheduleExpense
from ..models import schedule_tr
from datetime import datetime

def start():
    data_sc=schedule_tr.objects.all()
    for i in data_sc:
        date = i.added_on
        year=date.year
        month=date.month
        day=date.day

        scheduler = BackgroundScheduler()
        scheduler.add_job(scheduleExpense,run_date=datetime(year,month,day,00,00,00),id='scheduleExpense')
        scheduler.start()