import json

def municipio(mun):
    diccionario = {}
    cont = 0
    try:
        archivo = open("CPdescarga.txt", "r")
        for linea in archivo:
            d2 = linea.split("|")
            for dic in d2[3:]:
                if d2[3] == mun:
                    d3 = {}
                    d3["CP"] = d2[0]
                    d3["Tipo de asentamiento"] = d2[10]
                    d3["Zona"] = d2[13]
                    diccionario[cont] = d3
                    cont+=1
                    break
        archivo.close()
        json_data = json.dumps(diccionario, indent=3)
        print(json_data)
    except IOError:
        print( "Error de entrada/salida.")

def estado(edo):
    cont = 0
    diccionario = {}
    try:
        archivo = open("CPdescarga.txt", "r")
        for linea in archivo:
            d2 = linea.split("|")
            for dic in d2[3:]:
                if d2[4] == edo:
                    d3 = {}
                    d3["CP"] = d2[0]
                    d3["Municipio"] = d2[3]
                    diccionario[cont] = d3
                    cont += 1
        archivo.close()
        json_data = json.dumps(diccionario, indent=3)
        print(json_data)
    except Exception:
        print("Error")


# municipio("Jiquilpan")
estado("Michoacán de Ocampo")




# archivo = open("resultados.json", 'w') # abre el archivo datos.txt
# archivo.write(json_data)
# archivo.close()