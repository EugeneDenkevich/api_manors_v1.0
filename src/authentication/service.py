from authentication.models import TelegramIdUser


class TelegramService:
    """Сервис для работы с сущностью TelegramIdUser"""
    
    def get_telegram_ids(self):
        return [
            telegram_user.telegram_id
            for telegram_user in TelegramIdUser.objects.all()
        ]


telegram_service = TelegramService()
