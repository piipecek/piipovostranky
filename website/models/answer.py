from website import db
from website.models.common_methods_db_model import Common_methods_db_model

class Answer(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(200))
    term_id = db.Column(db.Integer, db.ForeignKey("term.id"))
    term = db.relationship("Term", back_populates="answers")