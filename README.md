# <h1 align=center> **PROYECTO INDIVIDUAL** </h1>

# <h1 align=center>**`DATA ENGINEER A UN DATASET DE PELÍCULAS`**</h1>


## **Introducción**

Dentro de este redme encontraras detalles acerca de un proyecto de DATA ENGINEER a un dataset de películas de las plataformas “Amazon premier”, “Disney plus”, “Hulu” y “Netflix. Este proyecto fue realizado por ELOY ARMAO estudiante de la carrera de DATA SCIENCE en la academia HENRY.  Para más informacion visitar la pagina https://www.soyhenry.com/carrera-data-science

`Application Programming Interface` es una interfaz que permite que dos aplicaciones se comuniquen entre sí, independientemente de la infraestructura subyacente. Son herramientas muy versátiles y fundamentales para la creación de, por ejemplo, pipelines, ya que permiten mover y brindar acceso simple a los datos que se quieran disponibilizar a través de los diferentes endpoints, o puntos de salida de la API.

Hoy en día contamos con **FastAPI**, un web framework moderno y de alto rendimiento para construir APIs con Python.

Esta herramienta es muy útil para la extracción de información, pero la gran mayoría no están disponibles de forma gratuita, por ello existen otro tipo de herramientas, como son las librerias **bs4** o **selenium**, ayudan al data scientics a buscar la información que requiere haciendo raspado de paginas web.

`BeautifulSoup` es una biblioteca de Python para analizar documentos HTML. Esta biblioteca crea un árbol con todos los elementos del documento y puede ser utilizado para extraer información, llamado web scraping.

En el siguiente proyecto se utilizo la librería bs4 con BeautifullSoup para rellenar algunos valores nulos  de un dataframe, que se origina al concatenar  un conjunto de dataframes.


## **Propuesta de trabajo**

El proyecto consiste en realizar una ingesta de datos desde diversas fuentes, posteriormente aplicar las transformaciones que consideren pertinentes, y luego disponibilizar los datos limpios para su consulta a través de una API. Esta API deberán construirla en un entorno virtual dockerizado.

Los datos serán provistos en archivos de diferentes extensiones, como *csv* o *json*. Se espera que realicen un EDA para cada dataset y corrijan los tipos de datos, valores nulos y duplicados, entre otras tareas. Posteriormente, tendrán que relacionar los datasets así pueden acceder a su información por medio de consultas a la API.

Las consultas a realizar son:

+ Máxima duración según tipo de film (película/serie), por plataforma y por año:
	El request debe ser: get_max_duration(año, plataforma, [min o season])

+ Cantidad de películas y series (separado) por plataforma
	El request debe ser: get_count_plataform(plataforma) 

+ Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo.
	El request debe ser: get_listedin('genero') 

Como ejemplo de género pueden usar 'comedy', el cuál deberia devolverles un cunt de 2099 para la plataforma de amazon.

+ Actor que más se repite según plataforma y año.
	El request debe ser: get_actor(plataforma, año)

## **Conceptos de interés**

- **`Docker`** es una solución completa para la producción, distribución y uso de containers. 
&nbsp;- **`Container`** es una abstracción de la capa de software que permite *empaquetar* código, con librerías y dependencias en un entorno parcialmente aislado. 
&nbsp;- **`Image`** es un ejecutable Docker que tiene todo lo necesario para correr aplicaciones, lo que incluye un archivo de configuración, variables -de entorno y runtime- y librerías. 
&nbsp;- **`Dockerfile`** archivo de texto con instrucciones para construir una imagen. Puede considerarse la automatización de creación de imágenes. 
- **`Deployment`** es el conjunto de actividades, infraestructura y recursos que posibilitan el uso de software. En este caso, la plataforma Mogenius les permitirá *montar* su imagen de Docker con la API en sus servidores para acceder a ella a través de internet.

## **Recursos y links provistos**

Imagen Docker con Uvicorn/Guinicorn para aplicaciones web de alta performance:

+ https://hub.docker.com/r/tiangolo/uvicorn-gunicorn-fastapi/ 

+ https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker

	FAST API Documentation:

+ https://fastapi.tiangolo.com/tutorial/

# **Como se realizo el proyecto**

**`Parte 1). Importación de librerías. Ingesta de cada dataset, creación de una nueva columna y concatenación.`**:

Se realizó la importación de las librerías necesarias para este proyecto como:

+ `pandas` para trabajar con dataframes 

+ `numpy` para trabajar de manera más eficiente con operaciones matemáticas 

+ `time` para trabajar con tiempo de espera

+ `bs4` para trabajar con beautifullsoup en el web scraping 

+ `request` para trabajar haciendo una petición a una página web

+ `re` para trabajar expresiones regulares

+ `random` para trabajar con secuencias pseudoaleatorias.

