import os
import sys
from sqlite3 import connect, IntegrityError

# Agregar la ruta actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_tables_and_data():
    # Conectar a la base de datos SQLite
    conn = connect('instance/biblioteca.db')
    cursor = conn.cursor()
    
    print("🗃️ Creando tablas...")
    
    # Leer y ejecutar el archivo de tablas
    with open('tablas.txt', 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    # Dividir el script en sentencias individuales
    statements = sql_script.split(';')
    
    for statement in statements:
        statement = statement.strip()
        if statement and not statement.startswith('--'):
            try:
                # Adaptar para SQLite (remover SERIAL, usar AUTOINCREMENT)
                statement = statement.replace('SERIAL PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT')
                statement = statement.replace('TEXT', 'TEXT')
                statement = statement.replace('INTEGER', 'INTEGER')
                
                cursor.execute(statement)
                print(f"✅ Ejecutado: {statement[:50]}...")
            except Exception as e:
                print(f"⚠️ Error en: {statement[:50]}... - {e}")
    
    # Confirmar cambios
    conn.commit()
    
    # Verificar tablas creadas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("\n📊 Tablas creadas:")
    for table in tables:
        print(f"   - {table[0]}")
    
    # Contar registros
    tables_to_count = ['usuario', 'autores', 'libros', 'calificacion', 'biblioteca_usuario']
    print("\n📈 Registros insertados:")
    for table in tables_to_count:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"   - {table}: {count} registros")
    
    conn.close()
    print("\n🎉 Base de datos poblada exitosamente!")

if __name__ == '__main__':
    create_tables_and_data()