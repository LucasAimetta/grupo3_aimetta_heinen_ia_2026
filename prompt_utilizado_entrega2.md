Actúa como un desarrollador experto en Python e Inteligencia Artificial. A continuación, te proporciono la descripción de un trabajo práctico que debe modelarse como un Problema de Satisfacción de Restricciones (CSP), junto con su correspondiente conjunto de tests unitarios (pytest).

Tu tarea es proporcionarme la solución completa implementando la función build_camp utilizando la biblioteca simpleai. Es fundamental que el código cumpla estrictamente con todas las reglas detalladas en el enunciado y esté optimizado para que logre pasar todos los casos de prueba provistos sin exceder los límites de tiempo. Por favor, entrega únicamente el código final en Python.

Entrega 2: Ares-1 — Diseño del campamento base

Contexto

Tras el exitoso regreso del rover Ares-1 con una valiosa colección de muestras marcianas, la misión entra en su siguiente fase crítica: el establecimiento de un campamento base permanente en la superficie del planeta rojo.
El equipo de ingeniería de la misión debe distribuir los módulos del campamento sobre una cuadrícula que representa el terreno explorado. Dado que las reglas de seguridad y operación son numerosas, no es posible hacerlo manualmente de forma confiable. El sistema debe ser capaz de generar automáticamente distribuciones válidas que satisfagan todas las restricciones. Para esto, el problema se modela como un Problema de Satisfacción de Restricciones (CSP).
Descripción del problema

El campamento base se diseña sobre una cuadrícula rectangular de filas × columnas. Cada celda puede contener un único módulo o estar vacía (corredor). Algunas celdas están marcadas de antemano como cráteres y no pueden ser utilizadas bajo ninguna circunstancia.
El sistema debe ubicar los siguientes tipos de módulos:
TipoIdentificadorDescripciónMódulo habitacional"hab"Dormitorios y área de descanso de la tripulaciónGenerador"gen"Planta de energía solar del campamentoLaboratorio"lab"Estación científica para el análisis de muestrasDepósito"dep"Almacén de suministros y muestras recolectadasEsclusa de aire"air"Punto de entrada y salida hacia la superficie marciana
Restricciones

Sin superposición: no puede haber dos módulos en la misma celda.
Cráteres intransitables: ningún módulo puede ubicarse en una celda marcada como cráter.
Esclusas en el borde: toda esclusa debe estar en el borde del mapa (primera o última fila, o primera o última columna), ya que necesita acceso directo al exterior.
Habitacionales al interior: ningún módulo habitacional puede estar en el borde del mapa; necesitan una capa de protección contra los elementos marcianos.
Seguridad energética: un generador no puede ser adyacente a un módulo habitacional (riesgo de radiación para la tripulación).
Aislamiento entre generadores: dos generadores no pueden ser adyacentes entre sí (interferencia en la red de distribución energética).
Cadena de suministro científico: cada laboratorio debe ser adyacente a al menos un depósito (acceso inmediato a muestras y suministros).
Ruta de evacuación: cada módulo habitacional debe tener al menos una celda adyacente libre (sin módulo ni cráter), que sirva como ruta de emergencia.
Se considera adyacencia ortogonal: arriba, abajo, izquierda y derecha (no diagonal).
Consignas

Ejercicio 1

Formular el problema de diseño del campamento como un CSP usando la biblioteca SimpleAI. Definir con precisión:
Variables: ¿qué elementos del problema hay que determinar?
Dominios: ¿qué valores posibles puede tomar cada variable?
Restricciones: implementar cada una de las ocho restricciones listadas como funciones compatibles con SimpleAI, indicando sobre qué variables actúa cada una.
Ejercicio 2

Implementar la función build_camp con la siguiente interfaz exacta:
def build_camp(camp_size, habs, generators, labs, deposits, airlocks, craters):
    ...

