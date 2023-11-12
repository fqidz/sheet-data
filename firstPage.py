import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import gspread as gs
import gspread_dataframe as gd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from tempfile import NamedTemporaryFile

st.cache(ttl=5)

gauth = GoogleAuth()
scope = ["https://www.googleapis.com/auth/drive"]
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('.streamlit/sheetsKey.json', scope)
drive = GoogleDrive(gauth)

st.set_page_config(page_title="Printing", page_icon=":printer:", layout="centered")


# --- HEADER SECTION ---
st.title("Printing Form")

# --- TABLE ---

conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(worksheet="Sheet1", usecols=list(range(8)), ttl=5)


st.subheader("Google Sheet")
st.dataframe(data, hide_index=True)
st.markdown("""---""")

# --- INPUT SECTION ---
st.subheader("Input data")

with st.form(key="printing_input"):
    # form
    name = st.text_input(label='''Name :red[\*]''', placeholder="eg. Faidz Arante")
    no_of_black_and_white = st.number_input(label='''Number of Black & White Pages :red[\*]''',step=1)
    no_of_colored = st.number_input(label='''Number of Colored Pages :red[\*]''',step=1)
    uploaded_file = st.file_uploader(label='''PDF :red[\*]''', type=["pdf"])
    note = st.text_input(label="Note", placeholder="eg. range of pages to print, special requests, etc.")
    st.markdown(''':red[*\* required*]''')
    
    submit_button = st.form_submit_button(use_container_width=True)
    if submit_button:
        # check if required info is filled
        if not name or not uploaded_file or (not no_of_black_and_white and not no_of_colored):
            st.warning("Please fill in the required information")
            st.stop()
        else:
            if uploaded_file is not None:
                
                with NamedTemporaryFile(delete=False) as temp:
                    temp.write(uploaded_file.getvalue())
                folder_id = "1qBfLSQVBMJgpbgXa7h6YdAbT3AJv_sCe"
                gfile = drive.CreateFile({"title": uploaded_file.name, "parents": [{"id": folder_id}]})
                gfile.SetContentFile(temp.name)
                gfile.Upload()

            # create new row with data
            printing_input = pd.DataFrame(
                [
                    {
                        "Printed": "FALSE",
                        "Name": name,
                        "B & W": no_of_black_and_white,
                        "Colored": no_of_colored,
                        "File Name": uploaded_file.name,
                        "Note": note
                        
                    }
                ]
            )

            # append to google sheets
            gc = gs.service_account(filename=".streamlit/sheetsKey.json") # link service acc
            sh = gc.open("COPY_PRINTING BUSINESS!!!1") # link sheets
            ws = sh.worksheet("Sheet1") # get the worksheet
            existing = gd.get_as_dataframe(ws) # get the existing data as a DataFrame
            updated = existing.append(printing_input) # append the new data to the existing data
            gd.set_with_dataframe(ws, updated) # update the worksheet with the updated data
            
            st.success("Your data has been added to the Google sheet")