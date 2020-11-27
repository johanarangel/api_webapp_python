#!/usr/bin/env python


__author__ = "Inove Coding School"
__email__ = "INFO@INOVE.COM.AR"
__version__ = "1.1"

# Realizar HTTP POST --> post.py

import traceback
import io
import sys
import os
import base64
import json
import sqlite3
from datetime import datetime, timedelta
import requests

import numpy as np
from flask import Flask, request, jsonify, render_template, Response, redirect
import matplotlib
matplotlib.use('Agg')   # Para multi-thread, non-interactive backend (avoid run in main loop)
import matplotlib.pyplot as plt
# Para convertir matplotlib a imagen y luego a datos binarios
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg

import title
from config import config


# Crear el server Flask
app = Flask(__name__)

# Clave que utilizaremos para encriptar los datos
app.secret_key = "flask_session_key_inventada"

# Obtener la path de ejecución actual del script
script_path = os.path.dirname(os.path.realpath(__file__))

# Obtener los parámetros del archivo de configuración
config_path_name = os.path.join(script_path, 'config.ini')
db = config('db', config_path_name)
server = config('server', config_path_name)

# Enviar los datos de config de la DB
title.db = db

@app.route("/")
def index():
    try:
        # Imprimir los distintos endopoints disponibles
        result = "<h1>Bienvenido!!</h1>"
        result += "<h2>Endpoints disponibles:</h2>"
        result += "<h3>[GET] /reset ----> borrar y crear la base de datos</h3>"
        result += "<h3>[GET] /registro --> acción que completa la base de datos con el json request proveniente de la URL</h3>"
        result += "<h3>[GET] /tabla_api ----> se muestra el api en una tabla proveniente de la url: https://jsonplaceholder.typicode.com/todos</h3>"
        result += "<h3>[GET] /user/{id}/titles--> muestra cuántos titulos completó el usuario cuyo id es el pasado como parámetro</h3>"
        result += "<h3>[GET] /user/graph --> comparativa de cuántos títulos completó cada usuario en un gráfico</h3>"
        result += "<h3>[GET] /user/comparativa --> mostrar cuántos títulos completó cada usuario en un gráfico</h3>"
        return(result)
    except:
        return jsonify({'trace': traceback.format_exc()})

@app.route("/reset")
def reset():
    try:
        # Borrar y crear la base de datos
        title.create_schema()
        result = "<h3>Base de datos re-generada!</h3>"
        return (result)
    except:
        return jsonify({'trace': traceback.format_exc()})
        

@app.route("/registro", methods=['GET'])
def registro():
    #se completa la base de datos con los datos de la URL 
    if request.method == 'GET': 
        try:
            title.fill()
            return render_template('llenado.html')

        except:
            return jsonify({'trace': traceback.format_exc()})


@app.route("/tabla_api")
def tabla_api():
    pass
    try:
        return render_template('registro.html')
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/user/<id>/titles")
def user_titles(id):
    try:
        total_completed, usuario = title.title_completed_count(id) 
        return render_template('usertitle.html', total_completed = total_completed, usuario = usuario)
        
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/user/graph")
def comparativa():
    
    try:
        title_completed, user_id = title.comparacion_user()
      
        fig, ax = plt.subplots(figsize=(16, 9))
        fig.suptitle('"Gráfico comparativo: titulos completados por usuario"', fontsize=18)
    
        ax.bar(user_id, title_completed, color='darkcyan')
        ax.set_facecolor('mintcream')
        ax.set_xlabel('Usuarios', fontsize=15)
        ax.set_ylabel('Cantidad de titulos completados', fontsize=15)
        ax.get_xaxis().set_visible(True)

    # Convertir ese grafico en una imagen para enviar por HTTP
    #     y mostrar en el HTML
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        plt.close(fig)  # Cerramos la imagen para que no consuma memoria del sistema
        return Response(output.getvalue(), mimetype='image/png')
    except:
        return jsonify({'trace': traceback.format_exc()})

@app.route("/user/comparativa")
def tabla_comparativa():

    try:
        data_completed, data_id = title.comparacion()

        fig, ax = plt.subplots(figsize=(16, 9))
        fig.suptitle('"Gráfico comparativo: titulos completados por usuario"', fontsize=18)
    
        ax.plot(data_id, data_completed, color='red', marker='.')
        ax.set_facecolor('mintcream')
        ax.set_xlabel('Id usuarios', fontsize=15)
        ax.set_ylabel('Cantidad de titulos completados', fontsize=15)
        ax.get_xaxis().set_visible(True)

    # Convertir ese grafico en una imagen para enviar por HTTP
        # y mostrar en el HTML
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        plt.close(fig)  # Cerramos la imagen para que no consuma memoria del sistema
        return Response(output.getvalue(), mimetype='image/png')
                          
    except:
        return jsonify({'trace': traceback.format_exc()})
    
if __name__ == '__main__':
    print('Subiendo el primer programa desde la nube!')
    comparativa()
    #Lanzar server
    app.run(host=server['host'],
            port=server['port'],
            debug=True)