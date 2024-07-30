# api/__init__.py

from fastapi import FastAPI

app = FastAPI()

# Importar los endpoints
from . import endpoints
