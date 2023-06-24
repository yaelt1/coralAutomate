coral_dict = {}
coral_dict["מתכות"] = "Steel"
coral_dict["מטען כללי"] = "General Cargo"
coral_dict["צוברים"] = "Bulk"
coral_dict["רכב מוביל"] = "Roro"
coral_dict["מכולות"] = "Containers"
coral_dict["תאית"] = "Wood Pulp"
coral_dict["כלי רכב"] = "Roro"
coral_dict["שקים"] = "Bags"
coral_dict["עץ נסור"] = "Sawn Wood"
coral_dict["VEHICLE"] = "Roro"
coral_dict["CONTAINER"] = "Containers"
coral_dict["GENERAL CARGO"] = "General Cargo"
coral_dict["כריכות"] = "Covers"
coral_dict["BULK CARGO"] = "Bulk"


def dict_trans(word):
  if word in coral_dict.keys():
    return coral_dict.get(word, word)
  else:
    return word
