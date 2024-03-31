from datetime import datetime
import pandas as pd
from tabulate import tabulate

from object.models import Purchase


class PurchaseServies:
    """Севис для работы с сущностью Purchase"""
    
    def get_daily_data(self):
        today = datetime.now().date()
        purchases = Purchase.objects.filter(
            stat="Approved",
            desired_arrival__lte=today,
            desired_departure__gte=today,
        )
        meal = [f"{purchase.count_adult} + {purchase.count_kids}" for purchase in purchases]
        dataframe = pd.DataFrame(
            {
                "Домик": [purchase.object.title for purchase in purchases],
                "Завтрак": meal,
                "Обед": meal,
                "Ужин": meal,
            }, 
        )
        adults = sum([purchase.count_adult for purchase in purchases])
        children = sum([purchase.count_kids for purchase in purchases])
        total = [f"{adults} + {children}"]*3
        dataframe.loc[len(dataframe.index)] = ["Итого", *total]
        table = tabulate(
            dataframe,
            headers="keys",
            tablefmt="grid",
            stralign='center',
            showindex=False
        )
        return table


purchase_service = PurchaseServies()
