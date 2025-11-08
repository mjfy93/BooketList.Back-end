from flask import Blueprint, request, jsonify
from app.models import UserLibrary, Book, Rating
from app import db
from app.errors import bad_request, not_found, internal_error
from flask_jwt_extended import jwt_required, get_jwt_identity

library_bp = Blueprint('library', __name__)

@library_bp.route('/my-library', methods=['GET'])
@jwt_required()
def get_my_library():
    """
    Obtener la librería personal completa del usuario actual
    Incluye: libros en UserLibrary (quiero_leer, leyendo) y Rating (leido)
    """
    try:
        user_id = get_jwt_identity()
        
        # ✅ Get books from UserLibrary (quiero_leer y leyendo)
        user_library = UserLibrary.query.filter_by(id_usuario=user_id).all()
        
        # ✅ Get books from Rating (leido)
        read_books = Rating.query.filter_by(id_usuario=user_id).all()
        
        # Organize by reading state
        quiero_leer_books = []
        leyendo_books = []
        leido_books = []
        
        # Process UserLibrary books
        for item in user_library:
            book = Book.query.get(item.id_libro)
            if book:
                book_data = {
                    'library_id': item.id_biblioteca,
                    'book': book.serialize(),
                    'added_at': item.created_at.isoformat() if item.created_at else None
                }
                
                if item.estado_lectura == 'quiero_leer':
                    quiero_leer_books.append(book_data)
                elif item.estado_lectura == 'leyendo':
                    leyendo_books.append(book_data)
        
        # ✅ Process Rating books (leido)
        for rating in read_books:
            book = Book.query.get(rating.id_libro)
            if book:
                leido_books.append({
                    'rating_id': rating.id_calificacion,
                    'book': book.serialize(),
                    'calificacion': rating.calificacion,  # Can be null
                    'resena': rating.resena,              # Can be null
                    'finished_at': rating.created_at.isoformat() if rating.created_at else None
                })
        
        # Calculate totals
        total_books = len(quiero_leer_books) + len(leyendo_books) + len(leido_books)
        
        return jsonify({
            'user_id': user_id,
            'total_books': total_books,
            'quiero_leer': quiero_leer_books,
            'leyendo': leyendo_books,
            'leido': leido_books,
            'counts': {
                'quiero_leer': len(quiero_leer_books),
                'leyendo': len(leyendo_books),
                'leido': len(leido_books)
            }
        }), 200
    
    except Exception as e:
        return internal_error(str(e))

