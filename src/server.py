#!/usr/bin/python3
import random
import socket                                      

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

# Crea un socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# Obtiene el nombre del equipo sobre el que se ejecuta
host = socket.gethostname()                           
port = 9999                                           
# Bind del socket al puerto
serversocket.bind((host, port))                                  
# A la escucha de hasta 5 sockets
serversocket.listen(5)
# Número de intentos para atrapar un Pokemon
attemptNumber = 3

def run(clientsocket):
    s0(10, clientsocket)

# Estado s0
# Estado inicial, desde aquí iniciara la conexión del protocolo de la 
# capa de aplicación.
def s0(stateCode, clientsocket):
    message = "Conexion establecida\n"
    clientsocket.send(message.encode())
    return s1(10)

# Estado s1
# Recibe solicitud del cliente, ofrece aleatoriamente un Pokemon para capturar.
def s1(stateCode):
    message = "Un " + pokemonArray[idPokemon] + " salvaje ha aparecido!\n"
    clientsocket.send(message.encode())
    return s2(20)

# Estado s2
# Indica si quiere capturar o no el Pokemon ofrecido.
def s2(stateCode):
    message = "Deseas capturarlo? [Si/No] "
    clientsocket.send(message.encode())
    clientMessage = clientsocket.recv(1024)
    clientMessage = clientMessage.decode()
    clientMessage = clientMessage.upper()

    if(clientMessage == "SI" or clientMessage == "S"):
        #print("Quiere capturarlo")
        return s3(30)
    elif(clientMessage == "NO" or clientMessage == "N"):
        #print("No quiere capturarlo")
        return s6(31)
    else:
        print("Entrada incorrecta")
        # Estado de error
        return s6(40)

# Estado s3
# Usa el contador como el máximo número de intentos. Aleatoriamente indica
# si se capturó al Pokemon o no.
def s3(stateCode):
    global attemptNumber
    attemptNumber -= 1
    # Si se acaban los intentos pasa al estado 6
    if(attemptNumber == 0):
        return s6(23)
    # Decide aleatoriamente si se captura el Pokemón o no
    # Si se captura va al estado 5
    elif(random.choice([True, False])):
        return s5(22, idPokemon)
    # En otro caso va al s4
    else:
        return s4(21, idPokemon, attemptNumber)

# Estado s4
# Da respuesta para reintentar captura de Pokemon.
def s4(stateCode, idPokemon, numAttempts):
    message = "Intentar capturar de nuevo? Quedan " + str(numAttempts) + " intento(s)"
    clientsocket.send(message.encode())
    clientMessage = clientsocket.recv(1024)
    clientMessage = clientMessage.decode()
    clientMessage = clientMessage.upper()

    if(clientMessage == "SI" or clientMessage == "S"):
        #print("Quiere capturarlo")
        return s3(30)
    elif(clientMessage == "NO" or clientMessage == "N"):
        #print("No quiere capturarlo")
        return s6(31)
    else:
        print("Entrada incorrecta")
        # Estado de error
        return s6(0)

# Estado s5
# Se recibe el pokemon capturado y envía la imagen.
def s5(stateCode, idPokemon):
    print("Has capturado a " + pokemonArray[idPokemon])
    #print("Aquí debería imprimir la imagen")
    #img = Image.open('img/'+str(idPokemon+1)+'.png')
    #img.show() 
    return s7(32)

# Estado s6 
# Se llega a este estado antes de terminar la conexion
# El parámetro es el código de estado recibido
def s6(stateCode):
    message = ""
    if(stateCode == 23):
        message = "Intentos agotados \n"
    if(stateCode == 31):
        message = "No quisiste capturar el Pokemon \n"
    message2 = "Conexion terminada \n"
    message = message + message2
    clientsocket.send(message.encode())
    return s7(32)

# Estado s7
# Termina las conexion actual
# El código de estado siempre será 32   
def s7(stateCode):
    # TODO ARREGLAR ESTE MENSAJE DE FINALIZAR
    #message = "SERVIDOR>>> FINALIZAR"
    #clientsocket.send(message.encode())
    clientsocket.close()

print("Servidor escuchando...")
while True:
    # Establece una conexión
    clientsocket,addr = serversocket.accept()
    print("Conexion de %s" % str(addr))  

    # Se escoje el id de Pokemon al azar
    idPokemon = random.randrange(len(pokemonArray))

    run(clientsocket)

    #confirmMsg = 'Conexion establecida'+ "\r\n"
    #clientsocket.send(confirmMsg.encode('ascii'))
    clientsocket.close()

    # EL SERVIRO DEBE TENER UN METODO RUN PARA CADA CONEXION QUE MANEJE TODOS LOS ESTADOS COMO  EN EL LOCAL