Se extrajo cada uno de los dataset suministrados, se transformaron en dataframes y se creó vistas de cada uno. Luego adicionamos una columna llamada "plataforma" en cada uno de estos, con valores "Amazon premier", "Disney plus", "Hulu", "Netflix" respectivamente y por último se realizó una concatenación de de los cuatro dataframes.

**`Parte 2). Limpieza del dataframe concatenado`**:

Se realizaron las consultas necesarias para determinar que tipo de datos están presentes en cada columna de nuestro dataframe y que no hubiesen filas duplicadas. Se extrajo la información de cuantas valores nulos tenia cada columna y se procedió hacer un análisis de esta información, determinando que seria más factible empezar realizando consultas sobre las columnas que poseían pocos valores nulos y que fuesen relevantes para hacer las consultas sobre nuestra API. Cada valor nulo se relleno con la cadena “Sin Dato”. Se

 
**`Parte 3). Scraping a los mismos datos y web scraping. Nota importante, esto lo haremos ya que no contamos con una API ofifical para corroborar los datos sumnistrados`**

El objetivo del scraping y web scraping es tratar de rellenar la mayor cantidad de valores nulo en nuestro dataframe.

Se dividió el dataframe en dos, creando así dataframes uno para películas y otro para tv show, respectivamente.

+ Primero se realizó un scraping a nuestro mismo dataframe.

	Se realizo la búsqueda de aquellos títulos de películas donde hubiesen la mayor cantidad de valores “Sin Dato” la cual fue la columna “cast” y se listo en variables que corresponden si es del tipo película o tv show.

	Algo de esperar. Una de las curiosidades, que llevo hacer el scraping fue plantearse si la columna “title” tenia valores duplicados, lo cual era cierto. Cada fila contiene información pertinente de cada tv show o película que se encuentra en la distintas plataformas antes mencionadas, pero en algunos casos comparten alguna misma información, esto es, que pueden tener: el mismos director (columna “director”), los mismos actores (columna “cast”), el mismos año de estreno (columna “release_year”, no confundir con el año de adición a la plataforma) y los misma duración (columna “duration”). 

	El criterio que se tomo para rellenar los valores “Sin Dato” fue el siguiente:

	Podemos decir que dos o más filas que contienen el mismo título de películas son iguales, si los valores de la columna "director" o columna "cast" o columna "release_year" o columna "duration".

	El criterio mencionado anterior se dedujo de lo siguiente: 

	Dos o más películas y tv show no pueden ser distintas y llevar mismo título en un mismo año o tener el mismo título  y el mismo director(es) y ser distintas a lo cual esto también ocurre con los actores, o tener el mimo titulo y la misma duración.  Ejemplo

	`The Avengers`
	La película de 1998 es una adaptación de una serie de tv británica sobre un par de agentes de inteligencia que deben unirse para detener a un científico loco. El film de 2012 es una adaptación de un cómic sobre un grupo de héroes que deben unir fuerzas para evitar que el mundo sea conquistado por una raza extra dimensional. Tomado de https://www.univision.com/entretenimiento/cine-y-series/20-pares-de-peliculas-con-el-mismo-titulo-que-no-tienen-ninguna-vinculacion-entre-si. 
	
	Otros ejemplos están dentro del archivo lis_para_proyectarlo.ipynb de esta misma parte.

+ Web Scrapin

	Se hizo web scraping a 2 paginas web, https://www.justwatch.com/ y https://www.rottentomatoes.com/ que son del tipo de base de datos de películas y tv show.
	
	Se realizo la búsqueda de aquellos títulos de películas donde hubiesen la mayor cantidad de valores “Sin Dato” la cual fue la columna “cast” y se listo en variables que corresponden si es del tipo película o tv show.

	Se creo la función de búsqueda, la cual varia para cada tipo pagina web y cada tipo de dataframe ya sea películas o tv show. Se trabajo con las librerías request y bs4. Se hizo una petición a una página en específico con la funcion request y si esta nos da como codigo 200 empezamos a utilizar la clase Beautifulsoup para para pasear el html y poder realizar la operaciones, para obtener la información que precisamos. 

	La información obtenida de cada búsqueda en bruto se guardo en archivos de tipo csv. Se realizo la limpieza de cada busqueda para luego ser cruzada con el dataframe original.

	Los criterios que se tomaron para cruzar la data se asemejan mucho al criterio que se tomo durante el scraping.

**`Parte 4). Normalizar el dataframe "df_concat"`**

+ Se crearon dos columnas llamadas “min” y “season” cada una con valores que tenia la columnas “duration” y se procedió a eliminar esta.

+ Se crearon nuevas claves en la columna “show_id”.

+ Guardamos nuestro dataframe en un archivo csv.

