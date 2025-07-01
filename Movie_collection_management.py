import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict


app = FastAPI(
    docs_url="/swagger",
    redoc_url="/redoc",
    title="Movie Collection Management",
    version="0.0.2"
)


class Movie(BaseModel):
    id: int = Field(description="id фільму")
    title: str = Field(max_length=60, description="назва фільму")
    director: str = Field(max_length=30, description="режисер фільму")
    release_year: int = Field(description="рік випуску")
    rating: float = Field(ge=0, lt=10.1, description="оцінки")  # ge only for int

    # @field_validator("release_year") # не можна порівняти int і date.year
    # def real_year(cls, release_year):
    #     if release_year > date.year:
    #         raise ValueError("Рік випуску фільма не може бути майбутнім!")
    #     return {"message": "Все ок"}


movies: List[Movie] = [
    Movie(
        id=1,
        title="Гаррі Поттер і В'язень Азкабану",
        director="Альфонсо Куарон",
        release_year=2007,
        rating=9.1
    ),
    Movie(
        id=2,
        title="Хоббіт: Несподівана подорож",
        director="Пітер Джексон",
        release_year=2012,
        rating=8
    )
]


@app.get("/movies", response_model=List[Movie])
async def get_movies():
    return movies


@app.post("/add_movie", response_model=List[Movie])
async def add_movie(movie: Movie):
    movies.append(movie)
    return movies


@app.get("/get_movie/{id}", response_model=Movie)
async def get_movie_info(id: int):
    for movie in movies:
        if movie.id == id:
            return movie
        raise HTTPException(status_code=404,
                            detail="На жаль, такого фільму не існує.Ви можете додати його для подальшого використання.")


@app.delete("/delete_movie/{id}", response_model=List[Movie])
async def delete_movie(id: int):
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
            return movies
        raise HTTPException(status_code=404, detail="На жаль, такого фільму не існує, отже вам немає чого видаляти")


if __name__ == "__main__":
    uvicorn.run(app, port=8002)
