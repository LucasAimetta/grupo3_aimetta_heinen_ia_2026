Necesito que resuelvas el enunicado que te envié en el txt y utilizando SimpleAI, teniendo en cuenta todo lo que dice el profesor y además deben pasar todos los test. Adjunto también las imágenes de como es el formato de respuesta de los test. 


Se desea programar el sistema de navegación para el explorador Ares-1 en Marte. El rover aterriza en una grilla que representa la superficie marciana. Su objetivo es juntar todas las muestras de rocas en el menor tiempo posible y dejar pequeñas "cápsulas" de muestras en el suelo, que luego serán recogidas por una futura misión.

Pero existen algunas restricciones:

Requisitos de herramientas: Existen dos tipos de muestras de rocas. Las rocas Ígneas requieren un taladro térmico, mientras que las rocas Sedimentarias requieren un taladro de percusión (nunca hay dos tipos de piedra diferentes en el mismo lugar). Y el rover solo puede tener activo un taladro a la vez, cambiar de taladro es una acción que cuesta tiempo y consume batería.
Capacidad de carga: El rover puede llevar un máximo de 2 muestras al mismo tiempo. Para recolectar más, primero debe vaciar su carga actual depositando las cápsulas de muestras en el suelo (en cualquier parte del mapa).
Batería limitada: El rover tiene batería limitada, si en algún momento se queda sin batería se perdería para siempre. Por ello, su batería nunca debe llegar a 0.
Para cumplir con su objetivo, el rover puede ejecutar las siguientes acciones:

Moverse: A cualquier celda adyacente (arriba, abajo, izquierda, derecha). Toma 1 minuto, consume 1 unidad de batería.

Sobremarcha (Overdrive): Moverse exactamente 2 celdas en línea recta (saltando por encima de la celda intermedia). Toma 1 minuto, consume 4 unidades de batería.

Equipar taladro: Cambia el taladro activo por el otro tipo (o equipa uno si todavía no tiene un taladro activo). Toma 3 minutos, consume 1 unidad de batería.

Perforar y recolectar: Si está en una celda con una muestra, tiene el taladro correcto equipado y tiene espacio disponible en la bodega de carga. Toma 2 minutos, consume 3 unidades de batería.

Depositar cápsula con muestras: Si tiene carga, vacía todas las muestras de la bodega de carga y las deja en una cápsula en el piso. Toma 1 minuto por muestra entregada, consume 1 unidad de batería. Para armar una cápsula es necesario que el rover tenga 2 muestras cargadas, a menos que sea la última existente.

Desplegar paneles solares: El rover se detiene para recargar. Toma 4 minutos, restaura 10 unidades de batería (hasta el límite máximo de 20). Restricción: No se puede realizar esta acción en las "zonas de sombra" (coordenadas específicas provistas en el mapa).

Implementación

La implementación consistirá en tener una función planear_rover que recibirá como parámetros:

# todas las coordenadas son en formato (fila, columna)
acciones = planear_rover(
    rover_inicio=(0, 0),
    bateria_inicial=20,
    zonas_sombra=[(0, 1), (0, 2)],
    muestras_igneas=[(1, 1), (1, 2)],
    muestras_sedimentarias=[(2, 3)],
)

Los valores de los parámetros pueden cambiar, y vamos a probar con diferentes escenarios posibles de distintos niveles de complejidad.

El resultado deberá ser una lista de las acciones a realizar. Cada acción debe ser una tupla con el siguiente formato: (str_tipo_accion, parametro_opcional).

Los tipos de acciones son los siguientes:

"moverse": para estas acciones, el segundo elemento de la tupla debe ser las coordenadas hacia donde se mueve el rover. Por ejemplo: ("moverse", (2, 4)).
"sobremarcha": para estas acciones, el segundo elemento de la tupla debe ser las coordenadas hacia donde se mueve el rover. Por ejemplo: ("sobremarcha", (2, 5)).
"equipar": equipar un tipo de taladro. El segundo elemento de la tupla es el tipo de taladro a equipar, que puede ser "termico" o "percusión". Ejemplo: ("equipar", "termico").
"recolectar": recolectar una muestra. El segundo elemento de la tupla es el tipo de muestra a recolectar, que puede ser "ignea" o "sedimentaria". Ejemplo: ("recolectar", "ignea").
"depositar": deposita la carga en piso, vaciando la bahía de carga. No requiere un segundo elemento, por lo que se debe dejar como None. Ejemplo: ("entregar", None).
"recargar": desplegar paneles solares para recargar la batería. No requiere un segundo elemento, por lo que se debe dejar como None. Ejemplo: ("recargar", None).
Por ejemplo, un resultado (incompleto, ilustrativo) podría ser el siguiente:

