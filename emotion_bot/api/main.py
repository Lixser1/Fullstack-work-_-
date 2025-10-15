import logging
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware  # Добавляем CORS
from pydantic import BaseModel
from transformers import pipeline
import os
from dotenv import load_dotenv
from datetime import datetime

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_logs.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Создаём FastAPI приложение
app = FastAPI(title="Sentiment & Emotion Analysis API")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Разрешить фронтенд
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API ключ из .env
API_KEY = os.getenv("API_KEY", "default_key")

# Загружаем модели при старте
print("⏳ Загружаю модели...")

# Модель для тональности (toxicity)
sentiment_classifier = pipeline(
    "text-classification",
    model="cointegrated/rubert-tiny-sentiment-balanced"
)

# Модель для эмоций (английский язык)
emotion_classifier = pipeline(
    "text-classification",
    model="bhadresh-savani/bert-base-uncased-emotion"
)

print("✅ Модели загружены!")

# Модель запроса
class AnalysisRequest(BaseModel):
    text: str
    mode: str  # "sentiment" или "emotion"

# Модель ответа
class AnalysisResponse(BaseModel):
    mode: str
    result: str
    score: float

# Проверка API ключа
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        logger.warning(f"Попытка доступа с неверным API ключом: {x_api_key}")
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key

# Главный эндпоинт
@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(
    request: AnalysisRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Анализирует текст на тональность или эмоции
    
    - **text**: текст для анализа
    - **mode**: "sentiment" или "emotion"
    """
    
    start_time = datetime.now()
    
    try:
        logger.info(f"Получен запрос: mode={request.mode}, text_length={len(request.text)}")
        
        if request.mode == "sentiment":
            # Анализ тональности
            result = sentiment_classifier(request.text)[0]
            label = result['label']
            score = result['score']
            
            # Маппинг меток
            label_map = {
                "neutral": "нейтрально",
                "positive": "позитив",
                "negative": "негатив"
            }
            
            response = AnalysisResponse(
                mode="sentiment",
                result=label_map.get(label, label),
                score=round(score, 2)
            )
            
        elif request.mode == "emotion":
            # Анализ эмоций
            result = emotion_classifier(request.text)[0]
            label = result['label']
            score = result['score']
            
            # Маппинг эмоций на русский
            emotion_map = {
                "joy": "радость",
                "sadness": "грусть",
                "anger": "злость",
                "fear": "страх",
                "love": "любовь",
                "surprise": "удивление"
            }
            
            response = AnalysisResponse(
                mode="emotion",
                result=emotion_map.get(label, label),
                score=round(score, 2)
            )
            
        else:
            raise HTTPException(status_code=400, detail="Mode должен быть 'sentiment' или 'emotion'")
        
        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info(f"Запрос обработан за {elapsed:.2f}с: {response.result} ({response.score})")
        
        return response
        
    except Exception as e:
        logger.error(f"Ошибка при обработке запроса: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Healthcheck эндпоинт
@app.get("/health")
async def health_check():
    """Проверка работоспособности API"""
    return {"status": "ok", "models": ["sentiment", "emotion"]}

# Информация об API
@app.get("/")
async def root():
    return {
        "message": "Sentiment & Emotion Analysis API",
        "endpoints": {
            "/analyze": "POST - анализ текста",
            "/health": "GET - проверка статуса",
            "/docs": "GET - документация Swagger"
        }
    }