def pretty_float(f) -> str:
    return str(round(f, 2)).replace(".", ",")


class Trida():
    def __init__(self) -> None:
        self.students: list[Student] = []
    
    def na_zobrazeni(self):
        return [s.na_zobrazeni() for s in self.students]
        


class Student:
    def __init__(self) -> None:
        self.jmeno = ""
        self.znamky_dict: list[dict[str:int, str: list[int]]] = []
        self.prumer_pct = None
        self.znamka = None
        self.klasifikovan = True
        self.vypocet = ""
    
    def spocist_prumer(self, styl):
        citatel = 0
        jmenovatel = 0
        citatel_strings = []
        jmenovatel_strings = []
        if styl == 1:
            for zaznam in self.znamky_dict:
                for znamka in zaznam["znamky"]:
                    citatel += znamka*zaznam["vaha"]
                    citatel_strings.append(f"{int(znamka)} \cdot {int(zaznam['vaha'])}")
                    jmenovatel += zaznam["vaha"]
                    jmenovatel_strings.append(str(int(zaznam["vaha"])))
        elif styl == 2:
            for zaznam in self.znamky_dict:
                if not len(zaznam["znamky"]) == 0:
                    citatel += sum(zaznam["znamky"]) / len(zaznam["znamky"])*zaznam["vaha"] 
                    citatel_strings.append("\\frac{" + " + ".join([str(z) for z in zaznam["znamky"]]) + " }{ " + str(len(zaznam["znamky"])) + "} \cdot " + str(zaznam["vaha"]))                        
                    jmenovatel += zaznam["vaha"]
                    jmenovatel_strings.append(str(zaznam["vaha"]))        
        if jmenovatel == 0:
                self.klasifikovan = False
        else:
            self.prumer_pct = citatel / jmenovatel
            citatel_str = " + ".join(citatel_strings)
            jmenovatel_str = " + ".join(jmenovatel_strings)
            self.vypocet = "\( \\frac{" + citatel_str + " }{ " + jmenovatel_str + "} = " + pretty_float(self.prumer_pct) + "\)"
    
    def vytvorit_znamku(self, hranice):
        if self.prumer_pct is None:
            pass
        elif self.prumer_pct >= hranice["12"]:
            self.znamka = 1
        elif self.prumer_pct >= hranice["23"]:
            self.znamka = 2
        elif self.prumer_pct >= hranice["34"]:
            self.znamka = 3
        elif self.prumer_pct >= hranice["45"]:
            self.znamka = 4
        else:
            self.znamka = 5

    def na_zobrazeni(self):
        for entry in self.znamky_dict:
            entry["znamky"] = ", ".join([str(int(x)) for x in entry["znamky"]])
        return {
            "jmeno": self.jmeno,
            "znamky_dict": self.znamky_dict,
            "prumer_pct": pretty_float(self.prumer_pct) if self.prumer_pct else "-",
            "klasifikovan": "Ano" if self.klasifikovan else "Ne",
            "znamka": self.znamka if self.znamka else "-",
            "vypocet": self.vypocet
        }