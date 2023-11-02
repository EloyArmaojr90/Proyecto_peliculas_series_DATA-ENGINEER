from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd

router = APIRouter()

####### ***********################***************####### FASTAPI FUNCTIONS #######***********################*************** #######

def concat():
    df_concat = pd.read_csv("api_movie_tvshow.csv", sep = ",") 
    return df_concat

# Máxima duración según tipo de film (película/serie), por plataforma y por año
@router.get("/get_maxima_duracion/")
def get_maxima_duracion(min_o_season: str, año: int, plataforma: str):
    '''
    Máxima duración según tipo de film (película/serie), por plataforma y por año

    plataforma: Amazon premier, Disney plus, Hulu, Netflix
    año: 1920 - 2021
    min_o_season: min, season
    '''
    dic = {}                                                                                     # Creamos un diccionario
    plataforma = plataforma.capitalize()                                                         # Para colocar la primera letra del nombre de la plataforma en Mayúscula
    df_max_dur = concat()[(concat()["year"] == año) & (concat()["plataforma"] == plataforma)]         # Mascara con filtros de los paramentros
    k = df_max_dur[min_o_season].idxmax()                                                        # Tomamos el id del maximo valor de la columna "min" o "season"
    peli = concat().loc[k, "title"]                                                             # Tomamos el titulo de la pelicula en la "k-esima" posición
    dic["Película"] = peli

    return dic

# Cantidad de películas y series (separado) por plataforma
@router.get("/get_count_plataform/plataformas")
def get_count_plataform(plataforma: str):
    '''
    Cantidad de películas y series por plataforma

    plataforma: Amazon premier, Disney plus, Hulu, Netflix
    '''    
    plataforma = plataforma.capitalize()                                            # Para colocar la primera letra del nombre de la plataforma en Mayúscula
    df_count_plataform = concat()[concat()["plataforma"] == plataforma]                 # Mascara con filtros de los paramentros
    diccionario = df_count_plataform.groupby(["type"]).count()["show_id"].to_dict() # Agrupamos por la columna "type" contando los valores que estas se repiten y tomamos 
                                                                                    # la columna "Show_id" y lo convertimos en un diccionario   
        
    return diccionario

#Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo.
@router.get("/get_listedin/generos)")
async def get_listedin(genero: str):
    '''
    Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo.
    '''
    genero = genero.capitalize()                         # Para colocar la primera letra del nombre de la plataforma en Mayúscula
    dic = {}                                             # Creamos un diccionario vacio
    pmax = 0                                             # Creamos un contador
    list_plataformas = concat()["plataforma"].unique()     # Creamos una lista con los valores únicos de la columna "plataforma"
    for k in list_plataformas:
        p = 0                                                       # Creamos un contador 
        lista_index = concat()[concat()["plataforma"] == k].index # Creamos una mascara filtrando la columna "plataforma" y tomamos sus indices
        for j in lista_index:
            generos = concat().loc[j, "listed_in"].split(", ")     # Tomamos la cadena que esta en la posición "j-esima" de la columna "listed_in" y lo esplintiamos
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
@router.get("/get_actor/plataformas,años")
async def get_actor(plataforma: str, año: int):
    pmax = 0      # Creamos un contador
    dic = {}      # Creamos un diccionario vacio
    df_actor = pd.DataFrame(concat()[(concat()["year"] == año) & (concat()["plataforma"] == plataforma.capitalize())]["cast"]) # Creamos una mascara filtrando las columnas "year"
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
