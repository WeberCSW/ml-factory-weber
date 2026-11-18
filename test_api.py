import requests
from PIL import Image
import io
import sys

# 1. O "Pacote" (O robô cria uma imagem falsa na memória)
# Vamos fazer um quadrado vermelho 32x32 (o tamanho que o modelo espera)
img = Image.new('RGB', (32, 32), color='red') 
buffer = io.BytesIO()
img.save(buffer, format="PNG")
buffer.seek(0)

# 2. O "Endereço" da fábrica
URL = "http://localhost:8000/prever"

print("🤖 Robô Inspetor: Enviando quadrado vermelho para o balcão...")

try:
    # 3. O "Envio"
    resposta = requests.post(URL, files={"arquivo": ("teste.png", buffer, "image/png")}, timeout=5)
    
    # 4. A "Verificação"
    if resposta.status_code == 200:
        dados = resposta.json()
        print("✅ SUCESSO! O balcão está vivo e respondeu.")
        print(f"   🏷️  Classe prevista: {dados['classe']}")
        print(f"   🎯 Confiança: {dados['confianca']}")
        print(f"   📊 Top 3: {dados['top3']}")
    else:
        print(f"❌ ERRO! O balcão respondeu com código {resposta.status_code}")
        print(f"   Detalhes: {resposta.text}")
        sys.exit(1)
        
except requests.exceptions.ConnectionError:
    print("❌ ERRO CRÍTICO: O robô não conseguiu achar o balcão!")
    print("   (Verifique se o uvicorn está rodando na porta 8000)")
    sys.exit(1)
