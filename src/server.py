#!/usr/bin/python3
import random
import socket  
import _thread

# Metodo para intentar atrapar un Pokemon
def catchPokemon(clientSocket, idPokemon, numAttemps):
    numAttemps = int(numAttemps)
    numAttemps -= 1
    if(numAttemps == 0):
        # Código 23: code
        serverMessage = "23"
        print("Sin intentos para atrapar el pokemon")
    # Decide aleatoriamente si se captura el Pokemón o no
    elif(random.choice([True, False])):
        # Código 22: code - idPokemon
        serverMessage = "22-" + idPokemon
        print("Pokemon atrapado")
    else:
        # Código 21: code - idPokemon - numAttemps
        serverMessage = "21-" + idPokemon + "-" + str(numAttemps)
        print("Fallo al intentar capturar Pokemon")
    clientSocket.send(serverMessage.encode())

# Método para procesar los mensajes del cliente
# Cada mensaje es una secuencia de números separados por un guión
def processClientMessage(clientSocket, clientMessage):
    clientMessage = clientMessage.decode()
    clientMessageArr = clientMessage.split("-")
    # Codigo 10: Solicita al servidor el inicio de la aplicación
    if(clientMessageArr[0] == "10"):
        print("Código 10 recibido")
        # Código 5: code
        serverMessage = "5"
        clientSocket.send(serverMessage.encode())
         print("Código 5 enviado")
    elif(clientMessageArr[0] == "5"):
        # Se obtiene un id de un pokemon aleatorio
        idPokemon = random.randrange(151)
        # Codigo 20: code - idPokemon
        serverMessage = "20-" + str(idPokemon)
        clientSocket.send(serverMessage.encode())
        print("Codigo 20 enviado")
    # Codigo 30: Si quiere atrapar al pokemon
    elif(clientMessageArr[0] == "30"):
        print("Código 30 recibido")
        catchPokemon(clientSocket, clientMessageArr[1], clientMessageArr[2])
        print("Intento de atrapar el Pokemon")
    # Codigo 31: No quiso atrapar al pokemon
    elif(clientMessageArr[0] == "31"):
        print("Código 31 recibido")
        serverMessage = "31"
        clientSocket.send(serverMessage.encode())
        print("Código 31 enviado")
    # Código 32: Intentos agotados
    elif(clientMessageArr[0] == "32"):
        print("Código 32 recibido")
        serverMessage = "32"
        clientSocket.send(serverMessage.encode())
        print("Código 32 enviado")
    # Codigo 40: Error para dirigir a estados finales
    elif(clientMessageArr[0] == "40"):
        print("Código 40 recibido")
        serverMessage = "40"
        clientSocket.send(serverMessage.encode())
        print("Código 40 enviado")
        clientSocket.close()

# Método para cada thread
# Se mantiene a la escucha de los mensajes de los clientes
def run(clientSocket):
    while True:
        try:
            clientMessage = clientSocket.recv(1024)
        except:
            print("Fin de la conexión")
            break
        processClientMessage(clientSocket, clientMessage)

# Metodo main
# Inicializa el socket del servidor
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
    # Mantiene el servidor en ejecución
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