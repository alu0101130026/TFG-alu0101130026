# -*- coding: utf-8 -*-

"""
oa_solver_gurobi.py

Generador de Arrays Ortogonales (OA) usando Gurobi como solver.

Autor: Diego Díaz Fernández
Fecha: 11-07-2025
Descripción:
    Resuelve el problema de generación de OA(N, k, s, t) 
    optimizando el número de filas seleccionadas que satisfacen
    todas las combinaciones posibles de t-factores.

Dependencias:
    - numpy
    - itertools
    - gurobipy
"""


import itertools
import numpy as np
import gurobipy as gp
from gurobipy import GRB
import time

def solve_oa(N, k, s, t):
    try:
        start_time = time.time()
        lambda_value = float(N) / (s ** t)
        if t > k or lambda_value * (s ** t) != N:
            return "Parámetros inválidos"

        lambda_value = int(lambda_value)
        tuplas = list(itertools.combinations(range(k), t))

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

        model = gp.Model("oa_generator")
        model.Params.OutputFlag = 0 

        x = {}
        for rv in allrows:
            x[tuple(rv)] = model.addVar(vtype=GRB.BINARY, name=f"x{rv}")

        for idx in tuplas:
            for j in intupla:
                model.addConstr(
                    gp.quicksum(x[row(idx, j, l)] for l in outupla) == lambda_value
                )

        model.setObjective(
            gp.quicksum(x[tuple(rv)] for rv in allrows),
            GRB.MINIMIZE
        )

        model.optimize()

        if model.Status == GRB.OPTIMAL:
            selected = [list(rv) for rv in allrows if x[tuple(rv)].X > 0.5]
            elapsed = round(time.time() - start_time, 4)
            return {
                "rows": selected,
                "objective": len(selected),
                "time": elapsed
            }
        else:
            return "No se encontró una solución óptima"

    except Exception as e:
        return "Error interno: {}".format(str(e))
