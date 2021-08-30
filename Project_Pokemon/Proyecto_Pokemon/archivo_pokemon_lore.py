import csv

class LimpiadorCsv:
    def __init__(self, archivo_original, archivo_parseado):

        self.archivo_original = archivo_original
        self.archivo_parseado = archivo_parseado
        self.limpiar_csv() #esto se lo paso para que me permita pasarle el nombre de los archivos en la llamada
    #metodo que limpia el csv
    def limpiar_csv(self):

        datos = []

        with open(self.archivo_original, "r", newline='', encoding='UTF-8') as file:
            with open(self.archivo_parseado, "w+") as f:
                lector_csv = csv.reader(file)

                for linea in lector_csv:
                    datos.append(
                        [linea[32], linea[30], linea[28], linea[19], linea[25], linea[33], linea[34], linea[35],
                         linea[40], linea[39]])

                escritor_csv = csv.writer(f)
                escritor_csv.writerows(datos)

#clase que selecciona un pokemon de los registros de forma aleatoria
class Pokebola():

    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.obtener_pokemon()

    def obtener_pokemon(self):
        import random

        with open ("{}".format(self.nombre_archivo), "r") as lectura:
            num_random = random.randint(0, 801)

            for x in range(0, num_random):
                registro = lectura.readline()
                self.registro_encontrado = registro

            self.registro_encontrado = self.registro_encontrado.split(",")

class Pokemon(Pokebola):

    def __init__(self, nombre_archivo):

        super().__init__(nombre_archivo)
        self.pocket_number = self.registro_encontrado[0]
        self.name = self.registro_encontrado[1]
        self.hp = self.registro_encontrado[2]
        self.attack = self.registro_encontrado[3]
        self.defense = self.registro_encontrado[4]
        self.special_attack = self.registro_encontrado[5]
        self.special_defense = self.registro_encontrado[6]
        self.speed = self.registro_encontrado[7]
        self.is_legendary = self.registro_encontrado[9]
        self.generation = self.registro_encontrado[8]


    def Atributos(self):

        print("Pokedex number: {}, Name: {}, HP: {}, Attack: {}, Defense: {}, Sp atk: {}, Sp def: {}, Speed: {}, Is legendary: {}, Generation: {}".format(self.pokedex_number,
        self.name, self.hp, self.attack, self.defense, self.sp_atk, self.sp_def, self.speed, self.is_legendary, self.generation))


#se genero un archivo con nombre (2do parametro) limpio
#csv_limpio = LimpiadorCsv("pokemon.csv", "pokemon_parseado_lore.csv")

#pokemon_hallado = Pokemon("pokemon_parseado_lore.csv")
#print(pokemon_hallado)



























 


