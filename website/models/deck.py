from website import db
from website.models.common_methods_db_model import Common_methods_db_model
from website.models.jointables import deck_term_jointable
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo
from flask_login import current_user
from website.helpers.pretty_date import pretty_datetime
import random
from werkzeug.datastructures import FileStorage
import openpyxl
from website.models.term import Term


def get_current_user_id():
    return current_user.id if current_user.is_authenticated else None

class Deck(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    uuid = db.Column(db.String(36), default=uuid.uuid4)
    datetime = db.Column(db.DateTime, default = lambda: datetime.now(ZoneInfo("Europe/Prague")))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), default=get_current_user_id)
    author = db.relationship("User", back_populates="decks")
    terms = db.relationship("Term", secondary=deck_term_jointable, back_populates="decks")


    @staticmethod
    def get_all_by_user(user_id) -> list["Deck"]:
        return Deck.query.filter_by(author_id=user_id).all()
    
    
    @staticmethod
    def get_all_for_user_list() -> list[dict]:
        decks = Deck.get_all_by_user(current_user.id)
        return [deck.for_user_list() for deck in decks]
    

    def for_user_list(self) -> dict:
        return {
            "id": self.id,
            "datetime": pretty_datetime(self.datetime),
            "name": self.name,
            "term_count": len(self.terms)
        }
        
        
    def for_detail(self) -> list[dict]:
        return {
            "id": self.id,
            "datetime": pretty_datetime(self.datetime),
            "name": self.name,
            "terms": [term.for_user_list() for term in self.terms],
            "term_count": len(self.terms)
        }
        
        
    def delete(self):
        self.terms = []
        db.session.delete(self)
        db.session.commit()
    
    
    def delete_and_words(self):
        for term in self.terms:
            db.session.delete(term)
        db.session.delete(self)
        db.session.commit()


    def for_quiz(self) -> list[dict]:
        terms = [
            {
                "id": term.id,
                "front": term.front,
                "back": term.back,
                "answers": []
            } for term in self.terms
        ]
        random.shuffle(terms)
        return terms
    
    
    @staticmethod
    def import_from_xlsx(file: FileStorage):
        result = {
            "success": False,
            "deck_id": None,
            "error": None
        }
        try:
            workbook = openpyxl.load_workbook(file)
            sheet = workbook.active
            deck_name = file.filename.rsplit(".", 1)[0]
            deck = Deck(name=deck_name, author_id=current_user.id)
            deck.update()
            result["deck_id"] = deck.id
            for row in sheet.iter_rows(values_only=True):
                front = row[0]
                back = row[1]
                term = Term(front=front, back=back)
                term.update()
                deck.terms.append(term)
            deck.update()
            result["success"] = True
            return result
        except Exception as e:
            result["error"] = str(e)
            if result["deck_id"]:
                deck = Deck.get_by_id(result["deck_id"])
                if deck:
                    deck.delete()
            return result
        
    def for_pdf(self) -> dict:
        return {
            "deck_name": self.name,
            "terms": [
                {
                    "front": term.front,
                    "back": term.back
                } for term in self.terms
            ]
        }