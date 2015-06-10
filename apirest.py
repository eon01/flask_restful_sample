#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
from flask import Flask, jsonify, abort, make_response, request
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
#Authentification
auth = HTTPBasicAuth()


genres = [
    {
        'id': 1,
        'name': u'Trash Metal',
        'bands': u'Metallica, Megadeth'
    },
    {
        'id': 2,
        'name': u'Death Metal',
        'bands': u'Dark Tranquility, Inflames'
    }
]

#Getting password
@auth.get_password
def get_password(username):
    if username == 'user':
        return 'rE_23KhAE°0@POI4%'
    return None

#Get genres
@app.route('/todo/api/v1.0/genres', methods=['GET'])
def get_genres():
    return jsonify({'genres': genres})

#Get genre by id
@app.route('/todo/api/v1.0/genres/<int:genre_id>', methods=['GET'])
def get_genre(genre_id):
    genre = [genre for genre in genres if genre['id'] == genre_id]
    if len(genre) == 0:
            abort(404)
    return jsonify({'genre': genre[0]})

#Create a genre
#Eample: curl -i -H "Content-Type: application/json" -X POST -d '{"name":"Headbanging"}' http://localhost:5000/todo/api/v1.0/genres
@auth.login_required
@app.route('/todo/api/v1.0/genres', methods=['POST'])
def create_genre():
    if not request.json or not 'name' in request.json:
        abort(400)
    genre = {
        'id': genres[-1]['id'] + 1,
        'name': request.json['name'],
        'bands': request.json.get('bands', "")
    }
    genres.append(genre)
    return jsonify({'genre': genre}), 201

#404 not found 
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}), 404)

#401 unauthorized access
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)