Parámetros:
camp_size: tupla (filas, columnas) con las dimensiones de la cuadrícula.
habs: entero, cantidad de módulos habitacionales a ubicar.
generators: entero, cantidad de generadores a ubicar.
labs: entero, cantidad de laboratorios a ubicar.
deposits: entero, cantidad de depósitos a ubicar.
airlocks: entero, cantidad de esclusas a ubicar.
craters: lista de tuplas (fila, columna) con las celdas inaccesibles.
Resultado:
Lista de tuplas (tipo, fila, columna), donde tipo es uno de "hab", "gen", "lab", "dep" o "air". Las filas y columnas son índices base 0.
Si no existe ninguna distribución válida que satisfaga todas las restricciones, retornar None.
Ejemplo de uso:
resultado = build_camp(
    camp_size=(5, 6),
    habs=2,
    generators=1,
    labs=1,
    deposits=2,
    airlocks=1,
    craters=[(2, 2), (2, 3)],
)# Una posible salida válida:# [#     ("air", 0, 3),#     ("hab", 2, 1), ("hab", 2, 4),#     ("gen", 4, 4),#     ("lab", 3, 2),#     ("dep", 3, 1), ("dep", 3, 3),# ]

Importante: el módulo no debe ejecutar el CSP al momento de ser importado. Toda lógica de resolución debe estar dentro de la función build_camp.
Ejercicio 3

Utilizar una herramienta de Inteligencia Artificial generativa (Claude, GitHub Copilot, ChatGPT, Gemini, etc.) para resolver el problema planteado, entregando el código generado sin modificaciones sustanciales.
Luego, analizar las diferencias entre la solución propia y la generada por IA en un texto de no más de 4 párrafos, considerando aspectos como: formulación del CSP, elección de variables y dominios, implementación de restricciones, legibilidad y corrección.
Entregables

ArchivoDescripciónentrega2.pySolución propia. Debe contener la función build_camp con la interfaz exacta descrita.entrega2_por_ia.pySolución generada íntegramente por una herramienta de IA.conclusiones_entrega2.mdAnálisis comparativo entre ambas soluciones (máximo 4 párrafos).
Todos los archivos deben estar en la raíz del repositorio.
La solución debe pasar todos los tests unitarios provistos por la cátedra. Una entrega que no pasa los tests, no se considera entregada. Para correr los tests, deben bajar el archivo test_entrega2.py del directorio 2026 en el repo de la cátedra (este archivo), y ubicarlo en la raíz del repositorio del grupo. Correrlos con la misma metodología explicada en la entrega 1, asegurándose de que todas las pruebas pasen antes de presentar la entrega.
Al importar el módulo, no se debe ejecutar sola ninguna búsqueda que demore. Solo se deben ejecutar búsquedas cuando se llama a la función pedida.
Criterios de Evaluación

Correctitud de la formulación CSP: variables, dominios y restricciones bien definidos.
Implementación correcta de las ocho restricciones.
Cumplimiento exacto de la interfaz de build_camp (nombres, tipos y semántica de parámetros y retorno).
Aprobación de los tests unitarios automatizados.
Calidad y profundidad del análisis comparativo en conclusiones_entrega2.md. - import warnings
from contextlib import contextmanager
from collections import namedtuple
from datetime import datetime
from inspect import signature
from itertools import combinations

import pytest


# test names, comments and printable error messages in spanish to help students


@contextmanager
def duration_warning(time_limit_s, message):
    """
    Context manager to check the duration of a piece of executed code, and trigger a warning if
    it's too much.
    """
    start = datetime.now()

    yield

    end = datetime.now()

    seconds = int((end - start).total_seconds())
    if time_limit_s is not None and seconds > time_limit_s:
        warnings.warn(message + f" [duración: {seconds} segundos]")


