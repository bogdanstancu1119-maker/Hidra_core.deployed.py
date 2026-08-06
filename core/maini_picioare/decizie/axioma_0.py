# Stratul superior include substratul
# Dizolvare Constienta = deschide 2+ optiuni, inchide 0
def verifica(actiune):
    return actiune.get("optiuni_noi",0) >= 2 and actiune.get("optiuni_inchise",0) == 0