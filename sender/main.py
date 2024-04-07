from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from dotenv import load_dotenv
from os import getenv
from exceptions import BadRequestError
import pandas as pd
import matplotlib.pyplot as plt
import dataframe_image as dfi
import logging
from pathlib import Path
import sys
import httpx
root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))
from bot.services import bot_service
import pytz


TIME_ZONE = "Europe/Moscow"
START_HOURS = 8
START_MINUTES = 0
sender_path = root_path / "sender"
log_path = sender_path / "py_log.log"
image_path = sender_path / "table.png"


logging.basicConfig(
    level=logging.INFO,
    filename=log_path,
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s"
)


load_dotenv()


def send_daily_data() -> None:
    wab_app_host = getenv("WEB_APP_HOST", "localhost:8000")
    url = wab_app_host + "/api/telegram/get_daily_data/"
    response = httpx.get(url=url)
    if response.status_code != 200:
        raise BadRequestError()
    daily_data = response.json()
    telegram_ids = daily_data["telegram_ids"]
    data = daily_data["data"]
    breakfast = daily_data["meals"]["breakfast"]
    lunch = daily_data["meals"]["lunch"]
    dinner = daily_data["meals"]["dinner"]
    purchases_count = daily_data["purchases_count"]
    dataframe = pd.DataFrame(
            data=data,
            index=range(1, purchases_count + 1),
        )
    total = [
        f'{breakfast["adults"]} + {breakfast["kids"]}',
        f'{lunch["adults"]} + {lunch["kids"]}',
        f'{dinner["adults"]} + {dinner["kids"]}',
    ]
    dataframe.loc[purchases_count + 1] = ["Итого", *total]
    # _drow_using_plt(dataframe)
    _drow_using_dfi(dataframe)
    for chat_id in telegram_ids:
        bot_service.send_daily_data(chat_id, open(image_path, "rb"))


def _drow_using_plt(dataframe: pd.DataFrame):
    """
    Нарисовать таблицу, используя matplotlib.
    Проблемы с оптимизацией.
    """
    ax = plt.subplot()
    ax.axis("off")
    table = ax.table(
        cellText=dataframe.values,
        colLabels=dataframe.columns,
        cellLoc="center",
        loc="center",
        colColours=["lightgray"]*len(dataframe.columns),
    )
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    for (i, j), cell in table.get_celld().items(): # Ищем "Итого" и делаем жирным.
        if i == len(dataframe) and j == 0:
            cell.set_text_props(fontweight='bold')
    plt.savefig(image_path, bbox_inches="tight")


def _drow_using_dfi(dataframe: pd.DataFrame):
    """
    Нарисовать таблицу, используя dataframe_image.
    Требует движок chromium на сервере.
    """
    df_styled = dataframe.style.map(
        lambda x: 'font-weight: bold' if x == "Итого" else ''
    )
    dfi.export(df_styled, image_path)


def start():
    scheduler = BackgroundScheduler()
    start_time = datetime.time(START_HOURS, START_MINUTES, 0)
    scheduler.add_job(
        send_daily_data,
        # "interval",
        # seconds=5,
        'cron',
        hour=start_time.hour,
        minute=start_time.minute,
        timezone=pytz.timezone(TIME_ZONE),
        max_instances=1,
    )
    scheduler.start()
    while True:
        pass


if __name__ == "__main__":
    start()
