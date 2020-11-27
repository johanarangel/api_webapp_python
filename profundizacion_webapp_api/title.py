#!/usr/bin/env python
'''
Heart DB manager
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Programa creado para administrar la base de datos de registro
de pulsaciones de personas
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.1"

import os
import sqlite3
import requests
import json

db = {}


def create_schema():

    # Conectarnos a la base de datos
    # En caso de que no exista el archivo se genera
    # como una base de datos vacia
    conn = sqlite3.connect(db['database'])

    # Crear el cursor para poder ejecutar las querys
    c = conn.cursor()

    # Obtener el path real del archivo de schema
    script_path = os.path.dirname(os.path.realpath(__file__))
    schema_path_name = os.path.join(script_path, db['schema'])

    # Crar esquema desde archivo
    c.executescript(open(schema_path_name, "r").read())

    # Para salvar los cambios realizados en la DB debemos
    # ejecutar el commit, NO olvidarse de este paso!
    conn.commit()

    # Cerrar la conexión con la base de datos
    conn.close()

def fill():
    
    response = requests.get("https://jsonplaceholder.typicode.com/todos")
    response_data = response.json()

    group = []    
    for row in response_data:
        userId = row.get('userId')
        title = row.get('title')
        completed = row.get('completed')
        group.append((userId, title, completed))
        

    conn = sqlite3.connect(db['database'])
    c = conn.cursor()

    c.executemany("""
        INSERT INTO titulo (userId, title, completed)
        VALUES (?,?,?);""", group)

    conn.commit()
    conn.close()   # Cerrar la conexión con la base de datos


def title_completed_count(userId):
    
    conn = sqlite3.connect(db['database'])
    c = conn.cursor()

    c.execute("""
                SELECT COUNT(id) as titulos_completados, userId FROM titulo
                WHERE completed = '1' AND userId=?;""", userId)

    query_results = c.fetchall()

    conn.commit()
    conn.close()

    total_completed = [x[0] for x in query_results]
    usuario_id = [x[1] for x in query_results]

    return total_completed, usuario_id

def comparacion_user():

    conn = sqlite3.connect(db['database'])
    c = conn.cursor()

    c.execute("""SELECT COUNT(id) as titulos_completados, userId FROM titulo WHERE completed = '1' GROUP BY userId;""")

    query_results = c.fetchall()

    conn.commit()
    conn.close()

    total_completed = [x[0] for x in query_results]
    usuario_id = [x[1] for x in query_results]

    return total_completed, usuario_id

def comparacion():

    conn = sqlite3.connect(db['database'])
    c = conn.cursor()

    c.execute("""SELECT COUNT(id) as titulos_completados, userId FROM titulo WHERE completed = '1' GROUP BY userId;""")

    query_results = c.fetchall()

    conn.commit()
    conn.close()

    total_completed = [x[0] for x in query_results]
    usuario_id = [x[1] for x in query_results]

    return total_completed, usuario_id

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def report(limit=0, offset=0, dict_format=False):
    # Conectarse a la base de datos
    conn = sqlite3.connect(db['database'])
    if dict_format is True:
        conn.row_factory = dict_factory
    c = conn.cursor()

    query = 'SELECT userId, title, completed  \
            FROM titulo'

    if limit > 0:
        query += ' LIMIT {}'.format(limit)
        if offset > 0:
            query += ' OFFSET {}'.format(offset)

    query += ';'

    c.execute(query)
    query_results = c.fetchall()

    # Cerrar la conexión con la base de datos
    conn.commit()
    conn.close()
    return query_results


