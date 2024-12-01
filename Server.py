import socket
import sqlite3

# Funciones para la base de datos
def crear_tabla_productos():
    """Crea la tabla de productos si no existe."""
    conn = sqlite3.connect('productos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            cantidad INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def agregar_producto(nombre, precio, cantidad):
    """Agrega un producto a la base de datos."""
    conn = sqlite3.connect('productos.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO productos (nombre, precio, cantidad) VALUES (?, ?, ?)', (nombre, precio, cantidad))
    conn.commit()
    conn.close()

def listar_productos():
    """Devuelve una lista de todos los productos."""
    conn = sqlite3.connect('productos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return productos

def buscar_producto(nombre):
    """Busca un producto por nombre."""
    conn = sqlite3.connect('productos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE nombre = ?', (nombre,))
    producto = cursor.fetchone()
    conn.close()
    return producto

# Configuración del servidor
HOST = '127.0.0.1'
PORT = 65432

# Crear la base de datos y la tabla si no existen
crear_tabla_productos()

# Iniciar el servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Servidor escuchando en {HOST}:{PORT}...")

    conn, addr = server_socket.accept()
    with conn:
        print(f"Conectado por {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            mensaje = data.decode('utf-8').split(';')
            comando = mensaje[0]
            print(f"Cliente: {comando}")

            if comando.upper() == 'SALIR':
                print("Cerrando conexión...")
                conn.sendall("Conexión cerrada.".encode('utf-8'))
                break

            elif comando.upper() == 'LISTAR':
                productos = listar_productos()
                if productos:
                    respuesta = '\n'.join([f"{p[1]}, Precio: {p[2]}, Cantidad: {p[3]}" for p in productos])
                else:
                    respuesta = "No hay productos disponibles."
                conn.sendall(respuesta.encode('utf-8'))

            elif comando.upper() == 'BUSCAR':
                nombre_producto = mensaje[1]
                producto = buscar_producto(nombre_producto)
                if producto:
                    respuesta = f"Producto: {producto[1]}, Precio: {producto[2]}, Cantidad: {producto[3]}"
                else:
                    respuesta = "Producto no encontrado"
                conn.sendall(respuesta.encode('utf-8'))

            elif comando.upper() == 'AGREGAR':
                nombre, precio, cantidad = mensaje[1], float(mensaje[2]), int(mensaje[3])
                agregar_producto(nombre, precio, cantidad)
                respuesta = f"Producto {nombre} agregado con éxito."
                conn.sendall(respuesta.encode('utf-8'))

            else:
                conn.sendall("Comando no reconocido".encode('utf-8'))
