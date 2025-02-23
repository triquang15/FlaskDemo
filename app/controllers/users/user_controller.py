from flask import Blueprint, request, jsonify
from app.status_code import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_401_UNAUTHORIZED,HTTP_201_CREATED, HTTP_200_OK
from app.models.user import User
from app.extension import db, bcrypt
from flask_jwt_extended import (
   jwt_required
)

users = Blueprint('users', __name__, url_prefix='/api/v1/users')

# 1.Get all users
@users.route('/all', methods=['GET'])
@jwt_required()
def getAllUsers():
    try:
        users = User.query.all()
        total_users = len(users)  
        return jsonify({
            'total_users': total_users,  
            'users': [user.to_dict() for user in users]
        }), HTTP_200_OK
    except Exception as e:
        return jsonify({'message': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
# 2.Get All Authors
@users.route('authors', methods=['GET'])
@jwt_required()
def getAllAuthors():
    try:
        all_authors = User.query.filter_by(user_type='author').all()
        total_authors = len(all_authors) 
        
        return jsonify({
            'total_authors': total_authors,
            'authors': [author.to_dict_with_relationships() for author in all_authors]
        }), HTTP_200_OK
    except Exception as e:
        return jsonify({'message': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

