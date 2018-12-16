#!/usr/bin/python3
import random
import socket  
import _thread                                    

def run(clientSocket):
    clientMessage = clientSocket.recv(1024)
    processClientMessage(clientSocket, clientMessage)

# Método para procesar los mensajes del cliente
# Cada mensaje es una secuencia de números separados por un guión
def processClientMessage(clientSocket, clientMessage):
    clientMessage = clientMessage.decode()
    clientMessageArr = clientMessage.split("-")
    # Solicita al servidor un Pokemon para capturar
    if(clientMessageArr[0] == "10"):
        # Se obtiene un id de un pokemon aleatorio
        idPokemon = random.randrange(151)
        # Codigo 20: code - idPokemon
        serverMessage = "20-" + str(idPokemon)
        print("Codigo 20 enviado")
        clientSocket.send(serverMessage.encode())

def main():
    # Crea un socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # Obtiene el nombre del equipo sobre el que se ejecuta
    HOST = '127.0.0.1'                          
    PORT = 9999                                           
    # Bind del socket al puerto
    serversocket.bind((HOST, PORT))                                  
    # A la escucha de hasta 5 sockets
    serversocket.listen(5)

    print("Servidor escuchando...")
    while True:
        # Establece una conexión
        clientSocket,addr = serversocket.accept()
        print("Conexion de %s" % str(addr))  

        serverMessage = "Conectado al servidor"
        clientSocket.send(serverMessage.encode())
        # Usa un thread para cada conexion
        try:
            _thread.start_new_thread(run, (clientSocket,))  
        except:
            print ("Error: No es posible inicializar el thread")
    clientSocket.close()

if __name__ == "__main__":
    main()