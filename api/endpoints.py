
# api/endpoints.py
from fastapi import FastAPI, HTTPException
import pandas as pd
from datetime import datetime
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = FastAPI(
    title="API Recomendadora de  Peliculas",
    description="API para consultar información sobre películas usando el dataset proporcionado por Henry.",
    version="1.0.0"
)

# Cargar los datos
movies_data_file = 'notebook/data/movies_df_fastApi.csv'
cast_data_file = 'notebook/data/cast_df.csv'
crew_data_file = 'notebook/data/crew_df.csv'

try:
    movies_df = pd.read_csv(movies_data_file)
    print("Carga exitosa de movies_df_fastApi.csv")
    print(f"Shape de movies_df: {movies_df.shape}")
except FileNotFoundError:
    print(f"El archivo {movies_data_file} no se encuentra")
    movies_df = pd.DataFrame()

try:
    cast_df = pd.read_csv(cast_data_file)
    print("Carga exitosa de cast_df.csv")
    print(f"Shape de cast_df: {cast_df.shape}")
except FileNotFoundError:
    print(f"El archivo {cast_data_file} no se encuentra")
    cast_df = pd.DataFrame()

try:
    crew_df = pd.read_csv(crew_data_file)
    print("Carga exitosa de crew_df.csv")
    print(f"Shape de crew_df: {crew_df.shape}")
except FileNotFoundError:
    print(f"El archivo {crew_data_file} no se encuentra")
    crew_df = pd.DataFrame()

if movies_df.empty or cast_df.empty or crew_df.empty:
    raise HTTPException(status_code=500, detail="Los archivos de datos no están cargados correctamente. Verifique que los archivos están en la ruta correcta.")

# Diccionario para la conversión de meses en español a números
meses_dict = {
    'Enero': 1,
    'Febrero': 2,
    'Marzo': 3,
    'Abril': 4,
    'Mayo': 5,
    'Junio': 6,
    'Julio': 7,
    'Agosto': 8,
    'Septiembre': 9,
    'Octubre': 10,
    'Noviembre': 11,
    'Diciembre': 12
}

# Diccionario para los días de la semana en español
dias_dict = {
    'Lunes': 0,
    'Martes': 1,
    'Miércoles': 2,
    'Jueves': 3,
    'Viernes': 4,
    'Sábado': 5,
    'Domingo': 6
}

@app.get("/cantidad_filmaciones_mes/{mes}", tags=["Consultas por mes"], description="Devuelve la cantidad de películas estrenadas en un mes específico.")
def cantidad_filmaciones_mes(mes: str):
    # Convertir el mes a número
    mes_num = meses_dict.get(mes.capitalize(), None)
    if mes_num is None:
        valid_months = ', '.join(meses_dict.keys())
        return {"error": f"Mes no válido. Los meses válidos son: {valid_months}"}

    # Filtrar las películas que se estrenaron en el mes dado
    count = 0
    for date in movies_df['release_date']:
        try:
            if datetime.strptime(date, '%Y-%m-%d').month == mes_num:
                count += 1
        except:
            continue

    return {"message": f"{count} cantidad de películas fueron estrenadas en el mes de {mes}"}

@app.get("/cantidad_filmaciones_dia/{dia}", tags=["Consultas por día"], description="Devuelve la cantidad de películas estrenadas en un día específico.")
def cantidad_filmaciones_dia(dia: str):
    # Convertir el nombre del día en número
    dia_num = dias_dict.get(dia.capitalize(), None)
    if dia_num is None:
        valid_days = ', '.join(dias_dict.keys())
        return {"error": f"Día no válido. Los días válidos son: {valid_days}"}

    # Filtrar las películas que se estrenaron en el día dado
    count = 0
    for date in movies_df['release_date']:
        try:
            if datetime.strptime(date, '%Y-%m-%d').weekday() == dia_num:
                count += 1
        except:
            continue

    return {"message": f"{count} cantidad de películas fueron estrenadas en los días {dia}"}

@app.get("/score_titulo/{titulo_de_la_filmacion}", tags=["Consultas por título"], description="Devuelve el título, el año de estreno y el score/popularidad de una película dada.")
def score_titulo(titulo_de_la_filmacion: str):
    # Buscar la película por título
    movie = movies_df[movies_df['title'].str.contains(titulo_de_la_filmacion, case=False, na=False)]

    if movie.empty:
        raise HTTPException(status_code=404, detail="Película no encontrada")

    # Obtener el primer resultado (en caso de múltiples coincidencias)
    movie = movie.iloc[0]
    release_year = datetime.strptime(movie['release_date'], '%Y-%m-%d').year
    score = movie['popularity']

    return {
        "titulo": movie['title'],
        "año_de_estreno": release_year,
        "score": score
    }

@app.get("/votos_titulo/{titulo_pelicula}", tags=["Consultas por título"], description="Devuelve el título, la cantidad de votos y el promedio de las votaciones de una película dada. Requiere al menos 2000 valoraciones.")
def votos_titulo(titulo_pelicula: str):
    # Buscar la película por nombre_pelicula
    movie = movies_df[movies_df['title'].str.contains(titulo_pelicula, case=False, na=False)]

    if movie.empty:
        raise HTTPException(status_code=404, detail="Película no encontrada")

    # Obtener el primer resultado (en caso de múltiples coincidencias)
    movie = movie.iloc[0]
    total_votos = movie['vote_count']
    promedio_votos = movie['vote_average']
    
    # Verificar si hay al menos 2000 valoraciones
    if total_votos < 2000:
        raise HTTPException(status_code=400, detail="La película no cumple con el requisito mínimo de 2000 valoraciones")

    return {
        "mensaje": f"La película '{movie['title']}' cuenta con un total de {total_votos} valoraciones, con un promedio de {promedio_votos:.1f}.",
        "titulo": movie['title'],
        "total_valoraciones": total_votos,
        "promedio_valoraciones": promedio_votos
    }

