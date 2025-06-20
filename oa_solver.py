# -*- coding: utf-8 -*-

"""
oa_solver.py

Generador de Arrays Ortogonales (OA) usando Hexaly Optimizer.

Autor: Diego Díaz Fernández
Fecha: 11-07-2025
Descripción:
    Este módulo resuelve el problema OA(N, k, s, t) utilizando
    el solver Hexaly para encontrar una matriz de tamaño mínimo
    que cumpla con todas las combinaciones de t-factores.

Dependencias:
    - numpy
    - itertools
    - hexaly (HxModel, HexalyOptimizer, HXSolutionStatus)
"""

import time
import itertools
import numpy as np
from hexaly.optimizer import HexalyOptimizer, HxModel, HxSolutionStatus


def solve_oa(N, k, s, t):
    start_time = time.time()
    try:
        lambda_value = float(N) / (s ** t)
        if t > k or lambda_value * (s ** t) != N:
            return "Parámetros inválidos"

        lambda_value = int(lambda_value)
        tupla = list(itertools.combinations(range(k), t))

        def sequences(base, digits):
            return [list(map(int, list(np.base_repr(x, base=base).zfill(digits)))) for x in range(base ** digits)]

        allrows = sequences(s, k)
        intupla = sequences(s, t)
        outupla = sequences(s, k - t)

        def row(index, inside, outside):
            r = [0] * k
            for i in range(t):
                r[index[i]] = inside[i]
            other = [x for x in range(k) if x not in index]
            for i in range(k - t):
                r[other[i]] = outside[i]
            return tuple(r)

        with HexalyOptimizer() as optimizer:
            model = HxModel(optimizer)

            x = {}
            for row_value in allrows:
                x[tuple(row_value)] = model.int(0, 1)

            for i in tupla:
                for j in intupla:
                    model.add_constraint(
                        sum([x[row(i, j, l)] for l in outupla]) == lambda_value
                    )

            model.minimize(sum([x[tuple(rv)] for rv in allrows]))
            model.close()
            optimizer.solve()
            elapsed = round(time.time() - start_time, 4)

            if optimizer.solution.status == HxSolutionStatus.OPTIMAL:
                result = [rv for rv in allrows if x[tuple(rv)].value == 1]
                obj_value = int(optimizer.solution.get_objective_bound(0))
                return {"rows": result, "objective": obj_value, "time": elapsed}
            else:
                return "No se encontró una solución óptima"

    except Exception as e:
        return "Error interno: {}".format(str(e))
