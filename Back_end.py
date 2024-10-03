from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Clave secreta para manejar sesiones

# Simulación de usuarios para inicio de sesión
users = {
    "student1": {"password": "password123", "name": "Juan Pérez", "notes": {"Matemáticas": 85, "Ciencia": 90}},
}

# Ruta para el inicio de sesión (muestra el archivo Front_end.html)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificación del usuario
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))  # Redirige al dashboard si el inicio de sesión es correcto
        else:
            return "Credenciales incorrectas. Inténtalo de nuevo."

    return render_template('Front_end.html')  # Renderiza tu archivo HTML (Front_end.html)

# Ruta del panel de control después del inicio de sesión
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        student = users[username]
        return render_template('dashboard.html', name=student['name'], notes=student['notes'])
    else:
        return redirect(url_for('login'))

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
