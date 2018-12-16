#!/usr/bin/python3
import random
import socket                                      
# Crea un socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# Obtiene el nombre del equipo sobre el que se ejecuta
HOST = '127.0.0.1'                          
PORT = 9999                                           
# Bind del socket al puerto
serversocket.bind((HOST, PORT))                                  
# A la escucha de hasta 5 sockets
serversocket.listen(5)

def run():
    clientMessage = clientSocket.recv(1024)
    clientMessage = clientMessage.decode()
    print("Mensaje cliente: " + clientMessage)

def processClientMessage(clientMessage):
    pass

print("Servidor escuchando...")
while True:
    # Establece una conexión
    clientSocket,addr = serversocket.accept()
    print("Conexion de %s" % str(addr))  

    serverMessage = "Conectado al servidor"
    clientSocket.send(serverMessage.encode())
    run()   
clientSocket.close()