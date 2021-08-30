
import time

import datetime

from playsound import playsound

from random import randint

from threading import Thread

from Proyecto_Pokemon.archivo_pokemon_juan import *  

from Proyecto_Pokemon.archivo_pokemon_peti import *

from Proyecto_Pokemon.archivo_pokemon_lore import *







class Entrenador:
	def __init__(self,nombre):
		self.nombre_entrenador = nombre
		self.lista_pokemones = []
	
	def agregar_pokemon(self,pokemon):
		self.lista_pokemones.append(pokemon)

class Estadio:
	def __init__(self,entrenador1,entrenador2,entrenador3):
		self.juan = entrenador1
		self.peti = entrenador2
		self.lore = entrenador3
		


	def buscar_pokemon(self,entrenador):
		
		if entrenador.nombre_entrenador == "Juan":	
			#archivo juan que trae el objeto pokemon seleccionado aleatoriamente
			objeto_limpiador = Limpieza_juan("Proyecto_Pokemon/ExtraFiles/pokemon.csv","Proyecto_Pokemon/CleanedFiles/NUEVO.csv")
			objeto_limpiador.limpieza_de_archivo()
			pokemon_comun_hallado = Pokemon_juan("Proyecto_Pokemon/CleanedFiles/NUEVO.csv")
			self.juan.agregar_pokemon(pokemon_comun_hallado)

		elif entrenador.nombre_entrenador == "Peti":
			csv_limpio = Limpiador_peti("Proyecto_Pokemon/ExtraFiles/pokemon.csv","Proyecto_Pokemon/CleanedFiles/NUEVO_PETI")
			lista_columnas = [32,30,28,19,25,33,34,35,40,39]
			csv_limpio.copiar_columnas(lista_columnas)
			master_ball = Pokeball_peti(csv_limpio)
			pokemon_peti = master_ball.atrapar()
			self.peti.agregar_pokemon(pokemon_peti)
			#archivo peti que trae el objeto pokemon 

		else:
			csv_limpio = LimpiadorCsv("Proyecto_Pokemon/ExtraFiles/pokemon.csv", "Proyecto_Pokemon/CleanedFiles/pokemon_parseado_lore.csv")
			pokemon_hallado = Pokemon("Proyecto_Pokemon/CleanedFiles/pokemon_parseado_lore.csv")
			self.lore.agregar_pokemon(pokemon_hallado)
			
	def ataque(self,atacante, posibles_defensores):
		#Primero hallamos al defensor
	
		if len(posibles_defensores)==2:
			pos_defensor = randint(0,1)
		else:
			pos_defensor=0
		defensor = posibles_defensores[pos_defensor]
		print(f"Oh no! El objetivo del ataque será {defensor.name}")
		esperanza_ataque = max(int(atacante.attack) - int(defensor.defense), int(atacante.special_attack) - int(defensor.special_defense))
		if esperanza_ataque <= 0:
			esperanza_ataque = 1	
		defensor.hp = int(defensor.hp)
		defensor.hp -= esperanza_ataque
		print(f"{defensor.name} recibió {esperanza_ataque} de daño por parte de {atacante.name}, quedando con {defensor.hp}")
		return

	def pelea(self):

		pokj = self.juan.lista_pokemones[0]
		pokp = self.peti.lista_pokemones[0]
		pokl = self.lore.lista_pokemones[0]
		diccionario  = {pokj:self.juan,pokp:self.peti,pokl:self.lore}
		print("                                                             ¡COMIENZA EL ENFRENTAMIENTO POKÉMON!")
		print("\n")
		print(f"Juan saca su {pokj.name}!")
		print(f"Parece que Peti decidió sacar su icónico {pokp.name}!")
		print(f"Y Lore encarará esta batalla con un {pokl.name}")
		#Se da la pelea calculando quien es el atacante, cuanto daño hace, y a quien
		frecuencia = min(float(pokj.speed),float(pokp.speed),float(pokl.speed))
		lista_participantes = [pokj, pokp, pokl]
		fecha_inicio = datetime.datetime.now()
		time.sleep(3)
		while True:
			#Calculamos quien es el atacante
			participantes = set(lista_participantes)
			velocidades = {pokj : float(pokj.speed), pokp : float(pokp.speed), pokl : float(pokl.speed)}
			#objeto,velocidad
			#print("velocidades: {}".format(velocidades))
			prioridades = {velocidades[pokj] : pokj, velocidades[pokp] : pokp, velocidades[pokl] : pokl}
			#velocidad, objeto
			velocidad_atacante = max(velocidades[pokj], velocidades[pokp], velocidades[pokl])
			#velocidad maxima de ataque
		
			atacante = prioridades[velocidad_atacante]
			#guarda objeto con maximo speed

			participantes.remove(atacante)
			#saca el pokemon atacante de la lista de los tres objetos
			print("\n")
			print(f"{atacante.name} está realizando un ataque...")

			#Se define a quien ataca, y cuanto daño hace
			participantes = list(participantes)
			#lista de tres objetos pokemon
			time.sleep(5)
			self.ataque(atacante, participantes)
			#llamamos a la funcion ataque con los parametros del obj con max speed y los obj defensores
			atacante.speed = int(atacante.speed)
			atacante.speed -= frecuencia

			#Verificamos si murió algún Pokémon, y si no se termina la pelea
			for pokemon in lista_participantes:
				if int(pokemon.hp) <= 0:
					lista_participantes.remove(pokemon)
					pokemon.speed = float("-inf")
					fecha_muerte = datetime.datetime.now()
					dif = fecha_muerte - fecha_inicio
					print(f"Oh no! {pokemon.name} ha quedado fuera de combate a los {dif.seconds} segundos desde que comenzo el combate")
					print("\n")
					time.sleep(3)

			if len(lista_participantes) == 1:
				break

		ganador = lista_participantes[0] #objeto pokx
		duracion = datetime.datetime.now()- fecha_inicio 
		print(f"Duracion de pelea:{duracion.seconds} segundos")
		time.sleep(3)
		print("El ganador de la batalla es: {} con su {}".format(diccionario[ganador].nombre_entrenador,ganador.name))		

		self.juan.lista_pokemones.remove(pokj)
		self.peti.lista_pokemones.remove(pokp)
		self.lore.lista_pokemones.remove(pokl)







class Music:
	def __init__(self,path):
		self.path = path
		self.thread()

	def thread(self):

		def play_sound():
			playsound(self.path)

		self.thread = Thread(target=play_sound)
	
	def play_music(self):
		self.thread.start()





#callings

Juan = Entrenador("Juan")
Peti = Entrenador("Peti")
Lore = Entrenador("Lore")

estadio_boca = Estadio(Juan,Peti,Lore)

estadio_boca.buscar_pokemon(Juan)
estadio_boca.buscar_pokemon(Peti)
estadio_boca.buscar_pokemon(Lore)


music = Music("Proyecto_Pokemon/ExtraFiles/musica_batalla.mp3")
music.play_music()


#fight
estadio_boca.pelea()
