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
from models import db, User, Personajes, Planetas, Favoritos
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
    all_users = User.query.all()
    results = list(map(lambda usuario: usuario.serialize(), all_users))
   
    return jsonify(results), 200

@app.route('/personajes', methods=['GET'])
def get_personajes():
    all_personajes = Personajes.query.all()
    results = list(map(lambda personaje: personaje.serialize(), all_personajes))

    return jsonify(results), 200

@app.route('/personajes/<int:personaje_id>', methods=['GET'])
def get_personaje(personaje_id):
    personaje = Personajes.query.filter_by(id=personaje_id).first()

    return jsonify(personaje.serialize()), 200

@app.route('/planetas/<int:planeta_id>', methods=['GET'])
def get_planeta(planeta_id):
    planeta = Planetas.query.filter_by(id=planeta_id).first()

    return jsonify(planeta.serialize()), 200

@app.route('/planetas', methods=['GET'])
def get_planetas():
    all_planetas = Planetas.query.all()
    results = list(map(lambda planeta: planeta.serialize(), all_planetas))

    return jsonify(results), 200

@app.route('/favoritos/<int:favorito_id>', methods=['GET'])
def get_favorito(favorito_id):
    favorito = Favoritos.query.filter_by(id=favorito_id).first()

    return jsonify(favorito.serialize()), 200

@app.route('/favoritos', methods=['GET'])
def get_favoritos():
    all_favoritos = Favoritos.query.all()
    results = list(map(lambda favorito: favorito.serialize(), all_favoritos))

    return jsonify(results), 200

@app.route('/favoritos', methods=['POST'])
def add_favoritos():
    body = request.get_json()
    favorito = Favoritos(usuario= body['Usuario'], Personajes = body['Personajes'], Planetas = body['Planetas'])
    db.session.add(favorito)
    db.session.commit()
    response_body = {
       "msg" : "se creo favorito"
   }


    return jsonify(response_body), 200

@app.route('/favoritos/<int:favorito_id>', methods=['DELETE'])
def delete_favorito(favorito_id):
    favorito = Favoritos.query.filter_by(id=favorito_id).first()
    
    if favorito is None:
        return jsonify({"error": "Favorito no encontrado"}), 404
    
    favorito_data = favorito.serialize()  # Serializa antes de eliminar
    db.session.delete(favorito)
    db.session.commit()
    
    return jsonify(favorito_data), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
