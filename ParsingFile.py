__author__ = 'agustin.salas@sagalid.cl'

import os
import numpy as np
from termcolor import colored

filas = 0
columnas = 0
vectorCosto = []
matriz_a = [[]]


def parsear(nombre):
    try:
        inicio_lectura = iniciaMatrizYVectorCosto(nombre)
        poblarCoberturas(inicio_lectura, nombre)
        print('End file parsing: ' + str(nombre))
    except Exception as ex:
        print("\n\t" + colored(ex, "red"))

def iniciaMatrizYVectorCosto(nombre_archivo):
    linea_fin_vcosto = 1
    numeroLineas = 1
    global vectorCosto
    global filas
    global columnas

    rutaArchivo = os.path.join(os.path.dirname(__file__), nombre_archivo)
    archivo = open(rutaArchivo, 'r')
    lineas = archivo.readlines()
    #Iteración por cada una de las líneas del archivo.
    for li in lineas:
        if numeroLineas is 1:
            filas, columnas = map(int, li.split())
        if numeroLineas >= 2 and vectorCosto.__len__() <= (columnas - 1):
            #vectorCosto = vectorCosto + map(int, li.split())
            li = li.strip()
            lista = [int(x) for x in li.split(" ")]
            for cost in lista:
                vectorCosto.append(cost)
            linea_fin_vcosto += 1

        numeroLineas = numeroLineas + 1

    archivo.close()
    return linea_fin_vcosto


def poblarCoberturas(inicio, nombre_archivo):
    global matriz_a
    ruta_archivo = os.path.join(os.path.dirname(__file__), nombre_archivo)
    archivo = open(ruta_archivo, 'r')
    lineas = archivo.readlines()[inicio:]
    global cantidad_de_restricciones
    vector_restriccion = []
    matriz_restriccion = []
    cantidad_de_numeros = []
    nueva_restriccion = True

    cantidad_de_restricciones = 0
    for li in lineas:
        contadorDePalabras = map(int, li.split())
        cantidad_de_palabras = contadorDePalabras.__len__()
        cantidad_en_vector_restriccion = vector_restriccion.__len__()

        if cantidad_de_palabras is 1 and nueva_restriccion:
            cantidad_de_numeros = map(int, li.split())[0]
            nueva_restriccion = False

        if cantidad_en_vector_restriccion <= cantidad_de_numeros:
            vector_restriccion += map(int, li.split())
            cantidad_en_vector_restriccion = vector_restriccion.__len__()

        if cantidad_en_vector_restriccion - 1 == cantidad_de_numeros:
            matriz_restriccion.append(vector_restriccion[1:])
            vector_restriccion = []
            cantidad_de_restricciones += 1
            nueva_restriccion = True

    archivo.close()
    # print "cantidad de restricciones: " + str(cantidad_de_restricciones)

    matriz_a = np.zeros((filas, columnas), dtype=np.int)

    i = 0
    for row in matriz_restriccion:
        for j in row:
            if i < getCantidadFilas() and j < getCantidadColumnas():
                matriz_a[i][j] = 1

        i += 1

    #for row in matriz_a:
    #    print row


def getCantidadColumnas():
    return columnas


def getCantidadFilas():
    return filas


def getVectorCosto():
    return vectorCosto


def getMatrizA():
    return matriz_a

