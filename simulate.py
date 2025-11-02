# simulate.py
from typing import Dict, List, Tuple
import numpy as np
from sympy import symbols, sympify, lambdify
from scipy.integrate import solve_ivp

def _make_symbols(names: List[str]):
    # Always return a tuple, even for a single name
    if not names:
        return tuple()
    return symbols(" ".join(names), seq=True)  # seq=True forces a tuple

def build_ode_fun(pk_json: Dict):
    # ---- Extract names/values
    state_names = [s["name"] for s in pk_json["states"]]                # e.g., ["C"]
    param_names = [p["name"] for p in pk_json["parameters"]]            # e.g., ["k"]
    param_vals  = {p["name"]: float(p["value"]) for p in pk_json["parameters"]}
    ic_map      = {ic["state"]: float(ic["value"]) for ic in pk_json["initial_conditions"]}

    # ---- Initial state vector in the order of state_names
    y0 = np.array([ic_map[name] for name in state_names], dtype=float)

    # ---- SymPy symbols
    state_syms = _make_symbols(state_names)   # tuple of Symbols
    param_syms = _make_symbols(param_names)   # tuple of Symbols

    # ---- Locals for parsing RHS strings
    sym_locals = {name: sym for name, sym in zip(state_names, state_syms)}
    sym_locals.update({name: sym for name, sym in zip(param_names, param_syms)})

    # ---- Parse RHS for each equation in the SAME order as state_names
    # Assumption: equations[i] corresponds to d(state_names[i])/dt
    rhs_exprs = []
    for eq in pk_json["equations"]:
        rhs_exprs.append(sympify(eq["rhs"], locals=sym_locals))

    # ---- Lambdify with FLATTENED argument list: [states..., params...]
    all_syms = list(state_syms) + list(param_syms)
    f = lambdify(all_syms, rhs_exprs, modules="numpy")

    def fun(t, y):
        args = list(y) + [param_vals[name] for name in param_names]
        return np.array(f(*args), dtype=float)

    t0  = float(pk_json["time"]["t0"])
    te  = float(pk_json["time"]["tend"])
    dt  = float(pk_json["time"]["dt"])
    return fun, y0, (t0, te, dt), state_names, param_vals

def simulate(pk_json: Dict):
    fun, y0, (t0, te, dt), state_names, params = build_ode_fun(pk_json)
    sol = solve_ivp(fun, (t0, te), y0, dense_output=True, max_step=dt)
    t = np.linspace(t0, te, int(round((te - t0) / dt)) + 1)
    y = sol.sol(t)
    return t, y, state_names, params
