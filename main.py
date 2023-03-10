from fastapi import FastAPI
import pandas as pd

app = FastAPI(title = "Proyecto Individual - BeautifulSoup - FastApi - Docker"
            ,description= '''Esta API permite hacer consultas como: máxima duración según tipo de film (película/serie), por plataforma y por año, cantidad de 
                             películas y series (separado) por plataforma, cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo,
                             actor que más se repite según plataforma y año. Sobre un dataset de películas de plataformas Amozon premier, Disney plus, Hulu, Netflix''',
            contact= {"name": "Eloy Armao", "email": "eloyjr.armao27@gmasil.com", "linkedin": ""})

# Leemos el archivo y lo tranformamos en un dataframe
@app.on_event("startup")
def startup():
    global df_concat
    df_concat = pd.read_csv("api_movie_tvshow.csv", sep = ",")

# Máxima duración según tipo de film (película/serie), por plataforma y por año
@app.get("/get_maxima_duracion/({minutos_o_seasons},{años},{plataformas})")
async def get_maxima_duracion(min_o_season: str, año: int, plataforma: str):
    dic = {}                                                                                     # Creamos un diccionario
    plataforma = plataforma.capitalize()                                                         # Para colocar la primera letra del nombre de la plataforma en Mayúscula
    df_max_dur = df_concat[(df_concat["year"] == año) & (df_concat["plataforma"] == plataforma)] # Mascara con filtros de los paramentros
    k = df_max_dur[min_o_season].idxmax()                                                        # Tomamos el id del maximo valor de la columna "min" o "season"
    peli = df_concat.loc[k, "title"]                                                             # Tomamos el titulo de la pelicula en la "k-esima" posición
    dic["Película"] = peli                                                                       # Agregamos al diccionario
        
    return dic
        
    

# Cantidad de películas y series (separado) por plataforma
@app.get("/get_count_plataform/({plataformas})")
async def get_count_plataform(plataforma: str):
        
    plataforma = plataforma.capitalize()                                            # Para colocar la primera letra del nombre de la plataforma en Mayúscula
    df_count_plataform = df_concat[df_concat["plataforma"] == plataforma]           # Mascara con filtros de los paramentros
    diccionario = df_count_plataform.groupby(["type"]).count()["show_id"].to_dict() # Agrupamos por la columna "type" contando los valores que estas se repiten y tomamos 
                                                                                    # la columna "Show_id" y lo convertimos en un diccionario   
        
    return diccionario 

#Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo.
@app.get("/get_listedin/({generos})")
async def get_listedin(genero: str):
    genero = genero.capitalize()                         # Para colocar la primera letra del nombre de la plataforma en Mayúscula
    dic = {}                                             # Creamos un diccionario vacio
    pmax = 0                                             # Creamos un contador
    list_plataformas = df_concat["plataforma"].unique()  # Creamos una lista con los valores únicos de la columna "plataforma"
    for k in list_plataformas:
        p = 0                                                       # Creamos un contador 
        lista_index = df_concat[df_concat["plataforma"] == k].index # Creamos una mascara filtrando la columna "plataforma" y tomamos sus indices
        for j in lista_index:
            generos = df_concat.loc[j, "listed_in"].split(", ")     # Tomamos la cadena que esta en la posición "j-esima" de la columna "listed_in" y lo esplintiamos
            if genero in generos:
                p += 1 
            
        if p > pmax:                                   # Aca tomamos el máximo de repeticiones del parametro género para cada una de las plataformas       
            pmax = p
            plataforma = k                               
        
        elif p == pmax:                                # Aca tomamos si el máximo de repeticiones del parametro género que coinciden en al menos dos plataformas 
            plataforma += ", " + k
        else:
            pass
    
    dic[plataforma] = pmax                             # Agregamos al dicionario
    return  dic 

#Actor que más se repite según plataforma y año.
@app.get("/get_actor/({plataformas},{años})")
async def get_actor(plataforma: str, año: int):
    pmax = 0      # Creamos un contador
    dic = {}      # Creamos un diccionario vacio
    df_actor = pd.DataFrame(df_concat[(df_concat["year"] == año) & (df_concat["plataforma"] == plataforma.capitalize())]["cast"]) # Creamos una mascara filtrando las columnas "year"
                                                                                # y "plataforma" con los parametros dados, y obtenemos la columna "cast" y la convertimos en un dataframe     
    
    df_actor = df_actor[df_actor["cast"] != "Sin Dato"]                         # Creamos una mascara filtrando la columna "cast" del dataframe anterior
    lista_index = df_actor.index                                                # Creamos una lista con los valores de indexación de la mascara
    for k in lista_index:
                   
        lista_actores = df_actor.loc[k ,"cast"].split(", ")    # Tomamos la cadena de la columna "cast" en la posición "k-esima" y la esplintiamos
        df_actor.drop([k], axis=0, inplace=True)               # Eliminamos la fila "k-esima" del dataframe "df_actor"
        lista_index2 = df_actor.index                          # Creamos una lista de los indices que quedan del dataframe al aplicar el paso anterior
                
        for actor in lista_actores:
            p = 1                        # Creamos un contador
                    
            for j in lista_index2:                                    # Recorremos la lista que hicimos en el paso anterior
                lista_actores2 = df_actor.loc[j ,"cast"].split(", ")  # Esplintiamos la cadena "j-esima" de la columna "cast" 
                    
                if actor in lista_actores2:                           
                    lista_actores2.remove(actor)                        # Removemos el actor si se encuentra en la lista que se creo en el paso anterior
                    df_actor.loc[j ,"cast"] = ", ".join(lista_actores2) # Convertimos la lista que obtenemos al remover el actor, en una cadena y la guardamos en la misma posición "j-esima" 
                    p += 1

            if p > pmax:                                # Aca tomamos el máximo de repeticiones del actor
                pmax = p
                actor_max = actor
                    
            elif p == pmax:
                actor_max += ", " + actor               # Aca tomamos los máximos de repeticiones de al menos dos actores
                    
            else:
                pass
        
    dic[actor_max] = pmax                                  # Agregamos al diccionario 
        
    return dic 