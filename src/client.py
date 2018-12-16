#!/usr/bin/python3

import socket
import sys

# Crea un socket nulo
s = None

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

def processServerMessage(serverMessage):
    serverMessage = serverMessage.decode()
    serverMessageArr = serverMessage.split("-")
    print(serverMessage)
    if(serverMessageArr[0] == "20"):
        idPokemon = int(serverMessageArr[1])
        print("¡Un " + pokemonArray[idPokemon] + " salvaje ha aparecido!")
        print("¿Deseas capturarlo? [Si/No] ")
        processClientInput(2)
    elif(serverMessage[0] == "31"):
        print("No quisiste capturar el Pokemon")

# Método que procesa la entrada del usuario para enviarla 
# como códigos al servidor
# La entrada solo debe consistir en [Si/No]
def processClientInput(stateNumber):
    userInput = input(">")
    userInput = userInput.upper()
    if(userInput == "SI" or userInput == "S"):
        # Codigo 30: Dirige al estado 3
        if(stateNumber == 2):
            clientMessage = "30-2"
    elif(userInput == "NO" or userInput == "N"):
        # Codigo 31: Dirige al estado 6
        if(stateNumber == 2):
            clientMessage = "31-2"
    else:
        # Estado de error
        print("Mensaje no válido")
        clientMessage = "40"
    s.send(clientMessage.encode())


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