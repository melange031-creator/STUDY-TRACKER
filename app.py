
import streamlit as st
import nbformat
from IPython.display import HTML, Markdown
import warnings

st.set_page_config(page_title="COMSATS Exam War Room", layout="wide")
st.title("🎯 COMSATS Exam War Room 2026")

# Replace notebook display functions with Streamlit-friendly versions
def display(obj):
    try:
        data = getattr(obj, "data", None)
        if data:
            st.markdown(data, unsafe_allow_html=True)
        else:
            st.write(obj)
    except Exception:
        st.write(obj)

globals_env = {
    "display": display,
    "HTML": HTML,
    "Markdown": Markdown,
    "warnings": warnings,
}

notebook_path = "COMSATS_ExamWarRoom_2026.ipynb"
nb = nbformat.read(notebook_path, as_version=4)

for cell in nb.cells:
    if cell.cell_type == "markdown":
        st.markdown(cell.source)
    elif cell.cell_type == "code":
        code = cell.source
        if "!pip install" in code:
            continue
        try:
            exec(code, globals_env)
        except Exception as e:
            st.error(f"Error in notebook cell: {e}")
