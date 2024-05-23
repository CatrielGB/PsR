import socket
import threading

# Lista de clientes conectados y un bloqueo para sincronizar el acceso a la lista.
clientes = []
clientes_lock = threading.Lock()

def difundir_mensaje(mensaje, conexion_remitente):
    """
    Envía un mensaje a todos los clientes conectados excepto al remitente.
    """
    with clientes_lock:
        for cliente in clientes:
            if cliente != conexion_remitente:
                try:
                    cliente.sendall(mensaje)
                except:
                    cliente.close()
                    clientes.remove(cliente)

def manejar_cliente(conexion, direccion):
    """
    Maneja la comunicación con un cliente individual.
    """
    global clientes
    with clientes_lock:
        # Agrega el nuevo cliente a la lista de clientes conectados.
        clientes.append(conexion)
        print(f"Conexión establecida con {direccion}. Total de clientes conectados: {len(clientes)}")
        # Notifica a todos los clientes sobre el nuevo cliente conectado.
        for cliente in clientes:
            cliente.sendall(f"Cliente {direccion} conectado. Total de clientes: {len(clientes)}".encode())

    # Envía un mensaje de conexión exitosa al nuevo cliente.
    conexion.sendall("Conectado satisfactoriamente".encode())

    try:
        while True:
            datos = conexion.recv(1024)
            if not datos:
                break

            mensaje = datos.decode()
            print(f"Recibido de {direccion}: {mensaje}")

            if mensaje.lower() == "logout":
                break

            if mensaje.startswith('#'):
                difundir_mensaje(datos, conexion)
            else:
                conexion.sendall(datos)
    finally:
        with clientes_lock:
            # Remueve el cliente de la lista de clientes conectados.
            clientes.remove(conexion)
            print(f"Conexión cerrada por {direccion}. Total de clientes conectados: {len(clientes)}")
            # Notifica a todos los clientes sobre la desconexión del cliente.
            for cliente in clientes:
                cliente.sendall(f"Cliente {direccion} desconectado. Total de clientes: {len(clientes)}".encode())
        conexion.close()

def iniciar_servidor(host='localhost', puerto=12345):
    """
    Inicia el servidor y escucha conexiones entrantes.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind((host, puerto))
        servidor.listen()
        print(f"Servidor escuchando en {host}:{puerto}")

        while True:
            # Acepta una nueva conexión.
            conexion, direccion = servidor.accept()
            # Crea un nuevo hilo para manejar la conexión del cliente.
            hilo_cliente = threading.Thread(target=manejar_cliente, args=(conexion, direccion))
            hilo_cliente.start()

if __name__ == "__main__":
    iniciar_servidor()
