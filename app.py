#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *
from auth import AuthError, requires_auth

#----------------------------------------------------------------------------#
# App Config
#----------------------------------------------------------------------------#

def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)
    setup_db(app)  
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers 
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response



  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ endpoints ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


    @app.route('/', methods=['GET'])
    def home():
        
        return jsonify({
            'success': True,
            'Wellcome': "Wellcome",
        })

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def retrive_actors(payload):

        all_actors = Actor.query.order_by(Actor.id).all()

        formatted_actors = [Actor.format() for Actor in all_actors]

        if len(formatted_actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'Actors': formatted_actors,
            'total_Actors': len(formatted_actors),
        })

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    @app.route('/actors' , methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):

        body = request.get_json()

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        actor = Actor(name=new_name ,age=new_age , gender=new_gender)
        actor.insert()

        all_actors = Actor.query.order_by(Actor.id).all()
        formatted_actors = [Actor.format() for Actor in all_actors]

        return jsonify({
            'success': True,
        })

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    @app.route('/actors/<int:actor_id>' , methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actor(payload, actor_id):

        actor = Actor.query.get(actor_id)

        if actor is None:
            abort(404)

        body = request.get_json()

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        if new_name is not None:
            actor.name = new_name

        if new_age is not None:
            actor.age = new_age
            
        if new_gender is not None:
            actor.gender = new_gender

        actor.update()

        return jsonify({
            'success': True,
        })
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):

        actor = Actor.query.get(actor_id)

        if actor is None:
            abort(404)

        actor.delete()

        return jsonify({
            'success': True,
        })

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def retrive_movies(payload):

        all_movies = Movie.query.order_by(Movie.id).all()

        formatted_movies = [Movie.format() for Movie in all_movies]

        if len(formatted_movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'Movies': formatted_movies,
            'total_Movies': len(formatted_movies),
        })

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):

        body = request.get_json()

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        movie = Movie(title=new_title ,release_date=new_release_date)
        movie.insert()

        all_movies = Movie.query.order_by(Movie.id).all()
        formatted_movies = [Movie.format() for Movie in all_movies]
        
        return jsonify({
            'success': True,
        })

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    @app.route('/movies/<int:movie_id>' , methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movie(payload, movie_id):

        movie = Movie.query.get(movie_id)

        if movie is None:
            abort(404)

        body = request.get_json()

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        if new_title is not None:
            movie.title = new_title

        if new_release_date is not None:
            movie.release_date = new_release_date
            
        movie.update()

        return jsonify({
            'success': True,
        })

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):

        movie = Movie.query.get(movie_id)

        if movie is None:
            abort(404)

        movie.delete()

        return jsonify({
            'success': True,
        })



  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Error Handlers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error',
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response


    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(debug=True)