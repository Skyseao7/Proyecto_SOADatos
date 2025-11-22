from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from services.database import DemographyService
from services.clima_service import OpenMeteoService

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

db_service = DemographyService()
weather_service = OpenMeteoService()

# Lista de distritos para el Frontend
@app.get("/api/lugares")
def listar_lugares():
    return db_service.get_lugares_list()

#Orquestación
@app.get("/api/dashboard/{nombre_lugar}")
async def get_dashboard(nombre_lugar: str):
    # 1. Obtener Datos Sociales y Coordenadas de SUPABASE
    social_data = db_service.get_data_by_name(nombre_lugar)
    
    if not social_data:
        raise HTTPException(status_code=404, detail="Lugar no encontrado")

    # 2. Usar las coordenadas de la DB para consultar OPEN-METEO
    clima_data = await weather_service.get_clima_dinamico(
        social_data['latitud'], 
        social_data['longitud']
    )

    # 3. Fusionar y responder
    return {
        "lugar": social_data['nombre'],
        "tipo": social_data['tipo'],
        "coordenadas": {"lat": social_data['latitud'], "lon": social_data['longitud']},
        "social": {
            "poblacion": social_data['poblacion'],
            "pbi": social_data['pbi'],
            "hospitales": social_data['hospitales'],
            "pobreza": social_data['indice_pobreza']
        },
        "clima": clima_data,
        "fuente_social": "Supabase (PostgreSQL)",
        "fuente_clima": "Open-Meteo API"
    }

app.mount("/", StaticFiles(directory="frontend", html=True), name="static")