import io
from pathlib import Path
import torch
import torch.nn.functional as F
import psycopg2
from fastapi import FastAPI, UploadFile, File
from PIL import Image
from torchvision import transforms
from modelo import CNN

CLASSES = ['avião','carro','pássaro','gato','veado',
           'cachorro','sapo','cavalo','navio','caminhão']
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

modelo = CNN().to(device)
caminho = Path(__file__).resolve().parent.parent / "modelo_cifar10.pt"
modelo.load_state_dict(torch.load(caminho, map_location=device, weights_only=True))
modelo.eval()

preparo = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,)*3, (0.5,)*3),
])

# 📒 O caderno mora no Vivobook!
DB = dict(host="100.87.235.13", port=5432, database="blog_db",
             user="meusistema", password="senha123", sslmode="disable",
             connect_timeout=3)

def registrar(classe, confianca):
    """Anota no caderno. Se o caderno sumir, o balcão CONTINUA atendendo!"""
    try:
        with psycopg2.connect(**DB) as conn:
            with conn.cursor() as cur:
                cur.execute("""CREATE TABLE IF NOT EXISTS atendimentos (
                    id SERIAL PRIMARY KEY,
                    quando TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    classe TEXT,
                    confianca REAL)""")
                cur.execute("INSERT INTO atendimentos (classe, confianca) VALUES (%s,%s)",
                            (classe, confianca))
    except Exception as e:
        print(f"⚠️ Caderno indisponível: {e}")

app = FastAPI(title="Balcão CIFAR-10", description="Mande uma foto, receba o palpite")

@app.get("/")
def raiz():
    return {"status": "online", "dispositivo": str(device), "classes": CLASSES}

@app.post("/prever")
async def prever(arquivo: UploadFile = File(...)):
    img = Image.open(io.BytesIO(await arquivo.read())).convert("RGB")
    tensor = preparo(img).unsqueeze(0).to(device)
    with torch.no_grad():
        probs = F.softmax(modelo(tensor), dim=1)[0]
    top3 = torch.topk(probs, 3)
    classe = CLASSES[int(top3.indices[0])]
    confianca = round(float(top3.values[0]), 4)
    registrar(classe, confianca)   # 📒 anota no caderno remoto
    return {"classe": classe, "confianca": confianca,
            "top3": [{"classe": CLASSES[int(i)], "prob": round(float(p), 4)}
                     for p, i in zip(top3.values, top3.indices)]}

@app.get("/atendimentos")
def atendimentos():
    """Lê as últimas 10 páginas do caderno."""
    with psycopg2.connect(**DB) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, quando, classe, confianca FROM atendimentos ORDER BY id DESC LIMIT 10")
            return [{"id": r[0], "quando": str(r[1]), "classe": r[2], "confianca": r[3]}
                    for r in cur.fetchall()]
