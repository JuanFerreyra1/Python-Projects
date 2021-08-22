#Tk es una clase y tk es la bibloteca que contiene esa clase

import tkinter as tk
import tkinter.font as tkfont
from tkinter import PhotoImage


from Dates.dates import *



class Aplicacion():
	def __init__(self,ventana):
		self.ventana = ventana
		self.ventana.title("Aplicacion Juan Ferreyra")
		self.ventana.geometry('1500x1500')
		self.frame = tk.Frame(ventana)
		self.creacion_de_widgets()




	def creacion_de_widgets(self):

		#imagen de fondo
		self.imagen = tk.PhotoImage(file="")
		self.etiqueta_imagen=tk.Label(image=self.imagen).place(x=10,y=150)


		#boton_inicio
		def boton_enviar_funcion():

			self.valores_login=[self.login_nombre.get(),self.login_constraseña.get()]
			self.ventana.destroy()
			global ventana2
			self.ventana2 = tk.Tk()
			self.frame2=tk.Frame(self.ventana2)
			self.ventana2.title("Aplicacion Juan Ferreyra")
			self.ventana2.geometry('1500x1500')	



			#ventana2
			self.boton_bienvenida = tk.Label(self.ventana2,text="Bienvenido {} {}".format(self.valores_login[0],self.valores_login[1])).pack()
			
			self.espacio_valores=tk.Listbox(bg="white",height=10,width=20)
			self.espacio_valores.place(x=205,y=20)


			def boton_inicial_funcion():

				self.espacio_valores.insert(1,"Year: {}".format(timestamp.year))
				self.espacio_valores.insert(2,"Month: {}".format(timestamp.month))
				self.espacio_valores.insert(3,"Day: {}".format(timestamp.day))
				self.espacio_valores.insert(4,"Hour: {}".format(timestamp.hour))
				self.espacio_valores.insert(5,"Minute: {}".format(timestamp.minute))
				self.espacio_valores.insert(6,"Second: {}".format(timestamp.second))
				self.espacio_valores.insert(7,"Microsecond: {}".format(timestamp.microsecond))

			
			self.boton_inicial = tk.Button(self.ventana2,text="Fecha actual",
				command=boton_inicial_funcion).place(x=0,y=20)



		#login
		#etiqueta bienvenida
		self.ingreso= tk.Label(self.ventana,text="COLOQUE SUS DATOS",font="Arial").place(x=80,y=5)
		
	
		self.etiqueta_login_nombre= tk.Label(self.ventana,text="NOMBRE",font="Arial").place(x=80,y=38)
		self.login_nombre=tk.Entry()
		self.login_nombre.place(x=200,y=38)

		self.etiqueta_login_contraseña= tk.Label(self.ventana,text="CONTRASEÑA",font="Arial").place(x=80,y=70)
		self.login_constraseña=tk.Entry()
		self.login_constraseña.place(x=200,y=70)
		

		self.boton_enviar= tk.Button(text="Enviar datos",width=10,command=boton_enviar_funcion).place(x=80,y=100)


ventana = tk.Tk()
app_de_juan = Aplicacion(ventana)
ventana.mainloop()

