def pretty_float(f) -> str:
    return str(round(f, 2)).replace(".", ",")


class Trida():
    def __init__(self) -> None:
        self.students: list[Student] = []
    
    def na_zobrazeni(self):
        return [s.na_zobrazeni() for s in self.students]

    def prumer_pct(self) -> float:
        return sum([s.prumer_pct for s in self.students if s.prumer_pct]) / len(self.students)
    
    def prumery_ve_vahach(self) -> list[str]:
        result = []
        for i, elem in enumerate(self.students[0].znamky_dict):
            new_entry = {
                "vaha": elem["vaha"],
                "znamky": [],
                "prumer": None
            }
            for s in self.students:
                new_entry["znamky"].extend(s.znamky_dict[i]["znamky"])
            new_entry["prumer"] = pretty_float(sum(new_entry["znamky"]) / len(new_entry["znamky"])) if len(new_entry["znamky"]) else "-"
            
            result.append(new_entry["prumer"])
        return result

    def prumerna_znamka(self) -> float:
        return sum([s.znamka for s in self.students if s.znamka]) / len(self.students)
        

class Student:
    def __init__(self) -> None:
        self.jmeno = ""
        self.znamky_dict: list[dict[str:int, str: list[int]]] = []
        self.prumer_pct = None
        self.znamka = None
        self.klasifikovan = True
        self.vypocet = ""
        self.chybi = None
        self.rezerva = None
    
    def spocist_prumer(self, styl):
        def smart_int_float_to_str(x):
            if int(x) == x:
                return str(int(x))
            else:
                return str(x).replace(".", ",")
        
        
        citatel = 0
        jmenovatel = 0
        citatel_strings = []
        jmenovatel_strings = []
        if styl in [1, 3]:
            for zaznam in self.znamky_dict:
                for znamka in zaznam["znamky"]:
                    citatel += znamka*zaznam["vaha"]
                    citatel_strings.append(f"{smart_int_float_to_str(znamka)} \cdot {smart_int_float_to_str(zaznam['vaha'])}")
                    jmenovatel += zaznam["vaha"]
                    jmenovatel_strings.append(str(int(zaznam["vaha"])))
        elif styl == 2:
            for zaznam in self.znamky_dict:
                if not len(zaznam["znamky"]) == 0:
                    citatel += sum(zaznam["znamky"]) / len(zaznam["znamky"])*zaznam["vaha"] 
                    citatel_strings.append("\\frac{" + " + ".join([smart_int_float_to_str(z) for z in zaznam["znamky"]]) + " }{ " + str(len(zaznam["znamky"])) + "} \cdot " + str(zaznam["vaha"]))                        
                    jmenovatel += zaznam["vaha"]
                    jmenovatel_strings.append(str(zaznam["vaha"]))
                    
        if jmenovatel == 0:
                self.klasifikovan = False
        else:
            self.prumer_pct = citatel / jmenovatel
            citatel_str = " + ".join(citatel_strings)
            jmenovatel_str = " + ".join(jmenovatel_strings)
            self.vypocet = "\( \\frac{" + citatel_str + " }{ " + jmenovatel_str + "} = " + pretty_float(self.prumer_pct) + "\)"
    
    def vytvorit_znamku_a_spocitat_chybejici_a_rezervu(self, styl: int, hranice: dict):
        print(self.jmeno, self.prumer_pct, styl, hranice)
        if styl in [1, 2]: # procenta - cim vice, tim lepe
            if self.prumer_pct is None:
                pass
            elif self.prumer_pct >= hranice["12"]:
                self.znamka = 1
                self.chybi = 0
                self.rezerva = self.prumer_pct - hranice["12"]
            elif self.prumer_pct >= hranice["23"]:
                self.znamka = 2
                self.chybi = hranice["12"] - self.prumer_pct
                self.rezerva = self.prumer_pct - hranice["23"]
            elif self.prumer_pct >= hranice["34"]:
                self.znamka = 3
                self.chybi = hranice["23"] - self.prumer_pct
                self.rezerva = self.prumer_pct - hranice["34"]
            elif self.prumer_pct >= hranice["45"]:
                self.znamka = 4
                self.chybi = hranice["34"] - self.prumer_pct
                self.rezerva = self.prumer_pct - hranice["45"]
            else:
                self.znamka = 5
                self.chybi = hranice["45"] - self.prumer_pct
                self.rezerva = 0
        
        elif styl in [3]: # 1-5 - cim mene, tim lepe
            if self.prumer_pct is None:
                pass
            elif self.prumer_pct <= hranice["12"]:
                self.znamka = 1
                self.chybi = 0
                self.rezerva = hranice["12"] - self.prumer_pct
            elif self.prumer_pct <= hranice["23"]:
                self.znamka = 2
                self.chybi = self.prumer_pct - hranice["12"]
                self.rezerva = hranice["23"] - self.prumer_pct
            elif self.prumer_pct <= hranice["34"]:
                self.znamka = 3
                self.chybi = self.prumer_pct - hranice["23"]
                self.rezerva = hranice["34"] - self.prumer_pct
            elif self.prumer_pct <= hranice["45"]:
                self.znamka = 4
                self.chybi = self.prumer_pct - hranice["34"]
                self.rezerva = hranice["45"] - self.prumer_pct
            else:
                self.znamka = 5
                self.chybi = self.prumer_pct - hranice["45"]
                self.rezerva = 0
        else:
            raise ValueError("Neznámý styl výpočtu.")


    def na_zobrazeni(self):
        return {
            "jmeno": self.jmeno,
            "znamky_dict": self.znamky_dict,
            "prumer_pct": pretty_float(self.prumer_pct) if self.prumer_pct else "-",
            "chybi": pretty_float(self.chybi) if self.chybi else "-",
            "rezerva": pretty_float(self.rezerva) if self.rezerva else "-",
            "klasifikovan": "Ano" if self.klasifikovan else "Ne",
            "znamka": self.znamka if self.znamka else "-",
            "vypocet": self.vypocet
        }