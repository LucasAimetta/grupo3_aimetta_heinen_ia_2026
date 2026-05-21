from simpleai.search import CspProblem, backtrack
import itertools
#Definimos Variables y el Dominio de estas.
#Para no tener que recorrer varias veces la lista de modulos, al crear uno, le asignamos el dominio en el diccionario
def modulos_a_ubicar(habs, generators, labs, deposits, airlocks,celda,celda_borde):
    lista_modulos=[]
    celdas_posible_por_modulo={}
    for i,_ in enumerate(range(habs)):
        modulo = f"hab{i}" #Cada iteracion, le asignara un nombre diferente al modulo, hab0, hab1 ...
        lista_modulos.append(modulo) #Agregamos a las variables el modulo+NRO iteracion
        celdas_posible_por_modulo[modulo]=list(x for x in celda if x not in celda_borde) #Agregamos al diccionario las posibles celdas en donde ubicaria al modulo
    for i,_ in enumerate(range(generators)):
        modulo = f"gen{i}"
        lista_modulos.append(modulo)
        celdas_posible_por_modulo[modulo]=list(celdas_grilla)
    for i,_ in enumerate(range(deposits)):
        modulo = f"dep{i}"
        lista_modulos.append(modulo)
        celdas_posible_por_modulo[modulo]=list(celdas_grilla)
    for i,_ in enumerate(range(labs)):
        modulo = f"lab{i}"
        lista_modulos.append(modulo)
        celdas_posible_por_modulo[modulo]=list(celdas_grilla)
  
    for i,_ in enumerate(range(airlocks)):
        modulo = f"air{i}"
        lista_modulos.append(modulo)
        celdas_posible_por_modulo[modulo] = list(celda_borde)
    return tuple(lista_modulos),celdas_posible_por_modulo #Devolvemos la tupla con las variables y el diccionario con el dominio


#Celdas en la grilla, toma las dimensiones y devuelve las celdas sin crater que existen 
def celdas(camp_size,craters):
    fila, columna = camp_size
    global celdas_grilla 
    celdas_grilla=[]
    for f in range(fila):
        for c in range(columna):
            celda = (f,c)
            if celda not in craters:
                celdas_grilla.append(celda)
    return celdas_grilla
#Celdas en el borde, toma las celdas posibles, y devuelven aquellas que no tengan crater y esten en el borde
def celdas_borde(camp_size,craters):  

    fila, columna = camp_size
    celda_borde =[]
    for f in range(fila):
        for c in range(columna):
            celda = (f,c)
            if (0==f or f==(fila-1) or 0==c or c == (columna-1)) and celda not in craters:
                celda_borde.append(celda)
    return celda_borde    
#Pasada dos coordenadas verifican si están a una celda de distancia
def es_adyacente(coor1,coor2):
    f1,c1 = coor1
    f2,c2=coor2
    return ((abs(f1-f2)+abs(c1-c2))==1)
    

#Definimos Restricciones
#APLICAMOS A TODAS LAS COMBINACIONES DE MODULO TOMADAS DE A 2
def celdas_diferentes(vars,vals):
    return vals[0]!=vals[1] #Si son distintas, devuelve TRUE
#APLICAMOS A TODAS LAS COMBINACIONES DE MODULO TOMADAS DE A 2
def seguridad_energetica(vars,vals):
    if ("hab" in vars[0][:3] and "gen" in vars[1][:3]) or ("gen" in vars[0][:3] and "hab" in vars[1][:3]): #Si las variables son hab y gen
        if es_adyacente(vals[0],vals[1]): #Verifica si son adyacentes
            return False
    return True
#APLICAMOS A TODAS LAS COMBINACIONES DE MODULO TOMADAS DE A 2
def aislamiento_generadores(vars,vals):
    if ("gen" in vars[0][:3] and "gen" in vars[1][:3]) : #Si las variables son 2 gen
        if es_adyacente(vals[0],vals[1]): #Verifica si son adyacentes
            return False
    return True
#APLICAMOS A TODOS LOS MODULOS
def laboratorio_con_deposito(vars,vals):
    for i,var in enumerate(vars):  #Recorremos todas las variables
        if var[:3] =="lab": 
            celda_lab = vals[i]    #Si la variable es del tipo Lab
            es_adyacente_con_deposito = False   #Bandera
            for j,var in enumerate(vars):  #Recorremos todas las variables
                    if var[:3] =="dep":     #Si la variable es del tipo dep
                        celda_dep=vals[j]
                        if es_adyacente(celda_lab,celda_dep):   #Si son adyacentes
                            es_adyacente_con_deposito = True
                            break    #Actualizamos bandera
            if not es_adyacente_con_deposito:   #Si probados todos los adyacentes, no actualizamos bandera, significa que no tiene deposito adyacente
                return False
    return True
#APLICAMOS A TODOS LOS MODULOS
def ruta_de_evacuacion(vars,vals):
    posibles_mov = [
            (1,0),
            (-1,0),
            (0,-1),
            (0,1)
        ]
    for i,var in enumerate(vars): #Recorremos todas las variables
        if var[:3] =="hab":         #Si es del tipo hab
            existe_celda_libre = False  #Bandera
            for mov in posibles_mov:    #Recorremos todos sus adyacentes
                celda_hab = vals[i]
                celda_libre= (celda_hab[0]+mov[0], celda_hab[1]+mov[1])
                if celda_libre not in crater and celda_libre not in vals:   #Si el adyacente esta libre y no es un crater
                    existe_celda_libre = True   #Actualizamos bandera
            if not existe_celda_libre: #Si probados todos los adyacentes, no actualizamos bandera, significa que no tiene celda libre adyacente
                return False
    return True


def build_camp(camp_size, habs, generators, labs, deposits, airlocks, craters):
    global crater 
    crater= craters
    restricciones=[]
    celda_totales=celdas(camp_size,craters)
    celda_borde=celdas_borde(camp_size,craters)
    modulo,dominio=modulos_a_ubicar(habs, generators, labs, deposits, airlocks,celda_totales,celda_borde)
    combinaciones = itertools.combinations(modulo,2)
    for mod1,mod2 in combinaciones:
        restricciones.append(((mod1,mod2),celdas_diferentes))
        if ("hab" in mod1[:3] and "gen" in mod2[:3]) or ("gen" in mod1[:3] and "hab" in mod2[:3]):#Unicamente verificamos para las combinaciones con hab y gen asi agilizamos la busqueda
            restricciones.append(((mod1,mod2),seguridad_energetica))
        if ("gen" in mod1[:3] and "gen" in mod2[:3]) : #Unicamente verificamos para las combinaciones con 2 gen  asi agilizamos la busqueda
            restricciones.append(((mod1,mod2),aislamiento_generadores))

    if modulo:  # Si esta definido el modulo y no esta vacio, le aplicamos las restricciones
        restricciones.append((modulo,ruta_de_evacuacion))

        laboratorios = [m for m in modulo if m[:3] == "lab"]
        depositos = [m for m in modulo if m[:3] == "dep"]
        for lab in laboratorios:
            variables_involucradas = tuple([lab] + depositos)
            restricciones.append((variables_involucradas, laboratorio_con_deposito))


    problema = CspProblem(modulo,dominio,restricciones)
    solucion = backtrack(problema)

    if solucion is None:
        return None
    resultado_final = []
    for variable, posicion in solucion.items():
        modulo = variable[:3]            
        fila = posicion[0]
        columna = posicion[1]

        resultado_final.append((modulo, fila, columna))

    return resultado_final



