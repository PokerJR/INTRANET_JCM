from flask import Flask, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'tu_usuario_mysql'
app.config['MYSQL_PASSWORD'] = 'tu_contraseña_mysql'
app.config['MYSQL_DB'] = 'nombre_de_tu_base_de_datos'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password'].encode('utf-8')
    
    # Consulta en la base de datos
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE username = %s", [username])
    user = cur.fetchone()
    cur.close()
    
    if user and bcrypt.checkpw(password, user[2].encode('utf-8')):  # Comparar contraseñas
        session['username'] = user[1]
        session['role'] = user[3]
        
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
    if session['role'] == 'docente':
        return "Bienvenido, docente!"
    else:
        return "Acceso no autorizado."

@app.route('/dashboard_estudiante')
def dashboard_estudiante():
    if session['role'] == 'estudiante':
        return "Bienvenido, estudiante!"
    else:
        return "Acceso no autorizado."

@app.route('/dashboard_administrativo')
def dashboard_administrativo():
    if session['role'] == 'administrativo':
        return "Bienvenido, administrativo!"
    else:
        return "Acceso no autorizado."

if __name__ == '__main__':
    app.run(debug=True)
