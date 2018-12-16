#!/usr/bin/python3

import socket
import sys

# Crea un socket nulo
s = None

def processServerMessage(serverMessage):
    serverMessage = serverMessage.decode()
    serverMessageArr = serverMessage.split("-")
    if(serverMessageArr[0] == "20"):
        print("¡Un " + serverMessageArr[1] + " salvaje ha aparecido!")

# Método que procesa la entrada del usuario para enviarla 
# como códigos al servidor
# La entrada solo debe consistir en [Si/No]
def processClientInput(stateNumber, userInput):
    pass

def main():
    print("Intentando conexión..")
    args = sys.argv
    # Revisa que los argumentos sean correctos
    if(len(args) != 3):
        print("Uso: python client.py <IP_SERVIDOR> <PUERTO>")
        exit()
    #Obtiene el host y el puerto desde los argumentos
    HOST = args[1]
    PORT = args[2]
    # Intenta crear el socket
    try:
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    except socket.error:
        print("Hubo un error al crear el socket")
        exit()
    # Verificacion del puerto
    PORT = int(PORT)
    if(PORT != 9999):
        print("El servidor no acepta conexiones por el puerto " + str(PORT))
        print("Intenta con el 9999")
        exit()
    # Conexion hacia el servidor con los parámetros dados
    try:
        s.connect((HOST, PORT))
        # Mensaje de confirmacion
        serverMessage = s.recv(1024)
        print(serverMessage.decode())
        # Codigo 10: code
        clientMessage = "10"
        s.send(clientMessage.encode())
    except:
        print("Conexion rechazada")
        exit()
    while True:
        serverMessage = s.recv(1024)
        processServerMessage(serverMessage)

if __name__ == "__main__":
    main()


#print (msg.decode('ascii'))

# El cliente siempre debe de estar preparado para la entrada, es su unico trabajo
# Hacer una funcion para convertir de entrada a codigo dependiendo del estado