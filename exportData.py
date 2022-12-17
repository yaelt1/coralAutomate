import pandas as pd
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
import webbrowser
import pyautogui

def importData1():
    webbrowser.open("https://israports.co.il/he/TaskYam/Pages/ShipStatus.aspx")




def importData():
    workbook = openpyxl.load_workbook(r"C:\Users\ASUS\Desktop\coralD\ship_status.xlsx")
    worksheet = workbook["info"]

    for page in range(1,10):
        data = pd.read_html("https://israports.co.il/he/TaskYam/Pages/ShipStatus.aspx".format(page))
        data_to_import = data
        print(data_to_import)
        for row in dataframe_to_rows(data_to_import, index = False, header= False):
            worksheet.append(row)



print(importData())
