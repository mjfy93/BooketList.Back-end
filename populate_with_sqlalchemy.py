import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.database import db
from app.models.user import User
from app.models.author import Author
from app.models.book import Book
from app.models.rating import Rating
from app.models.user_library import UserLibrary

def populate_complete_database():
    app = create_app()
    
    with app.app_context():
        print("🗑️ Limpiando base de datos existente...")
        UserLibrary.query.delete()
        Rating.query.delete()
        Book.query.delete()
        Author.query.delete()
        User.query.delete()
        
        print("👥 Insertando usuarios...")
        users_data = [
            {'nombre_usuario': 'Ana', 'apellido_usuario': 'García', 'correo_electronico': 'ana.garcia@email.com', 'contraseña_usuario': 'password123'},
            {'nombre_usuario': 'Carlos', 'apellido_usuario': 'Rodríguez', 'correo_electronico': 'carlos.rodriguez@email.com', 'contraseña_usuario': 'securepass456'},
            {'nombre_usuario': 'María', 'apellido_usuario': 'López', 'correo_electronico': 'maria.lopez@email.com', 'contraseña_usuario': 'mypassword789'},
            {'nombre_usuario': 'Juan', 'apellido_usuario': 'Martínez', 'correo_electronico': 'juan.martinez@email.com', 'contraseña_usuario': 'juanpass123'},
            {'nombre_usuario': 'Laura', 'apellido_usuario': 'Hernández', 'correo_electronico': 'laura.hernandez@email.com', 'contraseña_usuario': 'laurapass456'}
        ]
        
        for user_data in users_data:
            user = User(
                nombre_usuario=user_data['nombre_usuario'],
                apellido_usuario=user_data['apellido_usuario'],
                correo_electronico=user_data['correo_electronico']
            )
            user.set_password(user_data['contraseña_usuario'].replace('password', ''))
            db.session.add(user)
        
        db.session.commit()
        print(f"✅ {len(users_data)} usuarios insertados")
        
        print("✍️ Insertando TODOS los autores...")
        autores_data = [
            ('Sarah', 'Mitchell'), ('Hiroshi', 'Tanaka'), ('Emma', 'Thornton'),
            ('Marco', 'Bellini'), ('Claire', 'Anderson'), ('Yuki', 'Nakamura'),
            ('Dmitri', 'Volkov'), ('Sophie', 'Laurent'), ('James', 'Crawford'),
            ('Mei', 'Chen'), ('Robert', 'Harrison'), ('Annika', 'Bergström'),
            ('Thomas', 'Williams'), ('Natasha', 'Petrov'), ('Michael', 'Cohen'),
            ('Hans', 'Müller'), ('Victoria', 'Rhodes'), ('Pierre', 'Dubois'),
            ('Elena', 'Popescu'), ('William', 'Foster'), ('Margaret', 'Campbell'),
            ('Alexander', 'Sokolov'), ('Catherine', 'Bennett'), ('Giovanni', 'Romano'),
            ('Elizabeth', 'Thompson'), ('Klaus', 'Schmidt'), ('Anna', 'Kowalski'),
            ('Jonathan', 'Reed'), ('Olivia', 'Morrison'), ('Henrik', 'Andersen'),
            ('David', 'Sterling'), ('Kenji', 'Yamamoto'), ('Rachel', 'Montgomery'),
            ('Ivan', 'Kozlov'), ('Amanda', 'Walsh'), ('Takeshi', 'Sato'),
            ('Nicole', 'Beaumont'), ('Lucas', 'Silva'), ('Jessica', 'Parker'),
            ('Anton', 'Ivanov'), ('Emilia', 'Sandoval'), ('Santiago', 'Marín'),
            ('Paulina', 'Figueroa'), ('Mateo', 'Serrano'), ('Catalina', 'Villalobos'),
            ('Bruno', 'Pacheco'), ('Josefina', 'Leiva'), ('Joaquín', 'Miranda'),
            ('Antonia', 'Durán'), ('Felipe', 'Espinoza'), ('Charlotte', 'Pembroke'),
            ('Nikolai', 'Romanov'), ('Victoria', 'Ashford'), ('Friedrich', 'Weber'),
            ('Eleanor', 'Fitzgerald'), ('Alessandro', 'Conti'), ('Grace', 'Wellington'),
            ('Sebastian', 'Blackwood'), ('Marguerite', 'Fontaine'), ('Charles', 'Whitmore')
        ]
        
        for nombre, apellido in autores_data:
            autor = Author(nombre_autor=nombre, apellido_autor=apellido)
            db.session.add(autor)
        
        db.session.commit()
        print(f"✅ {len(autores_data)} autores insertados")
        
        print("📚 Insertando TODOS los libros...")
        libros_data = [
            # Ficción (10 libros)
            ('El susurro de las mareas', 1, 'Ficción', 'Una historia de amor y pérdida en un pueblo costero donde los secretos del pasado emergen con cada ola.', 'FIC001A2B3', 'https://images.example.com/covers/mareas.jpg'),
            ('Sombras en el jardín', 2, 'Ficción', 'Misterio y suspense en una mansión victoriana donde nada es lo que parece.', 'FIC002C4D5', 'https://images.example.com/covers/sombras.jpg'),
            ('Los días de ceniza', 3, 'Ficción', 'Drama familiar que explora las consecuencias de decisiones tomadas décadas atrás.', 'FIC003E6F7', 'https://images.example.com/covers/ceniza.jpg'),
            ('Luces de neón', 4, 'Ficción', 'Thriller urbano ambientado en el mundo nocturno de una gran metrópolis moderna.', 'FIC004G8H9', 'https://images.example.com/covers/neon.jpg'),
            ('El último verano', 5, 'Ficción', 'Novela coming-of-age sobre amistad y transformación durante un verano inolvidable.', 'FIC005I0J1', 'https://images.example.com/covers/verano.jpg'),
            ('Voces del silencio', 6, 'Ficción', 'Relato psicológico sobre una mujer que descubre verdades ocultas sobre su identidad.', 'FIC006K2L3', 'https://images.example.com/covers/voces.jpg'),
            ('La casa del olvido', 7, 'Ficción', 'Historia gótica sobre una familia marcada por una maldición ancestral.', 'FIC007M4N5', 'https://images.example.com/covers/olvido.jpg'),
            ('Caminos cruzados', 8, 'Ficción', 'Múltiples vidas se entrelazan en esta novela coral sobre destino y casualidad.', 'FIC008O6P7', 'https://images.example.com/covers/caminos.jpg'),
            ('El perfume de la memoria', 9, 'Ficción', 'Romance nostálgico que viaja entre el presente y recuerdos de juventud.', 'FIC009Q8R9', 'https://images.example.com/covers/perfume.jpg'),
            ('Bajo el cielo púrpura', 10, 'Ficción', 'Aventura épica en tierras lejanas donde honor y traición se encuentran.', 'FIC010S0T1', 'https://images.example.com/covers/purpura.jpg'),
            
            # No-Ficción (10 libros)
            ('Mentes brillantes', 11, 'No-Ficción', 'Explora los secretos de la creatividad y cómo las grandes ideas transforman el mundo.', 'NOF011U2V3', 'https://images.example.com/covers/mentes.jpg'),
            ('El poder del ahora', 12, 'No-Ficción', 'Guía práctica sobre mindfulness y presencia consciente en la vida cotidiana.', 'NOF012W4X5', 'https://images.example.com/covers/ahora.jpg'),
            ('Historias de éxito', 13, 'No-Ficción', 'Biografías inspiradoras de emprendedores que transformaron sus industrias.', 'NOF013Y6Z7', 'https://images.example.com/covers/exito.jpg'),
            ('La ciencia del sueño', 14, 'No-Ficción', 'Investigación científica sobre el descanso y su impacto en salud y rendimiento.', 'NOF014A8B9', 'https://images.example.com/covers/sueno.jpg'),
            ('Comer con conciencia', 15, 'No-Ficción', 'Guía nutricional basada en evidencia para una alimentación saludable y sostenible.', 'NOF015C0D1', 'https://images.example.com/covers/comer.jpg'),
            ('El cerebro feliz', 16, 'No-Ficción', 'Neurociencia aplicada para entender y cultivar el bienestar emocional.', 'NOF016E2F3', 'https://images.example.com/covers/cerebro.jpg'),
            ('Liderazgo auténtico', 17, 'No-Ficción', 'Principios fundamentales para liderar equipos con integridad y visión.', 'NOF017G4H5', 'https://images.example.com/covers/liderazgo.jpg'),
            ('Finanzas personales simples', 18, 'No-Ficción', 'Estrategias prácticas para administrar dinero y construir patrimonio duradero.', 'NOF018I6J7', 'https://images.example.com/covers/finanzas.jpg'),
            ('El arte de comunicar', 19, 'No-Ficción', 'Técnicas efectivas para mejorar habilidades de comunicación en cualquier contexto.', 'NOF019K8L9', 'https://images.example.com/covers/comunicar.jpg'),
            ('Vida minimalista', 20, 'No-Ficción', 'Filosofía y práctica del minimalismo para una existencia más plena y ligera.', 'NOF020M0N1', 'https://images.example.com/covers/minimalista.jpg'),
            
            # Historia (10 libros)
            ('Imperios olvidados', 21, 'Historia', 'Análisis de civilizaciones antiguas que desaparecieron dejando misterios sin resolver.', 'HIS021O2P3', 'https://images.example.com/covers/imperios.jpg'),
            ('La gran travesía', 22, 'Historia', 'Crónica de expediciones históricas que cambiaron nuestra comprensión del mundo.', 'HIS022Q4R5', 'https://images.example.com/covers/travesia.jpg'),
            ('Revoluciones silenciosas', 23, 'Historia', 'Movimientos sociales que transformaron sociedades sin violencia armada.', 'HIS023S6T7', 'https://images.example.com/covers/revoluciones.jpg'),
            ('Batallas decisivas', 24, 'Historia', 'Conflictos militares que definieron el curso de la historia mundial.', 'HIS024U8V9', 'https://images.example.com/covers/batallas.jpg'),
            ('Mujeres que cambiaron el mundo', 25, 'Historia', 'Biografías de líderes femeninas cuyo legado transformó sus épocas.', 'HIS025W0X1', 'https://images.example.com/covers/mujeres.jpg'),
            ('El comercio antiguo', 26, 'Historia', 'Historia económica de rutas comerciales que conectaron civilizaciones milenarias.', 'HIS026Y2Z3', 'https://images.example.com/covers/comercio.jpg'),
            ('Dinastías y poder', 27, 'Historia', 'Ascenso y caída de familias reales que gobernaron grandes territorios.', 'HIS027A4B5', 'https://images.example.com/covers/dinastias.jpg'),
            ('La era de los descubrimientos', 28, 'Historia', 'Exploración marítima y encuentros culturales durante los siglos XV y XVI.', 'HIS028C6D7', 'https://images.example.com/covers/descubrimientos.jpg'),
            ('Revoluciones industriales', 29, 'Historia', 'Transformaciones tecnológicas que redefinieron trabajo y sociedad moderna.', 'HIS029E8F9', 'https://images.example.com/covers/industriales.jpg'),
            ('Imperios coloniales', 30, 'Historia', 'Análisis crítico del colonialismo y su impacto en continentes enteros.', 'HIS030G0H1', 'https://images.example.com/covers/coloniales.jpg'),
            
            # Ciencia Ficción (10 libros)
            ('Horizontes estelares', 31, 'Ciencia Ficción', 'Exploradores espaciales descubren una civilización alienígena con secretos antiguos.', 'SCF031I2J3', 'https://images.example.com/covers/horizontes.jpg'),
            ('El algoritmo perfecto', 32, 'Ciencia Ficción', 'Inteligencia artificial desarrolla consciencia propia cuestionando su existencia.', 'SCF032K4L5', 'https://images.example.com/covers/algoritmo.jpg'),
            ('Naves de cristal', 33, 'Ciencia Ficción', 'Guerra interestelar donde tecnología avanzada determina supervivencia de especies.', 'SCF033M6N7', 'https://images.example.com/covers/naves.jpg'),
            ('El último refugio', 34, 'Ciencia Ficción', 'Humanidad busca nuevo hogar tras catástrofe que hizo inhabitable la Tierra.', 'SCF034O8P9', 'https://images.example.com/covers/refugio.jpg'),
            ('Memorias sintéticas', 35, 'Ciencia Ficción', 'Tecnología permite implantar recuerdos falsos alterando percepción de realidad.', 'SCF035Q0R1', 'https://images.example.com/covers/memorias.jpg'),
            ('Los guardianes del tiempo', 36, 'Ciencia Ficción', 'Agencia secreta protege línea temporal de alteraciones que podrían destruirla.', 'SCF036S2T3', 'https://images.example.com/covers/guardianes.jpg'),
            ('Ciudades flotantes', 37, 'Ciencia Ficción', 'Civilización futurista construye metrópolis en atmósfera tras inundaciones globales.', 'SCF037U4V5', 'https://images.example.com/covers/ciudades.jpg'),
            ('El gen inmortal', 38, 'Ciencia Ficción', 'Descubrimiento científico promete vida eterna con consecuencias inesperadas.', 'SCF038W6X7', 'https://images.example.com/covers/gen.jpg'),
            ('Mundos paralelos', 39, 'Ciencia Ficción', 'Físico descubre portal a universos alternos donde todo es ligeramente diferente.', 'SCF039Y8Z9', 'https://images.example.com/covers/paralelos.jpg'),
            ('La última colonia', 40, 'Ciencia Ficción', 'Colonos en planeta distante luchan por sobrevivir ante fauna hostil desconocida.', 'SCF040A0B1', 'https://images.example.com/covers/colonia.jpg'),
            
            # Libros Latinoamericanos (10 libros)
            ('Crónicas del altiplano', 41, 'Latinoamericano', 'Relatos que capturan esencia de comunidades andinas y su sabiduría ancestral.', 'LAT041C2D3', 'https://images.example.com/covers/altiplano.jpg'),
            ('La selva habla', 42, 'Latinoamericano', 'Novela mágica ambientada en Amazonía donde naturaleza tiene voz propia.', 'LAT042E4F5', 'https://images.example.com/covers/selva.jpg'),
            ('Tangos y sombras', 43, 'Latinoamericano', 'Historia de pasión y melancolía en barrios porteños de Buenos Aires.', 'LAT043G6H7', 'https://images.example.com/covers/tangos.jpg'),
            ('El café de las cinco', 44, 'Latinoamericano', 'Encuentros cotidianos en cafetería bogotana revelan dramas humanos universales.', 'LAT044I8J9', 'https://images.example.com/covers/cafe.jpg'),
            ('Memorias del Caribe', 45, 'Latinoamericano', 'Saga familiar que recorre tres generaciones en costas caribeñas colombianas.', 'LAT045K0L1', 'https://images.example.com/covers/caribe.jpg'),
            ('Los hijos del volcán', 46, 'Latinoamericano', 'Comunidad indígena enfrenta modernidad sin perder conexión con tierra sagrada.', 'LAT046M2N3', 'https://images.example.com/covers/volcan.jpg'),
            ('Calles de tierra', 47, 'Latinoamericano', 'Retrato íntimo de vida en barrios marginales de ciudad latinoamericana.', 'LAT047O4P5', 'https://images.example.com/covers/calles.jpg'),
            ('El mercado de los sueños', 48, 'Latinoamericano', 'Realismo mágico en mercado tradicional donde se venden esperanzas e ilusiones.', 'LAT048Q6R7', 'https://images.example.com/covers/mercado.jpg'),
            ('Cantos de revolución', 49, 'Latinoamericano', 'Novela histórica sobre movimientos sociales que sacudieron América Latina.', 'LAT049S8T9', 'https://images.example.com/covers/cantos.jpg'),
            ('La casa junto al río', 50, 'Latinoamericano', 'Drama familiar en pueblo ribereño donde tradiciones chocan con progreso.', 'LAT050U0V1', 'https://images.example.com/covers/rio.jpg'),
            
            # Clásicos (10 libros)
            ('El amor en tiempos difíciles', 51, 'Clásicos', 'Romance épico que trasciende décadas y obstáculos en contexto histórico turbulento.', 'CLA051W2X3', 'https://images.example.com/covers/amor.jpg'),
            ('Los herederos', 52, 'Clásicos', 'Exploración de legado familiar y peso de tradiciones en sociedad cambiante.', 'CLA052Y4Z5', 'https://images.example.com/covers/herederos.jpg'),
            ('Almas perdidas', 53, 'Clásicos', 'Introspección psicológica sobre búsqueda de identidad y propósito existencial.', 'CLA053A6B7', 'https://images.example.com/covers/almas.jpg'),
            ('La torre del reloj', 54, 'Clásicos', 'Narrativa simbólica sobre paso del tiempo y naturaleza efímera de gloria.', 'CLA054C8D9', 'https://images.example.com/covers/torre.jpg'),
            ('Senderos olvidados', 55, 'Clásicos', 'Viaje filosófico por caminos rurales que llevan a descubrimiento personal.', 'CLA055E0F1', 'https://images.example.com/covers/senderos.jpg'),
            ('La sinfonía inacabada', 56, 'Clásicos', 'Artista atormentado busca crear obra maestra mientras batalla sus demonios.', 'CLA056G2H3', 'https://images.example.com/covers/sinfonia.jpg'),
            ('Jardines prohibidos', 57, 'Clásicos', 'Amor imposible florece en jardín secreto desafiando convenciones sociales rígidas.', 'CLA057I4J5', 'https://images.example.com/covers/jardines.jpg'),
            ('El último banquete', 58, 'Clásicos', 'Reunión final de viejos amigos revela secretos guardados durante décadas.', 'CLA058K6L7', 'https://images.example.com/covers/banquete.jpg'),
            ('Cartas desde el exilio', 59, 'Clásicos', 'Correspondencia epistolar entre dos almas separadas por distancia y destino.', 'CLA059M8N9', 'https://images.example.com/covers/cartas.jpg'),
            ('La biblioteca secreta', 60, 'Clásicos', 'Descubrimiento de libros prohibidos desencadena búsqueda de verdades ocultas.', 'CLA060O0P1', 'https://images.example.com/covers/biblioteca.jpg')
        ]
        
        for titulo, autor_id, genero, descripcion, asin, portada in libros_data:
            libro = Book(
                titulo_libro=titulo,
                id_autor=autor_id,
                genero_libro=genero,
                descripcion_libros=descripcion,
                enlace_asin_libro=asin,
                enlace_portada_libro=portada
            )
            db.session.add(libro)
        
        db.session.commit()
        print(f"✅ {len(libros_data)} libros insertados")
        
        print("⭐ Insertando calificaciones...")
        ratings_data = [
            (1, 1, 5, 'Una historia conmovedora que no pude soltar. Los personajes son increíblemente reales.'),
            (1, 2, 4, 'Buena narrativa, aunque el ritmo fue un poco lento al principio.'),
            (31, 3, 5, '¡Impresionante! La construcción del mundo alienígena es fascinante.'),
            (42, 1, 5, 'Hermosa representación de la cultura latinoamericana. Me encantó.'),
            (15, 4, 4, 'Información muy útil, aunque algunos capítulos podrían ser más concisos.')
        ]
        
        for libro_id, usuario_id, calificacion, reseña in ratings_data:
            rating = Rating(
                id_libro=libro_id,
                id_usuario=usuario_id,
                calificacion_usuario=calificacion,
                reseña_usuario=reseña
            )
            db.session.add(rating)
        
        db.session.commit()
        print("✅ Calificaciones insertadas")
        
        print("📖 Insertando bibliotecas de usuario...")
        library_data = [
            (1, 1, 'favorito'), (2, 1, 'leyendo'), (31, 1, 'leido'),
            (42, 2, 'favorito'), (15, 3, 'por_leer'), (1, 3, 'leido'),
            (33, 4, 'leyendo')
        ]
        
        for libro_id, usuario_id, estado in library_data:
            library = UserLibrary(
                id_libro=libro_id,
                id_usuario=usuario_id,
                estado_fav=estado
            )
            db.session.add(library)
        
        db.session.commit()
        print("✅ Bibliotecas de usuario insertadas")
        
        print("\n🎉 BASE DE DATOS COMPLETA POBLADA EXITOSAMENTE!")
        print("=" * 50)
        print(f"👥 Usuarios: {User.query.count()}")
        print(f"✍️ Autores: {Author.query.count()}")
        print(f"📚 Libros: {Book.query.count()}")
        print(f"⭐ Calificaciones: {Rating.query.count()}")
        print(f"📖 Elementos en biblioteca: {UserLibrary.query.count()}")
        print("=" * 50)

if __name__ == '__main__':
    populate_complete_database()