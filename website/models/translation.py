from website import db
from website.models.common_methods_db_model import Common_methods_db_model

class Translation(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(200))
    times_learned = db.Column(db.Integer)
    times_tested = db.Column(db.Integer)
    times_known = db.Column(db.Integer)
    term_id = db.Column(db.Integer, db.ForeignKey("term.id"))
    language_id = db.Column(db.Integer, db.ForeignKey("language.id"))
    answers = db.relationship("Answer", backref="translation")
    def __repr__(self) -> str:
        return f"Translation | {self.value}"