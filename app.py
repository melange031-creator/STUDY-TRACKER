import streamlit as st
import nbformat
from pathlib import Path

st.set_page_config(page_title="COMSATS Exam War Room", layout="wide")
st.title("🎯 COMSATS Exam War Room 2026")

# Locate notebook automatically
notebooks = list(Path(".").glob("*.ipynb"))

if not notebooks:
    st.error("No notebook file found.")
    st.stop()

notebook_path = notebooks[0]

with open(notebook_path, "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

# ONE shared execution environment for ALL cells
shared_env = {
    "__name__": "__main__"
}

# Streamlit replacement display
def display(obj):
    st.write(obj)

shared_env["display"] = display
shared_env["st"] = st

for i, cell in enumerate(nb.cells):

    if cell.cell_type == "markdown":
        st.markdown(cell.source)

    elif cell.cell_type == "code":

        code = cell.source.strip()

        if not code:
            continue

        # skip notebook package installs
        if "!pip install" in code:
            continue

        try:
            exec(code, shared_env)

        except Exception as e:
            st.error(f"Cell {i+1} failed:")
            st.code(str(e))
