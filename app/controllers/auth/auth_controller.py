from flask import Blueprint, request, jsonify
from app.status_code import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_401_UNAUTHORIZED,HTTP_201_CREATED, HTTP_200_OK
from app.models.user import User
import validators
from app.extension import db, bcrypt
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_identity
)

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

# 1.User Registration
@auth.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact = data.get('contact')
    email = data.get('email')
    type = data.get('type')
    password = data.get('password')
    biography = data.get('biography', '') if type == 'author' else ''
    
    if not first_name or not last_name or not contact or not email or not password:
        return jsonify({'message': 'All fields are required'}), HTTP_400_BAD_REQUEST
    
    if type == 'author'and not biography:
        return jsonify({'message': 'Biography is required for authors'}), HTTP_400_BAD_REQUEST
    
    if len(password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters long'}), HTTP_400_BAD_REQUEST
    
    if not validators.email(email):
        return jsonify({'message': 'Invalid email'}), HTTP_400_BAD_REQUEST
    
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'message': 'Email already exists'}), HTTP_409_CONFLICT
    
    if User.query.filter_by(contact=contact).first() is not None:
        return jsonify({'message': 'Contact already exists'}), HTTP_409_CONFLICT
    
    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(first_name, last_name, email, contact, hashed_password, biography, type)
        db.session.add(new_user)
        db.session.commit()
        
        # Convert User object to dictionary
        user_data = {
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
            "contact": new_user.contact,
            "type": new_user.user_type,
            "biography": new_user.biography,
            "created_at": new_user.created_at
        }
        
        return jsonify({
            'message': f'{new_user.get_full_name()} has been successfully registered',
            'user': user_data
        }), HTTP_201_CREATED
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
    finally:
        db.session.close()
        return jsonify({'message': 'User registration failed'}), HTTP_500_INTERNAL_SERVER_ERROR

# 2.User Login
@auth.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
        
    try:
        if not email or not password:
            return jsonify({'message': 'All fields are required'}), HTTP_400_BAD_REQUEST
        user = User.query.filter_by(email=email).first()
        if user:
            check_password = bcrypt.check_password_hash(user.password, password)
            if check_password:
                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=str(user.id))
                return jsonify({
                    'message': f'Welcome back {user.get_full_name()}',
                    'access_token': access_token,   
                    'refresh_token': refresh_token,
                    'user': {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "contact": user.contact,
                        "type": user.user_type,
                        "biography": user.biography,
                        "created_at": user.created_at,  
                    }
                }), HTTP_200_OK
            else:
                return jsonify({'message': 'Invalid email or password'}), HTTP_400_BAD_REQUEST
        else:
            return jsonify({'message': 'User does not exist'}), HTTP_401_UNAUTHORIZED
    except Exception as e:
        return jsonify({'message': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR 
    
# 3.Refresh Token
@auth.route('/token/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    try:
        identity = get_jwt_identity()

        # Ensure identity is a string
        if not isinstance(identity, str):
            return jsonify({'message': 'Identity must be a string'}), HTTP_400_BAD_REQUEST

        access_token = create_access_token(identity=identity)  
        return jsonify({'access_token': access_token}), HTTP_200_OK

    except Exception as e:
        return jsonify({'message': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
