'''Introduction:
In this file i used requests package which allows me to make a connection with a server from python and make some actions such as
mofifying a register in the web page
import requests 
print('''
    ELija una opcion:
    1. Agregar un alumno.
    2. Modificar alumno existente.
    3. Listar alumnos.
    4. Eliminar un alumno.
    Coloque aqui el Nº:''')

while True:
    numero = input("Seleccione una opción: ")
    opciones = [1,2,3,4]
    if int(numero) in opciones:
        break

url = "http://localhost:7001/student"
def decision():
    if int(numero)==1:
        nombre = input("Coloque el nombre:")
        cursos = input("Coloque los cursos:")
        r = requests.post(url, json={"name":nombre, "courses":cursos})

        print("Código de estado:", r.status_code)    
        print("Contenido de la respuesta:", r.json())

        if r.status_code == 201:
            print("Alumno ingresado correctamente.")
        else:
            print("No se ha podido ingresar el alumno.")

    if int(numero)==2:
        valor_id = input("Coloque el ID para el cual vas a modificar datos:")
        valor_nombre = input("Coloque el nombre a agregar:")
        valor_cursos= input("Coloque los cursos a agregar:")
        valores_a_agregar = {"courses": valor_cursos,"name": valor_nombre}
        r = requests.put("http://localhost:7001/student/{val}".format(val=valor_id),json = valores_a_agregar)
        print("Código de estado:", r.status_code) 

        if r.status_code==204:
            print("Alumno modificado correctamente.")
        else:
            print("No se ha podido modificar el alumno.")
            

    if int(numero)==3:
        r = requests.get(url)
        lista_alumnos = r.json()["students"]

        if r.status_code==200:

            for x in lista_alumnos:
                nombre_a_exhibir,cursos_a_exhibir = x.get("name"),x.get("courses")
                print("Nombre: ",nombre_a_exhibir," Cursos: ",cursos_a_exhibir)
        else:
            print("Operacion no exitosa") 
   

        


    if int(numero)==4:

        valor_id = input("Coloque el ID para el cual vas a eliminar datos:")

        r = requests.delete("http://localhost:7001/student/{val}".format(val=valor_id))

        if r.status_code==204:
            print("Alumno/s eliminado/s correctamente") 
        else: 
            print("Algo salio mal, probablemente pusiste un id que no estaba en el servidor")


decision()