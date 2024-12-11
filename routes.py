from flask import  Blueprint, render_template
from flask import Blueprint, request, jsonify
from models import User
from extensions import db 
from sqlalchemy.exc import SQLAlchemyError
main = Blueprint('main', __name__) #routename=main
user_bp = Blueprint('user',__name__)


@main.route('/', methods=['GET'])
def home_page():
    return render_template('base.html')

# @main.route('/adduser', methods=['GET', 'POST'])
# def add_user():
#     return render_template('adduser.html')

@user_bp.route('/users', methods=['POST'])
def add_user():
    try: 
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if not username or not email or not password:
            return jsonify({"error": "Missing required fields"}), 400
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully", "user":new_user.data}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
         return jsonify({"error": f"Database error: {str(e)}"}), 500

# @user_bp.route('/getusers', methods=['GET'])
# def get_users():
#     try: