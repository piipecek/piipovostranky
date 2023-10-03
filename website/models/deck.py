from website import db
from website.models.common_methods_db_model import Common_methods_db_model
from website.models.jointables import deck_term_jointable, editor_candidates_jointable, editors_jointable, subscribers_jointable
import uuid
from datetime import datetime

class Deck(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), default=uuid.uuid4)
    name = db.Column(db.String(200))
    datetime = db.Column(db.DateTime, default = datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    terms = db.relationship("Term", secondary=deck_term_jointable, backref="decks")
    editors = db.relationship("User", secondary=editors_jointable, backref="editable_decks")
    subscribers = db.relationship("User", secondary=subscribers_jointable, backref="subscribed_decks")
    editor_candidates = db.relationship("User", secondary=editor_candidates_jointable, backref="editor_candidate_decks")
    exams = db.relationship("Exam", backref="deck")
    def __repr__(self) -> str:
        return f"Deck | {self.name}"
