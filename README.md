# README

Коротко: это Telegram-бот и воркер на Pyrogram, который следит за чатами из указанной папки, записывает их в файл и управляет двумя клиентами (BotAdmin и Watcher). Проект запускается локально или в Docker (docker-compose).

---

### Требования

- Python 3.11+
- pip-зависимости перечислены в requirements.txt
- Docker и docker-compose (опционально для контейнерной настройки)
- Telegram API credentials (API_ID, API_HASH) и токен бота (BOT_TOKEN)
- (опционально) SESSION_STRING для пользовательского Pyrogram-клиента

---

### Структура проекта

- main.py — основной вход, запускает BotAdmin и Watcher, выполняет однократное получение чатов и затем запускает клиентов
- app/chat_updater.py — функция get_chats_in_folder для получения чатов из фильтра (папки)
- app/bot_admin.py — реализация BotAdmin (в проекте)
- app/watcher.py — реализация Watcher (в проекте)
- requirements.txt — зависимости
- Dockerfile — образ для контейнера
- docker-compose.yml — сервис watcher
- example.env — пример .env с переменными окружения
- chats.txt — файл со списком chat.id (генерируется при запуске)

---

### Переменные окружения

Создайте файл .env на основе example.env и заполните поля.

Обязательные переменные:
- API_ID — числовой идентификатор Telegram API
- API_HASH — строковой API hash
- BOT_TOKEN — токен вашего бота
- SESSION_STRING — (опционально) строка сессии пользовательского аккаунта, если используется
- ALLOWED_USER_ID — id администратора (используется в BotAdmin)

Необязательные:
- FOLDER_NAME — название папки/фильтра в Telegram, откуда брать чаты (по умолчанию "test work")
- UPDATE_INTERVAL — интервал в секундах для обновления (если активируется)  
- CHATS_FILENAME — имя файла для записи id чатов (по умолчанию chats.txt)
- PYROGRAM_SESSION_NAME — имя сессии pyrogram для временного клиента (по умолчанию my_account)

Пример .env (example.env):
```
API_ID=1234567
API_HASH=your_api_hash_here
SESSION_STRING=your_user_session_string_here
BOT_TOKEN=123456:ABC-DEF...
ALLOWED_USER_ID=987654321
FOLDER_NAME=test work
```

---

### Команды бота

В боте реализованы следующие команды:
- /add <keyword> — добавить ключевое слово/фразу
- /remove <keyword> — удалить (точное совпадение, регистронезависимо)
- /list — показать все ключевые слова
- /clear — удалить все ключевые слова
- /help — показать справку с командами

---

### Локальный запуск

1. Создайте и заполните .env (на основе example.env).
2. Установите зависимости:
```bash
pip install -r requirements.txt
```
3. Запустите:
```bash
python main.py
```
При первом запуске скрипт один раз получит список чатов из указанной папки и запишет их в chats.txt, затем запустит BotAdmin и Watcher и перейдёт в режим ожидания (idle).

---

### Запуск через Docker

1. Скопируйте example.env в .env и заполните переменные.
2. Соберите образ и запустите через docker-compose:
```bash
docker compose up --build -d
```
3. Логи сервиса:
```bash
docker compose logs -f watcher
```
Контейнер монтирует локальную папку ./data в /app/data (в docker-compose указано). Файлы и база (если используются) сохраняются там.

---
