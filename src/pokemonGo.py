import random
from PIL import Image

# PokemonGO Local
# Estructura básica para el proyecto
# Los códigos de estado son representativos para el proyecto final

# Códigos de estado del cliente
# 10 Solicita al servidor por parte del cliente
stateCode10 = 10

# Códigos de estado del servidor 
# 20 ¿Capturar al Pokemon x?
stateCode20 = 20
# 21 ¿Intentar capturar de nuevo? 
stateCode21 = 21
# 22 Enviar Pokemon (imagen) capturado
stateCode22 = 22
# 23 Numero de intentos de captura agotados
stateCode23 = 23

# # Códigos de estado comunes del cliente y el servidor
# 30 Si
stateCode30 = 30
# 31 No
stateCode31 = 31
# 32 Terminando sesion 
stateCode32 = 32


print("Pokemon GO\n")

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

# Se escoje el id de Pokemon al azar
# pokemonChosen = pokemonArray[random.randrange(len(pokemonArray))]
idPokemon = random.randrange(len(pokemonArray))
# Número de intentos para atrapar un Pokemon
attemptNumber = 3

def s0():
    print("Inicia la conexión del protocolo de la capa de aplicación")
    return s1(stateCode10)

def s1(stateCode):
    print("¡Un " + pokemonArray[idPokemon] + " salvaje ha aparecido!")
    return s2(stateCode20)

def s2(stateCode):
    usrInput = input("¿Deseas capturarlo? [Si/No] ")
    usrInput = usrInput.upper()
    #print(usrInput)

    if(usrInput == "SI" or usrInput == "S"):
        #print("Quiere capturarlo")
        return s3(stateCode30)
    elif(usrInput == "NO" or usrInput == "N"):
        #print("No quiere capturarlo")
        return s6(stateCode31)
    else:
        print("Entrada incorrecta")
        # Estado de error
        return s6(0)

def s3(stateCode):
    global attemptNumber
    attemptNumber -= 1
    # Si se acaban los intentos pasa al estado 6
    if(attemptNumber == 0):
        return s6(stateCode23)
    # Si se captura va al s5
    elif(random.choice([True, False])):
        #print("Esto es verdadero")
        return s5(stateCode22, idPokemon)
    # En otro caso va al s4
    else:
        return s4(stateCode21, idPokemon, attemptNumber)

def s4(stateCode, idPokemon, numAttempts):
    usrInput = input("Intentar capturar de nuevo? Quedan " 
    + str(numAttempts) + " intento(s) ")
    usrInput = usrInput.upper()
    #print(usrInput)

    if(usrInput == "SI" or usrInput == "S"):
        #print("Quiere capturarlo")
        return s3(stateCode30)
    elif(usrInput == "NO" or usrInput == "N"):
        #print("No quiere capturarlo")
        return s6(stateCode31)
    else:
        print("Entrada incorrecta")
        # Estado de error
        return s6(0)

# Estado s5
# Se recibe el pokemon capturado y envía la imagen
def s5(stateCode, idPokemon):
    print("Has capturado a " + pokemonArray[idPokemon])
    print("Aquí debería imprimir la imagen")
    return s7(stateCode32)

# Estado s6 
# Se llega a este estado antes de terminar la conexion
# El parámetro es el código de estado recibido
def s6(stateCode):
    if(stateCode == stateCode23):
        print("Intentos agotados :(")
    if(stateCode == stateCode31):
        print("No quisiste capturar el Pokemon :(")
    print("Terminando la conexion")
    return s7(stateCode32)

# Estado s7
# Termina las conexion actual
# El código de estado siempre será 32   
def s7(stateCode):
    print("Estado 7")
    print("Conexión terminada")

s0()
#img = Image.open('test.jpg')
#img.show() 