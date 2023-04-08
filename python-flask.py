#----------------------------------------------------------
# Flask application and initialize the database connection:
#----------------------------------------------------------

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#------------------------
# Creating Database Model
#------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)

#---------------------
# Create a User - POST
#---------------------
@app.route('/users', methods=['POST'])
def create_user():
    name = request.json['name']
    email = request.json['email']
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email})
  
#------------------------------
# Get a List of the Users - GET
#------------------------------
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append({'id': user.id, 'name': user.name, 'email': user.email})
    return jsonify(result)

#-----------------------
# Get a User by ID - GET
#-----------------------
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email})

#--------------------------
# Update a User by ID - PUT
#--------------------------
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    name = request.json.get('name', user.name)
    email = request.json.get('email', user.email)
    user.name = name
    user.email = email
    db.session.commit()
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email})