# Definir endpoint para obtener información del actor
@app.get("/actor/{nombre_actor}", tags=["Consultas sobre actores"], description="Obtiene el éxito del actor medido a través del retorno, cantidad de películas y promedio de retorno.")
def get_actor(nombre_actor: str):
    if cast_df.empty or movies_df.empty:
        raise HTTPException(status_code=500, detail="Los archivos de datos no están cargados correctamente")

    # Filtrar el DataFrame del cast para obtener las películas en las que participó el actor
    actor_movies = cast_df[cast_df['name'] == nombre_actor]

    if actor_movies.empty:
        raise HTTPException(status_code=404, detail="El actor no fue encontrado en el dataset")

    # Merge con el DataFrame de movies para obtener el retorno de cada película
    actor_movies = actor_movies.merge(movies_df, left_on='id', right_on='id', how='left')

    # Calcular el retorno total y el promedio de retorno
    retorno_total = actor_movies['return'].sum()
    cantidad_peliculas = actor_movies.shape[0]
    promedio_retorno = retorno_total / cantidad_peliculas if cantidad_peliculas > 0 else 0

    return {
        "actor": nombre_actor,
        "cantidad_peliculas": cantidad_peliculas,
        "retorno_total": retorno_total,
        "promedio_retorno": promedio_retorno
    }

@app.get("/director/{nombre_director}", tags=["Consultas por director"], description="Devuelve el éxito de un director basado en el retorno de las películas que ha dirigido. Incluye detalles de cada película.")
def get_director(nombre_director: str):
    global crew_df, movies_df

    if crew_df.empty or movies_df.empty:
        raise HTTPException(status_code=500, detail="Los archivos de datos no están cargados correctamente")

    # Filtrar el DataFrame del crew para obtener las películas dirigidas por el director
    director_movies = crew_df[(crew_df['job_crew'] == 'Director') & (crew_df['name_crew'].str.contains(nombre_director, case=False, na=False))]

    if director_movies.empty:
        raise HTTPException(status_code=404, detail="El director no fue encontrado en el dataset")

    # Merge con el DataFrame de movies para obtener la información de cada película
    director_movies = director_movies.merge(movies_df, left_on='id', right_on='id', how='left')

    # Eliminar filas con valores NaN en las columnas relevantes
    director_movies = director_movies.dropna(subset=['title', 'budget', 'return'])

    # Calcular el retorno total
    retorno_total = director_movies['return'].sum()
    cantidad_peliculas = director_movies.shape[0]

    # Crear una lista con detalles de cada película
    movie_details = []
    for _, row in director_movies.iterrows():
        movie_details.append({
            "titulo": row['title'],
            "release_date": row['release_date'],
            "return": row['return'],
            "budget": row['budget'],
            "revenue": row['revenue']
        })

    return {
        "director": nombre_director,
        "cantidad_peliculas": cantidad_peliculas,
        "retorno_total": retorno_total,
        "peliculas": movie_details
    }
# Serializar la respuesta con json.dumps
    return json.loads(json.dumps(response, allow_nan=False))

# Sistema de REcomendacion
# Garantizamos que los títulos no tengan valores NaN y convertimos a minúsculas
movies_df['title'] = movies_df['title'].fillna('').str.lower()

# Crear la matriz TF-IDF a partir de los títulos de las películas
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies_df['title'])

# Calcular la similitud del coseno
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Construir un índice de mapeo de títulos a índices del DataFrame
indices = pd.Series(movies_df.index, index=movies_df['title']).drop_duplicates()

def recomendacion(titulo):
    # Verificar si el título está en el índice
    if titulo.lower() not in indices:
        return []

    # Obtener el índice de la película que coincide con el título
    idx = indices[titulo.lower()]

    # Obtener las puntuaciones de similitud de todas las películas con esa película
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Ordenar las películas por las puntuaciones de similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Obtener los índices de las 5 películas más similares (excluyendo la propia película)
    sim_scores = sim_scores[1:6]

    # Obtener los títulos de las películas más similares
    movie_indices = [i[0] for i in sim_scores]
    recommendations = movies_df['title'].iloc[movie_indices].tolist()

    return recommendations


# Decorador Funciòn de Recomendaciòn
@app.get("/recomendacion/{titulo}", tags=["Sistema de Recomendación"], description="Devuelve una lista de 5 películas recomendadas basadas en el título proporcionado.")
def get_recomendacion(titulo: str):
    return {"recomendaciones": recomendacion(titulo)}


# Decoradores de Verificacion para algunas funciones
@app.get("/meses_validos", tags=["Consultas auxiliares"], description="Devuelve una lista de meses válidos en español.")
def meses_validos():
    return {"meses_validos": list(meses_dict.keys())}

@app.get("/dias_validos", tags=["Consultas auxiliares"], description="Devuelve una lista de días válidos en español.")
def dias_validos():
    return {"dias_validos": list(dias_dict.keys())}

