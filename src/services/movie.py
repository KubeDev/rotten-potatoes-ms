import requests
from models.movie import Movie
import os

class MovieService:

    def __init__(self):
        self.base_url = os.getenv("MOVIE_SERVICE_URI", "http://localhost:8181")

    def get_movies(self):
        response = requests.get(self.base_url + '/api/movie')
        data = response.json()
        resultado = []

        for obj in data:
            resultado.append(Movie(id=obj['_id'],
                                   title=obj['title'],
                                   summary=obj['summary'],
                                   duration=obj['duration'],
                                   release=obj['release'],
                                   category=obj['category'],
                                   cast=obj['cast'],
                                   director=obj['director'],
                                   slide=obj['slide'],
                                   thumb=obj['thumb']))

        return resultado

    def get_movies_by_id(self, objId):
        response = requests.get(self.base_url + '/api/movie/' + str(objId))
        data = response.json()

        return Movie(id=data['_id'],
                       title=data['title'],
                       summary=data['summary'],
                       duration=data['duration'],
                       release=data['release'],
                       category=data['category'],
                       cast=data['cast'],
                       director=data['director'],
                       slide=data['slide'],
                       thumb=data['thumb'])
