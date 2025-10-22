from os import wait
from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from flask_login import login_user, logout_user, current_user, login_required

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    # Se o usuário já estiver logado, não deve se registrar
    if current_user.is_authenticated:
        return jsonify({'message': 'Already logged in'}), 400
    data = request.get_json()
    if not data or not 'email' in data or not 'password' in data:
        return jsonify({'message': 'Missing email or password'}), 400

    email = data.get('email')
    password = data.get('password')

    # Verifica se o usuário já existe
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'message': 'Email already registered'}), 400

    # Cria o novo usuário
    new_user = User(email=email)
    new_user.password = password  # Isso chama o @password.setter
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({'message': 'Already logged in'}), 200

    data = request.get_json()
    if not data or not 'email' in data or not 'password' in data:
        return jsonify({'message': 'Missing email or password'}), 400

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    # Verifica se o usuário existe E se a senha está correta
    if user and user.check_password(password):
        login_user(user, remember=data.get('remember', False)) # 'remember=True' cria um cookie persistente
        return jsonify({'message': 'Login successful'}), 200
    
    # Resposta genérica para não vazar informação (se o email existe ou não)
    return jsonify({'message': 'Invalid email or password'}), 401


@bp.route('/logout', methods=['POST'])
@login_required  # Só pode deslogar se estiver logado
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200


@bp.route('/status', methods=['GET'])
def status():
    # Rota útil para o frontend verificar se o usuário está logado
    if current_user.is_authenticated:
        return jsonify({'logged_in': True, 'user': {'id': current_user.id, 'email': current_user.email}}), 200
    else:
        return jsonify({'logged_in': False}), 200
