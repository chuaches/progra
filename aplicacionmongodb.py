'''
Fecha: 20 de octubre del 2022
'''
from env import variables
from conf import vars
from caja import Password
from crudmysql import MySQL
from mongodb import PyMongo

def cargar_estudiantes():
    objMySQL = MySQL(variables)
    obj_PyMongo = PyMongo(vars)
    # Crear las consultas
    sql_estudiante = "SELECT * FROM estudiantes"
    sql_kardex = "SELECT * FROM kardex"
    sql_usuario = "SELECT * FROM usuarios"
    objMySQL.conectar_mysql()
    lista_estudiantes = objMySQL.consulta_sql(sql_estudiante)
    lista_kardex = objMySQL.consulta_sql(sql_kardex)
    lista_usuarios = objMySQL.consulta_sql(sql_usuario)
    objMySQL.desconectar_mysql()

    # Insertar datos en MongoDB
    obj_PyMongo.conectar_mongodb()
    for est in lista_estudiantes:
        dicc = {
            'control': est[0],
            'nombre': est[1]
        }
        obj_PyMongo.insertar('estudiantes', dicc)

    for mat in lista_kardex:
        dicc = {
            "idKardex": mat[0],
            "control": mat[1],
            "materia": mat[2],
            "calificacion": float(mat[3])
        }
        obj_PyMongo.insertar('kardex', dicc)

    for usr in lista_usuarios:
        dicc = {
            "idUsuario": usr[0],
            "control": usr[1],
            "clave": usr[2],
            "clave_c": usr[3]
        }
        obj_PyMongo.insertar('usuarios', dicc)
    obj_PyMongo.desconectar_mongodb()


def Menu():
    while(True):
        print("-----------Menú Principal------------")
        print("1.- Insertar estudiante")
        print("2.- Actualizar calificación")
        print("3.- Consultar materias por estudiante")
        print("4.- Consulta general")
        print("5.- Eliminar estudiante")
        print("6.- Salir")
        try:
            op = int(input("Selecciona una opción: "))
        except Exception as error:
            print("ERROR", error)
            break
        else:
            if op==1:
                Insertar_estudiantesmongo()
            elif op ==2:
                actualizar_calificacion()
            elif op==3:
                consultar_materias()
                pass
            elif op==4:
                consulta_general()
                pass
            elif op==5:
                eliminar_estudiante()
                pass
            elif op==6:
                break
            else:
                print("Opción incorrecta")

def Insertar_estudiantesmongo():
    obj_PyMongo = PyMongo(vars)
    obj_PyMongo.conectar_mongodb()
    print("\n\n == INSERTAR ESTUDIANTES ==\n")
    ctrl = input("Ingresa el número de control: ")
    nombre = input("Ingresa el nombre: ")
    clave = input("Ingresa la clave de acceso: ")
    e = {
        "control": ctrl,
        "nombre": nombre
    }
    obj_PyMongo.insertar('estudiantes', e)

    obj_usuario = Password(contrasena=clave)
    u = {
        "control": ctrl,
        "clave": clave,
        "clave_c": obj_usuario.contrasena_cifrada.decode()
    }
    obj_PyMongo.insertar('usuarios', u)
    obj_PyMongo.desconectar_mongodb()

def actualizar_calificacion():
    obj_PyMongo = PyMongo(vars)
    print("\n\n == ACTUALIZAR PROMEDIO ==\n")
    ctrl = input("Ingresa el número de control: ")
    materia = input("Ingresa el nombre de la materia: ")
    filtro_buscar_materia = {'control': ctrl, 'materia': materia}
    obj_PyMongo.conectar_mongodb()
    respuesta = obj_PyMongo.consulta_mongodb('kardex', filtro_buscar_materia)
    for reg in respuesta["resultado"]:
        print(reg)
    if respuesta:
        promedio = float(input("Dame el nuevo promedio "))
        json_actualiza_prom = {"$set":{"calificacion": promedio}}
        resp = obj_PyMongo.actualizar('kardex', filtro_buscar_materia, json_actualiza_prom)
        if resp["status"]:
            print("El promedio ha sido actualizado")
        else:
            print("Ocurrió un error al actualizar")
        respuesta = obj_PyMongo.consulta_mongodb('kardex', filtro_buscar_materia)
        for reg in respuesta["resultado"]:
            print(reg)
    else:
        print(f"El estudiante con numero de control {ctrl} o la materia {materia} NO EXISTE")
    obj_PyMongo.desconectar_mongodb()

def consultar_materias():
    obj_PyMongo = PyMongo(vars)

    print("\n\n == CONSULTAR MATERIAS POR ESTUDIANTE ==\n")
    ctrl = input("Dame el número de control: ")

    filtro = {"control": ctrl}
    atributos_est = {"_id": 0, "nombre": 1}
    atributos_mat = {"_id": 0, "materia": 1, "calificacion": 1}

    obj_PyMongo.conectar_mongodb()
    respuesta1 = obj_PyMongo.consulta_mongodb('estudiantes', filtro, atributos_est)
    respuesta2 = obj_PyMongo.consulta_mongodb('kardex', filtro, atributos_mat)

    obj_PyMongo.desconectar_mongodb()
    print()
    if respuesta1["status"] and respuesta2["status"]:
        print(respuesta1["resultado"][0]["nombre"])
        for mat in respuesta2["resultado"]:
            print("   ", mat["materia"], mat["calificacion"])
    else:
        print("No encontrado")

def consulta_general():
    obj_PyMongo = PyMongo(vars)
    obj_PyMongo.conectar_mongodb()

    print("\n\n == CONSULTA GENERAL DE ESTUDIANTES ==\n")

    filtro = {}

    respuesta1 = obj_PyMongo.consulta_mongodb('estudiantes', filtro)

    for est in respuesta1["resultado"]:
        print()
        print(est["nombre"])
        filtro = {"control": est["control"]}
        respuesta2 = obj_PyMongo.consulta_mongodb('kardex', filtro)
        for mat in respuesta2["resultado"]:
            print("   ", mat["materia"], mat["calificacion"])
    obj_PyMongo.desconectar_mongodb()

def eliminar_estudiante():
    obj_PyMongo = PyMongo(vars)
    obj_PyMongo.conectar_mongodb()

    print("\n\n == ELIMINAR UN ESTUDIANTE ==\n")
    ctrl = input("Dame el número de control: ")

    filtro = {"control": ctrl}

    respuesta1 = obj_PyMongo.eliminar('kardex', filtro)
    respuesta2 = obj_PyMongo.eliminar('usuarios', filtro)
    respuesta3 = obj_PyMongo.eliminar('estudiantes', filtro)

    obj_PyMongo.desconectar_mongodb()

    if respuesta1 and respuesta2 and respuesta3:
        print(f"El alumno con número de control '{ctrl}' ha sido eliminado correctamente")
    else:
        print(f"Ocurrió un error al eliminar al alumno con número de control '{ctrl}'")


# cargar_estudiantes()

Menu()