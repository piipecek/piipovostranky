from website import db
from website.models.common_methods_db_model import Common_methods_db_model
from datetime import datetime
from zoneinfo import ZoneInfo
from website.helpers.pretty_date import pretty_datetime
from flask_login import current_user
from website.models.answer import Answer

def get_current_user_id():
    return current_user.id if current_user.is_authenticated else None


class Term(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default = lambda: datetime.now(ZoneInfo("Europe/Prague")))
    definition = db.Column(db.String(500))
    translation = db.Column(db.String(500))
    times_tested = db.Column(db.Integer, default=0)
    times_correct = db.Column(db.Integer, default=0)
    
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), default=get_current_user_id)
    author = db.relationship("User", back_populates="terms")
    decks = db.relationship("Deck", secondary="deck_term_jointable", back_populates="terms")
    answers = db.relationship("Answer", back_populates="term")
    
    
    def __repr__(self) -> str:
        return f"Term | {self.id}"
    
    
    @staticmethod
    def get_all_by_user(user_id) -> list["Term"]:
        return Term.query.filter_by(author_id=user_id).all()
    
    
    @staticmethod
    def get_all_for_user_list() -> list[dict]:
        terms = sorted(Term.get_all_by_user(current_user.id), key=lambda x: x.definition)
        return [term.for_user_list() for term in terms]
    

    def for_user_list(self) -> dict:
        return {
            "id": self.id,
            "datetime": pretty_datetime(self.datetime),
            "definition": self.definition,
            "translation": self.translation,
            "times_tested": self.times_tested,
            "times_correct": self.times_correct
        }
    
    
    def for_detail(self) -> dict:
        return {
            "id": self.id,
            "datetime": pretty_datetime(self.datetime),
            "definition": self.definition,
            "translation": self.translation,
            "times_tested": self.times_tested,
            "times_correct": self.times_correct,
            "decks": [{"id": deck.id, "name": deck.name} for deck in self.decks],
            "answers": [a.value for a in self.answers]
        }
        
        
    def delete(self):
        # rewrites the delete from common_methods_db_model to also delete the answers of the term and remove the term from the decks
        for answer in list(self.answers):
            db.session.delete(answer)
        for deck in list(self.decks):
            deck.terms.remove(self)
        db.session.delete(self)
        db.session.commit()
        
    
    def add_answer(self, answer_value):
        answer = Answer(value=answer_value, term_id=self.id)
        db.session.add(answer)
        db.session.commit()