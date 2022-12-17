import pandas as pd
import googletrans
from googletrans import Translator
import time
import datetime
from datetime import datetime
import openpyxl
import xlsxwriter
import webbrowser
import pyautogui
import selenium
from datetime import date
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os
from openpyxl.styles import Font
from openpyxl.utils.dataframe import dataframe_to_rows
from coral_dict import coral_dict
from coral_dict import uni_trans
def main():
    return exportData1()

def filterData(df):
    df1 = df[df['Status'] == 'ShipsExpectedNext48Hours']

    df1 = df1[df1['CARGO_TYPE_ARR'] != 'נוסעים']
    df1 = df1[df1['CARGO_TYPE_ARR'] != 'מכולות']
    df1 = df1.dropna(subset=['CARGO_TYPE_ARR'])

    df1.rename(columns={'Ship_x0020_Name_x002f_Number': 'VESSEL', "Ports": "PORT", "ARR_DTE_TIME": "Arrival Date",
                        "CARGO_TYPE_ARR": "Cargo Type"},
               inplace=True)
    df1 = df1[["PORT", "VESSEL", "Cargo Type", "Arrival Date"]]
    df1 = df1.sort_values(by=["Arrival Date"])
    for col in ["Cargo Type","PORT" ]:
        for index, row in df1.iterrows():
            words = row[col].split()
            translated_words=[]
            for word in words:
                if word in coral_dict.keys():
                    translated_words.append(coral_dict.get(word, word))
                else:
                    translated_words.append(uni_trans(word))
            translated_text = " ".join(translated_words)
            df1.at[index, col] = translated_text
    df1["Quantity"] = ""
    return df1

def exportData1():
    now = datetime.now()
    d3 = now.strftime("%d-%m-%Y %H-%M-%S")
    driver = webdriver.Chrome()
    driver.minimize_window()

    # Navigate to the website that contains the button you want to press
    driver.get(r"https://israports.co.il/en/IPCS/Pages/shippingschedule.aspx")

    # Find the button on the page using its ID or another unique identifier
    button = wait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'export-list-button')))

    # Click the button to press it
    button.click()
    while "IPCS-VesselSchedule.csv" not in os.listdir("C:/Users/ASUS/Downloads"):
        time.sleep(10)
    driver.close()
    # Wait for the export process to complete
    # You can use an explicit wait, a conditional statement, or another method to do this

    # Rename the file using the os.rename() method
    # Set the old and new file names as appropriate
    path1 = "C:/Users/ASUS/Downloads/IPCS-VesselSchedule.csv"
    print(os.path.isfile(path1))

    old_file_name = "C:/Users/ASUS/Downloads/IPCS-VesselSchedule.csv"
    new_file_name = "C:/Users/ASUS/Downloads/"+d3+".csv"

    print(os.getcwd())
    os.rename(old_file_name, new_file_name)


    return writingData(new_file_name)


    #resding it
def writingData(new_file_name):
    now = datetime.now()
    d3 = now.strftime("%d-%m-%Y %H-%M-%S")

    df = pd.read_csv(new_file_name, encoding="ISO-8859-8")
    df1 = filterData(df)
    res = pd.DataFrame()

    df1 = df1.groupby(["PORT"])

    workbook = xlsxwriter.Workbook("ship_status_"+d3+".xlsx", {'in_memory': True})
    worksheet = workbook.add_worksheet()
    colors = ['blue','red',"purple", "orange"]
    table_style = ['Table Style Light 9', 'Table Style Light 10', 'Table Style Light 12', 'Table Style Light 11', 'Table Style Light 14']

    prev = 0
    ports = [x for x in df1.groups]
    for i in range(len(df1.groups)):
        group = ports[i]
        new = pd.DataFrame(df1.get_group(group).reset_index(drop= True))

        # converting to dataframe
        df_x=new #only one group
        df_x["No"]= [i+1 for i in range(len(df_x))]
        df_x = df_x[[ "No", "VESSEL", "Cargo Type", "Arrival Date", "Quantity"]]
        n = len(df_x)


        caption = group[0].upper() + group[1:]
        cap_font = workbook.add_format()
        cap_font.set_font_color(colors[i])
        cap_font.set_font_size(14)
        if i > 0:
            index = 'C' + str(13 + prev +1+ 2)
            worksheet.write(index, caption, cap_font)
        else:
            worksheet.write('C13', caption, cap_font)
        main_header = "Vessels Status - Israeli Ports"
        main = workbook.add_format()
        main.set_font_size(48)
        main.set_bold()
        worksheet.write('E8',main_header, main)

        row_ater_caption = 14 + prev + 3 if i > 0 else 14
        table_start = "A" + str(row_ater_caption)
        table_ends = "E" + str(int(row_ater_caption+ n))
        size = table_start + ":" + table_ends
        size_without_num = "B"+str(row_ater_caption)+":" + table_ends
        #first_row_end = "E"+str(int(row_ater_caption))
        #size_header = table_start+":"+first_row_end

        (max_row, max_col) = df_x.shape
        table_format = workbook.add_format()
        table_format.set_border()

        column_settings = [{'header': column, "format":table_format} for column in df_x.columns]
        table  = worksheet.add_table(size, {"data":df_x.values.tolist(),'banded_columns': False,"style":table_style[i], 'autofilter': False, 'columns': column_settings,})
        worksheet.set_column(size_without_num, 22)
        prev += n


    workbook.close()








#print(writingData(r"C:\Users\ASUS\Downloads\17-12-2022 03-03-27.csv"))
print(main())