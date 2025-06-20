# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from oa_solver import solve_oa        # Si queremos que use Hexaly
#from oa_solver_gurobi import solve_oa   # Si queremos que use Gurobi

import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    objective = None
    time_taken = None
    params = None
    if request.method == "POST":
        try:
            N = int(request.form.get("N"))
            k = int(request.form.get("k"))
            s = int(request.form.get("s"))
            t = int(request.form.get("t"))
            output = solve_oa(N, k, s, t)
            if isinstance(output, dict):
                result = output["rows"]
                objective = output["objective"]
                time_taken = output.get("time")
            else:
                result = output  
        except Exception as e:
            error = "Error en los datos ingresados: {}".format(str(e))
        params = {"N": N, "k": k, "s": s, "t": t}

    return render_template("index.html", result=result, objective=objective, error=error, time=time_taken, params=params)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
