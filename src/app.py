"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/users/', methods=['POST'])
def create_user():
    request_body = request.get_json()
    user = User(username=request_body["username"], password=request_body["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 200

@app.route('/users/<int:id>', methods=['GET'])
def get_single_user(id):
    user = User.query.get(id)
    return jsonify(user.serialize()), 200

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(user.serialize(),'deleted'), 200




@app.route('/planets/<int:id>', methods=['GET'])
def get_single_planet(id):
    planet = Planet.query.get(id)
    return jsonify(planet.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planets', methods=['POST'])
def create_planet():
    request_body = request.get_json()
    planet = Planet(name=request_body["name"], climate=request_body["climate"], terrain=request_body["terrain"], population=request_body["population"])
    db.session.add(planet)
    db.session.commit()
    return jsonify(planet.serialize()), 200

@app.route('/planets/<int:id>', methods=['DELETE'])
def delete_planet(id):
    planet = Planet.query.get(id)
    db.session.delete(planet)
    db.session.commit()
    return jsonify(planet.serialize(),'deleted'), 200

# Character Routes
@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    return jsonify([character.serialize() for character in characters]), 200

@app.route('/characters', methods=['POST'])
def create_character():
    request_body = request.get_json()
    character =  Character(name=request_body["name"], height=request_body['height'], hair_color=request_body['hair_color'], eye_color=request_body['eye_color'], gender=request_body['gender'])
    db.session.add(character)
    db.session.commit()
    return jsonify(character.serialize()), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_single_character(character_id):
    character = Character.query.get(character_id)
    return jsonify(character.serialize()), 200

@app.route('/character/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Character.query.get(character_id)
    db.session.delete(character)
    db.session.commit()
    return jsonify(character.serialize(),'deleted'), 200

# Favorite Routes
@app.route('/favorites', methods=['GET'])
def get_favorites():
    favorites = Favorite.query.all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200

@app.route('/favorite', methods=['POST'])
def create_favorite():
    request_body = request.get_json()
    favorite = Favorite(user_id=request_body["user_id"], planet_id=request_body["planet_id"], character_id=request_body["character_id"])
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 200

@app.route('/favorite/<int:favorite_id>', methods=['GET'])
def get_single_favorite(favorite_id):
    favorite = Favorite.query.get(favorite_id)
    return jsonify(favorite.serialize()), 200

@app.route('/favorite/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    favorite = Favorite.query.get(favorite_id)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify(favorite.serialize(),'deleted'), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
