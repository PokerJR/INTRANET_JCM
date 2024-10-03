from flask import Flask, request, render_template, render_template_string, redirect, url_for, session
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'tu_usuario_mysql'  # Cambia esto por tu usuario de MySQL
app.config['MYSQL_PASSWORD'] = 'tu_contraseña_mysql'  # Cambia esto por tu contraseña de MySQL
app.config['MYSQL_DB'] = 'nombre_de_tu_base_de_datos'  # Cambia esto por el nombre de tu base de datos

mysql = MySQL(app)

@app.route('/')
def index():
    with open('Front_end.html', 'r', encoding='utf-8') as file:
        content = file.read()
    return render_template_string(content)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']  # Cambia 'username' por el nombre que corresponde a tu campo de documento
    password = request.form['password'].encode('utf-8')  # Asegúrate de que tu HTML tenga el campo de password

    # Consulta en la base de datos
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE username = %s", [username])  # Verifica que el campo username exista en tu base de datos
    user = cur.fetchone()
    cur.close()

    if user and bcrypt.checkpw(password, user[2].encode('utf-8')):  # Comparar contraseñas
        session['username'] = user[1]  # Cambia el índice según cómo esté estructurada tu tabla
        session['role'] = user[3]  # Cambia el índice según cómo esté estructurada tu tabla
        
        if user[3] == 'docente':
            return redirect(url_for('dashboard_docente'))
        elif user[3] == 'estudiante':
            return redirect(url_for('dashboard_estudiante'))
        else:
            return redirect(url_for('dashboard_administrativo'))
    else:
        return 'Usuario o contraseña incorrectos'

@app.route('/dashboard_docente')
def dashboard_docente():
    if 'role' in session and session['role'] == 'docente':
        return "Bienvenido, docente!"
    else:
        return "Acceso no autorizado."

@app.route('/dashboard_estudiante')
def dashboard_estudiante():
    if 'role' in session and session['role'] == 'estudiante':
        return "Bienvenido, estudiante!"
    else:
        return "Acceso no autorizado."

@app.route('/dashboard_administrativo')
def dashboard_administrativo():
    if 'role' in session and session['role'] == 'administrativo':
        return "Bienvenido, administrativo!"
    else:
        return "Acceso no autorizado."

if __name__ == '__main__':
    app.run(debug=True)
