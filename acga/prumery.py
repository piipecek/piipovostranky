import xlrd
from werkzeug.datastructures import FileStorage
from acga.models import Student, Trida, pretty_float
import json

def pocitani_prumeru(file: FileStorage, data=None) -> dict:
    wb = xlrd.open_workbook(file_contents=file.read())
    sheet = wb.sheet_by_index(0)
    hranice = {
        "12": float(data["hranice_12"].replace(",", ".")),
        "23": float(data["hranice_23"].replace(",", ".")),
        "34": float(data["hranice_34"].replace(",", ".")),
        "45": float(data["hranice_45"].replace(",", ".")),
    }
    
    names_col = int(data["names_col"]) # index od 1
    results_col = int(data["results_col"]) # index od 1
    name_row = int(data["name_row"]) # index od 1
    
    styl = int(data["styl"])
    
    rows_indexes = range(name_row-1, sheet.nrows) # index od 0
    names_index = names_col-1 # index od 0
    results_index = results_col-1 # index od 0
    results_indexes = []
    results_weights = []
    
    while True:
        sample = sheet.cell_value(0, results_index)
        if type(sample) == float:
            results_weights.append(sample*10)
            results_indexes.append(results_index)
            results_index += 1
        else:
            break
        
    
    # až sem jsem si ten soubor ošahával, teď jdu udělat konečně nějakou meaningful strukturu
    
    t = Trida()
    for i in rows_indexes:
        s = Student()
        s.jmeno = sheet.cell_value(i, names_index)
        znamky_dict = []
        for index, vaha in zip(results_indexes, results_weights):
            znamky_raw = sheet.cell_value(i, index)
            znamky_raw = str(znamky_raw) # normalizovani, kdyz tam je jen jedno cislo tak to je cislo, jinak to je string
            znamky_split = znamky_raw.split(" ")
            if "-" in znamky_split:
                s.klasifikovan = False
            znamky = []
            for z in znamky_split:
                if z in ["", "-", "[S]"]:
                    pass
                else:
                    znamky.append(float(z.replace(",", ".")))

            znamky_dict.append({
                "vaha": int(vaha),
                "znamky": znamky
            })
        s.znamky_dict = znamky_dict
        t.students.append(s)
        
    #mam je nacteny, ted je budu pocitat
    
    for s in t.students:
        s.spocist_prumer(styl=styl)
        s.vytvorit_znamku_a_spocitat_chybejici_a_rezervu(styl = styl, hranice=hranice)
        
        
    
        
    result = {
        "vahy": results_weights,
        "studenti": t.na_zobrazeni(),
        "title": file.filename,
        "prumer_prumeru": pretty_float(t.prumer_pct()),
        "prumery_ve_vahach": t.prumery_ve_vahach(),
        "prumer_znamka": pretty_float(t.prumerna_znamka())
    }
    return result
        
        
