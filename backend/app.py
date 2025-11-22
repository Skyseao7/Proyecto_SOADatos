from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.inei_service import IneiService
from services.clima_service import OpenMeteoService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

inei = IneiService()
clima_service = OpenMeteoService()

@app.get("/api/dashboard/{region}")
async def get_dashboard_data(region: str):
    datos_sociales = inei.get_datos_sociales(region)
    datos_clima = await clima_service.get_clima_real(region)
    
    return {
        "region": region,
        "social": datos_sociales,
        "clima": datos_clima,
        "fecha_consulta": "Tiempo Real"
    }