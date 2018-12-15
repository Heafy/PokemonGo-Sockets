#!/usr/bin/python3

import socket

# Método para procesar la entrada del usuario
# La entrada solo será [SI/NO]
# Dependiendo de la entrada devuelve el código de estado
# En otro caso envía al estado de error
def processInput(userInput, actualState):
    userInput = userInput.upper()

# Crea un socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# Obtiene el nombre del equipo sobre el que se ejecuta
host = socket.gethostname()                           
# Puerto designado
port = 9999
print("Intentando conexión")
# Conexión del host en el puerto
s.connect((host, port))                               
print("¡Conectado al servidor!")

# Si la conexión se establece pasa al estado 1 mediante un código 10.
stateCodeMsg = '10'
s.send(stateCodeMsg.encode())

msg = s.recv(1024)
msg = msg.decode()
print(msg)
usrInput = input("")
usrInput = usrInput.upper()

s.close()
#print (msg.decode('ascii'))

# El cliente siempre debe de estar preparado para la entrada, es su unico trabajo
# Hacer una funcion para convertir de entrada a codigo dependiendo del estado