print(acciones)
[
    ("moverse", (0, 1)),
    ("moverse", (0, 2)),
    ("recargar", None),
    ("moverse", (1, 2)),
    ("moverse", (2, 2)),
    ("equipar", "termico"),
    ("moverse", (3, 2)),
    ("moverse", (3, 3)),
    ("recolectar", "ignea"),
    ("moverse", (3, 4)),
    ("recolectar", "ignea"),
    ("depositar", None),
    ...  # y así hasta resolver todo el problema
]

La secuencia de acciones tiene que ser válida (se tienen que poder realizar esos movimientos bajo las restricciones explicadas). Y tiene que ser la secuencia de acciones que menos tiempo requiera para conseguir el objetivo.

Todos los casos que vamos a probar son resolubles.

Ejercicios:
Implementar la formulación del problema como problema de búsqueda tradicional para ser resuelto con SimpleAI, incluyendo definición de la clase problema y sus métodos: cost, actions, result, is_goal y heuristic (la heurística puede ser poco precisa, pero debe ser admisible).

Implementar la función planear_rover con exactamente la api detallada en la sección anterior (tanto para los datos esperados de entrada, como para el resultado devuelto).

Utilizar algún agente o editor de código asistido por IA (como Claude Code, Codex, Copilot, etc) para resolver el problema: presentarle la consigna y pedirle que la resuelva utilizando SimpleAI. Luego comparar la solución que les dio con la que ustedes implementaron, y analizar las diferencias entre ambas: qué diferencias hay en el enfoque (estado, acciones, heurística, etc)? Logró resolverlo pasando todos los tests? Cómo se comparan en pérformance? Escribir las conclusiones en no más de 4 párrafos.

Formato de entrega:
Se debe informar al grupo de Google de la materia: el número de grupo, los integrantes del mismo, y la url del repositorio git donde realizarán la entrega. Si el repositorio es privado, además deben darnos acceso a nuestros usuarios: fisadev, mfferrero, arielrossanigo, federicofrancesconi. Se va a utilizar un mismo repositorio para todas las entregas, por lo que el nombre del repo debería ser algo representativo del grupo (ej: "grupo1", "grupo_apellido1_apellido2", etc), y NO algo como "entrega_1" (porque en el mismo repo estarán todas las entregas).

La resolución del ejercicio debe realizarse en un archivo llamado entrega1.py, que debe ser subido a la raíz del repositorio git del grupo (no dentro de ningún subdirectorio).

El módulo debe tener la función pedida por la consigna, que reciba los parámetros mostrados anteriormente, y devuelva el resultado esperado en el formato explicado anteriormente.

Al importar el módulo, no se debe ejecutar sola ninguna búsqueda que demore. Solo se deben ejecutar búsquedas cuando se llama a la función pedida. En este archivo solo dejen la entrega, y si lo desean, para pruebas pueden tener otro .py que importe la entrega y ejecute las pruebas que ustedes quieren hacer.

Subir la resolución que les dio la IA en un archivo entrega1_por_ia.py también en la raíz del repo.

Agregar un archivo conclusiones_entrega1.md en la raíz del repositorio del grupo, con las conclusiones del ejercicio 3.

Respetar nombres de archivos, funciones, parámetros y tipos de datos exactamente como se explican en este enunciado. Cualquier falla por no respetar la interfaz definida, se considera no entregado.

Desde la materia desarrollamos un conjunto de unit tests que les validan muchísimo del funcionamiento de la entrega. La entrega debería pasar todos los tests antes de ser presentada, ya que una entrega que no pasa los tests se considera no resuelta.

Estos tests son también muy muy MUY útiles durante el desarrollo, por lo que les recomendamos que los ejecuten cada vez que quieran probar cosas, y que si tienen problemas nos envíen siempre el resultado de correrlos.

Para correr los tests, deben bajar el archivo test_entrega1.py del directorio 2026 en el repo de la cátedra (este archivo), y ubicarlo en la raíz del repositorio del grupo. Una vez allí, instalen las dependencias necesarias para correrlo dentro del entorno que recomendamos crear con uv:

uv pip install pytest pytest-dependency
(info sobre cómo usar virtualenvs)

Y luego pueden correr los tests de esta forma:

