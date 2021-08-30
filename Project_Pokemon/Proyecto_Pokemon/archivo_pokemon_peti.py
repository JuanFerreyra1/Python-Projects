import random
import csv

class Limpiador_peti:
     
    def __init__(self, archivo, archivo_nuevo):
        self.arch_completo = archivo
        self.arch_nuevo = archivo_nuevo

    @staticmethod
    def leer_registro(csv):
        linea = csv.readline()
        registro = linea.rstrip('\n').split(',')
        return registro

    def copiar_columnas(self, lista_columnas):
        
        csv_completo = open(self.arch_completo, "r", encoding="UTF-8")
        csv_nuevo = open(self.arch_nuevo, "w+", encoding="UTF-8", newline='')



        csv_reader = csv.reader(csv_completo)
        csv_writer = csv.writer(csv_nuevo)
        for registro in csv_reader:
            atributos = []
            for columna in lista_columnas:
                atributos.append(registro[columna])
            csv_writer.writerow(atributos)
        
        csv_completo.close()
        csv_nuevo.close()

    def obtener_columnas(self):
        csv_completo = open(self.arch_completo,"r+", encoding="UTF-8")
        lista_descripciones =  self.leer_registro(csv_completo)
        diccionario_elementos = {}
        i = 0
        for elemento in lista_descripciones:
            diccionario_elementos[i] = elemento
            i += 1
        csv_completo.close()
        for elemento in diccionario_elementos:
            print(f"{diccionario_elementos[elemento]}: {elemento}")

class Pokeball_peti:
    def __init__(self, csv_limpio):
        self.pokedex = csv_limpio.arch_nuevo
    
    @staticmethod
    def leer_registro(csv):
        linea = csv.readline()
        registro = linea.rstrip('\n').split(',')
        return registro

    def atrapar(self): 
        pokedex = open(self.pokedex, "r", encoding="UTF-8")
        num = random.randint(0,801)
        linea_descriptiva = self.leer_registro(pokedex)
        for i in range(0,num):
            lista_atributos = self.leer_registro(pokedex)
        diccionario = {}
        j = 0
        for elemento in linea_descriptiva:
            diccionario[elemento] = lista_atributos[j]
            j += 1
        pokemon = Pokemon_peti(diccionario)
        return pokemon

class Pokemon_peti:
    def __init__(self, dicc_atributos):

        self.pocket_number = dicc_atributos["pokedex_number"]
        self.name = dicc_atributos["name"]
        self.hp = dicc_atributos["hp"]
        self.attack = dicc_atributos["attack"]
        self.defense = dicc_atributos["defense"]
        self.special_attack = dicc_atributos["sp_attack"]
        self.special_defense = dicc_atributos["sp_defense"]
        self.speed = dicc_atributos["speed"]
        self.is_legendary = dicc_atributos["is_legendary"]
        self.generation = dicc_atributos["generation"]
        

