# -*- coding: utf-8 -*-

# import itertools
# import numpy as np
# from hexaly.optimizer import HexalyOptimizer, HxModel, HxSolutionStatus

# def solve_oa(N, k, s, t):
#     lambda_value = N / s**t
#     if t > k or lambda_value * s**t != N:
#         return "Parámetros inválidos"

#     lambda_value = int(lambda_value)
#     tupla = list(itertools.combinations(range(k), t))
#     sequences = lambda base, digits: [list(map(int, np.base_repr(x, base=base).zfill(digits))) for x in range(base**digits)]
#     allrows = sequences(s, k)
#     intupla = sequences(s, t)
#     outupla = sequences(s, k - t)

#     def row(index, inside, outside):
#         r = np.zeros(k, dtype=int)
#         for i in range(t):
#             r[index[i]] = inside[i]
#         other = [x for x in range(k) if x not in index]
#         for i in range(k - t):
#             r[other[i]] = outside[i]
#         return tuple(r)

#     with HexalyOptimizer() as optimizer:
#         model = HxModel(optimizer)
#         x = {tuple(row_value): model.int(0, 1) for row_value in allrows}

#         for i in tupla:
#             for j in intupla:
#                 model.add_constraint(sum(x[row(i, j, l)] for l in outupla) == lambda_value)

#         model.minimize(sum(x[rv] for rv in allrows))
#         model.close()
#         optimizer.solve()

#         if optimizer.solution.status == HxSolutionStatus.OPTIMAL:
#             result = [list(rv) for rv in allrows if x[tuple(rv)].value == 1]
#             return result
#         else:
#             return "No se encontró una solución óptima"

import itertools
import numpy as np
from hexaly.optimizer import HexalyOptimizer, HxModel, HxSolutionStatus

def solve_oa(N, k, s, t):
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

            if optimizer.solution.status == HxSolutionStatus.OPTIMAL:
                result = [rv for rv in allrows if x[tuple(rv)].value == 1]
                obj_value = int(optimizer.solution.get_objective_bound(0))
                return {"rows": result, "objective": obj_value}
            else:
                return "No se encontró una solución óptima"

    except Exception as e:
        return "Error interno: {}".format(str(e))
