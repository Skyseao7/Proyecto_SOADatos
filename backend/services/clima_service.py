import httpx

class OpenMeteoService:
    async def get_clima_dinamico(self, lat: float, lon: float):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
        
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url)
                data = resp.json()
                
                current = data.get("current_weather", {})
                daily = data.get("daily", {})
                
                return {
                    "temp_actual": current.get("temperature"),
                    "viento": current.get("windspeed"),
                    "temp_max": daily.get("temperature_2m_max", [0])[0],
                    "temp_min": daily.get("temperature_2m_min", [0])[0],
                    "estado": "Lluvioso" if current.get("weathercode", 0) > 50 else "Despejado"
                }
        except Exception as e:
            print(f"Error API Clima: {e}")
            return None