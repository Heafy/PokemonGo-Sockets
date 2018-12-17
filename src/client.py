#!/usr/bin/python3

from PIL import Image
from tempfile import mkstemp
from shutil import move
from os import fdopen, remove
import socket
import sys

# Crea un socket nulo
s = None
userId = None
# Archivo de texto con la información de los usuarios
userFile = "usr/users.txt"

# Los 151 Pokemon de la 1ra generación
pokemonArray = ["Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", 
"Charizard", "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", 
"Butterfree", "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", 
"Rattata", "Raticate", "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", 
"Raichu", "Sandshrew", "Sandslash", "Nidoran♀", "Nidorina", "Nidoqueen", 
"Nidoran♂", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", 
"Ninetales", "Jigglypuff", "Wigglytuff", "Zubat", "Golbat", "Oddish", 
"Gloom", "Vileplume", "Paras", "Parasect", "Venonat", "Venomoth", "Diglett", 
"Dugtrio", "Meowth", "Persian", "Psyduck", "Golduck", "Mankey", "Primeape", 
"Growlithe", "Arcanine", "Poliwag", "Poliwhirl", "Poliwrath", "Abra", 
"Kadabra", "Alakazam", "Machop", "Machoke", "Machamp", "Bellsprout", 
"Weepinbell", "Victreebel", "Tentacool", "Tentacruel", "Geodude", "Graveler", 
"Golem", "Ponyta", "Rapidash", "Slowpoke", "Slowbro", "Magnemite", "Magneton", 
"Farfetch’d", "Doduo", "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", 
"Shellder", "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee", 
"Hypno", "Krabby", "Kingler", "Voltorb", "Electrode", "Exeggcute", 
"Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan", "Lickitung", 
"Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela", "Kangaskhan", 
"Horsea", "Seadra", "Goldeen", "Seaking", "Staryu", "Starmie", "Mime", 
"Scyther", "Jynx", "Electabuzz", "Magmar", "Pinsir", "Tauros", "Magikarp", 
"Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon", "Flareon", 
"Porygon", "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", 
"Articuno", "Zapdos", "Moltres", "Dratini", "Dragonair", "Dragonite", 
"Mewtwo", "Mew"]

# Método auxiliar para enviar un Código 32
# Envía el mensaje para terminar la conexión con el servidor
def endConnection():
    clientMessage = "32"
    s.send(clientMessage.encode())

# Método para mostrar los usuarios registrados
def readUsers():
    with open(userFile) as fp:  
        line = fp.readline()
        while line:
            lineArr = line.split("*")
            print(lineArr[0] + " " + lineArr[1])
            line = fp.readline()

# Método para remplazar una cadena en un archivo
# No entiendo bien que hace, lo encontré en StackOverflow
def replace(file, oldString, newString):
    #Crea un archivo de usuarios temporal
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file) as old_file:
            for line in old_file:
                new_file.write(line.replace(oldString, newString))
    #Elimina el archivo actual
    remove(file)
    #Mueve el nuevo archivo
    move(abs_path, file)  

# Método que actualiza los Pokemons atrapados por el usuario
def updatePokemon(idUser, idPokemon):
     with open(userFile) as fp:  
        line = fp.readline()
        while line:
            # TODO ARREGLAR SALTOS DE LINEA AL AGREGAR POKEMON
            lineArr = line.split("*")
            if(str(idUser) == lineArr[0]):
                newline = line
                 # Quita los saltos de linea
                newline = newline[:len(newline)-1]
                newline += "-" + str(idPokemon) + "\n"
                replace(userFile, line, newline)
                print("Pokemones atrapados por %s" % str(lineArr[1]))
                catchedPokemon = lineArr[2].split("-")
                for x in catchedPokemon:
                    index = int(x)
                    print("* %s" % pokemonArray[index])
                # Muestra el último Pokemon capturado
                print("* %s" % pokemonArray[idPokemon])
            line = fp.readline()

# Método para procesar la entrada del usuario
def processIdInput():
    try:
        global userId
        userInput = input(">")
        userInput = int(userInput)
        userId = userInput
        clientMessage = "5"
        s.send(clientMessage.encode())
        if(userId < 1 or userId > 5):
            print("ID no válido")
            clientMessage = "40"
            s.send(clientMessage.encode())
    except:
        print("Respuesta no válida")
        clientMessage = "40"
        s.send(clientMessage.encode())

# Método para procesar los mensajes del servidor
# Cada mensajes es una secuencia de números separados por un guión
def processServerMessage(serverMessage):
    serverMessage = serverMessage.decode()
    serverMessageArr = serverMessage.split("-")
    if(serverMessageArr[0] == "5"):
        print("Selecciona el id de un usuario para empezar:")
        readUsers()
        processIdInput()
    if(serverMessageArr[0] == "20"):
        idPokemon = int(serverMessageArr[1])
        print("¡Un %s salvaje ha aparecido!" % pokemonArray[idPokemon])
        print("¿Deseas capturarlo? [Si/No] ")
        processClientInput(2, idPokemon, None)
    elif(serverMessageArr[0] == "21"):
        numAttemps = serverMessageArr[2]
        idPokemon = int(serverMessageArr[1])
        print("¿Intentar capturar de nuevo?")
        print("Quedan %s intento(s)" % numAttemps)
        processClientInput(4, idPokemon, numAttemps)
    elif(serverMessageArr[0] == "22"):
        idPokemon = int(serverMessageArr[1])
        print("Has capturado a %s" % pokemonArray[idPokemon])
        updatePokemon(userId, idPokemon)
        # Muestra la imagen del Pokemon
        img = Image.open('img/'+str(idPokemon+1)+'.png')
        img.show()
        endConnection()
    elif(serverMessageArr[0] == "23"):
        print("Intentos agotados")
        endConnection()
    elif(serverMessageArr[0] == "31"):
        print("No quisiste capturar el Pokemon")
        endConnection()
    elif(serverMessageArr[0] == "32" or serverMessageArr[0] == "40"):
        print("Fin de la conexión")
        s.close()
        exit()

# Método que procesa la entrada del usuario para enviarla 
# como códigos al servidor
# La entrada solo debe consistir en [Si/No]
def processClientInput(stateNumber, idPokemon, numAttemps):
    userInput = input(">")
    userInput = userInput.upper()
    if(userInput == "SI" or userInput == "S"):
        # Codigo 30: Dirige al estado 3
        if(stateNumber == 2):
            # Código 30: code - stateNumber - idPokemon - numAttemps
            clientMessage = "30-" + str(idPokemon) + "-" + str(3)
        elif(stateNumber == 4):
            clientMessage = "30-" + str(idPokemon) + "-" + numAttemps
    elif(userInput == "NO" or userInput == "N"):
        # Codigo 31: Dirige al estado 6
        clientMessage = "31"
    else:
        # Estado de error
        print("Respuesta no válida")
        clientMessage = "40"
    s.send(clientMessage.encode())

# Método main
# Inicializa la conexión y pone a la escucha de los mensajes del servidor
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
        print("El servidor no acepta conexiones por el puerto %d" % PORT)
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
    # Se mantiene a la escucha de los mensajes del servidor
    while True:
        serverMessage = s.recv(1024)
        processServerMessage(serverMessage)

if __name__ == "__main__":
    main()