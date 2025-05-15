from datetime import date
from pymongo import MongoClient
from flask import Flask, render_template, request
from models.usuario import Usuario

app = Flask(__name__)

cliente = MongoClient('mongodb+srv://jbarrui587:6KWZHOFEh4LQdT1i@tutorial.vqartjr.mongodb.net/')

app.db = cliente.gestion_tienda

productos = [producto for producto in app.db.productos.find({})]
clientes = [ usuario for usuario in app.db.usuarios.find({})]

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
for cliente in clientes:
    if cliente['activo']:
        total_activos += 1

cliente_max = ''
pedido_max = 0
for cliente in clientes:
    if cliente['pedidos'] > pedido_max:
        pedido_max = cliente['pedidos']
        cliente_max = cliente['nombre']

ingreso_total = 0
for pedido in pedidos:
    ingreso_total += pedido['total']

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():

    # Información en forma de variables para pasar a la plantilla html.

    nombre_admin = "Francisco"
    tienda = "TecnoMarket"
    fecha = date.today()

    # Calculo las variables de la información que pide en la práctica para pasarla a la plantilla.

    # Se devuelve a la plantilla con el return toda la información necesaria en la plantilla html.
    return render_template('dashboard.html', nombre_admin=nombre_admin, tienda=tienda, fecha=fecha, productos=productos,
                           clientes=clientes, pedidos=pedidos, total_stock=total_stock, total_activos=total_activos,
                           cliente_max=cliente_max, ingreso_total=ingreso_total)


@app.route('/añadir-productos', methods=['GET', 'POST'])
def añadir_productos():
    global productos

    if request.method == 'POST':
        nombre_formulario = request.form.get('nombre')
        precio_formulario = float(request.form.get('precio'))
        stock_formulario = int(request.form.get('stock'))
        categoria_formulario = request.form.get('categoria')
        diccionario_producto_nuevo ={
            'nombre' : nombre_formulario,
            'precio' : precio_formulario,
            'stock' : stock_formulario,
            'categoría' : categoria_formulario
        }

        productos.append(diccionario_producto_nuevo)
        app.db.productos.insert_one(diccionario_producto_nuevo)
    return render_template('añadir_productos.html')

@app.route('/productos')
def mostrar_productos():

    return render_template('productos.html', productos=productos, total_stock=total_stock)

@app.route('/añadir-usuarios')
def añadir_usuarios():
    global clientes

    if request.method == 'POST':
        nombre_formulario = request.form.get('nombre')
        email_formulario = request.form.get('email')
        contraseña_formulario = request.form.get('contraseña')

        usuario = Usuario(nombre_formulario, email_formulario, contraseña_formulario, date.today())
        app.db.usuarios.insert_one(usuario)
    return render_template('añadir_usuarios.html')
if __name__ == '__main__':
    app.run()
