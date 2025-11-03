# app/errors.py
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

def error_response(status_code, message=None):
    payload = {
        'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error'),
        'status': status_code
    }
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response

def bad_request(message):
    return error_response(400, message)

def unauthorized(message):
    return error_response(401, message)

def not_found(message):
    return error_response(404, message)

def conflict(message):
    return error_response(409, message)

def internal_error(message):
    return error_response(500, message)

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request_error(error):
        return bad_request('Solicitud incorrecta')
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        return unauthorized('No autorizado')
    
    @app.errorhandler(404)
    def not_found_error(error):
        return not_found('Recurso no encontrado')
    
    @app.errorhandler(409)
    def conflict_error(error):
        return conflict('Conflicto con el recurso')
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return internal_error('Error interno del servidor')