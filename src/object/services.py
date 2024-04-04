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
        Формирует таблицу для сотрудников усадьбы:
         - Получаем данные по питанию для всех домиков на сегодня.
         - Если сегодня заселение - завтрак не входит в данные.
         - Если сегодня выселение - ужин не входит в данные.
        
        :return: Открытый в памяти png файл - таблица с данными по питанию.
        """
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
        dataframe = pd.DataFrame(
            data=data,
            index=range(1, len(purchases) + 1),
        )
        total = [
            f'{breakfast["adults"]} + {breakfast["kids"]}',
            f'{lunch["adults"]} + {lunch["kids"]}',
            f'{dinner["adults"]} + {dinner["kids"]}',
        ]
        dataframe.loc[len(purchases) + 1] = ["Итого", *total]
        ax = plt.subplot()
        ax.axis("off")
        df_styled = dataframe.style.set_properties(**{'text-align': 'center'})
        table = ax.table(
            cellText=df_styled.values,
            colLabels=df_styled.columns,
            cellLoc="center",
            loc="center",
            colColours=["lightgray"]*len(dataframe.columns),
        )
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        for (i, j), cell in table.get_celld().items(): # Ищем "Итого" и делаем жирным.
            if i == len(dataframe) and j == 0:
                cell.set_text_props(fontweight='bold')
        plt.savefig("table.png", bbox_inches="tight")
        return open("table.png", "rb")

    def _fill_data(self, data: Dict[str, List], meal: str, repast: Dict[str, int], purchase: Purchase):
        data[meal].append(
            f"{purchase.count_adult} + {purchase.count_kids}"
        )
        repast["adults"] += purchase.count_adult
        repast["kids"] += purchase.count_kids


purchase_service = PurchaseService()
