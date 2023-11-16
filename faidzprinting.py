## TODO
## fix discord embed
## customize shit or something
## email notifs
## replace append thingies with concat https://pandas.pydata.org/docs/reference/api/pandas.io.formats.style.Styler.map.html#pandas.io.formats.style.Styler.map
##      maybe by allowing them to have multiple forms
## referral promo thingy -> need login i think
## place image of pdf on top of ink type choice

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
import time


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

st.info("11/16/2023 - You can now upload multiple files! 🎉")

# --- FORM SECTION ---

# ink choice radio button
def ink_choice(key):    
    ink_type = st.radio(
    "{} :red[\*]".format(single_file.name),
    ["Colored", "Black & White"],
    index=None,key=key)
    return {'value': ink_type}


with st.expander(label='Form'):
    
    # name input
    name = st.text_input(label='''Name :red[\*]''', placeholder="eg. Faidz Arante")
    # upload file
    uploaded_files = st.file_uploader(label='''PDF File(s) :red[\*]''', type=["pdf"],accept_multiple_files=True)
    
    # ink type choice
    st.write('Choose Ink Type:')    
    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3]
    ink_types = []

    for index, single_file in enumerate(uploaded_files):
        # spread out each radio option to columns
        with columns[(index % 3)]:
            ink = ink_choice(index)
            ink_types.append(ink)

    # note input
    note = st.text_input(label="Note", placeholder="eg. range of pages to print, special requests, etc.")
    # submit button
    submit_button = st.button(label='Submit', use_container_width=True)
    
    # initialize variables
    progress_text = 'Loading...'
    progress = 1

    total_price = 0
    total_colored = 0
    total_black_and_white = 0

    date_now = datetime.today().strftime('%Y-%m-%d')

    #initialize summary table dict
    summary_table = {'Filename': [], 'Ink type': [], 'No. of Pages': []}

    # when submit button click
    if submit_button:
        # check if required info is filled
        if not name or not uploaded_files or any(i['value'] == None for i in ink_types):
            st.warning("Please fill in the required information.")
            st.stop()
        else:
            # show progress bar
            progress_bar = st.progress(progress, progress_text)
            
            # loop through all uploaded files
            for index, current_file in enumerate(uploaded_files):
                
                # upload file to gdrive
                with NamedTemporaryFile(delete=False) as temp:
                    temp.write(current_file.getvalue())
                folder_id = "1qBfLSQVBMJgpbgXa7h6YdAbT3AJv_sCe" #'print' folder
                gfile = drive.CreateFile({"title": current_file.name, "parents": [{"id": folder_id}]})
                gfile.SetContentFile(temp.name)
                gfile.Upload()
                # get file link
                file_link = gfile['alternateLink']

                # get no. of pages
                with open(temp.name, 'rb'):
                    pdfReader = pypdf.PdfReader(current_file)
                    no_of_pages = len(pdfReader.pages)

                # increment progress bar
                progress_bar.progress(progress + (100/len(uploaded_files))/100, 'Uploading files to Google Drive...')
                progress += (100/len(uploaded_files))/100                
                
                # create dataframe table row with all the data
                ink_types_value = ink_types[index]
                printing_input = pd.DataFrame(
                    [
                        {
                            "Date": date_now,
                            "Printed": "NO",
                            "Paid": "NO",
                            "Name": name,
                            "File Name": current_file.name,
                            "File Link": file_link,
                            "Colored": no_of_pages if ink_types_value['value'] == "Colored" else 0,
                            "B & W": no_of_pages if ink_types_value['value'] != "Colored" else 0,
                            "Note": note
                            
                        }
                    ]
                )

                # append row to google sheets
                sh = gc.open("COPY_PRINTING BUSINESS!!!1") # link sheets
                ws = sh.worksheet("Sheet1") # get the worksheet
                existing = gd.get_as_dataframe(ws) # get the existing data as a DataFrame
                updated = existing.append(printing_input) # append the new data to the existing data
                gd.set_with_dataframe(ws, updated) # update the worksheet with the updated data

                # calculate total price
                if ink_types_value['value'] == "Colored":
                    total_colored += no_of_pages
                    total_price += (no_of_pages * 100)/1000
                else:
                    total_black_and_white += no_of_pages
                    total_price += (no_of_pages * 50)/1000

                # append the data to the summary table dict
                summary_table_row = [current_file.name, ink_types_value['value'], no_of_pages]
                summary_table['Filename'].append(summary_table_row[0])
                summary_table['Ink type'].append(summary_table_row[1])
                summary_table['No. of Pages'].append(summary_table_row[2])

            # remove progress bar
            time.sleep(1)
            progress_bar.empty()

            total_price = 'BHD {:.3f}'.format(total_price)

            # success message; grammar
            if len(uploaded_files) == 1:
                st.success("Your file has been recieved and will be printed as soon as possible.\n Thank you! 😊")
            else:
                st.success("Your files have been recieved and will be printed as soon as possible.\n Thank you! 😊")
            
            st.divider()

            # summarize their printing request
            st.write('Summary:')
            summary_table_dataframe = pd.DataFrame(summary_table)
            st.dataframe(summary_table, hide_index=True)
            st.dataframe(
                [
                    {
                        'Total Colored Pages': total_colored,
                        'Total Black & White Pages': total_black_and_white,
                        'Total Price': total_price
                    }
                ]
            )