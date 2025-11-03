import os
from dotenv import load_dotenv

# Cargar .env
load_dotenv()

print("📁 Directorio actual:", os.getcwd())
print("🔍 Verificando variables...")
print(f"   SECRET_KEY: {os.getenv('SECRET_KEY', '❌ No encontrada')}")
print(f"   DATABASE_URL: {os.getenv('DATABASE_URL', '❌ No encontrada')}")

from app import create_app

app = create_app()