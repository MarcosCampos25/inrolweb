from flask import Flask, flash, jsonify, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, MultipleFileField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import os
SECRET_KEY = '5f92751c26aa9723cecc78bc3560947881ea9e222a7e68ca'
RUTA_IMAGENES_PRODUCTOS = '\\static\\images\\productos\\miniaturas'



db = SQLAlchemy()

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=False, nullable=False)
    descripcion = db.Column(db.String(180), unique=False, nullable=False)
    imagen_url = db.Column(db.String(120), unique=True, nullable=False)
    imagen_alt = db.Column(db.String(120), unique=False, nullable=True)
    parrafo_descripcion_1 = db.Column(db.String(120), unique=False, nullable=False)
    parrafo_descripcion_2 = db.Column(db.String(120), unique=False, nullable=False)
    precio = db.Column(db.Integer, unique=False, nullable=False)
    imagenes = db.relationship('ImagenProducto', back_populates='producto', lazy='dynamic')

class ImagenProducto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ruta_imagen = db.Column(db.String(255), nullable=False)
    imagen_alt = db.Column(db.String(255), nullable=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    producto = db.relationship('Producto', back_populates='imagenes')

class Carruselbanner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alt = db.Column(db.String(80), unique=False, nullable=False)
    url = db.Column(db.String(120), unique=False, nullable=False)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    admin = db.Column(db.Boolean(), unique=False, nullable=False)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()], description="Va encima de la imagen de producto destacado")
    parrafo_descripcion_1 = TextAreaField('Descripción', validators=[DataRequired()], description="Primer parrafo de la visualizacion")
    parrafo_descripcion_2 = TextAreaField('Descripción', validators=[DataRequired()], description="Segundo parrafo de la visualizacion")
    precio = IntegerField('Precio', validators=[DataRequired()])
    imagen = FileField('Imagen del Producto', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp', 'svg'], 'Imágenes solamente!'), DataRequired()])
    imagen_alt = StringField('Alt de la imagen')
    submit = SubmitField('Crear Producto')

class ProductoImagenForm(FlaskForm):
    imagen = FileField('Imagen del Producto', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp', 'svg'], 'Imágenes solamente!'), DataRequired()])
    imagen_alt = StringField('Alt de la imagen')
    submit = SubmitField('Subir Imágenes')

class BannerForm(FlaskForm):
    alt = StringField('Alt de la imagen', validators=[DataRequired()])
    imagen = FileField('Imagen del Producto', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp', 'svg'], 'Imágenes solamente!')])
    submit = SubmitField('Crear Banner')


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inrol.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static/images/productos')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # por ejemplo, 16 megabytes
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db.init_app(app)

def producto_a_dict(producto):
    return {
        'id': producto.id,
        'nombre': producto.nombre,
        'descripcion': producto.descripcion,
        'imagen_url': producto.imagen_url,
        'imagen_alt': producto.imagen_alt,
        'parrafo_descripcion_1': producto.parrafo_descripcion_1,
        'parrafo_descripcion_2': producto.parrafo_descripcion_2,
        'precio': producto.precio
        # Añade más campos según sea necesario
    }

def producto_imgen_dict(imagen):
    return {
        'id': imagen.id,
        'ruta': imagen.ruta_imagen,
        'alt': imagen.imagen_alt,
        'producto_id': imagen.producto_id,    # Añade más campos según sea necesario
    }

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def index():
    productos = Producto.query.all()
    banners = Carruselbanner.query.all()
    return render_template('index.html', productos=productos, banners=banners)

@app.route('/ver-producto/<int:id>', methods=['GET'])
def ver_producto(id):
    imagenes = ImagenProducto.query.filter_by(producto_id=id).all()
    producto = Producto.query.get_or_404(id)
    producto_dict = producto_a_dict(producto)
    imagen_dict = [producto_imgen_dict(imagen) for imagen in imagenes]
    return render_template('productos.html', productos=jsonify(producto_dict).json,  imagenes=jsonify(imagen_dict).json)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(nombre=username).first()
        # Aquí deberías validar las credenciales con tu base de datos
        if user and user.nombre == username and user.password == password and user.admin:
            user = User(username)
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
    flash("Credenciales incorrectas")
    return render_template('login.html') # Asegúrate de tener un template de login

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')


@app.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        descripcion = form.descripcion.data
        imagen_alt = form.imagen_alt.data
        imagen_archivo = form.imagen.data
        parrafo_descripcion_1 = form.parrafo_descripcion_1.data
        parrafo_descripcion_2 = form.parrafo_descripcion_2.data
        precio = form.precio.data
        filename = secure_filename(imagen_archivo.filename)
        imagen_archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        nuevo_producto = Producto(nombre=nombre, descripcion=descripcion, imagen_url=filename, imagen_alt=imagen_alt, parrafo_descripcion_1=parrafo_descripcion_1, parrafo_descripcion_2=parrafo_descripcion_2, precio=precio)
        db.session.add(nuevo_producto)
        db.session.commit()

        flash('Producto creado con éxito!', 'success')
        return redirect(url_for('index'))

    return render_template('agregar_producto.html', form=form)

@app.route('/nueva-miniatura/<int:id>', methods=['GET', 'POST'])
@login_required
def configurar_imagenes(id):
    form = ProductoImagenForm()
    if form.validate_on_submit():
        imagen_archivo = form.imagen.data
        imagen_alt = form.imagen_alt.data
        nombre_archivo = secure_filename(imagen_archivo.filename)
        directorio = os.path.join(app.config['UPLOAD_FOLDER'], 'miniaturas')
        imagen_archivo.save(os.path.join(directorio, nombre_archivo))

        nueva_imagen = ImagenProducto(ruta_imagen=nombre_archivo, imagen_alt=imagen_alt, producto_id=id)
        db.session.add(nueva_imagen)
        db.session.commit()
        return redirect(url_for('configurar_imagenes', id=id))
    
    return render_template('agregar_imagen_producto.html', form=form)

@app.route('/miniaturas/<int:id>', methods=['GET'])
@login_required
def mostrar_miniaturas(id):
    miniaturas = ImagenProducto.query.filter_by(producto_id=id).all()
    producto = Producto.query.get_or_404(id)
    return render_template('mostrar_miniaturas.html', miniaturas=miniaturas, producto=producto)


@app.route('/nuevo-banner', methods=['GET', 'POST'])
@login_required
def nuevo_banner():
    form = BannerForm()
    if form.validate_on_submit():
        imagen_alt = form.alt.data
        imagen_archivo = form.imagen.data
        nombre_archivo = secure_filename(imagen_archivo.filename)
        imagen_archivo.save(os.path.join(os.path.dirname(__file__), 'static/images/banners', nombre_archivo))

        nuevo_banner = Carruselbanner(alt=imagen_alt, url=nombre_archivo)
        db.session.add(nuevo_banner)
        db.session.commit()
        flash('Nuevo banner agregado')
        return redirect(url_for('index'))
    return render_template('agregar_banner.html', form=form)

@app.route('/productos')
@login_required
def mostrar_productos():
    productos = Producto.query.all()
    banners = Carruselbanner.query.all()
    return render_template('mostrar_productos.html', productos=productos, banners=banners)


@app.route('/eliminar_producto/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    imagen_path = os.path.join('static/images/productos', producto.imagen_url)
    if os.path.exists(imagen_path):
        os.remove(imagen_path)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('mostrar_productos'))

@app.route('/eliminar_miniatura/<int:id>', methods=['POST'])
@login_required
def eliminar_miniatura(id):
    miniatura = ImagenProducto.query.get_or_404(id)
    imagen_path = os.path.join('static/images/productos/miniaturas', miniatura.ruta_imagen)
    if os.path.exists(imagen_path):
        os.remove(imagen_path)
    db.session.delete(miniatura)
    db.session.commit()
    return redirect(url_for('mostrar_productos'))

@app.route('/eliminar_banner/<int:id>', methods=['POST'])
@login_required
def eliminar_banner(id):
    banner = Carruselbanner.query.get_or_404(id)
    banner_path = os.path.join('static/images/banners', banner.url)
    if os.path.exists(banner_path):
        os.remove(banner_path)
    db.session.delete(banner)
    db.session.commit()
    return redirect(url_for('mostrar_productos'))

@app.route('/editar_producto/<int:id>', methods=['GET'])
@login_required
def editar_producto_form(id):
    producto = Producto.query.get_or_404(id)
    return render_template('editar_producto.html', producto=producto)

@app.route('/actualizar_producto/<int:id>', methods=['POST'])
@login_required
def actualizar_producto(id):
    producto = Producto.query.get_or_404(id)
    
    imagen_file = request.files['imagen']
    print(imagen_file.filename)
    if imagen_file.filename != '':
        imagen_nombre = secure_filename(imagen_file.filename)
        imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], imagen_nombre)
        
        # Eliminar la imagen anterior si existe
        imagen_anterior_path = os.path.join(app.config['UPLOAD_FOLDER'], producto.imagen_url)
        if os.path.exists(imagen_anterior_path):
            os.remove(imagen_anterior_path)
        
        # Guardar la nueva imagen
        imagen_file.save(imagen_path)
        producto.imagen_url = imagen_nombre  # Esta es la asignación correcta
    
    # Actualizar otros campos del producto
    producto.nombre = request.form['nombre']
    producto.descripcion = request.form['descripcion']
    # La línea problemática ha sido eliminada
    db.session.commit()
    return redirect(url_for('mostrar_productos'))








if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

