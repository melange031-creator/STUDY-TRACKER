import streamlit as st
import nbformat
from pathlib import Path

# preload notebook-style imports
from datetime import datetime, timedelta
from IPython.display import HTML, Markdown, display

st.set_page_config(page_title="COMSATS Exam War Room", layout="wide")
st.title("🎯 COMSATS Exam War Room 2026")

# locate notebook automatically
notebooks = list(Path(".").glob("*.ipynb"))

if not notebooks:
    st.error("Notebook file missing")
    st.stop()

notebook_path = notebooks[0]

with open(notebook_path, "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

# streamlit display replacement
def st_display(obj):

    try:
        if isinstance(obj, HTML):
            st.markdown(obj.data, unsafe_allow_html=True)

        elif isinstance(obj, Markdown):
            st.markdown(obj.data)

        else:
            st.write(obj)

    except Exception:
        st.write(obj)

shared_env = {
    "__name__": "__main__",

    # notebook compatibility
    "datetime": datetime,
    "timedelta": timedelta,
    "HTML": HTML,
    "Markdown": Markdown,
    "display": st_display,

    # streamlit access
    "st": st,
}

for idx, cell in enumerate(nb.cells):

    if cell.cell_type == "markdown":
        st.markdown(cell.source)

    elif cell.cell_type == "code":

        code = cell.source.strip()

        if not code:
            continue

        if "!pip install" in code:
            continue

        try:
            exec(code, shared_env)

        except Exception as e:
            st.error(f"Cell {idx+1} failed:")
            st.code(str(e))
