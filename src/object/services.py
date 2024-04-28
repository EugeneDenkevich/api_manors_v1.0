from typing import List, Dict
from datetime import datetime, timedelta

from object.models import Purchase


class PurchaseService:
    """Сервис для работы с сущностью Purchase"""

    def get_daily_data(self) -> Dict:
        """
        Формируем данные по усадьбе:
         - Получаем данные по питанию для всех домиков на завтра.
         - Если завтра заселение - завтрак не входит в данные.
         - Если завтра выселение - ужин не входит в данные.
        
        :return: Данные для создания таблицы.
        """
        tomorrow = datetime.now().date() + timedelta(days=1)
        purchases = Purchase.objects.filter(
            stat="Approved",
            desired_arrival__lte=tomorrow,
            desired_departure__gte=tomorrow,
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
            if purchase.desired_arrival == tomorrow:
                data["Завтрак"].append("-")
            else:
                self._fill_data(data, "Завтрак", breakfast, purchase)
            self._fill_data(data, "Обед", lunch, purchase)
            if purchase.desired_departure == tomorrow:
                data["Ужин"].append("-")
            else:
                self._fill_data(data, "Ужин", dinner, purchase)
        return {
            "data": data,
            "meals": {
                "breakfast": breakfast,
                "lunch": lunch,
                "dinner": dinner,
            },
            "purchases_count": len(purchases),
        }

    def _fill_data(
        self,
        data: Dict[str, List],
        meal: str,
        repast: Dict[str, int],
        purchase: Purchase
    ):
        data[meal].append(
            f"{purchase.count_adult} + {purchase.count_kids}"
        )
        repast["adults"] += purchase.count_adult
        repast["kids"] += purchase.count_kids


purchase_service = PurchaseService()
