from typing import List, Dict
from datetime import datetime
import pandas as pd
from io import BufferedReader
import matplotlib.pyplot as plt

from object.models import Purchase


class PurchaseService:
    """Сервис для работы с сущностью Purchase"""
    
    def get_daily_data(self) -> BufferedReader:
        """
        Формируем данные по усадьбе:
         - Получаем данные по питанию для всех домиков на сегодня.
         - Если сегодня заселение - завтрак не входит в данные.
         - Если сегодня выселение - ужин не входит в данные.
        
        :return: Данные для создания таблицы.
        """
        # TODO Результат сделать в виде датакласса или pydantic схемы.
        today = datetime.now().date()
        purchases = Purchase.objects.filter(
            stat="Approved",
            desired_arrival__lte=today,
            desired_departure__gte=today,
        )
        data = {
            "Домик": [],
            "Завтрак": [],
            "Обед": [],
            "Ужин": [],
        }
        breakfast = {
            "adults": 0,
            "kids": 0,
        }
        lunch = {
            "adults": 0,
            "kids": 0,
        }
        dinner = {
            "adults": 0,
            "kids": 0,
        }
        for purchase in purchases:
            data["Домик"].append(purchase.object.title)
            if purchase.desired_arrival == today:
                data["Завтрак"].append("-")
            else:
                self._fill_data(data, "Завтрак", breakfast, purchase)
            self._fill_data(data, "Обед", lunch, purchase)
            if purchase.desired_departure == today:
                data["Ужин"].append("-")
            else:
                self._fill_data(data, "Ужин", dinner, purchase)
        result = {
            "data": data,
            "meals": {
                "breakfast": breakfast,
                "lunch": lunch,
                "dinner": dinner,
            },
            "purchases_count": len(purchases),
        }
        return result

    def _fill_data(self, data: Dict[str, List], meal: str, repast: Dict[str, int], purchase: Purchase):
        data[meal].append(
            f"{purchase.count_adult} + {purchase.count_kids}"
        )
        repast["adults"] += purchase.count_adult
        repast["kids"] += purchase.count_kids


purchase_service = PurchaseService()
