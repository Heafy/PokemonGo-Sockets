#!/usr/bin/python3

import socket

# Crea un socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# Obtiene el nombre del equipo sobre el que se ejecuta
host = socket.gethostname()                           
# Puerto designado
port = 9999
print("Intentando conexión..")
# Conexión del host en el puerto
s.connect((host, port))                               

# Si la conexión se establece pasa al estado 1 mediante un código 10.
#stateCodeMsg = '10'
#s.send(stateCodeMsg.encode())
# Recupera los mensajes

serverMessage = s.recv(1024)
serverMessage = serverMessage.decode()

while serverMessage != "SERVIDOR>>> FINALIZAR":
    if not serverMessage:
        break
    print(serverMessage)
    clientMessage = input("CLIENTE>>> ")
    s.send(clientMessage.encode())
    serverMessage = s.recv(1024)
    serverMessage = serverMessage.decode()

s.close()
#print (msg.decode('ascii'))

# El cliente siempre debe de estar preparado para la entrada, es su unico trabajo
# Hacer una funcion para convertir de entrada a codigo dependiendo del estado