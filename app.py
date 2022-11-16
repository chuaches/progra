from crudmysql import MySQL
from env import variables

def metodo2(ctrl):
    obj_MySQL = MySQL(variables)
    print("\n\n == CONSULTAR PROMEDIO ESTUDIANTE ==\n")

    sql_buscar_materias = "SELECT E.nombre, K.materia, K.calificacion FROM estudiantes E, kardex K " \
                          f"WHERE K.control='{ctrl}' AND E.control='{ctrl}';"

    resp = obj_MySQL.consulta_sql(sql_buscar_materias)

    estudiante = resp[0][0]
    prom = 0
    long = 0

    for mat in resp:
        prom = prom + mat[2]
        long += 1

    prom = prom / long

    dicc = {
        "estudiante": estudiante,
        "promedio": str(prom)[0:5]
    }

    import json
    dicc = json.dumps(dicc, indent=3)
    print(dicc)




ctrl = input("Dame el número de control: ")
metodo2(ctrl)
# metodo(ctrl)