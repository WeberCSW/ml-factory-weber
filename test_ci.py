import sys, io
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "api"))   # deixa o Python achar o main.py

import torch
from PIL import Image
from fastapi.testclient import TestClient
import main   # importar o balcão já carrega o cérebro!

# 1. O molde encaixa no cérebro?
n = sum(p.numel() for p in main.modelo.parameters())
print(f"✅ Cérebro carregado: {n:,} numerinhos")

# 2. DUBLÊ: na nuvem não existe Vivobook, então desligamos o caderno
main.registrar = lambda *a, **k: None

# 3. O balcão está vivo?
cliente = TestClient(main.app)
r = cliente.get("/")
assert r.status_code == 200, r.text
print("✅ GET / →", r.json()["status"])

# 4. O balcão dá palpite?
buf = io.BytesIO()
Image.new("RGB", (32, 32), "red").save(buf, format="PNG")
buf.seek(0)
r = cliente.post("/prever", files={"arquivo": ("t.png", buf, "image/png")})
assert r.status_code == 200, r.text
d = r.json()
assert d["classe"] in main.CLASSES
assert 0 <= d["confianca"] <= 1
print("✅ POST /prever →", d["classe"], d["confianca"])

print("🎉 FÁBRICA APROVADA")
