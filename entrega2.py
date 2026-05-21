from simpleai.search import CspProblem, backtrack
import itertools

#Dadas dos coordenadas verifican si están a una celda de distancia
def es_adyacente(coor1,coor2):
    f1,c1 = coor1
    f2,c2=coor2
    return ((abs(f1-f2)+abs(c1-c2))==1)
    
#R1: Verifica que no haya dos módulos en la misma celda
def celdas_diferentes(vars,vals):
    return vals[0]!=vals[1]
 
#R3 y R4 Son unitarias => Sacamos esas casillas del dominio

#R5: Verifica que no haya un generador adyacente a un módulo habitacional
def seguridad_energetica(vars,vals):
    if ("hab" in vars[0][:3] and "gen" in vars[1][:3]) or ("gen" in vars[0][:3] and "hab" in vars[1][:3]): #Si las variables son hab y gen
        if es_adyacente(vals[0],vals[1]): #Verifica si son adyacentes
            return False
    return True

#R6: Verifica que no haya un generadores adyacentes entre sí
def aislamiento_generadores(vars,vals):
    if ("gen" in vars[0][:3] and "gen" in vars[1][:3]) : #Si las variables son 2 gen
        if es_adyacente(vals[0],vals[1]): #Verifica si son adyacentes
            return False
    return True

#R7: Verficia que un laboratorio sea adyacente de al menos un depósito
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

#R8: Verficia que un modulo habitacional sea adyacente de al menos una celda libre
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
                if celda_libre not in celdas_con_craters and celda_libre not in vals:   #Si el adyacente esta libre y no es un crater
                    existe_celda_libre = True   #Actualizamos bandera
            if not existe_celda_libre: #Si probados todos los adyacentes, no actualizamos bandera, significa que no tiene celda libre adyacente
                return False
    return True


def build_camp(camp_size, habs, generators, labs, deposits, airlocks, craters):
    global celdas_con_craters
    celdas_con_craters = craters
    celdas_grilla=[]    #Creamos lista con las casillas de la grilla
    celdas_borde = []     #Creamos lista con las casillas que estan en el borde
    for f in range(fila):
        for c in range(columna):
            celda = (f,c)
            if celda not in craters:
                celdas_grilla.append(celda)
                if (0==f or f==(fila-1) or 0==c or c == (columna-1)): 
                    celdas_borde.append(celda)


    lista_modulos=[]    #Creamos una Lista con las Variables 
    celdas_posible_por_modulo={}    #Creamos un diccionario con los valores posibles de las variables

    for i,_ in enumerate(range(habs)): #Iteramos la cantidad de modulos del tipo hab que haya.
        modulo = f"hab{i}" #Cada iteracion, le asignara un nombre diferente al modulo, hab0, hab1 ...
        lista_modulos.append(modulo) #Agregamos a las variables el modulo+NRO iteracion
        celdas_posible_por_modulo[modulo]=list(x for x in celda if x not in celdas_borde) #Agregamos al diccionario las posibles celdas en donde ubicaria al modulo
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
        celdas_posible_por_modulo[modulo] = list(celdas_borde)

    modulos=tuple(lista_modulos)

    restricciones=[]
    combinaciones = itertools.combinations(modulos,2)
    for mod1,mod2 in combinaciones:
        #Aplicamos a todas las combinaciones de variables que haya
        restricciones.append(((mod1,mod2),celdas_diferentes))   
        #Unicamente verificamos para las combinaciones con hab y gen asi agilizamos la busqueda
        if ("hab" in mod1[:3] and "gen" in mod2[:3]) or ("gen" in mod1[:3] and "hab" in mod2[:3]):
            restricciones.append(((mod1,mod2),seguridad_energetica))
        #Unicamente verificamos para las combinaciones con 2 gen  asi agilizamos la busqueda
        if ("gen" in mod1[:3] and "gen" in mod2[:3]) : 
            restricciones.append(((mod1,mod2),aislamiento_generadores))

# Si esta definido el modulo y no esta vacio, le aplicamos las restricciones globales
    if modulos:  
        restricciones.append((modulos,ruta_de_evacuacion))
        laboratorios = [m for m in modulos if m[:3] == "lab"]
        depositos = [m for m in modulos if m[:3] == "dep"]
        #Unicamente verificamos para las combinaciones con lab y dep asi agilizamos la busqueda
        for lab in laboratorios:
            variables_involucradas = tuple([lab] + depositos)
            restricciones.append((variables_involucradas, laboratorio_con_deposito))


    problema = CspProblem(modulos,celdas_posible_por_modulo,restricciones)
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
