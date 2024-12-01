import socket

# Configuración del cliente
HOST = '127.0.0.1'
PORT = 65432

def mostrar_menu():
    print("\n--- Menú de Opciones ---")
    print("1. Agregar Producto")
    print("2. Listar Productos")
    print("3. Buscar Producto")
    print("4. Salir")
    print("------------------------")

def ejecutar_opcion(opcion, client_socket):
    if opcion == '1':
        # Agregar un nuevo producto
        nombre = input("Nombre del producto: ")
        precio = input("Precio del producto: ")
        cantidad = input("Cantidad del producto: ")
        mensaje = f"AGREGAR;{nombre};{precio};{cantidad}"
        client_socket.sendall(mensaje.encode('utf-8'))
    
    elif opcion == '2':
        # Listar todos los productos
        client_socket.sendall("LISTAR".encode('utf-8'))

    elif opcion == '3':
        # Buscar un producto por nombre
        nombre = input("Nombre del producto a buscar: ")
        mensaje = f"BUSCAR;{nombre}"
        client_socket.sendall(mensaje.encode('utf-8'))

    elif opcion == '4':
        # Terminar la conexión
        client_socket.sendall("SALIR".encode('utf-8'))
        print("Cerrando conexión...")
        return False
    
    else:
        print("Opción no válida.")
    return True

# Crear el socket del cliente
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print("Conectado al servidor.")

    # Mantener la conexión hasta que el cliente decida salir
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        # Ejecutar la opción seleccionada
        continuar = ejecutar_opcion(opcion, client_socket)

        if not continuar:
            break

        # Recibir la respuesta del servidor solo si se envió una solicitud válida
        if opcion in ['1', '2', '3']:  # Evitamos recibir cuando la opción es inválida
            data = client_socket.recv(1024)
            print(f"\nRespuesta del servidor:\n{data.decode('utf-8')}")
