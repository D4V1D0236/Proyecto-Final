import requests

# URL de tu servidor Flask
base_url = "http://127.0.0.1:5000"

# Registrar un nuevo estudiante
def register_student(nombre, apellido, promedio):
    url = f"{base_url}/register_student"
    student_data = {
        "nombre": nombre,
        "apellido": apellido,
        "promedio": promedio
    }
    response = requests.post(url, json=student_data)
    if response.status_code == 201:
        print("Estudiante registrado exitosamente")
    else:
        print("Error al registrar estudiante:", response.text)

# Obtener todos los estudiantes
def get_students():
    url = f"{base_url}/students"
    response = requests.get(url)
    if response.status_code == 200:
        students = response.json()
        for student in students:
            print(f"Estudiante: {student['nombre']} {student['apellido']}, Promedio: {student['promedio']}")
    else:
        print("Error al obtener estudiantes:", response.text)

def register_note(estudiante_codigo, curso_codigo, nota):
    url = f"{base_url}/register_note"
    note_data = {
        "estudiante_codigo": estudiante_codigo,
        "curso_codigo": curso_codigo,
        "nota": nota
    }
    response = requests.post(url, json=note_data)
    if response.status_code == 201:
        print("Nota registrada exitosamente y promedio actualizado")
    else:
        print("Error al registrar nota:", response.text)

get_students()
register_note()