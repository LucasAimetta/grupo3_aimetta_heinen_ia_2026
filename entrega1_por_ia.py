#COPILOT

# entrega1.py
from math import ceil
from collections import deque
from simpleai.search import SearchProblem, astar

# Dominio / constantes
MAX_BATT = 20
MAX_LOAD = 2

# Tiempos (minutos) por acción
ACTION_TIME = {
    "moverse": 1,
    "sobremarcha": 1,
    "equipar": 3,
    "recolectar": 2,
    "depositar": 1,  # se aplica por muestra depositada
    "recargar": 4,
}

# Consumo de batería por acción (recargar es negativo = recarga)
ACTION_BATT = {
    "moverse": 1,
    "sobremarcha": 4,
    "equipar": 1,
    "recolectar": 3,
    "depositar": 1,   # por muestra depositada
    "recargar": -10,
}


def _ceil_overdrive_distance(d):
    """
    Tiempo mínimo (en minutos) para recorrer una distancia Manhattan d,
    asumiendo que podemos usar sobremarcha (2 celdas en 1 minuto).
    Es una cota optimista (mínima posible): ceil(d/2).
    """
    return ceil(d / 2)


class RoverProblem(SearchProblem):
    """
    Estado: (r, c, battery, drill, load, ig_tuple, sed_tuple)
      - drill: "ninguno", "termico", "percusion"
      - ig_tuple, sed_tuple: tuplas ordenadas de coordenadas restantes
    Acciones: tuplas (tipo, parametro) compatibles con los tests.
    """

    def __init__(self, start_state, shadows):
        self.shadows = set(shadows)
        super(RoverProblem, self).__init__(start_state)

    # helpers
    def _unpack(self, state):
        r, c, batt, drill, load, ig, sed = state
        return (r, c), batt, drill, load, tuple(ig), tuple(sed)

    def actions(self, state):
        (r, c), batt, drill, load, ig_rem, sed_rem = self._unpack(state)
        ig_rem = tuple(ig_rem)
        sed_rem = tuple(sed_rem)

        acts = []

        # 1) movimientos: moverse (1 celda) y sobremarcha (2 celdas)
        moves = [
            ("moverse", (r + 1, c)),
            ("moverse", (r - 1, c)),
            ("moverse", (r, c + 1)),
            ("moverse", (r, c - 1)),
            ("sobremarcha", (r + 2, c)),
            ("sobremarcha", (r - 2, c)),
            ("sobremarcha", (r, c + 2)),
            ("sobremarcha", (r, c - 2)),
        ]
        for act_type, dest in moves:
            # calcular batería resultante según la regla de los tests:
            batt_after = min(MAX_BATT, batt - ACTION_BATT[act_type])
            # la acción solo es válida si la batería resultante > 0
            if batt_after > 0:
                acts.append((act_type, dest))

        # 2) equipar taladro (si es distinto al actual)
        for taladro in ("termico", "percusion"):
            if drill != taladro:
                batt_after = min(MAX_BATT, batt - ACTION_BATT["equipar"])
                if batt_after > 0:
                    acts.append(("equipar", taladro))

        # 3) recolectar si hay muestra en la celda, taladro correcto y espacio
        if load < MAX_LOAD:
            if (r, c) in ig_rem and drill == "termico":
                batt_after = min(MAX_BATT, batt - ACTION_BATT["recolectar"])
                if batt_after > 0:
                    acts.append(("recolectar", "ignea"))
            if (r, c) in sed_rem and drill == "percusion":
                batt_after = min(MAX_BATT, batt - ACTION_BATT["recolectar"])
                if batt_after > 0:
                    acts.append(("recolectar", "sedimentaria"))

        # 4) depositar: si tiene carga y cumple la regla (2 muestras o 1 si es la última)
        if load > 0:
            remaining_any = (len(ig_rem) + len(sed_rem)) > 0
            can_deposit = False
            if load == 2:
                can_deposit = True
            elif load == 1 and not remaining_any:
                can_deposit = True
            if can_deposit:
                # batería resultante tras depositar todas las muestras:
                batt_after = min(MAX_BATT, batt - ACTION_BATT["depositar"] * load)
                if batt_after > 0:
                    acts.append(("depositar", None))

        # 5) recargar: solo fuera de sombras y si no está al máximo
        if (r, c) not in self.shadows and batt < MAX_BATT:
            batt_after = min(MAX_BATT, batt - ACTION_BATT["recargar"])
            if batt_after > 0:
                acts.append(("recargar", None))

        return acts

    def result(self, state, action):
        (r, c), batt, drill, load, ig_rem, sed_rem = self._unpack(state)
        ig_rem = list(ig_rem)
        sed_rem = list(sed_rem)

        act_type, param = action

        if act_type == "moverse":
            nr, nc = param
            batt_after = min(MAX_BATT, batt - ACTION_BATT["moverse"])
            return (nr, nc, batt_after, drill, load, tuple(ig_rem), tuple(sed_rem))

        if act_type == "sobremarcha":
            nr, nc = param
            batt_after = min(MAX_BATT, batt - ACTION_BATT["sobremarcha"])
            return (nr, nc, batt_after, drill, load, tuple(ig_rem), tuple(sed_rem))

        if act_type == "equipar":
            taladro = param
            batt_after = min(MAX_BATT, batt - ACTION_BATT["equipar"])
            return (r, c, batt_after, taladro, load, tuple(ig_rem), tuple(sed_rem))

        if act_type == "recolectar":
            tipo = param
            batt_after = min(MAX_BATT, batt - ACTION_BATT["recolectar"])
            if tipo == "ignea":
                # eliminar muestra ignea en (r,c)
                ig_rem = [m for m in ig_rem if m != (r, c)]
                return (r, c, batt_after, drill, load + 1, tuple(ig_rem), tuple(sed_rem))
            else:
                sed_rem = [m for m in sed_rem if m != (r, c)]
                return (r, c, batt_after, drill, load + 1, tuple(ig_rem), tuple(sed_rem))

        if act_type == "depositar":
            # vacía toda la carga
            batt_after = min(MAX_BATT, batt - ACTION_BATT["depositar"] * load)
            return (r, c, batt_after, drill, 0, tuple(ig_rem), tuple(sed_rem))

        if act_type == "recargar":
            batt_after = min(MAX_BATT, batt - ACTION_BATT["recargar"])  # recarga +10 hasta MAX_BATT
            return (r, c, batt_after, drill, load, tuple(ig_rem), tuple(sed_rem))

        # acción desconocida (no debería ocurrir)
        return state

    def is_goal(self, state):
        (r, c), batt, drill, load, ig_rem, sed_rem = self._unpack(state)
        return (len(ig_rem) == 0) and (len(sed_rem) == 0) and (load == 0)

    def cost(self, state, action, state2):
        act_type, _ = action
        if act_type == "depositar":
            # el coste en minutos es 1 por muestra depositada; calcular según carga en 'state'
            # extraemos la carga de 'state'
            _, _, _, load, _, _ = self._unpack(state)
            return ACTION_TIME["depositar"] * load
        else:
            return ACTION_TIME[act_type]

    def heuristic(self, state):
        """
        Heurística admisible (cota inferior optimista del tiempo restante en minutos).
        Construida para ser simple y segura (no sobreestimar):
          - Para cada muestra restante asumimos 2 minutos para recolectarla (acción 'recolectar').
          - Para el movimiento, tomamos la distancia Manhattan mínima desde la posición actual
            hasta la muestra más cercana y convertimos a tiempo mínimo usando sobremarcha:
            tiempo_mov = ceil(min_distance / 2).
          - No contamos equipar ni depositar (optimista).
        Esto es una cota inferior (admisible).
        """
        (r, c), batt, drill, load, ig_rem, sed_rem = self._unpack(state)
        remaining = list(ig_rem) + list(sed_rem)
        n = len(remaining)
        if n == 0:
            # si no hay muestras, pero puede quedar carga (no meta), heurística 0
            return 0

        # tiempo mínimo de recolección: 2 minutos por muestra
        collect_time = 2 * n

        # distancia mínima desde (r,c) a cualquier muestra
        min_dist = min(abs(r - mr) + abs(c - mc) for (mr, mc) in remaining)
        move_time = _ceil_overdrive_distance(min_dist)

        # heurística = movimiento mínimo hasta la primera muestra + tiempo de recolección
        return move_time + collect_time


