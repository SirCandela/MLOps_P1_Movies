import subprocess
import uvicorn
from fastapi import FastAPI
from api.endpoints import app as api_app


def run_notebook():
    # Ejecutar el notebook de Jupyter para los procesos de Machine Learning
    subprocess.run(["jupyter", "nbconvert", "--to", "notebook", "--execute", "notebooks/ml_model.ipynb"])

def run_api():
    # Correr el servidor de FastAPI para las funciones
    uvicorn.run("api.endpoints:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    #run_notebook()  # Ejecuta el notebook de ML
    run_api()       # Inicia el servidor de FastAPI