@pytest.mark.dependency()
def test_modulo_existe():
    # Si falla este test es porque no se pudo encontrar el código python de la entrega.
    # Probablemente el nombre del archivo no es correcto (debe ser entrega2.py), o no está en la
    # raiz del repo, o no se están corriendo los tests desde la raiz del repo.
    duration_msg = (
        "El import de la entrega demora demasiado tiempo, probablemente están "
        "ejecutando el CSP al importar el módulo. Toda la lógica de resolución "
        "debe estar dentro de la función pedida, no a nivel de módulo."
    )
    with duration_warning(1, duration_msg):
        try:
            import entrega2
        except ModuleNotFoundError:
            pytest.fail("No se encuentra el módulo entrega2.py")


@pytest.fixture()
def build_camp():
    import entrega2
    fn = getattr(entrega2, "build_camp", None)
    return fn


@pytest.mark.dependency(depends=["test_modulo_existe"])
def test_funcion_existe(build_camp):
    assert build_camp is not None, "La función build_camp no existe en entrega2.py"


@pytest.mark.dependency(depends=["test_funcion_existe"])
def test_funcion_bien_definida(build_camp):
    params = list(signature(build_camp).parameters)
    expected_params = [
        "camp_size",
        "habs",
        "generators",
        "labs",
        "deposits",
        "airlocks",
        "craters",
    ]
    assert params[: len(expected_params)] == expected_params, (
        "La función build_camp no recibe los parámetros definidos en la entrega"
    )


Case = namedtuple(
    "Case",
    [
        "id",
        "description",
        "camp_size",
        "habs",
        "generators",
        "labs",
        "deposits",
        "airlocks",
        "craters",
        "is_possible",
        "time_limit_s",
    ],
)


