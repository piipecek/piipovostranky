from website import db
from website.models.common_methods_db_model import Common_methods_db_model
from datetime import datetime
from website.paths import acga_kody_slova, acga_default_formular
import json
from random import choice
from flask_login import current_user
from website.helpers.pretty_date import pretty_datetime


def get_default_formular() -> str:
    with open(acga_default_formular()) as file:
        return json.dumps(json.load(file))
    

class Evaluace(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    ucitel_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    data_json = db.Column(db.Text, default = get_default_formular())
    datetime_vytvoreni = db.Column(db.DateTime, default = datetime.utcnow)
    datetime_odevzdani = db.Column(db.DateTime)
    kod = db.Column(db.Text)
    je_odevzdana = db.Column(db.Boolean, default=False)
    
    def __repr__(self) -> str:
        return f"Exam | {self.datetime}"
    
    @staticmethod
    def vytvorit_evaluace(pocet) -> list[str]:
        with open(acga_kody_slova()) as file:
            slova = json.load(file)
        result_list = []
        for _ in range(pocet):
            kod_list = []
            for _ in range(3):
                kod_list.append(choice(slova))
            kod = " ".join(kod_list)
            result_list.append(f"Evaluace | {current_user.acga_jmeno} | {kod}")
            e = Evaluace()
            e.ucitel = current_user
            e.kod = kod
            e.update()
        
        result = "\n".join(result_list)
        return result
            
    
    def get_info_pro_seznam(self):
        return {
            "datetime_vytvoreni": pretty_datetime(self.datetime_vytvoreni),
            "kod": self.kod,
            "je_odevzdana": self.je_odevzdana,
            "id": self.id
        }
    
    @staticmethod
    def get_by_kod(kod):
        for e in Evaluace.get_all():
            if e.kod == kod:
                return e
        else:
            return None