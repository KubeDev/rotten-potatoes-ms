from flask import Flask, render_template, request, url_for, redirect, Response, jsonify
import os

from flask.helpers import send_file 
from models.review import Review
from models.movie import Movie
from middleware import set_unhealth, set_unready_for_seconds, middleware
import logging
from services.movie import MovieService
from services.review import ReviewService
import requests

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

app.wsgi_app = middleware(app.wsgi_app)

@app.route('/')
def index():

    service = MovieService()
    filmes = service.get_movies()
    app.logger.info('Obtendo a lista de filmes no MongoDB')
    sliders = filmes[-3:]
    return render_template('index.html', filmes=filmes, sliders=sliders)

@app.route('/single/<string:oid>', methods=['GET','POST'])
def single(oid):

    service = ReviewService()
    movieService = MovieService()
    filme = movieService.get_movies_by_id(oid)
    reviews = service.get_reviews(filme.id);

    if request.method == 'GET':
        app.logger.info('Entrando na pagina de review do filme %s', filme.title)
        return render_template('single.html', filme=filme, reviews=reviews)
    else:
        app.logger.info('Efetuando cadastro de review no filme %s', filme.title)
        nome = request.form['nome']
        review = request.form['review']
        o_review = Review(reviewer=nome, reviewed=oid, description=review)
        service.add_review(o_review)

        return redirect(url_for('single', oid=oid))

@app.route('/host')
def host():
    return jsonify({"host": os.uname().nodename})

# @app.route('/stress/<int:seconds>')
# def stress(seconds):
#     pystress(seconds, 1)
#     return Response('OK')

@app.route('/unreadyfor/<int:seconds>', methods=['PUT'])
def unready_for(seconds):
    set_unready_for_seconds(seconds)
    return Response('OK')

@app.route('/health', methods=['GET'])
def heath():
    return Response('OK')

@app.route('/unhealth', methods=['PUT'])
def unhealth():
    set_unhealth()
    return Response('OK')
    
@app.route('/ready', methods=['GET'])
def ready():
    return Response('OK')

if __name__ == '__main__':
    app.run()
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

@app.route('/img/<path:path>')
def send_js(path):
    return send_file('static/' + str(path))