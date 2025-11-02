# app.py
import streamlit as st
import plotly.graph_objects as go
from extract_model import extract_pk_json
from simulate import simulate

st.set_page_config(page_title="PharmaK2 (OpenAI)", layout="centered")
st.title("PharmaK2 – PK model extractor (OpenAI)")

default_text = """We consider a one-compartment model with first-order elimination.
The plasma concentration C decreases proportionally to C with rate constant k (1/h).
Initial concentration is 10 mg/L. Simulate for 24 h with step 0.1 h.
Typical k is around 0.2 1/h (range 0.05–0.5)."""

biomed_text = st.text_area("Paste PK text:", value=default_text, height=220)

if st.button("Extract model and simulate"):
    with st.spinner("Extracting model…"):
        #pk_json = extract_pk_json(biomed_text, model="gpt-5")  # or "o4-mini"
        pk_json = {
  "states": [{"name": "C", "unit": "mg/L", "description": "Plasma drug concentration"}],
  "parameters": [{"name": "k", "value": 0.2, "unit": "1/h", "description": "Elimination rate constant", "bounds": {"min": 0.05, "max": 0.5}}],
  "equations": [{"lhs": "dC/dt", "rhs": "-k * C"}],
  "initial_conditions": [{"state": "C", "value": 10.0}],
  "time": {"t0": 0.0, "tend": 24.0, "dt": 0.1}
}
    st.success("Model extracted.")

    # Parameter sliders
    st.subheader("Parameters")
    param_values = {}
    for p in pk_json["parameters"]:
        val = st.slider(
            label=f'{p["name"]} ({p["unit"]})',
            min_value=float(p["bounds"]["min"]),
            max_value=float(p["bounds"]["max"]),
            value=float(p["value"]),
            step=max( (p["bounds"]["max"] - p["bounds"]["min"]) / 200, 1e-4 )
        )
        p["value"] = val
        param_values[p["name"]] = val

    # Simulate
    t, y, state_names, _ = simulate(pk_json)

    fig = go.Figure()
    for i, s in enumerate(state_names):
        fig.add_trace(go.Scatter(x=t, y=y[i], mode="lines", name=s))
    fig.update_layout(xaxis_title="Time", yaxis_title="State value", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    st.download_button("Download JSON model", data=str(pk_json), file_name="pk_model.json")
