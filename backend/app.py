from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.database import DemographyService
from services.clima_service import OpenMeteoService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

db_service = DemographyService()
weather_service = OpenMeteoService()

@app.get("/api/lugares")
def listar_lugares():
    """Devuelve la lista completa para llenar los selectores"""
    datos = db_service.get_lugares_list()
    if not datos:
        return []
    return datos

@app.get("/api/dashboard/{nombre_lugar}")
async def get_dashboard(nombre_lugar: str):
    social_data = db_service.get_data_by_name(nombre_lugar)
    
    if not social_data:
        raise HTTPException(status_code=404, detail="Lugar no encontrado en BD")

    clima_data = await weather_service.get_clima_dinamico(
        social_data['latitud'], 
        social_data['longitud']
    )

    return {
        "lugar": social_data['distrito'],
        "region": social_data['region'],
        "provincia": social_data['provincia'],
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