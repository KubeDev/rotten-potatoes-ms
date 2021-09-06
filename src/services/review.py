import json
import requests
from models.review import Review, ReviewEncoder
import os
class ReviewService:

    def __init__(self):
        self.base_url = os.getenv("REVIEW_SERVICE_URI", "http://localhost:8282")

    def get_reviews(self, idObj):
        response = requests.get(self.base_url + '/api/review/' + idObj)
        data = response.json()
        resultado = []

        for obj in data:
            resultado.append(Review(reviewed=obj['reviewed'],
                                   reviewer=obj['reviewer'],
                                   description=obj['description']))

        return resultado

    def add_review(self, review):
        headers = {'Content-type': 'application/json'}
        response = requests.post(self.base_url + '/api/review', data=json.dumps(review, cls=ReviewEncoder), headers=headers)
