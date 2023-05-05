from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from flask_session import Session
from sqlalchemy.dialects.postgresql import *
from flask_sqlalchemy import SQLAlchemy

import psycopg2
from config import ApplicationConfig
from models import db, User, Recipe, Feedback, Report

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
server_Session = Session(app)
db.init_app(app)

with app.app_context():
    db.create_all()


@cross_origin
@app.route("/@me")
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorised"}), 401

    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "email": user.email
    })


@cross_origin
@app.route("/register", methods=["POST"])
def register_user():
    email = request.json["email"]
    password = request.json["password"]

    user_exists = User.query.filter_by(email=email).first() is not None

    if user_exists:
        return jsonify({"error": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "email": new_user.email
    })


@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401

    session["user_id"] = user.id

    return jsonify({
        "id": user.id,
        "email": user.email
    })

@app.route('/myrecipe/<int:recipe_id>', methods=['GET'])
def my_recipe(recipe_id):
    # Retrieve the recipe with the specified id that belongs to the logged in user
    recipe = Recipe.query.filter_by(id=recipe_id, user_id=current_user.id).first()

    if recipe is None:
        # If the recipe does not exist or does not belong to the user, return a 404 error
        return make_response(jsonify({'error': 'Recipe not found'}), 404)

    # Return a JSON representation of the recipe
    return jsonify({
        'id': recipe.id,
        'name': recipe.name,
        'photo_url': recipe.photo_url,
        'ingredients': recipe.ingredients,
        'directions': recipe.directions,
        'video_url': recipe.video_url,
        'cooking_time': recipe.cooking_time,
        'prep_time': recipe.prep_time,
        'calories': recipe.calories,
        'user_id': recipe.user_id,
        'ratings': recipe.ratings,
        'favourite': recipe.favourite,
        'created_at': recipe.created_at,
    })
    
    
    
@app.route('/recipes', methods=['POST'])
def create_recipe():
    recipe_data=request.get_json()
    user_id = recipe_data.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'error': f'user {user_id} not found'}), 404
    new_recipe=Recipe(
    name = recipe_data.get('name'),
    photo_url = recipe_data.get('photo_url'),
    ingredients = recipe_data.get('ingredients'),
    directions = recipe_data.get('directions'),
    video_url = recipe_data.get('video_url'),
    cooking_time = recipe_data.get('cooking_time'),
    prep_time = recipe_data.get('prep_time'),
    calories = recipe_data.get('calories'),
    user=user,
        ratings=recipe_data.get('ratings'),
        favourite=recipe_data.get('favourite')
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({'message': 'Recipe created successfully.'}), 201

@app.route("/logout", methods=["POST"])
def logout_user():
    session.pop("user_id")
    return "200"


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port =50100, debug=True, ssl_context=("cert.pem","key.pem"))
