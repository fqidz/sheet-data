import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Printing", page_icon=":printer:", layout="centered")


# --- HEADER SECTION ---
st.title("Printing Thingymajig")

# --- TABLE ---

conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(worksheet="Sheet1", usecols=list(range(8)), ttl=5)


st.subheader("Google Sheet")
st.dataframe(data, hide_index=True)
st.markdown("""---""")

# --- Input ---
st.subheader("Input data")

with st.form(key="printing_input"):
    name = st.text_input(label='''Name :red[\*]''', placeholder="eg. Faidz Arante")
    no_of_black_and_white = st.number_input(label='''Number of Black & White Pages :red[\*]''',step=1)
    no_of_colored = st.number_input(label='''Number of Colored Pages :red[\*]''',step=1)
    file = st.file_uploader(label='''File :red[\*]''')
    note = st.text_input(label="Note", placeholder="eg. range of pages to print, special requests, etc.")
    st.markdown(''':red[*\* required*]''')

    submit_button = st.form_submit_button(use_container_width=True)

    if submit_button:
        # check if required info is filled
        if not name or not file:
            st.warning("Please fill in the required information")
            st.stop()
        else:
            # create new row with data
            printing_input = pd.DataFrame(
                [
                    {
                        "Name": name,
                        "B & W": no_of_black_and_white,
                        "Colored": no_of_colored,
                        "File Name": file.__str__
                        
                    }
                ]
            )

            



