#!/usr/bin/python3
import random
import socket  
import _thread

def catchPokemon(attemptNumber):
    print("Método para intentar atrapar pokemones")

# Método para procesar los mensajes del cliente
# Cada mensaje es una secuencia de números separados por un guión
def processClientMessage(clientSocket, clientMessage):
    clientMessage = clientMessage.decode()
    clientMessageArr = clientMessage.split("-")
    # Codigo 10: Solicita al servidor un Pokemon para capturar
    if(clientMessageArr[0] == "10"):
        print("Código 10 recibido")
        # Se obtiene un id de un pokemon aleatorio
        idPokemon = random.randrange(151)
        # Codigo 20: code - idPokemon
        serverMessage = "20-" + str(idPokemon)
        print("Codigo 20, estado 1 enviado")
        clientSocket.send(serverMessage.encode())
    # Codigo 30: Si quiere atrapar al pokemon
    elif(clientMessageArr[0] == "30"):
        print("Código 30 recibido")
        # Inicia el intento de atrapar el Pokemon con 3 intentos
        if(clientMessageArr[1] == "2"):
            catchPokemon(3)
    # Codigo 31: No quiso atrapar al pokemon
    elif(clientMessageArr[0] == "31"):
        print("Código 31 recibido")
        serverMessage = "31"
        if(clientMessageArr[1] == "2"):
            serverMessage += "-2"
            print("Código 31, estado 2 enviado")
        elif(clientMessageArr[1] == "4"):
            serverMessage += "-4"
            print("Código 31, estado 4 enviado")
        clientSocket.send(serverMessage.encode())
    # Codigo 40: Error para dirigir a estados finales
    elif(clientMessageArr[0] == "40"):
        print("Código 40 recibido")

def run(clientSocket):
    while True:
        clientMessage = clientSocket.recv(1024)
        processClientMessage(clientSocket, clientMessage)

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