def validate_result(
    result, camp_size, habs, generators, labs, deposits, airlocks, craters, case_name
):
    rows, cols = camp_size
    craters_set = set(craters)

    assert isinstance(result, (list, tuple)), (
        f"{case_name}: el resultado de build_camp no es una lista sino {type(result)}"
    )

    valid_types = {"hab", "gen", "lab", "dep", "air"}
    positions = {}

    for item in result:
        assert isinstance(item, (list, tuple)) and len(item) == 3, (
            f"{case_name}: cada elemento debe ser una tupla (tipo, fila, columna), se obtuvo {item}"
        )
        tipo, r, c = item

        assert tipo in valid_types, (
            f"{case_name}: tipo de módulo inválido '{tipo}', debe ser uno de {valid_types}"
        )
        assert 0 <= r < rows, (
            f"{case_name}: fila {r} fuera de la cuadrícula (rango válido: 0 a {rows - 1})"
        )
        assert 0 <= c < cols, (
            f"{case_name}: columna {c} fuera de la cuadrícula (rango válido: 0 a {cols - 1})"
        )

        pos = (r, c)

        # Restricción 1: sin superposición
        assert pos not in positions, (
            f"{case_name}: superposición en la celda {pos} ('{tipo}' y '{positions[pos]}')"
        )
        positions[pos] = tipo

        # Restricción 2: no en cráteres
        assert pos not in craters_set, (
            f"{case_name}: el módulo '{tipo}' está ubicado en el cráter {pos}"
        )

    # Verificar que se colocaron exactamente las cantidades pedidas
    counts = {t: 0 for t in valid_types}
    for tipo, r, c in result:
        counts[tipo] += 1

    assert counts["hab"] == habs, (
        f"{case_name}: se esperaban {habs} habitacional(es), se obtuvieron {counts['hab']}"
    )
    assert counts["gen"] == generators, (
        f"{case_name}: se esperaban {generators} generador(es), se obtuvieron {counts['gen']}"
    )
    assert counts["lab"] == labs, (
        f"{case_name}: se esperaban {labs} laboratorio(s), se obtuvieron {counts['lab']}"
    )
    assert counts["dep"] == deposits, (
        f"{case_name}: se esperaban {deposits} depósito(s), se obtuvieron {counts['dep']}"
    )
    assert counts["air"] == airlocks, (
        f"{case_name}: se esperaban {airlocks} esclusa(s), se obtuvieron {counts['air']}"
    )

    def is_border(r, c):
        return r == 0 or r == rows - 1 or c == 0 or c == cols - 1

    def adjacent(r1, c1, r2, c2):
        return abs(r1 - r2) + abs(c1 - c2) == 1

    def neighbors(r, c):
        return [
            (r + dr, c + dc)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if 0 <= r + dr < rows and 0 <= c + dc < cols
        ]

    habs_pos = [(r, c) for t, r, c in result if t == "hab"]
    gens_pos = [(r, c) for t, r, c in result if t == "gen"]
    labs_pos = [(r, c) for t, r, c in result if t == "lab"]
    deps_pos = [(r, c) for t, r, c in result if t == "dep"]

    # Restricción 3: esclusas en el borde
    for t, r, c in result:
        if t == "air":
            assert is_border(r, c), (
                f"{case_name}: esclusa en ({r},{c}) no está en el borde del mapa"
            )

    # Restricción 4: habitacionales al interior
    for r, c in habs_pos:
        assert not is_border(r, c), (
            f"{case_name}: módulo habitacional en ({r},{c}) está en el borde del mapa"
        )

    # Restricción 5: generador no adyacente a habitacional
    for gr, gc in gens_pos:
        for hr, hc in habs_pos:
            assert not adjacent(gr, gc, hr, hc), (
                f"{case_name}: generador en ({gr},{gc}) es adyacente al habitacional en ({hr},{hc})"
            )

    # Restricción 6: generadores no adyacentes entre sí
    for (gr1, gc1), (gr2, gc2) in combinations(gens_pos, 2):
        assert not adjacent(gr1, gc1, gr2, gc2), (
            f"{case_name}: generadores en ({gr1},{gc1}) y ({gr2},{gc2}) son adyacentes entre sí"
        )

    # Restricción 7: laboratorio adyacente a al menos un depósito
    for lr, lc in labs_pos:
        assert any(adjacent(lr, lc, dr, dc) for dr, dc in deps_pos), (
            f"{case_name}: laboratorio en ({lr},{lc}) no tiene ningún depósito adyacente"
        )

    # Restricción 8: habitacional con al menos una celda adyacente libre (ruta de evacuación)
    occupied = set((r, c) for t, r, c in result) | craters_set
    for hr, hc in habs_pos:
        adj_cells = neighbors(hr, hc)
        assert any((ar, ac) not in occupied for ar, ac in adj_cells), (
            f"{case_name}: habitacional en ({hr},{hc}) no tiene ninguna celda adyacente libre para evacuación"
        )


