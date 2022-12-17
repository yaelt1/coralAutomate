import googletrans
from googletrans import Translator

coral_dict = { }
coral_dict["מסוף כימיקלים צפון"]= "Chemical north terminal"
coral_dict["מספנות ישראל"]= "Haifa Shipyard Port"
coral_dict["חיפה"]= "Haifa"
coral_dict["ממגורות חיפה"]= "Gadot Terminal"
coral_dict["המפרץ"]= "Gulf port"
coral_dict["הדרום"]= "South port"
coral_dict["אשדוד"]= "Ashdod"
coral_dict["אילת"]= "Eilat"
coral_dict["מתכות"]= "Steel"
coral_dict["מטען כללי"]= "General Cargo"
coral_dict["צוברים"]= "Grain"
coral_dict["רכב מוביל"]= "leading vehicle"

def uni_trans(word):
    translator = Translator()
    translated = translator.translate(word, dest="en")
    return translated.text

