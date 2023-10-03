from website import db
from website.models.common_methods_db_model import Common_methods_db_model
from website.models.jointables import user_role_jointable
from datetime import datetime

class User(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    last_login_datetime = db.Column(db.DateTime)
    registration_datetime = db.Column(db.DateTime, default = datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)
    roles = db.relationship("Role", secondary=user_role_jointable, backref="users")
    terms = db.relationship("Term", backref="author")
    decks = db.relationship("Deck", backref="author")
    exams = db.relationship("Exam", backref="author")
    suggestions = db.relationship("Suggestion", backref="author")
    def __repr__(self) -> str:
        return f"Uživatel | {self.email}"