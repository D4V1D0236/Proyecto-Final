from flask import Flask, render_template, request, jsonify, redirect
import mysql.connector

app = Flask(__name__)

# Conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',  
        password='12345',  # Cambiar de acuerdo a la contraseña del equipo en sql
        database='UniversidadUAN'
    )

@app.route('/')
def index():
    # Conexión a la base de datos
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Consulta para obtener los estudiantes
    cursor.execute('SELECT * FROM Estudiante')
    estudiantes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('index.html', estudiantes=estudiantes)

@app.route('/register_student', methods=['POST'])
def register_student():
    # Obtener los datos en formato JSON
    data = request.get_json()  # Obtiene los datos enviados como JSON

    # Extraer los valores del JSON
    nombre = data['nombre']
    apellido = data['apellido']
    promedio = 0  # Inicializamos el promedio como 0, se puede actualizar después

    # Conexión a la base de datos
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insertar los datos del estudiante en la base de datos
    cursor.execute('INSERT INTO Estudiante (nombre, apellido) VALUES (%s, %s)', 
               (nombre, apellido))
    conn.commit()

    # Obtener el código del estudiante recién insertado
    cursor.execute('SELECT codigo FROM Estudiante WHERE nombre = %s AND apellido = %s', (nombre, apellido))
    estudiante_codigo = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return jsonify({'message': 'Estudiante registrado exitosamente', 'codigo': estudiante_codigo}), 201

@app.route('/register_note', methods=['POST'])
def register_note():
    # Obtener los datos en formato JSON
    data = request.get_json()  # Obtiene los datos enviados como JSON

    estudiante_codigo = data['estudiante_codigo']
    curso_codigo = data['curso_codigo']
    nota = data['nota']

    # Conexión a la base de datos
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insertar la nota en la tabla RegistrarNotas
    cursor.execute(""" 
        INSERT INTO RegistrarNotas (estudiante_codigo, curso_codigo, nota) 
        VALUES (%s, %s, %s)
        """, (estudiante_codigo, curso_codigo, nota))
    conn.commit()

    # Calcular el nuevo promedio para el estudiante en todos sus cursos
    cursor.execute("""
        SELECT AVG(nota) FROM RegistrarNotas WHERE estudiante_codigo = %s
    """, (estudiante_codigo,))
    nuevo_promedio = cursor.fetchone()[0]

    # Actualizar el promedio del estudiante
    cursor.execute("""
        UPDATE Estudiante 
        SET promedio = %s 
        WHERE codigo = %s
    """, (nuevo_promedio, estudiante_codigo))
    conn.commit()

    # Calcular el nuevo promedio para el curso
    cursor.execute("""
        SELECT AVG(nota) FROM RegistrarNotas WHERE curso_codigo = %s
    """, (curso_codigo,))
    nuevo_curso_promedio = cursor.fetchone()[0]

    # Actualizar el promedio en la tabla Curso (agregar columna promedio a Curso si es necesario)
    cursor.execute("""
        UPDATE Curso 
        SET nota = %s 
        WHERE codigo = %s
    """, (nuevo_curso_promedio, curso_codigo))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({'message': 'Nota registrada y promedio actualizado exitosamente'}), 201

if __name__ == '__main__':
    app.run(port=5000)
