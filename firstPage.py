import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Printing", page_icon=":printer:", layout="wide")


# --- HEADER SECTION ---
st.title("Printing Thingymajig")

# --- TABLE ---

conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(worksheet="Sheet1", usecols=list(range(7)))


st.subheader("Google Sheet")
st.dataframe(data, hide_index=True)
st.markdown("""---""")

# --- Input ---
st.subheader("Input data")
st.text_input(label="Name", placeholder="eg. Faidz Arante")