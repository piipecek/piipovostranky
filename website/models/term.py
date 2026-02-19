from website import db
from website.models.common_methods_db_model import Common_methods_db_model
from datetime import datetime, timezone

class Term(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default = datetime.now(timezone.utc))
    definition = db.Column(db.String(500))
    translation = db.Column(db.String(500))
    times_tested = db.Column(db.Integer, default=0)
    times_correct = db.Column(db.Integer, default=0)
    
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", back_populates="terms")
    decks = db.relationship("Deck", secondary="deck_term_jointable", back_populates="terms")
    answers = db.relationship("Answer", back_populates="term")
    def __repr__(self) -> str:
        return f"Term | {self.id}"