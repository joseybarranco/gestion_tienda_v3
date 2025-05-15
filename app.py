from datetime import datetime, date
from pymongo import MongoClient
from flask import Flask, render_template, request
from models.usuario import Usuario

app = Flask(__name__)

cliente = MongoClient('mongodb+srv://jbarrui587:6KWZHOFEh4LQdT1i@tutorial.vqartjr.mongodb.net/')

app.db = cliente.gestion_tienda

productos = [producto for producto in app.db.productos.find({})]
users = [usuario for usuario in app.db.usuarios.find({})]

pedidos = [
    {'cliente': 'Fran', 'total': 36.48, 'fecha': '24-10-2024'},
    {'cliente': 'Fran', 'total': 58.99, 'fecha': '10-1-2025'},
    {'cliente': 'Fran', 'total': 45.98, 'fecha': '5-3-2025'},
    {'cliente': 'José', 'total': 125.50, 'fecha': '20-2-2025'},
    {'cliente': 'Ana', 'total': 63.95, 'fecha': '13-5-2024'},
    {'cliente': 'Ana', 'total': 77.99, 'fecha': '8-9-2024'},
    {'cliente': 'Ana', 'total': 53.98, 'fecha': '16-12-2024'},
    {'cliente': 'Ana', 'total': 63.95, 'fecha': '5-2-2025'},
    {'cliente': 'Ana', 'total': 39.90, 'fecha': '22-5-2025'},
    {'cliente': 'Juan', 'total': 45.49, 'fecha': '1-4-2025'}
]
total_stock = 0
for producto in productos:
    total_stock += producto['stock']

total_activos = 0
for user in users:
    if  user['activo'] == "True":
        total_activos += 1

user_max = ''
pedido_max = 0
for user in users:
    if user['pedidos'] > pedido_max:
         pedido_max = user['pedidos']
         user_max = user ['nombre']

ingreso_total = 0
for pedido in pedidos:
    ingreso_total += pedido['total']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    # Información en forma de variables para pasar a la plantilla html.
    global total_activos
    nombre_admin = "Francisco"
    tienda = "TecnoMarket"
    fecha = date.today()

    # Calculo las variables de la información que pide en la práctica para pasarla a la plantilla.

    # Se devuelve a la plantilla con el return toda la información necesaria en la plantilla html.
    return render_template('dashboard.html', nombre_admin=nombre_admin, tienda=tienda, fecha=fecha, productos=productos,
                           clientes=users, pedidos=pedidos, total_stock=total_stock, total_activos=total_activos,
                           cliente_max=user_max, ingreso_total=ingreso_total)


@app.route('/añadir-productos', methods=['GET', 'POST'])
def añadir_productos():

    if request.method == 'POST':
        nombre_formulario = request.form.get('nombre')
        precio_formulario = float(request.form.get('precio'))
        stock_formulario = int(request.form.get('stock'))
        categoria_formulario = request.form.get('categoria')
        diccionario_producto_nuevo = {
            'nombre': nombre_formulario,
            'precio': precio_formulario,
            'stock': stock_formulario,
            'categoría': categoria_formulario
        }

        app.db.productos.insert_one(diccionario_producto_nuevo)
    return render_template('añadir_productos.html')


@app.route('/productos')
def mostrar_productos():
    return render_template('productos.html', productos=productos, total_stock=total_stock)


@app.route('/añadir-usuarios', methods=['GET', 'POST'])
def añadir_usuarios():
    mensaje=''
    if request.method == 'POST':
        fecha = date.today()
        fecha_clase = datetime.combine(fecha, datetime.min.time())
        nombre_usuario = request.form.get('nombre')
        email_formulario = request.form.get('email')
        contraseña_formulario = request.form.get('contraseña')
        activo_formulario = request.form.get('activo')
        pedidos_formulario = int(request.form.get('pedidos'))
        dict_usuario = {
            'nombre': nombre_usuario,
            'email': email_formulario,
            'contraseña': contraseña_formulario,
            'activo': activo_formulario,
            'pedidos': pedidos_formulario,
            'fecha': fecha_clase
        }

        usuario1 = Usuario(nombre_usuario, email_formulario, contraseña_formulario,activo_formulario, pedidos_formulario, fecha_clase )
        usuario_dict=dict(usuario1.__dict__)

        app.db.usuarios.insert_one(usuario_dict)
        mensaje ='Usuario añadido Correctamente,!!!!!Enhorabuena¡¡¡¡¡'
    return render_template('añadir_usuarios.html', mensaje=mensaje)

@app.route('/usuarios')
def mostrar_usuarios():
    global users
    global total_activos
    global total_stock
    global user_max

    return render_template('usuarios.html', clientes=users, total_activos=total_activos, user_max=user_max)

@app.route('/productos/<username>')
def perfil_productos(username):
    product_found = None
    for elemento in app.db.productos.find({}):
        if elemento['nombre'] == username:
            product_found = elemento
            break

    if product_found:
        return render_template('perfil_producto.html', product_found=product_found)

    else:
        return render_template('404.html')



if __name__ == '__main__':
    app.run()
