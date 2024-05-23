import socket
import threading

def recibir_mensajes(sock):
    """
    Hilo que recibe mensajes del servidor y los muestra en pantalla.
    """
    while True:
        try:
            datos = sock.recv(1024)
            if not datos:
                break
            print(datos.decode())
        except:
            print("Conexión cerrada por el servidor")
            break

def iniciar_cliente(host='localhost', puerto=12345):
    """
    Inicia el cliente y permite la comunicación con el servidor.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((host, puerto))
        print("Conectado satisfactoriamente")

        # Crea un hilo para recibir mensajes del servidor.
        hilo_receptor = threading.Thread(target=recibir_mensajes, args=(cliente,))
        hilo_receptor.start()

        while True:
            mensaje = input()
            cliente.sendall(mensaje.encode())
            if mensaje.lower() == "logout":
                break

        cliente.close()
        hilo_receptor.join()

if __name__ == "__main__":
    iniciar_cliente()
