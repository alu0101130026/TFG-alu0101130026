# 🔧 Generador de Arrays Ortogonales (OA)

Aplicación web interactiva desarrollada con Python y Flask que permite generar **Arrays Ortogonales** OA(N, k, s, t), resolviendo el problema mediante distintos solvers de optimización:

- [Hexaly Optimizer](https://www.hexaly.com/)
- [Gurobi Optimizer](https://www.gurobi.com/)

---

## 🧮 ¿Qué es un Array Ortogonal?

Un array ortogonal OA(N, k, s, t) es una matriz de `N` filas y `k` columnas que garantiza que **cada combinación posible de `t` columnas** contiene **todas las combinaciones de `s` símbolos** exactamente `λ` veces.

Estos arrays tienen aplicaciones en:

- Diseño de experimentos
- Pruebas de software
- Codificación y transmisión de datos

---

## 🚀 Cómo ejecutar la aplicación localmente

### 1. Clona el repositorio

```bash
git clone https://github.com/tuusuario/oa-web.git
cd oa-web
```

2. Crea y activa un entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instala dependencias
```bash
pip install -r requirements.txt
pip install hexaly -i https://pip.hexaly.com   # Solo si usas Hexaly
```
Si usas Gurobi, asegúrate de tenerlo instalado y licenciado localmente.

4. Ejecuta la app
```bash
python app.py
```
5. Accede desde tu navegador en http://localhost:5000

⚙️ Solvers disponibles
Solver	Archivo	Requisitos
Hexaly	oa_solver.py	Hexaly Optimizer + licencia
Gurobi	oa_solver_gurobi.py	Gurobi instalado y activado

Puedes alternar entre ellos editando app.py:
```bash
from oa_solver_gurobi import solve_oa  # Gurobi
# from oa_solver import solve_oa      # Hexaly
```

💡 Características

    Interfaz web clara y responsiva 

    Entrada validada por formulario

    Visualización de la matriz generada

    Indicadores de tiempo de resolución

📁 Estructura del proyecto

├── app.py
├── oa_solver.py               # Versión con Hexaly
├── oa_solver_gurobi.py        # Versión con Gurobi
├── requirements.txt
├── render.yaml                # Configuración para despliegue en Render
├── templates/
│   └── index.html             # Interfaz web

✍️ Autor

Diego Díaz Fernández
alu0101130026@ull.edu.es
Universidad de La Laguna

🌐 Despliegue online

[Generador](https://array-ortogonal.onrender.com) 