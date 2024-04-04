from object.services import purchase_service
from bot.services import bot_service
from django.conf import settings
from authentication.service import telegram_service
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import pytz


def send_daily_data():
    daily_data = purchase_service.get_daily_data()
    for chat_id in telegram_service.get_telegram_ids():
        bot_service.send_daily_data(chat_id, daily_data)


def start():
    scheduler = BackgroundScheduler()
    start_time = datetime.time(6, 0, 0)
    scheduler.add_job(
        send_daily_data,
        "interval",
        seconds=10,
        # 'cron',
        # hour=start_time.hour,
        # minute=start_time.minute,
        # timezone=pytz.timezone(settings.TIME_ZONE)
    )
    scheduler.start()


start()
