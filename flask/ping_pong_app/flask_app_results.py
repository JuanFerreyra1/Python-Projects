from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from flask import Flask, Response
import csv
import io
import pandas as pd
import os

app = Flask(__name__,template_folder="templates")


host = os.getenv("HOST_APP_PING_PONG")
user = os.getenv("USER_APP_PING_PONG")
password = os.getenv("PASSWORD_APP_PING_PONG")
database = os.getenv("DATABASE_APP_PING_PONG")



@app.route('/')
def index():

    return render_template('index.html')


@app.route('/options', methods=['GET'])
def options():

    return render_template('options.html')


@app.route('/statistics', methods=['GET'])
def statistics():

    return render_template('/statistics.html')


@app.route('/load_of_results', methods=['GET'])
def load_of_results():

    return render_template('/load_of_results.html')



@app.route('/analytics', methods=['POST'])
def analytics():

    db_connection= mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
        )
    cursor = db_connection.cursor()
    cursor.execute('''
                    SELECT 
                        jugador,
                        COUNT(*) AS partidos_jugados,
                        SUM(resultado = 'gano') AS partidos_ganados,
                        CONCAT((SUM(resultado = 'gano') / COUNT(*)) * 100, '%') AS rendimiento
                    FROM (
                        SELECT 'Nu' AS jugador, resultado FROM Nu
                        UNION ALL
                        SELECT 'Fede' AS jugador, resultado FROM Fede
                        UNION ALL
                        SELECT 'Ingfe' AS jugador, resultado FROM Ingfe
                        UNION ALL
                        SELECT 'Bru' AS jugador, resultado FROM Bru
                        UNION ALL
                        SELECT 'Iancin' AS jugador, resultado FROM Iancin
                    ) AS t
                    GROUP BY jugador
                    ORDER BY partidos_ganados DESC
    ''')
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=['nombre', 'partidos_jugados', 'partidos_ganados', 'rendimiento'])
    table_html = df.to_html(index=False)
    cursor.close()

    return render_template('analytics.html', table=table_html)



@app.route('/login', methods=['POST'])
def login():

    nombre_de_usuario = request.form['username']
    contrasena = request.form['apassword']
    
    db_connection= mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
        )
    conn = db_connection

    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE name = %s AND password = %s', (nombre_de_usuario, contrasena))


    usuario_db = cursor.fetchone()
  
    cursor.close()
    
    if usuario_db:
        return render_template('options.html',nombre_de_usuario = nombre_de_usuario)
    else:
        message = "Usuario o contraseña incorrecto"
        return render_template('index.html',message = message)



@app.route('/resultado', methods=['POST'])
def resultado():
    usuario1 = request.form['jugador1']
    resultado1 = request.form['resultado1']
    usuario2 = request.form['jugador2']
    resultado2 = request.form['resultado2']
    try:
        int(resultado1)
        int(resultado2)
    except:
        message = "Datos de carga erroneos"
        return render_template('load_of_results.html',message = message)
    if usuario1 == usuario2:
        message = "Estas colocando un unico jugador"
        return render_template('load_of_results.html',message = message)
    if int(resultado1) > 21 or int(resultado2)>21:
        message2 = "El maximo puntaje por partido para un jugador es 21"
        return render_template('load_of_results.html',message2 = message2)
    
    
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
        )
    cursor = conn.cursor()


    resultado_palabra_1 = str()
    resultado_palabra_2 = str()


    if int(resultado1) > int(resultado2):
        resultado_palabra_1 = 'gano'
        resultado_palabra_2 = 'perdio'  
    else:
        resultado_palabra_1 = 'perdio'
        resultado_palabra_2 = 'gano'

    insert_query1 = f"""
    INSERT INTO {usuario1} (puntos_del_partido,contrincante,resultado) 
    VALUES ({resultado1},'{usuario2}','{resultado_palabra_1}')""".format(usuario1=usuario1,resultado1=resultado1,usuario2=usuario2,resultado_palabra_1 = resultado_palabra_1)
    
    insert_query2 = f"""
    INSERT INTO {usuario2} (puntos_del_partido,contrincante,resultado) 
    VALUES ({resultado2},'{usuario1}','{resultado_palabra_2}')""".format(usuario2=usuario2,resultado2=resultado2,usuario1=usuario1,resultado_palabra_2 = resultado_palabra_2)

    cursor.execute(insert_query1)
    cursor.execute(insert_query2)
    conn.commit()

    cursor.close()
    conn.close()
    message1 = "Carga exitosa"

    return render_template('load_of_results.html',message1 = message1)
    

if __name__ == '__main__':
    app.run(debug=True)