from flask import Blueprint, request, jsonify
from app.status_code import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED
from app.models.user import User
import validators
from app.extension import db, bcrypt

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

#User Registration
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
    
    
    