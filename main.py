from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pathlib import Path
import json, platform, time
import psutil

BASE = Path(__file__).resolve().parent.parent
MEMORY = BASE / "data" / "memory.json"

app = FastAPI(title="JARVIS V2")
app.mount("/static", StaticFiles(directory=str(BASE / "app" / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE / "app" / "templates"))

class ChatRequest(BaseModel):
    message: str

def load_memory():
    try:
        return json.loads(MEMORY.read_text(encoding="utf-8"))
    except Exception:
        return []

def save_memory(items):
    MEMORY.write_text(json.dumps(items[-100:], ensure_ascii=False, indent=2), encoding="utf-8")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/status")
def status():
    return {
        "assistant": "JARVIS V2",
        "online": True,
        "platform": platform.system(),
        "cpu": psutil.cpu_percent(interval=0.1),
        "ram": psutil.virtual_memory().percent,
        "uptime": int(time.time() - psutil.boot_time())
    }

@app.get("/api/memory")
def memory():
    return {"items": load_memory()}

@app.post("/api/chat")
def chat(payload: ChatRequest):
    msg = payload.message.strip()
    if not msg:
        return {"reply": "Estou ouvindo. Diga o que você precisa."}

    mem = load_memory()
    mem.append({"user": msg, "time": int(time.time())})
    save_memory(mem)

    lower = msg.lower()
    if "status" in lower:
        reply = "Todos os sistemas principais da V2 estão online. O painel está monitorando CPU, RAM e estado do assistente."
    elif "memória" in lower or "memoria" in lower:
        reply = f"Tenho {len(mem)} registros locais de memória nesta V2."
    elif "bolsaia" in lower:
        reply = "Módulo BolsaIA identificado. A V2 está preparada para integração com o projeto, mediante configuração das APIs necessárias."
    elif "quem é você" in lower or "quem e voce" in lower:
        reply = "Eu sou o JARVIS V2: um assistente modular, com dashboard, memória local, monitoramento e automações autorizadas."
    else:
        reply = f"Entendido. Registrei sua solicitação: “{msg}”. Na V2, ações externas devem passar por permissões antes de serem executadas."

    return {"reply": reply}

@app.get("/api/modules")
def modules():
    return {"modules": [
        {"name":"Núcleo IA","status":"online"},
        {"name":"Memória","status":"online"},
        {"name":"Monitor do sistema","status":"online"},
        {"name":"Automação autorizada","status":"ready"},
        {"name":"BolsaIA","status":"ready"},
        {"name":"Voz","status":"ready"}
    ]}
