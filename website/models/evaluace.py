from website import db
from website.models.common_methods_db_model import Common_methods_db_model
from datetime import datetime
from website.paths import acga_kody_slova, acga_default_formular
import json
from random import choice
from flask_login import current_user
from website.helpers.pretty_date import pretty_datetime
import uuid


def get_default_formular() -> str:
    with open(acga_default_formular()) as file:
        return json.dumps(json.load(file))
    

class Evaluace(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    ucitel_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    data_json = db.Column(db.Text, default = get_default_formular)
    datetime_vytvoreni = db.Column(db.DateTime, default = datetime.now)
    datetime_odevzdani = db.Column(db.DateTime)
    kod = db.Column(db.Text)
    je_odevzdana = db.Column(db.Boolean, default=False)
    uuid = db.Column(db.String(36), default=uuid.uuid4)
    
    def __repr__(self) -> str:
        return f"Exam | {self.datetime}"
    
    @staticmethod
    def vytvorit_evaluace(pocet) -> list[str]:
        with open(acga_kody_slova()) as file:
            slova = json.load(file)
        result = []
        for _ in range(pocet):
            kod_list = []
            for _ in range(3):
                kod_list.append(choice(slova))
            kod = " ".join(kod_list)
            e = Evaluace()
            e.ucitel = current_user
            e.kod = kod
            e.update()
            result.append(e)
        return result
    
    
    @staticmethod
    def vytvorit_kody_k_tisku(evaluace: list["Evaluace"]) -> list[str]:
        result = []
        for e in evaluace:
            result.append(f"Evaluace | {current_user.acga_jmeno} | {e.kod} | www.piipovostranky.cz/acga/evaluace")
        return result

    
    def get_info_pro_seznam(self):
        return {
            "datetime_vytvoreni": pretty_datetime(self.datetime_vytvoreni),
            "datetime_odevzdani": pretty_datetime(self.datetime_odevzdani),
            "kod": self.kod,
            "je_odevzdana": self.je_odevzdana,
            "id": self.id
        }
    
    def locked_data(self):
        return {
            "datetime_vytvoreni": pretty_datetime(self.datetime_odevzdani),
            "datetime_odevzdani": pretty_datetime(self.datetime_odevzdani),
            "data": json.loads(self.data_json),
            "name": self.ucitel.acga_jmeno
        }
    
    @staticmethod
    def get_by_kod(kod) -> "Evaluace":
        for e in Evaluace.get_all():
            if e.kod == kod:
                return e
        else:
            return None
        
    @staticmethod
    def get_by_uuid(uuid) -> "Evaluace":
        for e in Evaluace.get_all():
            if e.uuid == uuid:
                return e
        else:
            return None
        
    def ulozit_nova_data(self, data: dict):
        data_json = json.loads(self.data_json)
        for q in data_json:
            if q["typ"] == "otevrena":
                q["value"] = data.get(str(q["id"]))
            if q["typ"] == "ciselna":
                q["value"] = data.get(str(q["id"]))
            if q["typ"] == "single":
                q["value"] = data.get(str(q["id"]))
            if q["typ"] == "multiple":
                q["values"] = data.get(str(q["id"]))
        self.data_json = json.dumps(data_json)
        self.update()
    
    def oznacit_za_odevzdane(self):
        self.je_odevzdana = True
        self.datetime_odevzdani = datetime.now()
        self.update()