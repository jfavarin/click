import streamlit as st
import pandas as pd

# ---------------------
# INTERFACE
# ---------------------
# configuração da tela
st.set_page_config(
    page_title="USPAX - Gestão empresarial",
    page_icon="📊",
    layout="wide",
    )
header = st.container()

# ---------------------
# HEADER
# ---------------------
with header:
    st.title("📊 USPAX - Gestão empresarial")