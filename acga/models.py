
class Trida():
    def __init__(self) -> None:
        self.students: list[Student] = []
    
    def na_zobrazeni(self):
        return [s.na_zobrazeni() for s in self.students]
        


class Student:
    def __init__(self) -> None:
        self.jmeno = ""
        self.znamky_dict = []
        self.prumer_pct = None
        self.znamka = None
        self.klasifikovan = True
    
    def spocist_prumer(self):
        citatel = 0
        jmenovatel = 0
        for zaznam in self.znamky_dict:
            for znamka in zaznam["znamky"]:
                citatel += znamka*zaznam["vaha"]
                jmenovatel += zaznam["vaha"]
        if jmenovatel == 0:
            self.prumer_pct = 0
        else:
            self.prumer_pct = citatel / jmenovatel
    
    def vytvorit_znamku(self, hranice):
        
        if self.prumer_pct >= hranice["12"]:
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
            "prumer_pct": round(self.prumer_pct, 2),
            "klasifikovan": "Ano" if self.klasifikovan else "Ne",
            "znamka": self.znamka
        }