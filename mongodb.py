'''
Fecha: 20 de octubre del 2022
'''
# Clase para conectarnos a MongoDB

import pymongo
from conf import vars

class PyMongo():
    def __init__(self, variables):
        self.MONGO_URL = 'mongodb://'+vars["host"]+':'+vars["port"]
        self.MONGO_DATABASE = variables["bd"]
        self.MONGO_TIMEOUT = variables["timeout"]
        self.MONGO_CLIENT = None
        self.MONGO_RESPUESTA = None

    def conectar_mongodb(self):
        try:
            self.MONGO_CLIENT = pymongo.MongoClient(self.MONGO_URL, serverSelectionTimeOutMS = self.MONGO_TIMEOUT) # Conectado

        except Exception as error:
            print(error)
        else:
            # print('Conexión al servidor de MongoDB realizada')
            pass

    def desconectar_mongodb(self):
        if self.MONGO_CLIENT:
            self.MONGO_CLIENT.close()

    def consulta_mongodb(self, collection, filtro, atributos={"_id":0}):
        response = {"status": False, "resultado": []}
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][collection].find(filtro, atributos)
        if self.MONGO_RESPUESTA:
            response["status"] = True
            for reg in self.MONGO_RESPUESTA:
                response["resultado"].append(reg)
        return response


        # for reg in self.MONGO_RESPUESTA:
        #     print(reg)

    def insertar(self, collection, document):
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][collection].insert_one(document)
        if self.MONGO_RESPUESTA:
            return self.MONGO_RESPUESTA
        return None

    def actualizar(self, collection, filtro, new_values):
        response = {"status": False}
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][collection].update_many(filtro, new_values)
        if self.MONGO_RESPUESTA:
            response = {"status": True}
            # return self.MONGO_RESPUESTA
        # return None
        return response

    def eliminar(self, collection, filtro):
        response = {"status": False}
        self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE][collection].delete_many(filtro)
        if self.MONGO_RESPUESTA:
            response = {"status": True}
            # return self.MONGO_RESPUESTA
        # return None
        return response

    def cargar_datos(self):
        obj_estudiante = PyMongo(vars)
        obj_estudiante.conectar_mongodb()

        for ctrl, nom in Estudiantes():
            dicc = {}
            dicc["control"] = ctrl
            dicc["nombre"] = nom
            self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE]['estudiantes'].insert_one(dicc)

        for ctrl, mat, cal in Materias():
            dicc = {}
            dicc["control"] = ctrl
            dicc["materia"] = mat
            dicc["calificacion"] = cal
            self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE]['kardex'].insert_one(dicc)

        for ctrl, cve, cve_c in Usuarios():
            dicc = {}
            dicc["control"] = ctrl
            dicc["clave"] = cve
            dicc["cve_c"] = cve_c
            self.MONGO_RESPUESTA = self.MONGO_CLIENT[self.MONGO_DATABASE]['usuarios'].insert_one(dicc)

def Estudiantes():          #Ejercicio 1
    archivo = open("Estudiantes.prn", "r")
    conjunto = set()
    for linea in archivo:
        conjunto.add((linea[0:8], linea[8:-1]))
    return conjunto

def Materias():             #Ejercicio 2
    archivo = open("Kardex.txt", "r")
    materias = set()
    for linea in archivo:
        d2 = linea.split("|")
        dato = int(str(d2[2]))
        materias.add((linea[0:8], d2[1], dato))
    archivo.close()
    return materias

def Usuarios():          #Ejercicio 1
    archivo = open("usuarios.txt", "r")
    usuarios = set()
    for linea in archivo:
        d2 = linea.split(" ")
        usuarios.add((d2[0], d2[1], d2[2]))
    return usuarios



obj_MongoDB = PyMongo(vars)
obj_MongoDB.conectar_mongodb()
# obj_MongoDB.insertar_estudiante(alumno)
# obj_MongoDB.cargar_datos()

# for i in obj_MongoDB.consulta_mongodb('estudiantes'):
#     print(i)
#
# for i in obj_MongoDB.consulta_mongodb('kardex'):
#     print(i)
#
# for i in obj_MongoDB.consulta_mongodb('usuarios'):
#     print(i)

obj_MongoDB.desconectar_mongodb()