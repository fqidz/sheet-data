## TODO
## fix discord embed
## customize shit or something
## email notifs
## replace append thingies with concat https://pandas.pydata.org/docs/reference/api/pandas.io.formats.style.Styler.map.html#pandas.io.formats.style.Styler.map
## auto get pages from just pdf, no need input
## upload multiple files

##test test

import streamlit as st
import pandas as pd
import gspread as gs
import gspread_dataframe as gd
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from tempfile import NamedTemporaryFile
from datetime import datetime
from PIL import Image

gauth = GoogleAuth()
scope = ["https://www.googleapis.com/auth/drive"]
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gsheets"]["sheet_service_account"], scope)
gc = gs.authorize(gauth.credentials) # link service acc

drive = GoogleDrive(gauth)

st.set_page_config(page_title="Faidz Printing", page_icon=":printer:", layout="centered")


# --- HEADER SECTION ---
st.title("Printing Form")

# --- INPUT SECTION ---

with st.form(key="printing_input"):
    # form
    name = st.text_input(label='''Name :red[\*]''', placeholder="eg. Faidz Arante")
    

    ink_type = st.radio(
    "Select Ink Type :red[\*]",
    ["Colored", "Black & White"],
    captions = ["100 fils per page", "50 fils per page"],
    index=None)

    
    no_of_pages = st.number_input(label='''Number of Pages :red[\*]''',step=1)
    uploaded_file = st.file_uploader(label='''PDF File :red[\*]''', type=["pdf"])
    note = st.text_input(label="Note", placeholder="eg. range of pages to print, special requests, etc.")
    st.markdown(''':red[*\* required*]''')
    
    submit_button = st.form_submit_button(use_container_width=True)
    if submit_button:
        # check if required info is filled
        if not name or not uploaded_file or not no_of_pages or not ink_type:
            st.warning("Please fill in the required information.")
            st.stop()
        else:
            if uploaded_file is not None:
                # upload file to gdrive
                with NamedTemporaryFile(delete=False) as temp:
                    temp.write(uploaded_file.getvalue())
                folder_id = "1qBfLSQVBMJgpbgXa7h6YdAbT3AJv_sCe" #'print' folder
                gfile = drive.CreateFile({"title": uploaded_file.name, "parents": [{"id": folder_id}]})
                gfile.SetContentFile(temp.name)
                gfile.Upload()
                
                file_link = gfile['alternateLink']

            # create new row with data
            
            date_now = datetime.today().strftime('%Y-%m-%d')
            
            printing_input = pd.DataFrame(
                [
                    {
                        "Date": date_now,
                        "Printed": "NO",
                        "Name": name,
                        "File Name": uploaded_file.name,
                        "File Link": file_link,
                        "Colored": no_of_pages if ink_type == "Colored" else 0,
                        "B & W": no_of_pages if ink_type != "Colored" else 0,
                        "Note": note
                        
                    }
                ]
            )



            # append to google sheets
            sh = gc.open("COPY_PRINTING BUSINESS!!!1") # link sheets
            ws = sh.worksheet("Sheet1") # get the worksheet
            existing = gd.get_as_dataframe(ws) # get the existing data as a DataFrame
            updated = existing.append(printing_input) # append the new data to the existing data
            gd.set_with_dataframe(ws, updated) # update the worksheet with the updated data
            
            st.success("Your file, '" + uploaded_file.name + "' has been recieved and will be printed as soon as possible.\n Thank you! 😊")

            
# absolutely crucial for the web app to run; do not delete
#st.divider()

#dog = Image.open('dog.jpg')

#st.write('photo of a dog')
#st.image(dog, caption='photo of a dog')
