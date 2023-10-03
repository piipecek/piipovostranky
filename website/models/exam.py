from website import db
from website.models.common_methods_db_model import Common_methods_db_model
from datetime import datetime

class Exam(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default = datetime.utcnow)
    score = db.Column(db.Float)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    deck_id = db.Column(db.Integer, db.ForeignKey("deck.id"))
    source_language_id = db.Column(db.Integer, db.ForeignKey("language.id"))
    target_language_id = db.Column(db.Integer, db.ForeignKey("language.id"))
    # tohle je cesta, jak udelat ty dva foreign keys mezi dvema tabulkama.
    source_language = db.relationship("Language", foreign_keys=[source_language_id], backref="sourced_exams")
    target_language = db.relationship("Language", foreign_keys=[target_language_id], backref="targetted_exams")
    answers = db.relationship("Answer", backref="exam")
    def __repr__(self) -> str:
        return f"Exam | {self.datetime}"