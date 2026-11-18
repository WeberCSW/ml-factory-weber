# 🧠 My ML Image — Ambiente de Machine Learning Containerizado

> Projeto pessoal de ML reproduzível: treino/inferência com PyTorch+CUDA rodando
> dentro do Docker no WSL2, dados persistidos em volume e metadados no PostgreSQL.

![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat&logo=pytorch&logoColor=white)
![CUDA](https://img.shields.io/badge/CUDA-76B900?style=flat&logo=nvidia&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791?style=flat&logo=postgresql&logoColor=white)

---

## 🗺️ Como as peças se encaixam
┌───────────────────────── MeuPC (Dell, WSL2) ─────────────────────────┐
│ │
│ NVIDIA GPU T1200 (4 GB VRAM) │
│ │ CUDA │
│ ▼ │
│ ┌─────────────────────────────┐ ┌──────────────────────────┐ │
│ │ Container: my-pytorch-env:v2│─────►│ Volume ~/ml_data │ │
│ │ PyTorch + Pandas + psycopg2 │ bind │ dados, checkpoints, │ │
│ └──────────┬──────────────────┘ mount│ modelos salvos │ │
│ │ └──────────────────────────┘ │
│ ▼ │
│ ┌─────────────────────────────┐ │
│ │ PostgreSQL 18 (WSL2) │ ◄── metadados / resultados │
│ └─────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘

**Por que isso?** A imagem fecha a versão de tudo (PyTorch, CUDA, Pandas).
O volume guarda os dados *fora* do container — se eu apagar a imagem, os dados sobrevivem. O Postgres registra o que foi treinado.

---

## 📁 Estrutura do projeto
ml-factory/
├── Dockerfile # receita da imagem my-pytorch-env:v2
├── api/ # código do balcão (FastAPI)
│ ├── main.py # servidor da API
│ └── modelo.py # arquitetura da rede neural (CNN)
├── modelo_cifar10.pt # o "cérebro" treinado (pesos da rede)
└── README.md # este arquivo


---

## 🚀 Rodando em 4 passos

### 1. Pré-requisitos
- WSL2 com driver NVIDIA instalado no Windows
- Docker Desktop (ou Docker Engine no WSL2)
- PostgreSQL 18 em execução no WSL2

### 2. Build e Execução da Imagem
```bash
# Constrói a imagem
docker build -t my-pytorch-env:v2 .

# Sobe o container com GPU e volume persistente
docker run --rm --gpus all \
  -p 8000:8000 \
  -v ~/ml_data:/home/jovyan/work \
  -it my-pytorch-env:v2 bash

# Dentro do container, inicie a API
cd /home/jovyan/work/api
uvicorn main:app --host 0.0.0.0 --port 8000


🐞 Troubleshooting (Problemas comuns)
Problema
Causa provável
Solução
torch.cuda.is_available() = False
Driver NVIDIA ausente no WSL2
Reinstalar driver Windows (não instalar CUDA dentro do WSL!)
CUDA out of memory
VRAM de 4 GB é pequena
Usar batch menor, torch.no_grad() ou modelo menor
Connection refused no Postgres
Container não alcança o WSL2
Usar host.docker.internal e liberar 5432 no pg_hba.conf
Dados sumiram
Esqueceu o -v ~/ml_data:/...
Sempre rodar com o bind mount de volume
👤 Autor
CSW — Projeto de estudo em DevOps + ML (aprendendo visualmente, um passo de cada vez 😄).

---

## 🤖 Status da Fábrica

![CI](https://github.com/WeberCSW/ml-factory-weber/actions/workflows/ci.yml/badge.svg)

O robô inspetor testa o cérebro e o balcão a cada `git push`.
Verde = fábrica aprovada. Vermelho = algo quebrou.
