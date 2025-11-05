# Взаимодействие с приватным API
BASE_URL: str = 'https://example.com/api' 
LOGIN: str = '...'
PASSWORD: str = '...'

# Кол-во дней, когда расписание 
# перестанет быть актуальным
TIMEOUT: int = 10 

# Ссылка на репозиторий для парсинга обновлений
# и ссылок для некоторых кнопок (без / в конце)
REPO_URL: str = 'https://github.com/ktnk-dev/ZatupsSchedule'

# Текущая версия приложения
VERSION: str = '1.2.3'

# Ссылка на телеграм бота для синхронизации (indev)
TELEGRAM_BOT: str | None = 'https://t.me/zatups_bot'
