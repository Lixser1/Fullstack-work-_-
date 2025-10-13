from transformers import pipeline

class EmotionAnalyzer:
    def __init__(self):
        print("⏳ Загружаю модель для анализа тональности...")
        # Используем более точную модель
        self.classifier = pipeline(
            "text-classification",
            model="cointegrated/rubert-tiny-sentiment-balanced"
        )
        print("✅ Модель загружена!")
    
    def analyze(self, text: str) -> dict:
        """
        Анализирует тональность текста
        
        Возвращает словарь с результатом анализа
        """
        result = self.classifier(text)[0]
        
        label = result['label']
        score = result['score']
        
        # Переводим метки на русский
        label_map = {
            "neutral": "нейтральная 😐",
            "positive": "позитивная 😊",
            "negative": "негативная 😢"
        }
        
        return {
            "sentiment": label_map.get(label, label),
            "confidence": round(score * 100, 2),
            "raw_label": label
        }