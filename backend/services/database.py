from supabase import create_client, Client

# --- TUS CREDENCIALES (Asegúrate de que sean las correctas) ---
URL = "https://rqphwksumemrqhjjbpjx.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJxcGh3a3N1bWVtcnFoampicGp4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM4MDc0NDMsImV4cCI6MjA3OTM4MzQ0M30.OmgzFUx2EyFiYlpLMjKjR9YUhEghXxEQqy5JnW49Zm8"

supabase: Client = create_client(URL, KEY)

class DemographyService:
    def get_lugares_list(self):
        # CORRECCION: Traemos TODO (*) para poder filtrar por región/provincia en el HTML
        try:
            response = supabase.table("lugares").select("*").execute()
            return response.data
        except Exception as e:
            print("Error en DB:", e)
            return []

    def get_data_by_name(self, nombre_distrito: str):
        # CORRECCION: Ahora buscamos por la columna 'distrito'
        try:
            response = supabase.table("lugares").select("*").eq("distrito", nombre_distrito).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print("Error buscando distrito:", e)
            return None