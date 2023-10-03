from website import db
from website.models.common_methods_db_model import Common_methods_db_model
from datetime import datetime

class Term(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    asociace = db.Column(db.String(200))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    datetime = db.Column(db.DateTime, default = datetime.utcnow)
    translations = db.relationship("Translation", backref="term")
    def __repr__(self) -> str:
        return f"Term | {self.id}"