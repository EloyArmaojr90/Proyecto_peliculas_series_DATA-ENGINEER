from fastapi import FastAPI
from routes import routes

app = FastAPI(title = "Proyecto Individual - BeautifulSoup - FastApi - Docker"
            ,description= '''Esta API permite hacer consultas como: máxima duración según tipo de film (película/serie), por plataforma y por año, cantidad de 
                             películas y series (separado) por plataforma, cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo,
                             actor que más se repite según plataforma y año. Sobre un dataset de películas de plataformas Amozon premier, Disney plus, Hulu, Netflix''',
            docs_url='/')

app.include_router(routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
