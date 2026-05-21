from simpleai.search import CspProblem, backtrack, MOST_CONSTRAINED_VARIABLE
from itertools import combinations

def adyacente(pos1, pos2):
    """Función auxiliar: verifica si dos coordenadas son ortogonalmente adyacentes."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) == 1

def build_camp(camp_size, habs, generators, labs, deposits, airlocks, craters):
    filas, columnas = camp_size
    craters_set = set(craters)

    # ---------------------------------------------------------
    # 1. VARIABLES Y DOMINIOS
    # ---------------------------------------------------------
    variables = []
    dominios = {}

    # Pre-calcular tipos de celdas válidas (Restricción 2: Sin cráteres aplicada aquí)
    celdas_validas = [(f, c) for f in range(filas) for c in range(columnas) if (f, c) not in craters_set]
    celdas_borde = [(f, c) for f, c in celdas_validas if f == 0 or f == filas - 1 or c == 0 or c == columnas - 1]
    celdas_interior = [(f, c) for f, c in celdas_validas if (f, c) not in celdas_borde]

    # Diccionario para iterar y crear variables de forma limpia
    configuracion_modulos = [
        ("hab", habs, celdas_interior),    # R4: Habitacionales al interior
        ("air", airlocks, celdas_borde),   # R3: Esclusas en el borde
        ("gen", generators, celdas_validas),
        ("lab", labs, celdas_validas),
        ("dep", deposits, celdas_validas)
    ]

    for prefijo, cantidad, dominio_base in configuracion_modulos:
        for i in range(cantidad):
            var_name = f"{prefijo}_{i}" # Nombres únicos: hab_0, hab_1, gen_0
            variables.append(var_name)
            dominios[var_name] = dominio_base[:]

    # Si no hay módulos que ubicar (Test s1)
    if not variables:
        return []

    # ---------------------------------------------------------
    # 2. RESTRICCIONES
    # ---------------------------------------------------------
    restricciones = []

    # --- R1: Sin superposición ---
    def celdas_diferentes(vars, vals):
        return vals[0] != vals[1]

    for v1, v2 in combinations(variables, 2):
        restricciones.append(((v1, v2), celdas_diferentes))

    # --- Romper Simetría (Optimizador crítico para M4) ---
    def romper_simetria(vars, vals):
        return vals[0] < vals[1]

    for prefijo, cantidad, _ in configuracion_modulos:
        mismos_modulos = [v for v in variables if v.startswith(prefijo)]
        for m1, m2 in combinations(mismos_modulos, 2):
            restricciones.append(((m1, m2), romper_simetria))

    # --- Agrupación de variables ---
    var_habs = [v for v in variables if v.startswith("hab")]
    var_gens = [v for v in variables if v.startswith("gen")]
    var_labs = [v for v in variables if v.startswith("lab")]
    var_deps = [v for v in variables if v.startswith("dep")]

    # --- R5 y R6: Energía y Aislamiento ---
    def no_adyacente(vars, vals):
        return not adyacente(vals[0], vals[1])

    for g in var_gens:
        for h in var_habs:
            restricciones.append(((g, h), no_adyacente)) # R5

    for g1, g2 in combinations(var_gens, 2):
        restricciones.append(((g1, g2), no_adyacente)) # R6

    # --- R7: Cadena de suministro científico ---
    def lab_con_deposito(vars, vals):
        pos_lab = vals[0]
        pos_deps = vals[1:]
        return any(adyacente(pos_lab, d) for d in pos_deps)

    if var_deps:
        for l in var_labs:
            restricciones.append(([l] + var_deps, lab_con_deposito))
    elif var_labs:
        # Si hay laboratorios pero 0 depósitos, es matemáticamente imposible
        return None 

    # --- R8: Ruta de evacuación ---
    def ruta_evacuacion(vars, vals):
        pos_hab = vals[0]
        otras_pos = set(vals[1:]) # Set para búsqueda ultra rápida O(1)
        
        for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            vecino = (pos_hab[0] + df, pos_hab[1] + dc)
            # ¿Está en el mapa, no es cráter, y está libre?
            if 0 <= vecino[0] < filas and 0 <= vecino[1] < columnas:
                if vecino not in craters_set and vecino not in otras_pos:
                    return True
        return False

    for h in var_habs:
        otros_modulos = [v for v in variables if v != h]
        restricciones.append(([h] + otros_modulos, ruta_evacuacion))

    # ---------------------------------------------------------
    # 3. EJECUCIÓN CSP Y FORMATEO DE RESULTADO
    # ---------------------------------------------------------
    problema = CspProblem(variables, dominios, restricciones)
    
    solucion = backtrack(
        problema,
        variable_heuristic=MOST_CONSTRAINED_VARIABLE,
    )

    if solucion:
        resultado_final = []
        for var_name, coordenada in solucion.items():
            tipo = var_name.split("_")[0] # "hab_0" -> "hab"
            resultado_final.append((tipo, coordenada[0], coordenada[1]))
        return resultado_final
        
    return None