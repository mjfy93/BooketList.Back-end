from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db
from app.errors import bad_request, not_found, internal_error, conflict
from flask_jwt_extended import jwt_required, get_jwt_identity

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    try:
        current_user_id = get_jwt_identity()
        
        usuario = User.query.get(current_user_id)
        if not usuario:
            return not_found('Usuario no encontrado')

        user_profile = {
            'user_id': usuario.id_usuario,
            'username': usuario.nombre_usuario,
            'last_name': usuario.apellido_usuario,
            'email': usuario.email_usuario,
            'join_date': usuario.created_at.strftime('%Y-%m-%d') if usuario.created_at else None,
            'last_update': usuario.updated_at.strftime('%Y-%m-%d') if usuario.updated_at else None
        }

        return jsonify(user_profile), 200

    except Exception as e:
        return internal_error(str(e))

@profile_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_user_profile():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        usuario = User.query.get(current_user_id)
        if not usuario:
            return not_found('Usuario no encontrado')

        
        if 'username' in data:
            
            existing_user = User.query.filter(
                User.nombre_usuario == data['username'],
                User.id_usuario != current_user_id
            ).first()
            if existing_user:
                return conflict('El nombre de usuario ya está en uso')
            usuario.nombre_usuario = data['username']

        if 'last_name' in data:
            usuario.apellido_usuario = data['last_name']

        if 'email' in data:
            
            existing_email = User.query.filter(
                User.email_usuario == data['email'],
                User.id_usuario != current_user_id
            ).first()
            if existing_email:
                return conflict('El correo electrónico ya está en uso')
            usuario.email_usuario = data['email']

        if 'password' in data and data['password']:
            usuario.set_password(data['password'])

        db.session.commit()

        return jsonify({
            'message': 'Perfil actualizado exitosamente',
            'profile': {
                'user_id': usuario.id_usuario,
                'username': usuario.nombre_usuario,
                'last_name': usuario.apellido_usuario,
                'email': usuario.email_usuario
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return internal_error(str(e))