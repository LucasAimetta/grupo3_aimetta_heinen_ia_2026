from simpleai.search import SearchProblem, astar


def muestras_por_recolectar(state):
    return len(state[4]) + len(state[5])


def distancia_a_las_muestras(state):
    costo_mas_lejano = 0
    ubicacion = state[0]
    muestras_totales = state[4] + state[5]
    bandera = 0
    for muestra in muestras_totales:
        if bandera ==0:
            distancia_fila = abs(ubicacion[0] - muestra[0])
            distancia_columna = abs(ubicacion[1] - muestra[1])
            costo_mas_lejano = distancia_fila + distancia_columna
            bandera=1
        else:
            distancia_fila = abs(ubicacion[0] - muestra[0])
            distancia_columna = abs(ubicacion[1] - muestra[1])
            
            costo_camino = distancia_fila + distancia_columna
            if costo_camino>costo_mas_lejano:
                costo_mas_lejano = costo_camino


    return costo_mas_lejano

def planear_rover(rover_inicio,bateria_inicial,zonas_sombra,muestras_igneas,muestras_sedimentarias):
    global sombras
    sombras = zonas_sombra
    state = (rover_inicio,bateria_inicial,"",0,muestras_igneas,muestras_sedimentarias)
    problem = AresProblem(state)
    solution = astar(problem,graph_search=True)
    ares_actions=[]

    if solution is not None:
        for action, _ in solution.path():
            if action is None:
                continue
            ares_actions.append(action)
    else:
        print("what the potato?")
    return ares_actions


def muestras_por_recolectar(state):
    return len(state[4]) + len(state[5])

class AresProblem(SearchProblem):

    def is_goal(self, state):
        return state[3]==len(state[4])==len(state[5])==0 #Verifica que no tenga muestras cargadas ni muestras por recolectar

    def actions(self, state):
        acciones = []
        posibles_mov = [
            (1,0),
            (-1,0),
            (0,-1),
            (0,1)
        ]
        if state[1]>1:
            for mov in posibles_mov:
                nueva_columna = state[0][1] + mov[1] 
                nueva_fila = state[0][0] + mov[0]
                nueva_posicion = (nueva_fila,nueva_columna)
                #PREGUNTAR A LOS PROFES SI HAY RANGO EN LA GRILLA.
                # if no se va de rango.
                acciones.append(("moverse",nueva_posicion) )
        posibles_sobremarcha = [
            (2,0),
            (-2,0),
            (0,2),
            (0,-2)
        ]
        if state[1]>4:
            for mov in posibles_sobremarcha:
                nueva_columna = state[0][1] + mov[1] 
                nueva_fila = state[0][0] + mov[0]
                nueva_posicion = (nueva_fila,nueva_columna)
                #PREGUNTAR A LOS PROFES SI HAY RANGO EN LA GRILLA.
                # if no se va de rango.
                acciones.append(("sobremarcha",nueva_posicion))

        if state[1]>1:
            if len(state[4])>0 and state[2] !="termico":
                acciones.append(("equipar","termico"))
            if len(state[5])>0 and state[2] !="percusion":
                acciones.append(("equipar","percusion"))
        if state[1]>3 and state[3]<2: #Si tiene bateria y espacio en la bodega
            if state[2]=="termico" and state[0] in state[4]: # Si esta en posicion de una muestra ignea y tiene el martillo termico
                acciones.append(("recolectar","ignea"))
            if state[2]=="percusion" and state[0] in state[5]: # Si esta en posicion de una muestra sedimentaria y tiene el martillo de percusion
                acciones.append(("recolectar","sedimentaria"))
        #CONSUME 1 DE BATERIA POR MUESTRA O 1 EN TOTAL?
        if (state[1]>state[3]) and (state[3]==2 or (state[3]==1 and 0==muestras_por_recolectar(state))): 
            acciones.append(("depositar",None))
        
        if state[0] not in sombras and state[1] <20:
            acciones.append(("recargar",None))
        return acciones


    def result(self, state, action):
        list_state = list(state)

        if action[0] == "moverse": 
            list_state[0] = action[1]
            list_state[1] -= 1
        elif action[0] == "sobremarcha":
            list_state[0] = action[1]
            list_state[1] -= 4
        elif action[0] == "equipar":
            list_state[2] = action[1]
            list_state[1] -= 1
        elif action[0] == "recolectar":
            list_state[3] +=1
            list_state[1] -= 3
            if action[1] == "ignea":
                muestras_igneas_restantes = tuple(x for x in list_state[4] if x != state[0])
                list_state[4] = muestras_igneas_restantes
            else: 
                muestras_sedimentarias_restantes = tuple(x for x in list_state[5] if x != state[0])
                list_state[5] = muestras_sedimentarias_restantes
        elif action[0] == "depositar":
            list_state[1] -= 1
            list_state[3] =0
        else:
            if list_state[1]>10:
                list_state[1]=20
            else:
                list_state[1]+=10

        return tuple(list_state)

    def cost(self, state1, action, state2):
        cost = 0
        if action[0] in ("moverse","sobremarcha"):
            cost = 1
        elif action[0] == "equipar":
            cost = 3
        elif action[0] == "recolectar":
            cost = 2
        elif action[0] == "depositar":
            cost = state1[3]
        else:
            cost = 4
        return cost


   
    def heuristic(self,state):
        costo = 0
        if muestras_por_recolectar(state) !=0:
            costo += muestras_por_recolectar(state) * (2+1)  #La suma de las muestras a recolectar por la suma del tiempo que nos lleva recolectarlas y depositarlas 
        costo += distancia_a_las_muestras(state)/2
        costo += state[3]

        if state[2] != "termico" and len(state[4]) !=0:
            costo+=3
        if state[2] != "percusion" and len(state[5]) !=0: 
            costo+=3
        
        return costo

