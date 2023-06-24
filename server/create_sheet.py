import pandas as pd
import time
import datetime
import xlsxwriter
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
from coral_dict import dict_trans
import shutil
import datetime
import pytz
import webbrowser
from mail import mail_it



def main():
    path = exportData1()
    print(path)
    return path

def open_click():
  chrome_options = Options()
#   chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
#   chrome_options.add_argument('--disable-gpu')
#   chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)  #opens chrome
  driver.get(r"https://israports.co.il/en/IPCS/Pages/shippingschedule.aspx")  #opens website
  print("after sleep")
  try:
    wait = WebDriverWait(driver, 5)
    element = wait.until(
      EC.element_to_be_clickable((
        By.XPATH,
        "/html/body/form/div[4]/div/main/span/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/div/div[2]/div[1]/button[1]"
      )))
    element.click()
    print("clicked")
    time.sleep(2)
    
  except Exception as e:
    print("Element not found: ", e)
    open_click()
  driver.close()

def filterData(df):
    df1 = df[df['Status'].isin(['ShipsOnBerth', 'ShipsAnchoredOutsidePort'])]
    df1 = df1[~df1['CARGO_TYPE_ARR'].isin(['נוסעים', 'מכולות'])]
    df1 = df1.dropna(subset=['CARGO_TYPE_ARR'])
    df1.rename(columns={
        'Ship_x0020_Name_x002f_Number': 'Vessel',
        "Ports": "PORT",
        "ARR_DTE_TIME": "Arrival Date",
        "CARGO_TYPE_ARR": "Cargo Type"
    },
                inplace=True)
    status_priority = {"ShipsOnBerth": 1,"ShipsAnchoredOutsidePort": 2}

    df1 = df1[["PORT", "Vessel","Status", "Cargo Type", "Arrival Date"]]
    df1 = df1.sort_values(by=["Status", "Arrival Date"], key= lambda x: x.map(status_priority))
    for col in ["Cargo Type"]:
        for index, row in df1.iterrows():
            words = row[col]
            translated_words = []
            translated_words.append(dict_trans(words))
            translated_text = " ".join(translated_words)
            df1.at[index, col] = translated_text

    for name in ["Vessel"]:
        for index, row in df1.iterrows():
            cur = row[name]
            n = len(cur)
            cur = cur[:n - 6]
            df1.at[index, name] = cur
    df1["Quantity"] = ["-" for i in df1["Vessel"]]
    return df1

def exportData1():
    israel_tz = pytz.timezone('Israel')
    local_now = datetime.datetime.now()
    israel_now = local_now.astimezone(israel_tz)
    d3 = israel_now.strftime("%d-%m-%Y %H-%M-%S")
    print(d3)
    try:
        print("first try")
        open_click()
    except:
        print("second try")
        open_click()
    

    file_name = "IPCS-VesselSchedule.xlsx"

    # check if file exists in directory
    while not '../../{file_name}' :
        time.sleep(5)
    print("file in download dir")
    # new_file_name = os.path.join(docs_path, d3 + ".xlsx")
    # #moving files
    # shutil.move(downloads_file, new_file_name)
    return writingData(file_name, d3, './')

def writingData(new_file_name, d3, destination_path):
    df = pd.read_excel(new_file_name)
    df1 = filterData(df)
    df1 = df1.groupby(["PORT"])
    path = os.path.join(destination_path, "ship_status_" + d3 + ".xlsx")
    workbook = xlsxwriter.Workbook(path,
        {'in_memory': True})
    worksheet = workbook.add_worksheet()

    colors = ['blue', 'red', "purple", "green", "orange", "aqua"]
    table_style = [
        'Table Style Light 9', 'Table Style Light 10', 'Table Style Light 12',
        'Table Style Light 11', 'Table Style Light 14', 'Table Style Light 13',
    ]
    main_header = "Vessels Status - Israeli Ports"
    main = workbook.add_format()
    main.set_font_size(48)
    main.set_bold()
    worksheet.write('F8', main_header, main)

    prev = 0
    ports = [x for x in df1.groups]
    for i in range(len(df1.groups)):
        group = ports[i]
        print(group)
        new = pd.DataFrame(df1.get_group(group).reset_index(drop=True))

        # converting to dataframe and adding "No" col
        df_x = new  #only one group
        df_x["No"] = [i + 1 for i in range(len(df_x))]
        df_x = df_x[["No", "Vessel", "Status","Cargo Type", "Arrival Date", "Quantity"]]
        n = len(df_x)
        #adding caption for every table
        caption = group[0].upper() + group[1:]
        cap_font = workbook.add_format()
        cap_font.set_font_color(colors[i % len(colors)])
        cap_font.set_font_size(14)
        if i > 0:
            index = 'C' + str(13 + prev + 2)  # for caption
            worksheet.write(index, caption, cap_font)
        else:
            worksheet.write('C13', caption, cap_font)

        row_ater_caption = 13 + prev + 3 if i > 0 else 14
        table_start = "A" + str(row_ater_caption)
        table_ends = "F" + str(int(row_ater_caption + n))
        size = table_start + ":" + table_ends
        size_without_num = "B" + str(row_ater_caption) + ":" + table_ends
        table_format = workbook.add_format()
        table_format.set_border()
        table_format.set_center_across()

        column_settings = [{
        'header': column,
        "format": table_format
        } for column in df_x.columns]
        worksheet.add_table(
        size, {
            "data": df_x.values.tolist(),
            'banded_columns': False,
            "style": table_style[i % len(table_style)],
            'autofilter': False,
            'columns': column_settings,
        })
        worksheet.set_column(size_without_num, 22)
        prev += n + 4
        time.sleep(1)

    workbook.close()
    try:
        os.remove(new_file_name)
        print(f"{new_file_name} deleted successfully.")
    except OSError as error:
        print(error)    
    return (path)



print(main())