uv run pytest -v
Si eso no funciona, pueden estar seguros de que algo no están haciendo bien. En los casos de error más comunes, los tests pueden explicarles lo que están haciendo mal. En casos más raros, no tanto. Recuerden que pueden preguntar en el grupo todo lo que necesiten!

El resultado de una corrida exitosa de tests se ve así:

image

(ejemplo con pocos tests de otro año, pero la cantidad de tests va a ir creciendo a medida que agreguemos casos de ejemplo. Mantengan actualizado el archivo de tests que tienen bajado!)

Y utilizando uv run pytest -vvv -s pueden ver mucha más info de debug sobre las soluciones que devuelven en cada caso!

Mientras que el resultado cuando hay errores o advertencias (recuerden mirar ambas cosas!) se ve así:

image

Como pueden ver, es super útil para entender qué pueden estar haciendo mal. Miren especialmente el texto en rojo, que les indica bien claro cuál es el problema, y la última linea en rojo, que les dice cuántos tests fallaron en total.

Notas útiles:

Los viewers son útiles para probar y visualizar cosas, encontrar problemas, etc. Pero recuerden desactivarlos para la versión entregada, de lo contrario cuando la corrección automática trate de llamar a los algoritmos, se va a quedar tildada esperando o va a demorar demasiado.

Test para tener en cuenta a la hora de resolver: 

import warnings
from contextlib import contextmanager
from collections import namedtuple
from datetime import datetime
from inspect import signature

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
    # Probablemente el nombre del archivo no es correcto (debe ser entrega1.py), o no está en la
    # raiz del repo, o no se están corriendo los tests desde la raiz del repo.
    duration_msg = ("El import de la entrega demora demasiado tiempo, probablemente están "
                    "haciendo búsqueda en el import. Hagan lo del if __name__ ... que se "
                    "recomienda en la consigna")
    with duration_warning(1, duration_msg):
        try:
            import entrega1
        except ModuleNotFoundError:
            pytest.fail("No se encuentra el módulo entrega1.py")


@pytest.fixture()
def planear_rover():
    import entrega1
    fn = getattr(entrega1, "planear_rover", None)
    return fn


@pytest.mark.dependency(depends=["test_modulo_existe"])
def test_funcion_existe(planear_rover):
    assert planear_rover is not None, "La función planear_rover no existe en entrega1.py"


@pytest.mark.dependency(depends=["test_funcion_existe"])
def test_funcion_bien_definida(planear_rover):
    params = list(signature(planear_rover).parameters)
    expected_params = [
        "rover_inicio",
        "bateria_inicial",
        "zonas_sombra",
        "muestras_igneas",
        "muestras_sedimentarias",
    ]

    # los primeros parámetros de la función tienen que ser los pedidos
    assert params[:len(expected_params)] == expected_params, \
           "La función planear_rover no recibe los parámetros definidos en la entrega"


Case = namedtuple(
    "Case",
    [
        "id",
        "description",
        "rover",
        "battery",
        "shadows",
        "igneous",
        "sediments",
        "expected_cost",  # costo de la solución esperada (óptima)
        "time_limit_s",  # tiempo máximo en segundos que planear_rover debería demorar en encontrar solución
    ],
)

