import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", 8000))
    
    print(f"🚀 Запускаю API на {host}:{port}")
    
    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        reload=True  # Автоперезагрузка при изменении кода
    )