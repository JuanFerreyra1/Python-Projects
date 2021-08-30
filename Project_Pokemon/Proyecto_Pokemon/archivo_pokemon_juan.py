import csv

#1era clase
class Limpieza_juan():


	def __init__ (self,nombre_archivo_sucio,nombre_archivo_limpio):
		self.nombre_archivo_sucio = nombre_archivo_sucio
		self.nombre_archivo_limpio = nombre_archivo_limpio
		self.limpieza_de_archivo()
	
	def limpieza_de_archivo(self):

		
		with open("{}".format(self.nombre_archivo_sucio),"r") as f:
			with open('{}'.format(self.nombre_archivo_limpio),'w+') as csvfile:
				while True:
					
					try:
						self.line = f.readline()
						self.line = self.line.split(",") #me genera un string con 41 casilleros, cada uno un campo 

						csvfile.write("{},{},{},{},{},{},{},{},{},{}".format(self.line[-11],
							self.line[-9],self.line[-13],self.line[-22],self.line[-16],self.line[-8],
							self.line[-7],self.line[-6],self.line[-2],self.line[-1]))
					except:
						break		


#objeto_limpiador = Limpieza("pokemon.csv","NUEVO.csv")

#2da clase
class Seleccion_de_pokemon_juan():
	
	
	def __init__(self,nombre_del_contenedor):
		self.nombre_del_contenedor = nombre_del_contenedor
		self.seleccion_pokemon_aleatorio()
		#self.seleccion_pokemon_legendario_aleatorio()




	
	def seleccion_pokemon_aleatorio(self):
		import random

		self.count=0
		self.conteo=0

		with open("{}".format(self.nombre_del_contenedor),"r") as lectura: #conteo de reg. y num aleatorio.
			self.recorrido = csv.reader(lectura)
			for x in self.recorrido:
				self.count = self.count+1 #calculo cantidad de registros
			#print(self.count)
			self.num_ale = random.randrange(2,self.count,1)
		
		with open("{}".format(self.nombre_del_contenedor),"r") as lectura: #registro coincidente	
			while True:
				l = lectura.readline()
				self.conteo=self.conteo+1
				if self.num_ale == self.conteo: #aca cuando un registro es igual al random...
					self.registro_coincidente = l	
					break
	
		#mostrar string
		self.registro_coincidente = self.registro_coincidente.split(",")








	def seleccion_pokemon_legendario_aleatorio(self):
		import random
		self.count=0
		self.conteo=0
		self.c=0
		self.reg_pok_leg=[]

		#nos quedamos con los pokemones que son legendarios
		with open("{}".format(self.nombre_del_contenedor),"r") as lectura1: 
			
			lectura = csv.reader(lectura1)
			for x in lectura:
				if x[-1].strip() != "" and x[-1].strip()!="is_legendary":
					if int(x[-1].strip()) == 1:
						self.reg_pok_leg.append(x)
			
		
		import random #buscamos el pokemon legendario por aleatoridad
		self.numero_random = random.randrange(1,len(self.reg_pok_leg),1)

		self.elemento=0   #buscamos el registro coincidente
		for x in self.reg_pok_leg:
			self.elemento=self.elemento+1
			if self.elemento==self.numero_random:
				self.registro_coincidente_pok_lg = x

		#mostrar string



#3ra clase
class Pokemon_juan(Seleccion_de_pokemon_juan):
	def __init__(self,nombre_del_contenedor):
		super().__init__(nombre_del_contenedor)
		self.name = self.registro_coincidente[0]
		self.pocket_number = self.registro_coincidente[1]
		self.hp = self.registro_coincidente[2]
		self.attack = self.registro_coincidente[3]
		self.defense = self.registro_coincidente[4]
		self.special_attack = self.registro_coincidente[5]
		self.special_defense = self.registro_coincidente[6]
		self.speed = self.registro_coincidente[7]
		self.generation = self.registro_coincidente[8]
		self.is_legendary = self.registro_coincidente[9]


	def MisAtributos(self):
		print("Pokemon aleatorio: {}\nPocket Number: {}\nhp:{}\nattack:{}\ndefense:{}\nspecial attack:{}\nspecial defense:{}\nspeed:{}\ngeneration:{}\nIsLegendary:{}"
					.format(self.name,self.pocket_number,
					self.hp,self.attack,self.defense,
					self.special_attack,self.special_defense,self.speed,self.generation,self.is_legendary))


class PokemonLegendario_juan(Seleccion_de_pokemon_juan):
	def __init__(self,nombre_del_contenedor):
		super().__init__(nombre_del_contenedor)	
		self.name2 = self.registro_coincidente_pok_lg[0]
		self.pocket_number2 = self.registro_coincidente_pok_lg[1]
		self.hp2 = self.registro_coincidente_pok_lg[2]
		self.attack2 = self.registro_coincidente_pok_lg[3]
		self.defense2 = self.registro_coincidente_pok_lg[4]
		self.special_attack2 = self.registro_coincidente_pok_lg[5]
		self.special_defense2 = self.registro_coincidente_pok_lg[6]
		self.speed2 = self.registro_coincidente_pok_lg[7]
		self.generation2 = self.registro_coincidente_pok_lg[8]
		self.is_legendary2 = self.registro_coincidente_pok_lg[9]
	
	def MisAtributos(self):
				print("Pokemon aleatorio: {}\nPocket Number: {}\nhp:{}\nattack:{}\ndefense:{}\nspecial attack:{}\nspecial defense:{}\nspeed:{}\ngeneration:{}\nIsLegendary:{}"
					.format(self.name2,self.pocket_number2,
					self.hp2,self.attack2,self.defense2,
					self.special_attack2,self.special_defense2,self.speed2,self.generation2,self.is_legendary2))







#llamadas
#objeto_limpiador = Limpieza_juan("pokemon.csv","NUEVO.csv")







#OBJETO POKEMON COMUN
#def define_objeto():

	#pokemon_comun_hallado = Pokemon_juan("NUEVO.csv")
	
#print(pokemon_comun_hallado.name)
#print(pokemon_comun_hallado)
#OBJETO POKEMON LEGENDARIO
#pokemon_legendario_hallado = PokemonLegendario_juan("NUEVO.csv")


#pokemon_comun_hallado = Pokemon_juan("NUEVO.csv")
#pokemon_comun_hallado.MisAtributos()

'''
por ejemplo, si yo quiero conocer el nombre del pokemon legendario hallado
puedo acceder a la propiedad del mismo objeto:
'''
#print(pokemon_legendario_hallado.name2)

''' por ejemplo, si yo quiero invocar el metodo del objeto pokemon legendario el cual es capaz
de mostrar sus atributos:
'''
#pokemon_legendario_hallado.MisAtributos()

