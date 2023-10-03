from website import db
from website.models.common_methods_db_model import Common_methods_db_model

class Answer(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(200))
    exam_id = db.Column(db.Integer, db.ForeignKey("exam.id"))
    translation_id = db.Column(db.Integer, db.ForeignKey("translation.id"))
    def __repr__(self) -> str:
        return f"Answer | {self.value}"