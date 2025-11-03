from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from app.errors import bad_request, not_found, internal_error
from flask_jwt_extended import jwt_required, get_jwt_identity

users_bp = Blueprint('users', __name__)

@users_bp.route('/admin/users', methods=['GET'])
@jwt_required()
def get_all_users():
    """
    Obtener lista de todos los usuarios (solo administradores)
    """
    try:
        # En una aplicación real, verificarías si el usuario actual es admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if not current_user or not current_user.is_admin:
            return jsonify({"error": "No autorizado"}), 403
        
        users = User.query.all()
        return jsonify([user.serialize_public() for user in users]), 200
    
    except Exception as e:
        return internal_error(str(e))

@users_bp.route('/admin/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """
    Obtener información detallada de un usuario específico
    """
    try:
        user = User.query.get_or_404(user_id)
        return jsonify(user.serialize()), 200
    
    except Exception as e:
        return not_found(str(e))

@users_bp.route('/admin/users/<int:user_id>/block', methods=['PUT'])
@jwt_required()
def block_user(user_id):
    """
    Bloquear un usuario (desactivar)
    """
    try:
        user = User.query.get_or_404(user_id)
        
        # No permitir bloquearse a sí mismo
        current_user_id = get_jwt_identity()
        if user.id_usuario == current_user_id:
            return bad_request("No puedes bloquear tu propia cuenta")
        
        user.is_active = False
        db.session.commit()
        
        return jsonify({
            "message": f"Usuario {user.nombre_usuario} {user.apellido_usuario} bloqueado exitosamente",
            "user": user.serialize_public()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return internal_error(str(e))

@users_bp.route('/admin/users/<int:user_id>/unblock', methods=['PUT'])
@jwt_required()
def unblock_user(user_id):
    """
    Desbloquear un usuario (activar)
    """
    try:
        user = User.query.get_or_404(user_id)
        user.is_active = True
        db.session.commit()
        
        return jsonify({
            "message": f"Usuario {user.nombre_usuario} {user.apellido_usuario} desbloqueado exitosamente",
            "user": user.serialize_public()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return internal_error(str(e))

@users_bp.route('/admin/users/<int:user_id>/toggle-status', methods=['PUT'])
@jwt_required()
def toggle_user_status(user_id):
    """
    Alternar estado de usuario (bloquear/desbloquear)
    """
    try:
        user = User.query.get_or_404(user_id)
        
        # No permitir cambiar estado a sí mismo
        current_user_id = get_jwt_identity()
        if user.id_usuario == current_user_id:
            return bad_request("No puedes cambiar el estado de tu propia cuenta")
        
        user.is_active = not user.is_active
        db.session.commit()
        
        action = "desbloqueado" if user.is_active else "bloqueado"
        
        return jsonify({
            "message": f"Usuario {user.nombre_usuario} {user.apellido_usuario} {action} exitosamente",
            "user": user.serialize_public()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return internal_error(str(e))

@users_bp.route('/admin/users/active', methods=['GET'])
@jwt_required()
def get_active_users():
    """
    Obtener solo usuarios activos
    """
    try:
        users = User.query.filter_by(is_active=True).all()
        return jsonify([user.serialize_public() for user in users]), 200
    
    except Exception as e:
        return internal_error(str(e))

@users_bp.route('/admin/users/blocked', methods=['GET'])
@jwt_required()
def get_blocked_users():
    """
    Obtener solo usuarios bloqueados
    """
    try:
        users = User.query.filter_by(is_active=False).all()
        return jsonify([user.serialize_public() for user in users]), 200
    
    except Exception as e:
        return internal_error(str(e))

@users_bp.route('/admin/users/stats', methods=['GET'])
@jwt_required()
def get_users_stats():
    """
    Obtener estadísticas de usuarios
    """
    try:
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        blocked_users = User.query.filter_by(is_active=False).count()
        
        return jsonify({
            "total_users": total_users,
            "active_users": active_users,
            "blocked_users": blocked_users,
            "active_percentage": round((active_users / total_users) * 100, 2) if total_users > 0 else 0
        }), 200
    
    except Exception as e:
        return internal_error(str(e))

@users_bp.route('/users/public', methods=['GET'])
def get_public_users():
    """
    Obtener lista pública de usuarios (sin necesidad de token)
    Solo información básica para mostrar en la interfaz
    """
    try:
        users = User.query.filter_by(is_active=True).all()
        
        return jsonify([{
            "id_usuario": user.id_usuario,
            "nombre_usuario": user.nombre_usuario,
            "apellido_usuario": user.apellido_usuario,
            "miembro_desde": user.created_at.strftime('%Y-%m-%d') if user.created_at else None,
            "total_libros_biblioteca": len(user.biblioteca) if user.biblioteca else 0,
            "total_resenas": len(user.calificaciones) if user.calificaciones else 0
        } for user in users]), 200
    
    except Exception as e:
        return internal_error(str(e))
