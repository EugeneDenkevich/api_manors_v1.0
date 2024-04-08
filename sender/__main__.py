import datetime
from pathlib import Path
import os
import logging

from dotenv import load_dotenv

from src.sender import Sender


load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    filename=Path(__file__).parent / "py_log.log",
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s"
)


if __name__ == "__main__":
    """Запуск сервиса sender"""
    root_path = Path(__file__).parent
    wab_app_host = os.getenv("WEB_APP_HOST", "http://localhost:8000")
    endpoint = "/api/telegram/get_daily_data/"
    sender = Sender(
        url = wab_app_host + endpoint,
        time_zone="Europe/Moscow",
        start_time=datetime.time(18, 0, 0),
        image_path=root_path / "table.png",
        interval=True,
    )
    sender.start()
