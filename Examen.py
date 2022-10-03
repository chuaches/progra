import json

def Estudiantes():
    try:
        archivo = open("Estudiantes.prn", "r")
        conjunto = set()
        for linea in archivo:
            conjunto.add((linea[0:8], linea[8:-1]))
        return conjunto
    except Exception as error:
        print(error)




def Materias():
    try:
        archivo = open("Kardex.txt", "r")
        materias = set()
        for linea in archivo:
            d2 = linea.split("|")
            dato = int(str(d2[2]))
            materias.add((linea[0:8], d2[1], dato))
        archivo.close()
        return materias
    except Exception as error:
        print(error)



def regresa_estudiantes(**kwargs):
    try:
        alumnos = Estudiantes()
        lista_alumnos = []
        print(alumnos)
        for key, value in kwargs.items():
            for alu in alumnos:
                c, n = alu
                if str(c) == str(value):
                    lista_alumnos.append(n)
        return lista_alumnos
    except Exception as error:
        print(error)

def crear_mats(promedios, ctrl):
    try:
        l_datos = []

        for materias in promedios:
            if materias[0] == ctrl:
                l_datos.append(materias[1])
        return l_datos
    except Exception as error:
        print(error)



    except Exception as error:
        print(error)

def regresa_materias_por_estudiante(**kwargs):
    try:
        datos = {}
        promedios = Materias()
        lista_materias = []
        lista_estudiantes = regresa_estudiantes(**kwargs)
        cont = 0
        cont2 = 0

        for key, value in kwargs.items():
            if cont2 == cont:
                for mat in promedios:
                    c, m, p = mat
                    if str(value) == str(c):
                        for estudiante in lista_estudiantes:
                            n = estudiante
                            if str(value) == str(c):
                                datos_est = {}
                                datos_est["Nombre"] = n
                                datos_est["Materias:"] = crear_mats(promedios, c)
                                datos = datos_est
                                lista_materias.append(datos_est)
        return json.dumps(lista_materias, indent= 3)
    except Exception as error:
        print(error)



print(regresa_materias_por_estudiante(c = 18420430, c2 = 18420469))

# print(regresa_materias_por_estudiante("18420430"))