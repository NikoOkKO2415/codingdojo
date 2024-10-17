from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configura SQLite como base de datos
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de publicación
class Publicacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(200), nullable=True)

# Crear las tablas
with app.app_context():
    db.create_all()

# Ruta para la página de inicio, redirige a login
@app.route('/')
def home():
    return redirect(url_for('login'))

# Ruta para la página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Procesar el login (aquí podrías verificar usuario y contraseña)
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html')

# Ruta para el registro de usuario
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Procesar el registro (puedes guardar el usuario en una base de datos o similar)
        username = request.form['username']
        email = request.form['email']
        # Aquí iría la lógica de registro
        return redirect(url_for('login'))
    return render_template('registro.html')

# Ruta para la página principal después de iniciar sesión
@app.route('/index')
def index():
    if 'username' in session:
        publicaciones = Publicacion.query.all()  # Obtiene todas las publicaciones
        username = session['username']
        return render_template('index.html', username=username, publicaciones=publicaciones)
    return redirect(url_for('login'))

# Ruta para el perfil de usuario
@app.route('/perfil')
def perfil():
    if 'username' in session:
        username = session['username']
        return render_template('perfil.html', username=username)
    return redirect(url_for('login'))

# Ruta para crear una publicación
@app.route('/crear_publicacion', methods=['GET', 'POST'])
def crear_publicacion():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        imagen = request.files['imagen']
        
        # Guardar la imagen en /static/uploads/
        if imagen:
            filename = imagen.filename
            filepath = os.path.join('static/uploads', filename)
            imagen.save(filepath)
            image_url = f'/static/uploads/{filename}'
        else:
            image_url = None

        # Guardar la publicación en la base de datos
        nueva_publicacion = Publicacion(titulo=titulo, descripcion=descripcion, imagen=image_url)
        db.session.add(nueva_publicacion)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('crear_publicacion.html')  # Renderiza crear_publicacion.html en GET

# Ruta para editar el perfil
@app.route('/editar_perfil', methods=['GET', 'POST'])
def editar_perfil():
    if 'username' in session:
        if request.method == 'POST':
            # Aquí puedes procesar la actualización del perfil
            session['username'] = request.form.get('username')
            profile_image = request.form.get('profile_image')
            # Guardar la imagen en localStorage o base de datos (esto es solo un ejemplo)
            return redirect(url_for('perfil'))  # Redirige a la página de perfil
        return render_template('editar_perfil.html')
    return redirect(url_for('login'))

# Ruta para la página de donaciones
@app.route('/donaciones', methods=['GET', 'POST'])
def donaciones():
    if 'username' in session:
        if request.method == 'POST':
            # Procesar el donativo
            amount = request.form['amount']
            # Aquí iría la lógica para manejar el donativo
            return redirect(url_for('index'))  # Redirige a la página principal después de hacer la donación
        return render_template('donaciones.html')  # Renderiza donaciones.html en GET
    return redirect(url_for('login'))

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

    # Crear las tablas
with app.app_context():
    db.create_all()
