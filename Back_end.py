<<<<<<< HEAD
from flask import Flask, render_template_string, request, redirect, url_for, session
=======
from flask import Flask, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
import bcrypt
>>>>>>> 86084ea0d45b132017d75b435b562181d46a86c9

app = Flask(__name__)
app.secret_key = 'your_secret_key'

<<<<<<< HEAD
# Simulación de usuarios para inicio de sesión
users = {
    "student1": {"password": "password123", "name": "Juan Pérez", "notes": {"Matemáticas": 85, "Ciencia": 90}},
    "student2": {"password": "mypassword", "name": "Ana López", "notes": {"Historia": 78, "Inglés": 92}},
}

# Ruta para el inicio de sesión
@app.route('/', methods=['GET', 'POST'])
=======
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
>>>>>>> 86084ea0d45b132017d75b435b562181d46a86c9
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
<<<<<<< HEAD
            return "Credenciales incorrectas. Inténtalo de nuevo."

    # Leer el contenido del archivo HTML
    with open('Front_end.html', 'r', encoding='utf-8') as file:
        content = file.read()
    return render_template_string(content)  # Renderiza el contenido directamente

# Ruta del panel de control después del inicio de sesión
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        student = users[username]
        return render_template_string('''
            <h1>Bienvenido {{ name }}</h1>
            <h2>Notas:</h2>
            <ul>
                {% for subject, grade in notes.items() %}
                    <li>{{ subject }}: {{ grade }}</li>
                {% endfor %}
            </ul>
            <a href="{{ url_for('logout') }}">Cerrar sesión</a>
        ''', name=student['name'], notes=student['notes'])
=======
            return redirect(url_for('dashboard_administrativo'))
>>>>>>> 86084ea0d45b132017d75b435b562181d46a86c9
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
