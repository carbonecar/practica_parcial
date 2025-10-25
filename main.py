"""
    Servidor de ejemplo para la práctica de FastAPI
"""
import os
from pydantic import BaseModel
from fastapi import FastAPI



class ArchivoRequest(BaseModel):
    """
        Modelo para la solicitud de creación de archivo
    """
    name: str
    content: str


app = FastAPI(
    title="ChatGPT App Demo - MCP Server",
    description="Servidor MCP con transporte HTTP/SSE para ChatGPT",
    version="1.0.0"
)

@app.get("/")
async def prueba_root():
    """
    Endpoint de prueba en la raíz
    """
    return {"message": "Accediste al endpoint de prueba"}


@app.get("/files")
async def listar_archivos():
    """
    Develve los archivos del directorio
    """
    archivos = os.listdir("./files")
    return {"archivos": archivos}

@app.get("/files/{nombre_archivo}")
async def leer_archivo(nombre_archivo: str):
    """
    Lee el contenido de un archivo específico
    """
    ruta_archivo = os.path.join("./files", nombre_archivo)

    if not os.path.isfile(ruta_archivo):
        return {"error": "El archivo no existe"}

    with open(ruta_archivo, "r") as archivo:
        contenido = archivo.read()    
    return {"nombre_archivo": nombre_archivo, "contenido": contenido}

@app.post("/files")
async def crear_archivo(request: ArchivoRequest):
    """
    Crea un archivo con el nombre proporcionado en el cuerpo de la solicitud y contenido que se envia en el request 
    """
    data = request.dict()
    nombre_archivo = data.get("name")
    contenido = data.get("content", "")
    if not nombre_archivo:
        return {"error": "Se debe proporcionar un nombre de archivo"}

    ruta_archivo = os.path.join("./files", nombre_archivo)

    with open(ruta_archivo, "w") as archivo:
        archivo.write(contenido)

    return {"message": f"Archivo '{nombre_archivo}' creado exitosamente"}


