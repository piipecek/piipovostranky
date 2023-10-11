from website import db
from website.models.common_methods_db_model import Common_methods_db_model

class Language(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    system_name = db.Column(db.String(200))
    display_name = db.Column(db.String(200))
    translations = db.relationship("Translation", backref="language")
    def __repr__(self) -> str:
        return f"Jazyk | {self.system_name}"
    
    def get_detail_for_seznam_jazyku(self) -> dict:
        return {
            "id": self.id,
            "system_name": self.system_name,
            "display_name": self.display_name,
            "number_of_translations": len(self.translations)
        }
    
    def get_detail_jazyka(self) -> dict:
        return {
            "id": self.id,
            "system_name": self.system_name,
            "display_name": self.display_name,
            "number_of_translations": len(self.translations)
        }