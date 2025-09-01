from flask_login import current_user
from website import db
from website.models.common_methods_db_model import Common_methods_db_model
import json
from website.helpers.krouzky_helpers import get_students_from_xlsx

class Krouzek(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    description = db.Column(db.Text)
    enrolled_emails=db.Column(db.Text, default="[]") # json list
    
    
    @staticmethod
    def get_all_for_seznam():
        result = []
        for krouzek in Krouzek.get_all():
            pocet_lidi = len(json.loads(krouzek.enrolled_emails))
            result.append({
                "id": krouzek.id,
                "name": krouzek.name,
                "pocet_lidi": pocet_lidi
            })
        return result
    
    
    def _get_student_data(self) -> dict:
        students = get_students_from_xlsx()
        enrolled_emails = json.loads(self.enrolled_emails) # ne kazdy enrolled email musi nutne byt v students
        result = []

        # seznam studentu
        for email in enrolled_emails:
            student = next((s for s in students if s["email"] == email), None)
            if student:
                result.append(student)
            else:
                result.append({"full_name": "-", "surname": "-", "email": email, "class": "-"})
        result.sort(key=lambda x: (x["class"], x["surname"], x["email"]))
        for i, student in enumerate(result):
            student["cislo"] = i + 1
        return result
    

    def get_data_for_detail(self):
        result = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "students":[],
            "table_data": ""
        }

        result["students"] = self._get_student_data()
            
        #string do tabulek
        nadpisy = ["#", "Jméno", "Třída", "E-mail"]
        result["table_data"] = "\t".join(nadpisy)
        for student in result["students"]:
            result["table_data"] += f"\n{student['cislo']}\t{student['full_name']}\t{student['class']}\t{student['email']}"
        return result
    
    
    @staticmethod
    def get_data_for_list():
        krouzky = Krouzek.get_all()
        krouzky.sort(key=lambda x: x.name)
        
        result = {
            "krouzky": [],
            "table_data": ""
        }
        
        for k in krouzky:
            pocet_lidi = len(json.loads(k.enrolled_emails))
            result["krouzky"].append({
                "id": k.id,
                "name": k.name,
                "pocet_lidi": pocet_lidi
            })
        
        header_row = "\t".join(["#", "Jméno", "Třída", "E-mail"])

        for k in krouzky:
            result["table_data"] += f"Název\t{k.name}"
            result["table_data"] += f"\nPopis\t{k.description}"
            result["table_data"] += f"\n{header_row}"
            for student in k._get_student_data():
                result["table_data"] += f"\n{student['cislo']}\t{student['full_name']}\t{student['class']}\t{student['email']}"
            result["table_data"] += "\n"
            result["table_data"] += "\n"

        return result
        
        
    @staticmethod
    def get_data_for_current_user() -> list:
        result = []
        krouzky = sorted(Krouzek.get_all(), key=lambda x: x.name)
        for k in krouzky:
            result.append({
                "name": k.name,
                "description": k.description,
                "id": k.id,
                "enrolled": current_user.email in json.loads(k.enrolled_emails)
            })
        return result
    
    
    @staticmethod
    def manage_incoming_zapis(krouzky_ids: list) -> None:
        for krouzek in Krouzek.get_all():
            emails: list = json.loads(krouzek.enrolled_emails)
            if current_user.email in emails:
                emails.remove(current_user.email)
            if krouzek.id in krouzky_ids:
                emails.append(current_user.email)
            krouzek.enrolled_emails = json.dumps(emails)
            krouzek.update()
