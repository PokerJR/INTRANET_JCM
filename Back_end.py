from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector
import urllib.parse as urlparse

class MyServer(BaseHTTPRequestHandler):
    def do_POST(self):
        # Procesar los datos del formulario
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        fields = urlparse.parse_qs(post_data.decode('utf-8'))
        username = fields['username'][0]
        password = fields['password'][0]

        # Conectar a la base de datos MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="tu_usuario_mysql",
            password="tu_contraseña_mysql",
            database="nombre_de_tu_base_de_datos"
        )
        cursor = conn.cursor()

        # Verificar el usuario en la base de datos
        cursor.execute("SELECT role FROM usuarios WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        # Si las credenciales son correctas
        if user:
            role = user[0]
            response = f"Bienvenido, {role}."
        else:
            response = "Usuario o contraseña incorrectos."

        # Enviar la respuesta al cliente
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(response.encode())

        # Cerrar la conexión con la base de datos
        cursor.close()
        conn.close()

if __name__ == "__main__":
    webServer = HTTPServer(('localhost', 8080), MyServer)
    print("Servidor iniciado en http://localhost:8080")
    webServer.serve_forever()
