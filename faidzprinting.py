## TODO
## fix discord embed
## customize shit or something
## email notifs
## replace append thingies with concat https://pandas.pydata.org/docs/reference/api/pandas.io.formats.style.Styler.map.html#pandas.io.formats.style.Styler.map
## allow upload multiple files
##      maybe by allowing them to have multiple forms
## referral promo thingy -> need login i think

import streamlit as st
import pandas as pd
import gspread as gs
import gspread_dataframe as gd
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from tempfile import NamedTemporaryFile
from datetime import datetime
import pypdf


gauth = GoogleAuth()
scope = ["https://www.googleapis.com/auth/drive"]
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gsheets"]["sheet_service_account"], scope)
gc = gs.authorize(gauth.credentials) # link service acc

drive = GoogleDrive(gauth)

st.set_page_config(page_title="Faidz Printing", page_icon=":printer:", layout="centered")


# --- HEADER SECTION ---
st.title("Printing Form")

# --- CONTENT ---
## TODO

st.info("You can upload multiple files now! 🎉")

# --- INPUT SECTION ---

def ink_choice(key):    
    st.radio(
    "{} :red[\*]".format(single_file.name),
    ["Colored", "Black & White"],
    index=None,key=key)


with st.expander(label='Form'):
    # form
    name = st.text_input(label='''Name :red[\*]''', placeholder="eg. Faidz Arante")
    
    uploaded_file = st.file_uploader(label='''PDF File(s) :red[\*]''', type=["pdf"],accept_multiple_files=True)


    st.write('Choose Ink Type:')

    # ink type choice
    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3]
    ink_types = []

    for index, single_file in enumerate(uploaded_file):
        with columns[(index % 3)]:
            ink = ink_choice(index)
            ink_types.append(ink)

    note = st.text_input(label="Note", placeholder="eg. range of pages to print, special requests, etc.")
    submit_button = st.button(label='Submit', use_container_width=True)

    st.write(ink_types)

    if submit_button:
        # check if required info is filled
        if not name or not uploaded_file or not ink_types:
            st.warning("Please fill in the required information.")
            st.stop()
        else:
            pass
            
            
            
            
            
            
            # # upload file to gdrive
            # with NamedTemporaryFile(delete=False) as temp:
            #     temp.write(uploaded_file.getvalue())
            # folder_id = "1qBfLSQVBMJgpbgXa7h6YdAbT3AJv_sCe" #'print' folder
            # gfile = drive.CreateFile({"title": uploaded_file.name, "parents": [{"id": folder_id}]})
            # gfile.SetContentFile(temp.name)
            # gfile.Upload()
            
            # file_link = gfile['alternateLink']

            # with open(temp.name, 'rb'):
            #     pdfReader = pypdf.PdfReader(uploaded_file)
            #     no_of_pages = len(pdfReader.pages)

            # # create new row with data
            # date_now = datetime.today().strftime('%Y-%m-%d')
            
            # printing_input = pd.DataFrame(
            #     [
            #         {
            #             "Date": date_now,
            #             "Printed": "NO",
            #             "Name": name,
            #             "File Name": uploaded_file.name,
            #             "File Link": file_link,
            #             "Colored": no_of_pages if ink_types == "Colored" else 0,
            #             "B & W": no_of_pages if ink_types != "Colored" else 0,
            #             "Note": note
                        
            #         }
            #     ]
            # )


            # # append to google sheets
            # sh = gc.open("COPY_PRINTING BUSINESS!!!1") # link sheets
            # ws = sh.worksheet("Sheet1") # get the worksheet
            # existing = gd.get_as_dataframe(ws) # get the existing data as a DataFrame
            # updated = existing.append(printing_input) # append the new data to the existing data
            # gd.set_with_dataframe(ws, updated) # update the worksheet with the updated data
            
            # st.divider()

            # #calculate price
            # if ink_types == "Colored":
            #     total_price = (no_of_pages * 100)/1000
            # else:
            #     total_price = (no_of_pages * 50)/1000

            # total_price = 'BHD {:.3f}'.format(total_price)
            

            # # do this as expanded
            # summary = '''Filename: {}\nInk Type: {}\nNo. of Pages: {}\nTotal Price: {}'''.format(uploaded_file.name, ink_types, no_of_pages, total_price)
            # st.code(summary,language="yaml")
            # st.success("Your file has been recieved and will be printed as soon as possible.\n Thank you! 😊")