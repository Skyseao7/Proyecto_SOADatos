import httpx

class OpenMeteoService:
    def __init__(self):
        # Coordenadas de capitales de región para buscar el clima real
        self.coordenadas = {
            "Amazonas": {"lat": -6.23, "lon": -77.86},
            "Ancash": {"lat": -9.52, "lon": -77.52},
            "Arequipa": {"lat": -16.40, "lon": -71.53},
            "Ayacucho": {"lat": -13.16, "lon": -74.22},
            "Cajamarca": {"lat": -7.16, "lon": -78.51},
            "Cusco": {"lat": -13.53, "lon": -71.96},
            "Lima": {"lat": -12.04, "lon": -77.04},
            "Loreto": {"lat": -3.74, "lon": -73.25},
            "Piura": {"lat": -5.19, "lon": -80.63},
            "La Libertad": {"lat": -8.11, "lon": -79.02}
        }

    async def get_clima_real(self, region: str):
        coords = self.coordenadas.get(region)
        if not coords:
            return {"temp": 0, "humedad": 0, "estado": "Desconocido"}
            
        url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current_weather=true"
        
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url)
                data = resp.json()
                clima = data.get("current_weather", {})
                
                return {
                    "temp": clima.get("temperature"),
                    "velocidad_viento": clima.get("windspeed"),
                    "estado": "Lluvia" if clima.get("weathercode", 0) > 50 else "Despejado/Nublado",
                    "fuente": "Open-Meteo API"
                }
        except:
            return {"temp": 0, "humedad": 0, "estado": "Error API"}