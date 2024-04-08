import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path
import datetime

from apscheduler.schedulers.background import BackgroundScheduler
import dataframe_image as dfi
import httpx
import pytz

sys.path.append(str(Path(__file__).parent.parent.parent))
from bot.services import bot_service
from src.exceptions import BadRequestError


class Sender():
    
    def __init__(
        self,
        *,
        url: str,
        time_zone: str,
        start_time: datetime.time,
        image_path: Path,
        interval: bool = False,
    ) -> None:
        self.url = url
        self.time_zone = time_zone
        self.start_time = start_time
        self.image_path = image_path
        self.interval = interval

    def send_daily_data(self) -> None:
        """
        Берём данные из джанго приложения.
        Формируем из них таблицу и сохраняем в файл "table.png".
        Открываем файл и передаём его сервису бота для отправки сообщения.
        """
        # Получаем данные из джанги
        response = httpx.get(url=self.url)
        if response.status_code != 200:
            raise BadRequestError()

        # Парсим данные и дополняем таблицу пустыми строками, если данных мало
        daily_data = response.json()
        telegram_ids = daily_data["telegram_ids"]
        data = daily_data["data"]
        breakfast = daily_data["meals"]["breakfast"]
        lunch = daily_data["meals"]["lunch"]
        dinner = daily_data["meals"]["dinner"]
        purchases_count = daily_data["purchases_count"]
        while len(data["Домик"]) < 4: # Оптимальное количество строк
            data["Домик"].append("")
            data["Завтрак"].append("")
            data["Обед"].append("")
            data["Ужин"].append("")
            purchases_count += 1

        # Формируем таблицу и сохраняем в файл
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
        self._drow_using_dfi(dataframe) # Можно использовать _drow_using_plt

        # Передаём данные сервису бота для отправки сообщения
        for chat_id in telegram_ids:
            bot_service.send_daily_data(chat_id, open(self.image_path, "rb"))


    def _drow_using_plt(self, dataframe: pd.DataFrame) -> None:
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
        for (i, j), cell in table.get_celld().items():
            if i == len(dataframe) and j == 0:
                cell.set_text_props(fontweight='bold')
        plt.savefig(self.image_path, bbox_inches="tight")


    def _drow_using_dfi(self, dataframe: pd.DataFrame) -> None:
        """
        Нарисовать таблицу, используя dataframe_image.
        Требует движок chromium на сервере.
        """
        df_styled = dataframe.style.map(
            lambda x: 'font-weight: bold' if x == "Итого" else ''
        )
        dfi.export(df_styled, self.image_path)


    def start(self) -> None:
        """
        Запуск планировщика
        """
        scheduler = BackgroundScheduler()
        kwargs = {}
        if self.interval:
            kwargs["trigger"] = "interval"
            kwargs["seconds"] = 5
        else:
            kwargs["trigger"] = "cron"
            kwargs["hour"] = self.start_time.hour
            kwargs["minute"] = self.start_time.minute
            kwargs["timezone"] = pytz.timezone(self.time_zone)
            kwargs["max_instances"] = 1
        scheduler.add_job(self.send_daily_data, **kwargs)
        scheduler.start()
        while True:
            pass
