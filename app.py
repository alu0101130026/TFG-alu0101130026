# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from oa_solver import solve_oa

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    objective = None
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
            else:
                result = output  # será string de error
        except Exception as e:
            error = "Error en los datos ingresados: {}".format(str(e))
    return render_template("index.html", result=result, objective=objective, error=error)



if __name__ == "__main__":
    app.run(debug=True)
