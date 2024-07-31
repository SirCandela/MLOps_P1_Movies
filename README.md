# 🎬 Proyecto Recomendador de Películas 🎥
Descripción General
Este proyecto tiene como objetivo desarrollar una API para un sistema de recomendación de películas utilizando datos de películas, actores y equipos de producción. El proyecto incluye procesos de ETL (Extracción, Transformación y Carga), Análisis Exploratorio de Datos (EDA), implementación de funciones específicas y la creación de un algoritmo de recomendación de películas.
_______________________________________________________________________________________________________________________________________________________
# 📚 Tabla de Contenidos
ETL (Extracción, Transformación y Carga)
EDA (Análisis Exploratorio de Datos)
Funciones Implementadas
Algoritmo de Recomendación
Conclusiones
_______________________________________________________________________________________________________________________________________________________
# 🔄 ETL
🛠️ Extracción
La extracción de datos se realizó a partir de un conjunto de archivos CSV que contienen información sobre películas, actores y el equipo de producción. Los datos incluyen detalles como el presupuesto de la película, el retorno de inversión, los géneros, el equipo de producción, entre otros.

🧹 Transformación
Limpieza de Datos:

Se eliminaron filas con valores nulos en campos críticos como title, budget, return, etc.
Se convirtieron tipos de datos para asegurar la coherencia; por ejemplo, budget y return fueron convertidos a numéricos.
Reducción de Tamaño:

Se seleccionó una muestra representativa del 10% de los datos para cada DataFrame (cast_df, movies_df, crew_df) para reducir el tamaño y facilitar el procesamiento.
💾 Carga
Los datos transformados y limpios fueron guardados en nuevos archivos CSV, listos para ser utilizados en la API y análisis posteriores.

_______________________________________________________________________________________________________________________________________________________
# 📊 EDA (Análisis Exploratorio de Datos)
Se realizaron varios análisis exploratorios para entender mejor los datos:

Distribución del Presupuesto y Retorno:

Se generaron histogramas para visualizar la distribución del presupuesto y el retorno de las películas.
Nube de Palabras:

Se creó una nube de palabras para visualizar las palabras más frecuentes en los títulos de las películas. Esto ayuda a identificar tendencias y patrones en los nombres de las películas.
Tendencias por Año:

Se analizó cómo el retorno de inversión ha variado a lo largo de los años, identificando posibles tendencias en la industria cinematográfica.
🔧 Funciones Implementadas
📚 Funciones de API
meses_validos():

Devuelve una lista de meses válidos en español.
recomendacion(titulo: str):

Recibe el nombre de una película y devuelve una lista con las cinco películas más similares, basándose en el contenido de los títulos y otros atributos relevantes.

_______________________________________________________________________________________________________________________________________________________
# 🎯 Función de Recomendación
Esta función utiliza el TF-IDF Vectorizer para convertir los títulos de las películas en vectores numéricos. Luego, calcula la similitud de coseno entre los vectores para encontrar las películas más similares al título ingresado. Devuelve una lista de cinco películas recomendadas.

💡 Algoritmo de Recomendación
El algoritmo de recomendación se basa en la similitud de contenido, específicamente utilizando la técnica de TF-IDF (Term Frequency-Inverse Document Frequency).

Vectorización de Títulos:

Se vectorizan los títulos de las películas para representar cada palabra como un número, lo que permite calcular similitudes.
Cálculo de Similitud:

Se utiliza la similitud de coseno para medir la semejanza entre la película consultada y todas las demás películas en la base de datos.
Generación de Recomendaciones:

Se ordenan las películas según la similitud calculada y se devuelven las cinco más similares.

_______________________________________________________________________________________________________________________________________________________
# 📝 Conclusiones
Este proyecto demuestra la eficacia de los sistemas de recomendación basados en contenido para sugerir películas a los usuarios. A través de un proceso riguroso de ETL y EDA, se prepararon y analizaron los datos, permitiendo la implementación de un modelo de recomendación preciso y eficiente. Las herramientas y técnicas utilizadas, como la vectorización de texto y el cálculo de similitud de coseno, proporcionaron una base sólida para desarrollar un sistema que puede adaptarse y mejorar con más datos y funcionalidades adicionales en el futuro.

Este README proporciona una visión detallada del proceso y las funcionalidades del proyecto, ofreciendo una guía clara para futuros desarrolladores o usuarios interesados en el sistema de recomendación de películas.