@pytest.mark.dependency(depends=["test_funcion_bien_definida"])
@pytest.mark.parametrize("case", (
    # casos super simples donde hay que hacer casi nada

    Case(id="goal", description="sin muestras a recolectar, ya es meta",
         rover=(0, 0), battery=20, shadows=[],
         igneous=[], sediments=[],
         expected_cost=0, time_limit_s=1),

    # casos simples donde hay que hacer muy poco, con una sola muestra

    Case(id="s1", description="una sola muestra a recolectar, con bateria de sobra",
         rover=(0, 0), battery=20, shadows=[],
         igneous=[(0, 1)], sediments=[],
         expected_cost=7, time_limit_s=2),

    Case(id="s2", description="una sola muestra a recolectar del otro tipo",
         rover=(0, 0), battery=20, shadows=[],
         igneous=[], sediments=[(0, 1)],
         expected_cost=7, time_limit_s=2),

    Case(id="s3", description="una sola muestra a recolectar, pero lo ideal es con overdive",
         rover=(0, 0), battery=20, shadows=[],
         igneous=[(0, 2)], sediments=[],
         expected_cost=7, time_limit_s=2),

    Case(id="s4", description="una sola muestra a recolectar, pero hace falta cargar bateria antes",
         rover=(0, 0), battery=1, shadows=[],
         igneous=[(0, 1)], sediments=[],
         expected_cost=11, time_limit_s=2),

    Case(id="s5", description="una sola muestra a recolectar, pero hace falta cargar bateria y no en el lugar donde estamos",
         rover=(0, 0), battery=2, shadows=[(0, 0)],
         igneous=[(0, 1)], sediments=[],
         expected_cost=11, time_limit_s=2),

    # casos medianos donde hay que resolver situaciones un poco más interesantes

    Case(id="m1", description="3 muestras relativamente cerca",
         rover=(0, 0), battery=20, shadows=[],
         igneous=[(0, 1), (0, 2)], sediments=[(1, 1)],
         expected_cost=18, time_limit_s=30),

    Case(id="m2", description="3 muestras un poco más lejos",
         rover=(0, 0), battery=20, shadows=[],
         igneous=[(2, 2), (2, 3)], sediments=[(1, 1)],
         expected_cost=20, time_limit_s=30),

    Case(id="m3", description="1 muestra lejana",
         rover=(0, 0), battery=20, shadows=[],
         igneous=[(0, 30)], sediments=[],
         expected_cost=40, time_limit_s=30),

    Case(id="m4", description="2 muestras en direcciones opuestas",
         rover=(0, 0), battery=20, shadows=[],
         igneous=[(0, -5), (0, 5)], sediments=[],
         expected_cost=25, time_limit_s=60),

    Case(id="m5", description="1 muestra pero con poca batería y un camino muy específico entre las sombras",
         rover=(0, 0), battery=8, shadows=[
             (row, col)
             for col in range(-10, 10)
             for row in range(-10, 10)
             if (row, col) != (0, 7)
         ],
         igneous=[(5, 5)], sediments=[],
         expected_cost=25, time_limit_s=30),

    # casos grandes

    Case(id="g1", description="3 muestras en direcciones opuestas",
         rover=(0, 0), battery=20, shadows=[],
         igneous=[(0, -5), (0, 5), (5, 5)], sediments=[],
         expected_cost=36, time_limit_s=600),

    Case(id="g2", description="5 muestras",
         rover=(0, 0), battery=20, shadows=[],
         igneous=[], sediments=[(1, col) for col in range(5)],
         expected_cost=27, time_limit_s=200),
))
def test_resultado_es_correcto(planear_rover, case):
    id_, description, rover, battery, shadows, igneous, sediments, expected_cost, time_limit_s = case
    shadows = tuple(shadows)
    igneous = tuple(igneous)
    sediments = tuple(sediments)

    # helpers para mensajes de error y warnings
    case_name = f"[{id_}: {description}]"
    duration_msg = (f"El caso {case_name} demoró demasiado tiempo (más de {time_limit_s} "
                    "segundos), probablemente algo no está bien")

    with duration_warning(time_limit_s, duration_msg):
        print()
        print("Resolviendo caso", case_name)
        print(f"{rover=} {battery=} {shadows=} {igneous=} {sediments=}")
        print("...")
        start = datetime.now()
        result = planear_rover(rover, battery, shadows, igneous, sediments)
        end = datetime.now()
        duration_seconds = (end - start).total_seconds()
        print(f"Solución obtenida en {duration_seconds:.1f} segundos:")

    # otros helpers
    times = {
        "moverse": 1,
        "sobremarcha": 1,
        "equipar": 3,
        "recolectar": 2,
        "depositar": 1,
        "recargar": 4,
    }
    batt_consumptions = {
        "moverse": 1,
        "sobremarcha": 4,
        "equipar": 1,
        "recolectar": 3,
        "depositar": 1,
        "recargar": -10,  # consumo negativo = recarga
    }
    error_prefix = f"Error en caso {case_name}:"

    # chequeamos la estructura de datos de forma muy básica
    assert isinstance(result, (list, tuple)), \
        f"{error_prefix} el resultado de planear_rover no fue una lista, sino {type(result)}"

    # simulamos el resultado del juego usando un mundo mutable
    load = 0
    drill = "ninguno"
    max_batt = 20
    max_load = 2
    total_cost = 0  # in minutes

    print("Simulando pasos obtenidos...")
    # por cada accion, hacemos chequeos y vamos simulando todo para ver que sea posible
    for idx_action, action in enumerate(result):
        print(f"{rover=} {battery=} {load=} {drill=} {shadows=} {igneous=} {sediments=}", "-->", action)

        # helper para mensajes de error
        action_error_prefix = f"Error en {case_name} acción {idx_action}={action}:"

        assert isinstance(action, (list, tuple)), \
            f"{action_error_prefix} la acción no es una tupla, sino {type(action)}"
        assert len(action) == 2, \
            f"{action_error_prefix} la acción no es una tupla de 2 elementos, sino {action}"

        action_type, target = action
        assert action_type in times, \
            f"{action_error_prefix} el tipo de acción {action_type} no existe"

        battery = min(max_batt, battery - batt_consumptions[action_type])
        assert battery >= 0, \
            f"{action_error_prefix} la acción consume más batería de la disponible"
        assert battery > 0, \
            f"{action_error_prefix} el rover se quedó sin batería después de esta acción, nunca debe quedar sin batería"

        if action_type == "depositar":
            total_cost += times[action_type] * load
        else:
            total_cost += times[action_type]
        assert total_cost <= expected_cost, \
            f"{action_error_prefix} la acción hace que el tiempo total sea {total_cost}, pero no puede ser mayor a {expected_cost}"

        if action_type in ("moverse", "sobremarcha"):
            assert isinstance(target, (list, tuple)), \
                f"{action_error_prefix} el destino no es una tupla de posición, sino {type(target)}"
            assert len(action) == 2, \
                f"{action_error_prefix} el destino no es una coordenada de 2 elementos, sino {target}"

            rover_r, rover_c = rover

            if action_type == "moverse":
                move_valid_targets = [
                    (rover_r + 1, rover_c),
                    (rover_r - 1, rover_c),
                    (rover_r, rover_c + 1),
                    (rover_r, rover_c - 1),
                ]
                assert target in move_valid_targets, \
                    f"{action_error_prefix} movimiento hacia una casilla que no es adyacente de {rover}"
            elif action_type == "sobremarcha":
                overdrive_valid_targets = [
                    (rover_r + 2, rover_c),
                    (rover_r - 2, rover_c),
                    (rover_r, rover_c + 2),
                    (rover_r, rover_c - 2),
                ]
                assert target in overdrive_valid_targets, \
                    f"{action_error_prefix} sobremarcha hacia una casilla que no es destino válido desde {rover}"

            rover = target
        elif action_type == "equipar":
            assert target in ("termico", "percusion"), \
                "{action_error_prefix} el tipo de taladro a equipar no es válido: {target}"

            drill = target
        elif action_type == "recolectar":
            assert target in ("ignea", "sedimentaria"), \
                f"{action_error_prefix} el tipo de muestra a recolectar no es válido: {target}"

            assert load < max_load, \
                f"{action_error_prefix} el rover ya tiene la carga máxima de 2 muestras, no puede recolectar más sin depositar"

            if target == "ignea":
                assert drill == "termico", \
                    f"{action_error_prefix} para recolectar muestra ígnea se necesita el taladro térmico equipado"
                assert rover in igneous, \
                    f"{action_error_prefix} no hay muestra ígnea para recolectar en la posición del rover {rover}"

                igneous = tuple(m for m in igneous if m != rover)
            elif target == "sedimentaria":
                assert drill == "percusion", \
                    f"{action_error_prefix} para recolectar muestra sedimentaria se necesita el taladro de percusión equipado"
                assert rover in sediments, \
                    f"{action_error_prefix} no hay muestra sedimentaria para recolectar en la posición del rover {rover}"

                sediments = tuple(m for m in sediments if m != rover)

            load += 1
        elif action_type == "depositar":
            assert load, \
                f"{action_error_prefix} no hay muestras para depositar"

            assert load == 2 or (load == 1 and not (igneous + sediments)), \
                f"{action_error_prefix} solo se puede depositar 1 muestra si es la última"

            load = 0
        elif action_type == "recargar":
            assert rover not in shadows, \
                f"{action_error_prefix} no se puede recargar en una zona de sombra: {rover}"
            # no hay otro cambio más que actualizar battery, que ya se hizo arriba

    print("Simulación de pasos finalizada!")
    print("Costo total de la solución obtenida:", total_cost)

    # al final, el rover debería haber recolectado todas las muestras y dejado todas en el punto de extracción
    assert not load, f"{error_prefix} al final del proceso quedan cargas en el rover: {load}"
    assert not igneous, f"{error_prefix} al final del proceso quedan muestras ígneas por recolectar: {igneous}"
    assert not sediments, f"{error_prefix} al final del proceso quedan muestras sedimentarias por recolectar: {sediments}"

    # por las dudas, si lo resolvió mejor de lo esperado, revisar!
    if total_cost < expected_cost:
        warnings.warn(
            f"La solución para {case_name} fue mejor de lo esperado: {total_cost} mins, pero"
            f"se esperaba {expected_cost} mins"
        )