def planear_rover(
    rover_inicio=(0, 0),
    bateria_inicial=20,
    zonas_sombra=[],
    muestras_igneas=[],
    muestras_sedimentarias=[],
):
    """
    API exigida por la consigna.
    Devuelve una lista de acciones en el formato pedido por los tests.
    """
    # normalizar entradas a tuplas
    start_pos = tuple(rover_inicio)
    shadows = tuple(zonas_sombra)
    igneous = tuple(tuple(p) for p in muestras_igneas)
    sediments = tuple(tuple(p) for p in muestras_sedimentarias)

    # estado inicial: (r, c, battery, drill, load, ig_tuple, sed_tuple)
    start_state = (start_pos[0], start_pos[1], bateria_inicial, "ninguno", 0, igneous, sediments)

    problem = RoverProblem(start_state, shadows)

    # Ejecutar A* (SimpleAI)
    result = astar(problem, graph_search=True)

    if result is None:
        # según el enunciado todos los casos son resolubles; si no, devolver lista vacía
        return []

    # result.path() devuelve lista de (accion, estado) desde inicio hasta meta (sin incluir estado inicial)
    path = result.path()
    actions = [step[0] for step in path]  # cada step = (accion, estado)
    # Asegurar que cada acción sea una tupla de 2 elementos (tipo, parametro)
    normalized = []
    for a in actions:
        # a puede ser None (en algunos casos), pero en nuestro diseño siempre es una tupla
        if a is None:
            continue
        normalized.append(a)

    return normalized


if __name__ == "__main__":
    # No ejecutar búsquedas pesadas al importar el módulo.
    # Solo pruebas locales muy pequeñas si se ejecuta directamente.
    # Ejemplo rápido:
    acciones = planear_rover(
        rover_inicio=(0, 0),
        bateria_inicial=20,
        zonas_sombra=[(0, 1), (0, 2)],
        muestras_igneas=[(1, 1), (1, 2)],
        muestras_sedimentarias=[(2, 3)],
    )
    print("Acciones ejemplo:", acciones)