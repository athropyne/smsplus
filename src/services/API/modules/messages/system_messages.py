from modules.messages.dto import SystemMessage

USER_NOT_AVAILABLE: str = SystemMessage(
    signal="Пользователь не в сети и не подписан на уведомления. Сообщение не отправлено").model_dump_json()
SEND_TO_TELEGRAM: str = SystemMessage(signal="Сообщение отправлено в телегу").model_dump_json()
INCORRECT_DATA: str = SystemMessage(signal="Не валидные данные").model_dump_json()