@library_bp.route('/my-library/books', methods=['POST'])
@jwt_required()
def add_book_to_my_library():
    """
    Agregar libro a la librería personal del usuario
    Acepta: id_libro, estado_lectura (opcional, default: 'quiero_leer')
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('id_libro'):
            return bad_request('ID del libro es requerido')
        
        book_id = data['id_libro']
        reading_state = data.get('estado_lectura', 'quiero_leer')
        
        # ✅ CHANGED: Only 2 valid states now (removed 'leido')
        valid_states = ['quiero_leer', 'leyendo']
        if reading_state not in valid_states:
            return bad_request(f'Estado de lectura inválido. Debe ser: {", ".join(valid_states)}')
        
        # Verificar si el libro existe
        book = Book.query.get(book_id)
        if not book:
            return not_found('Libro no encontrado')
        
        # Verificar si ya está en la librería
        existing = UserLibrary.query.filter_by(
            id_usuario=user_id, 
            id_libro=book_id
        ).first()
        
        if existing:
            return bad_request('El libro ya está en tu librería')
        
        # ✅ NEW: Check if book has already been read (exists in Rating)
        from app.models import Rating
        already_read = Rating.query.filter_by(
            id_usuario=user_id,
            id_libro=book_id
        ).first()
        
        if already_read:
            return bad_request('Ya has marcado este libro como leído. No se puede agregar nuevamente a tu librería.')
        
        # Agregar a la librería
        library_item = UserLibrary(
            id_usuario=user_id,
            id_libro=book_id,
            estado_lectura=reading_state
        )
        
        db.session.add(library_item)
        db.session.commit()
        
        return jsonify({
            'message': 'Libro agregado a tu librería personal exitosamente',
            'book': book.serialize(),
            'reading_state': reading_state
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return internal_error(str(e))

@library_bp.route('/my-library/books/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book_in_library(book_id):
    """
    Actualizar estado de lectura de un libro en la librería
    Solo permite cambiar entre 'quiero_leer' y 'leyendo'
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'estado_lectura' not in data:
            return bad_request('Estado de lectura es requerido')
        
        # Buscar el item en la librería
        library_item = UserLibrary.query.filter_by(
            id_usuario=user_id,
            id_libro=book_id
        ).first()
        
        if not library_item:
            return not_found('Libro no encontrado en tu librería personal')
        
        # ✅ CHANGED: Only 2 valid states (removed 'leido')
        valid_states = ['quiero_leer', 'leyendo']
        new_state = data['estado_lectura']
        
        if new_state not in valid_states:
            # ✅ NEW: Helpful error message for 'leido'
            if new_state == 'leido':
                return bad_request(
                    'Para marcar un libro como leído, usa el endpoint POST /my-library/books/{book_id}/mark-read'
                )
            return bad_request(
                f'Estado de lectura inválido. Debe ser: {", ".join(valid_states)}'
            )
        
        # Actualizar estado de lectura
        library_item.estado_lectura = new_state
        db.session.commit()
        
        return jsonify({
            'message': 'Estado de lectura actualizado exitosamente',
            'library_item': library_item.serialize()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return internal_error(str(e))

@library_bp.route('/my-library/books/<int:book_id>', methods=['DELETE'])
@jwt_required()
def remove_book_from_my_library(book_id):
    """
    Remover libro de la librería personal del usuario
    """
    try:
        user_id = get_jwt_identity()
        
        # Buscar el item en la librería
        library_item = UserLibrary.query.filter_by(
            id_usuario=user_id,
            id_libro=book_id
        ).first()
        
        if not library_item:
            return not_found('Libro no encontrado en tu librería personal')
        
        db.session.delete(library_item)
        db.session.commit()
        
        return jsonify({
            'message': 'Libro removido de tu librería personal exitosamente'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return internal_error(str(e))

@library_bp.route('/my-library/books/<int:book_id>', methods=['GET'])
@jwt_required()
def check_book_in_my_library(book_id):
    """
    Verificar si un libro está en la librería personal del usuario
    """
    try:
        user_id = get_jwt_identity()
        
        library_item = UserLibrary.query.filter_by(
            id_usuario=user_id,
            id_libro=book_id
        ).first()
        
        book = Book.query.get(book_id)
        
        response = {
            'in_my_library': library_item is not None,
            'book': book.serialize() if book else None
        }
        
        if library_item:
            response['reading_state'] = library_item.estado_lectura
        
        return jsonify(response), 200
    
    except Exception as e:
        return internal_error(str(e))
    
@library_bp.route('/my-library/books/<int:book_id>/mark-read', methods=['POST'])
@jwt_required()
def mark_book_as_read(book_id):
    """
    Marcar un libro como leído
    - Elimina el libro de UserLibrary (si existe)
    - Crea una entrada en Rating
    - Acepta calificacion (1-5, opcional) y resena (opcional)
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        
        # Verificar si el libro existe
        book = Book.query.get(book_id)
        if not book:
            return not_found('Libro no encontrado')
        
        # ✅ Check if already marked as read
        existing_rating = Rating.query.filter_by(
            id_usuario=user_id,
            id_libro=book_id
        ).first()
        
        if existing_rating:
            return bad_request('Este libro ya está marcado como leído. Usa el endpoint PATCH para actualizar la calificación o reseña.')
        
        # ✅ Get optional calificacion and resena from request
        calificacion = data.get('calificacion')
        resena = data.get('resena')
        
        # ✅ Validate calificacion if provided
        if calificacion is not None:
            if not isinstance(calificacion, (int, float)):
                return bad_request('La calificación debe ser un número')
            if calificacion < 1 or calificacion > 5:
                return bad_request('La calificación debe estar entre 1 y 5')
        
        # ✅ Check if book is in UserLibrary and delete it
        library_item = UserLibrary.query.filter_by(
            id_usuario=user_id,
            id_libro=book_id
        ).first()
        
        if library_item:
            db.session.delete(library_item)
            print(f"📚 Libro removido de UserLibrary para usuario {user_id}")
        else:
            print(f"ℹ️ Libro no estaba en UserLibrary, creando Rating directamente")
        
        # ✅ Create Rating entry
        new_rating = Rating(
            id_usuario=user_id,
            id_libro=book_id,
            calificacion=calificacion,  # Can be None
            resena=resena                # Can be None
        )
        
        db.session.add(new_rating)
        db.session.commit()
        
        return jsonify({
            'message': 'Libro marcado como leído exitosamente',
            'book': book.serialize(),
            'rating': {
                'rating_id': new_rating.id_calificacion,
                'calificacion': new_rating.calificacion,
                'resena': new_rating.resena,
                'finished_at': new_rating.created_at.isoformat() if new_rating.created_at else None
            }
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return internal_error(str(e))
    
@library_bp.route('/my-library/books/<int:book_id>/rating', methods=['PATCH'])
@jwt_required()
def update_book_rating(book_id):
    """
    Actualizar calificación y/o reseña de un libro ya marcado como leído
    - Solo actualiza los campos proporcionados (partial update)
    - Ignora valores null
    - Requiere que el libro ya tenga un Rating existente
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return bad_request('Debe proporcionar al menos calificacion o resena para actualizar')
        
        # ✅ Find existing Rating
        rating = Rating.query.filter_by(
            id_usuario=user_id,
            id_libro=book_id
        ).first()
        
        if not rating:
            return not_found('No has marcado este libro como leído. Usa el endpoint POST /mark-read primero.')
        
        # ✅ Get optional fields (only if provided and not null)
        calificacion = data.get('calificacion')
        resena = data.get('resena')
        
        # Track if anything was updated
        updated = False
        
        # ✅ Update calificacion if provided and not null
        if 'calificacion' in data and calificacion is not None:
            # Validate calificacion
            if not isinstance(calificacion, (int, float)):
                return bad_request('La calificación debe ser un número')
            if calificacion < 1 or calificacion > 5:
                return bad_request('La calificación debe estar entre 1 y 5')
            
            rating.calificacion = calificacion
            updated = True
        
        # ✅ Update resena if provided and not null
        if 'resena' in data and resena is not None:
            rating.resena = resena
            updated = True
        
        if not updated:
            return bad_request('No se proporcionaron campos válidos para actualizar')
        
        db.session.commit()
        
        return jsonify({
            'message': 'Calificación actualizada exitosamente',
            'book': Book.query.get(book_id).serialize(),
            'rating': {
                'rating_id': rating.id_calificacion,
                'calificacion': rating.calificacion,
                'resena': rating.resena,
                'updated_at': rating.updated_at.isoformat() if rating.updated_at else None
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return internal_error(str(e))