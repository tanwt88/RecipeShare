from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import datetime

db=SQLAlchemy()

def get_uuid():
    return uuid4().hex
    

class User(db.Model):
    __tablename__ = "users"
    user=db.Column(db.String(32),primary_key=True,unique=True)
    id = db.Column(db.String(32),primary_key=True,unique=True, default =get_uuid)
    country=db.Column(db.String(20),primary_key=True)
    email = db.Column(db.String(345), unique=True)
    password =db.Column(db.Text, nullable =False)
    created_at=db.Column(db.DateTime,nullable=False, default=datetime.utcnow)

class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    photo_url = db.Column(db.String(200), unique=True)
    ingredients = db.Column(db.String(1000), nullable=False)
    directions = db.Column(db.String(1000), nullable=False)
    video_url = db.Column(db.String(200), unique=True)
    cooking_time = db.Column(db.Integer,nullable = False)
    prep_time = db.Column(db.Integer, nullable = False)
    calories = db.Column(db.Integer, nullable= False)
    user_id = db.Column(db.String(32), primary_key=True, default=get_uuid)
    ratings = db.Column(db.Float(2))
    favourite = db.Column(db.Boolean)
    created_at=db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    
class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.String(32),primary_key=True,unique=True, default =get_uuid)
    user_id = db.Column(db.String(32), primary_key=True)
    feedback = db.Column(db.String(1000), nullable=False)
    created_at=db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    
class Report(db.Model):
    __tablename__ = "report"
    id = db.Column(db.String(32),primary_key=True,unique=True, default =get_uuid)
    user_id = db.Column(db.String(32), primary_key=True, default=get_uuid)
    feedback = db.Column(db.String(1000), nullable=False)
    created_at=db.Column(db.DateTime,nullable=False, default=datetime.utcnow)