@pytest.mark.dependency(depends=["test_funcion_bien_definida"])
@pytest.mark.parametrize(
    "case",
    (
        # Casos simples: restricciones básicas, respuesta rápida esperada

        Case(
            id="s1",
            description="sin módulos: debe retornar lista vacía",
            camp_size=(4, 4),
            habs=0, generators=0, labs=0, deposits=0, airlocks=0,
            craters=[],
            is_possible=True,
            time_limit_s=2,
        ),
        Case(
            id="s2",
            description="una sola esclusa debe quedar en el borde",
            camp_size=(4, 4),
            habs=0, generators=0, labs=0, deposits=0, airlocks=1,
            craters=[],
            is_possible=True,
            time_limit_s=5,
        ),
        Case(
            id="s3",
            description="habitacionales deben quedar al interior del mapa",
            camp_size=(5, 5),
            habs=2, generators=0, labs=0, deposits=0, airlocks=0,
            craters=[],
            is_possible=True,
            time_limit_s=10,
        ),
        Case(
            id="s4",
            description="generador no puede ser adyacente a habitacional",
            camp_size=(4, 5),
            habs=1, generators=1, labs=0, deposits=0, airlocks=0,
            craters=[],
            is_possible=True,
            time_limit_s=15,
        ),
        Case(
            id="s5",
            description="laboratorio debe quedar adyacente a al menos un depósito",
            camp_size=(4, 5),
            habs=0, generators=0, labs=1, deposits=1, airlocks=0,
            craters=[],
            is_possible=True,
            time_limit_s=15,
        ),
        Case(
            id="s6",
            description="caso completo con todos los tipos de módulos en grilla chica",
            camp_size=(5, 5),
            habs=1, generators=1, labs=1, deposits=1, airlocks=1,
            craters=[],
            is_possible=True,
            time_limit_s=60,
        ),

        # Casos medianos: combinaciones de restricciones más exigentes

        Case(
            id="m1",
            description="dos generadores no pueden ser adyacentes entre sí",
            camp_size=(5, 5),
            habs=0, generators=2, labs=0, deposits=0, airlocks=0,
            craters=[],
            is_possible=True,
            time_limit_s=30,
        ),
        Case(
            id="m2",
            description="dos laboratorios, cada uno debe tener su depósito adyacente",
            camp_size=(5, 6),
            habs=0, generators=0, labs=2, deposits=2, airlocks=0,
            craters=[],
            is_possible=True,
            time_limit_s=60,
        ),
        Case(
            id="m3",
            description="cráteres que restringen la ubicación de los módulos",
            camp_size=(5, 6),
            habs=2, generators=1, labs=1, deposits=2, airlocks=1,
            craters=[(2, 2), (2, 3)],
            is_possible=True,
            time_limit_s=120,
        ),
        Case(
            id="m4",
            description="múltiples módulos de cada tipo, todas las restricciones activas",
            camp_size=(6, 7),
            habs=3, generators=2, labs=2, deposits=3, airlocks=2,
            craters=[(1, 3), (4, 5)],
            is_possible=True,
            time_limit_s=300,
        ),

        # Casos imposibles: el CSP no debe encontrar solución

        Case(
            id="i1",
            description="grilla de 2 filas no tiene celdas interiores para habitacionales",
            camp_size=(2, 6),
            habs=1, generators=0, labs=0, deposits=0, airlocks=0,
            craters=[],
            is_possible=False,
            time_limit_s=10,
        ),
        Case(
            id="i2",
            description="todas las celdas del borde son cráteres, la esclusa no puede ubicarse",
            camp_size=(3, 3),
            habs=0, generators=0, labs=0, deposits=0, airlocks=1,
            craters=[(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
            is_possible=False,
            time_limit_s=10,
        ),
    ),
)
def test_resultado_es_correcto(build_camp, case):
    (
        id_,
        description,
        camp_size,
        habs,
        generators,
        labs,
        deposits,
        airlocks,
        craters,
        is_possible,
        time_limit_s,
    ) = case

    craters = tuple(craters)
    case_name = f"[{id_}: {description}]"
    duration_msg = (
        f"El caso {case_name} demoró demasiado tiempo (más de {time_limit_s} segundos), "
        "probablemente algo no está bien con la implementación del CSP"
    )

    with duration_warning(time_limit_s, duration_msg):
        print()
        print("Resolviendo caso", case_name)
        print(
            f"{camp_size=} {habs=} {generators=} {labs=} {deposits=} {airlocks=} {craters=}"
        )
        start = datetime.now()
        result = build_camp(camp_size, habs, generators, labs, deposits, airlocks, craters)
        end = datetime.now()
        duration_seconds = (end - start).total_seconds()
        print(f"Solución obtenida en {duration_seconds:.1f} segundos: {result}")

    if not is_possible:
        assert result is None, (
            f"{case_name}: se esperaba None (caso sin solución posible) pero se obtuvo: {result}"
        )
        print(f"Caso {case_name} correctamente identificado como imposible.")
        return

    assert result is not None, (
        f"{case_name}: build_camp retornó None, pero existe al menos una solución válida para este caso"
    )

    validate_result(
        result, camp_size, habs, generators, labs, deposits, airlocks, craters, case_name
    )
    print(f"Caso {case_name} resuelto correctamente con {len(result)} módulos ubicados.