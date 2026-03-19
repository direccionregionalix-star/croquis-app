from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import base64, os, json
from datetime import datetime

app = FastAPI()

# CORS (por si después llamas desde otro lado)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carpeta templates
templates = Jinja2Templates(directory="templates")

# Carpeta datos
os.makedirs("data", exist_ok=True)

# Ruta principal (sirve el HTML)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint guardar
@app.post("/guardar")
async def guardar(request: Request):
    data = await request.json()

    nombre = data.get("nombre", "sin_nombre")
    imagen = data.get("imagen")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"{nombre}_{timestamp}".replace(" ", "_")

    # Guardar JSON
    with open(f"data/{base}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # Guardar imagen
    if imagen:
        img_data = base64.b64decode(imagen.split(",")[1])
        with open(f"data/{base}.png", "wb") as f:
            f.write(img_data)

    return {"status": "ok", "archivo": base}