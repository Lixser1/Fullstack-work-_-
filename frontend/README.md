# Чтобы включить  и просмотреть проект надо
## Добавить .env в корень бэк части
``` bash
BOT_TOKEN="ТОКЕН ДЛЯ РАБОТЫ БОТА"
API_KEY=my_secret_api_key_12345 # Ключ вставлен по примеру. 
API_HOST=127.0.0.1
API_PORT=8000
```
Для начала в одном терминале запусткаем сервер
```bash
cd emotion_bot

python run_api.py
```
Далее во втором терминале запускаем frontend часть
```bash
cd frontend
npm i
npm run dev
