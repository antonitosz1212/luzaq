from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
from assistant import get_response
from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv() # Carga las variables del archivo .env

# Crea la instancia de FastAPI
app = FastAPI()
# Sirve los archivos estáticos (CSS y JS) desde la carpeta "public"
app.mount("/static", StaticFiles(directory="public"), name="static")

# Ruta principal que sirve el index.html
@app.get("/")
def get_index():
    return FileResponse("public/index.html")

env = Environment(loader=FileSystemLoader('backend/templates'))

# Conexión a la base de datos
def get_db():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
    except mysql.connector.Error as e:
        print("❌ Error en la conexión a MySQL:", e)
        raise

@app.post("/api/contact")
async def save_contact(data: Request):
    body = await data.json()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO contactos (nombre, email, mensaje) VALUES (%s, %s, %s)",
        (body['nombre'], body['email'], body['mensaje'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return JSONResponse({"message": "Gracias por contactarnos"})

@app.post("/chat/respond")
async def chat_respond(request: Request):
    try:
        body = await request.json()
        user_msg = body.get("message")
        print("[DEBUG] Mensaje recibido:", user_msg)

        if not user_msg:
            raise ValueError("El mensaje del usuario está vacío o no existe.")

        response = get_response(user_msg)
        print("[DEBUG] Respuesta del asistente:", response)

        # Guardar en base de datos (opcional)
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chats (usuario, asistente) VALUES (%s, %s)",
            (user_msg, response)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return JSONResponse({"response": response})

    except Exception as e:
        print("[ERROR /chat/respond]:", str(e))
        return JSONResponse(
            {"response": "Ocurrió un error al procesar tu pregunta."},
            status_code=500
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)