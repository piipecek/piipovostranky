from website import db
from website.models.common_methods_db_model import Common_methods_db_model
from website.models.jointables import user_role_jointable
from datetime import datetime, timedelta, timezone
from flask import current_app
from flask_login import UserMixin, current_user
from typing import List
import jwt

class User(Common_methods_db_model, UserMixin):
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
    
    @staticmethod
    def get_by_email(email) -> "User":
        return db.session.scalars(db.select(User).where(User.email == email)).first()
        
        
    def get_reset_token(self, expires_sec=9000) -> str:
        reset_token = jwt.encode(
            {
                "user_id": self.id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expires_sec)
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256"
        )
        return reset_token    
    
    
    @staticmethod
    def verify_reset_token(token) -> "User":
        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return None
        return User.get_by_id(data["user_id"])
    


def get_roles(u: User = current_user) -> List["str"]:
    result = []
    if u.is_authenticated:
        result.append("prihlasen")
        result.extend([r.system_name for r in u.roles])
    return result