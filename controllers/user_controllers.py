from flask import Blueprint, request, jsonify
from models import User
from extensions import db 
from sqlalchemy.exc import SQLAlchemyError

user_bp = Blueprint('user',__name__)

@user_bp.route('/users', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400 
        username = data.get('username')
        email=data.get('email')
        password=data.get('password')
        if not username or not email or not password:
            return jsonify({"error": "Missing required fieldss"}), 400
        new_user = User(username=username,email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully", "user":new_user.data}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    
    except Exception as e:
         return jsonify({"error": f"Database error: {str(e)}"}), 500