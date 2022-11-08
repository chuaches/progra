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
        return json_data
    except IOError:
        print( "Error de entrada/salida.")

def estado(edo):
    dic = {}
    jsonres = open("jsonres.json", mode="w")
    archivo = open("CPdescarga.txt", mode="r")

    try:
       if archivo.readable():
          cont = 0
          for ren in archivo.read().split("\n"):
            if cont > 0:
                 if(cont == 1):
                    titulos = ren.split("|")
                 else:
                    estado = ren.split("|")
                    if estado[4] == edo:
                        dic[titulos[0]] = estado[0]
                        dic[titulos[3]] = estado[3]
            cont += 1
       json.dump(dic, jsonres)
       archivo.close()
    except IndexError:
       print("")


print(municipio("Jiquilpan"))
estado("Michoacï¿½n de Ocampo")
