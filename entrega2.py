from simpleai.search import CspProblem, backtrack
import itertools
#Definimos Variables

def modulos_a_ubicar(habs, generators, labs, deposits, airlocks):
    lista_modulos=[]
    for _ in range(habs):
        lista_modulos.append("hab")
    for _ in range(generators):
        lista_modulos.append("gen")
    for _ in range(labs):
        lista_modulos.append("lab")
    for _ in range(deposits):
        lista_modulos.append("dep")
    for _ in range(airlocks):
        lista_modulos.append("air")
    return tuple(lista_modulos)
#Celdas en la grilla
def celdas(camp_size,craters):
    fila, columna = camp_size
    celdas_grilla =[]
    for f in range(fila):
        for c in range(columna):
            celda = (f,c)
            if celda not in craters:
                celdas_grilla.append(celda)
    return celdas_grilla
#Celdas en el borde
def celdas_borde(camp_size,craters):             
    fila, columna = camp_size
    celda_borde =[]
    for f in range(fila):
        for c in range(columna):
            celda = (f,c)
            if (0==f or f==(fila-1) or 0==c or c == (columna-1)) and celda not in craters:
                celda_borde.append(celda)
    return celda_borde    
# Definimos Dominio.
def celdas_por_modulo(celdas_grilla,celdas_borde):
        
    celdas_posible_por_modulo = {
        "hab": tuple(x for x in celdas_grilla if x not in celdas_borde),
        "lab": tuple(celdas_grilla),
        "gen":  tuple(celdas_grilla),
        "dep":  tuple(celdas_grilla),
        "air":  tuple(celdas_borde)
}
    return celdas_posible_por_modulo

def es_adyacente(coor1,coor2):
    f1,c1 = coor1
    f2,c2=coor2
    return ((abs(f1-f2)+abs(c1-c2))==1)
    

#Definimos Restricciones
restricciones=[]
#APLICAMOS A TODAS LAS COMBINACIONES DE MODULO TOMADAS DE A 2
def celdas_diferentes(vars,vals):
    return vals[0]!=vals[1]
#APLICAMOS A TODAS LAS COMBINACIONES DE MODULO TOMADAS DE A 2
def seguridad_energetica(vars,vals):
    if "hab" in vars and "gen" in vars:
        if es_adyacente(vals[0],vals[1]):
            return False
    return True
#APLICAMOS A TODAS LAS COMBINACIONES DE MODULO TOMADAS DE A 2
def aislamiento_generadores(vars,vals):
    if vars.count("gen") ==2:
        if es_adyacente(vals[0],vals[1]):
            return False
    return True
#APLICAMOS A TODOS LOS MODULOS
def laboratorio_con_deposito(vars,vals):
    posibles_mov = [
            (1,0),
            (-1,0),
            (0,-1),
            (0,1)
        ]
    for i,var in enumerate(vars): 
        if var =="lab":
            for mov in posibles_mov:
                celda_lab = vals[i]
                celda_lab[0]+= mov[0]
                celda_lab[1]+=mov[1]
                if celda_lab in vals:
                    indice=vals.index(celda_lab)
                    if "dep"==vars[indice]:
                        return True
    return False
#APLICAMOS A TODOS LOS MODULOS
def ruta_de_evacuacion(vars,vals):
    posibles_mov = [
            (1,0),
            (-1,0),
            (0,-1),
            (0,1)
        ]
    for i,var in enumerate(vars): 
        if var =="hab":
            for mov in posibles_mov:
                celda_hab = vals[i]
                celda_hab[0]+= mov[0]
                celda_hab[1]+=mov[1]
                if celda_hab not in crater and celda_hab not in vals:
                    return True
    return False






def build_camp(camp_size, habs, generators, labs, deposits, airlocks, craters):
    global crater 
    crater= craters
    modulo=modulos_a_ubicar(habs, generators, labs, deposits, airlocks)
    celda_totales=celdas(camp_size,craters)
    celda_borde=celdas_borde(camp_size,craters)
    celda_por_modulo=celdas_por_modulo(celda_totales,celda_borde)

    combinaciones = itertools.combinations(modulo,2)
    for mod1,mod2 in combinaciones:
        restricciones.append(((mod1,mod2),celdas_diferentes))
        restricciones.append(((mod1,mod2),seguridad_energetica))
        restricciones.append(((mod1,mod2),aislamiento_generadores))
    restricciones.append((modulo,laboratorio_con_deposito))
    restricciones.append((modulo,ruta_de_evacuacion))


    problema = CspProblem(modulo,celda_por_modulo,restricciones)
    solucion = backtrack(problema)

"""if __name__ == "__main__":
    camp_size =(5, 6)
    craters=[(2, 2), (2, 3)]
    celdas_grilla=celdas(camp_size,craters)
    celda_bordes=celdas_borde(camp_size,craters)
    valores_celda=celda_por_modulo(celdas_grilla,celda_bordes)
    for c in valores_celda:
        print(f"MODULO: {c}, {valores_celda[c]}")
"""
