import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,People,Planet


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




@app.route('/people', methods=['GET'])
def get_people():
    all_people= People.query.all() ## consulta model.py
    serialize_all_people = list(map(lambda people : people.serialize(),all_people)) #mapeo
    return jsonify(serialize_all_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):
    people = People.query.get(people_id)

    if not people:
        raise APIException('People not found', status_code=404)

    serialize_people = people.serialize()
    return jsonify(serialize_people), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planet.query.all()
    serialized_planets = list(map(lambda planet: planet.serialize(), all_planets))
    return jsonify(serialized_planets), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException('Planet not found', status_code=404)
    return jsonify(planet.serialize()), 200


@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    serialize_all_users = list(map(lambda user: user.serialize(), all_users))
    return jsonify(serialize_all_users), 200


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id')
    if user_id is None:
        return jsonify({'message': 'User ID is required as query parameter'}), 400

    user = User.query.get(user_id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404

    favorites = user.favorites
    serialize_favorites = list(map(lambda favorite: favorite.serialize(), favorites))
    return jsonify(serialize_favorites), 200


    # Add a new favorite planet to the current user with the planet id = planet_id.
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = 1 # replace with actual user id from session or token
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({'message': 'Planet not found'}), 404

    if planet in user.favorite_planets:
        return jsonify({'message': 'Planet already favorited'}), 409

    user.favorite_planets.append(planet)
    db.session.commit()

    return jsonify({'message': 'Planet favorited successfully'}), 201


# Add a new favorite people to the current user with the people id = people_id.
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = 1 # replace with actual user id from session or token
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    people = People.query.get(people_id)
    if not people:
        return jsonify({'message': 'People not found'}), 404

    if people in user.favorite_people:
        return jsonify({'message': 'People already favorited'}), 409

    user.favorite_people.append(people)
    db.session.commit()

    return jsonify({'message': 'People favorited successfully'}), 201


# Delete a favorite planet by id
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    # Check if planet exists in database
    planet = Planet.query.filter_by(id=planet_id).first()
    if not planet:
        raise APIException('Planet not found', status_code=404)
    
    # Get the current user
    user = get_current_user()
    if not user:
        raise APIException('Unauthorized', status_code=401)

    # Check if planet is already a favorite
    if planet in user.favorite_planets:
        user.favorite_planets.remove(planet)
        db.session.commit()

    return jsonify({'success': True}), 200

# Delete a favorite people by id
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    # Check if people exists in database
    people = People.query.filter_by(id=people_id).first()
    if not people:
        raise APIException('People not found', status_code=404)
    
    # Get the current user
    user = get_current_user()
    if not user:
        raise APIException('Unauthorized', status_code=401)

    # Check if people is already a favorite
    if people in user.favorite_people:
        user.favorite_people.remove(people)
        db.session.commit()

    return jsonify({'success': True}), 200



@app.route('/people', methods=['POST'])
def create_people():
    data = request.get_json()
    new_people = People(data['name'], data['birth_date'], data['description'], data['planet_id'], data['eye_color'], data['hair_color'])
    db.session.add(new_people)
    db.session.commit()
    all_people = People.query.all()
    serialize_all_people = list(map(lambda people: people.serialize(), all_people))
    return jsonify(serialize_all_people), 200











# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)