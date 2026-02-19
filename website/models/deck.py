from website import db
from website.models.common_methods_db_model import Common_methods_db_model
from website.models.jointables import deck_term_jointable
import uuid
from datetime import datetime, timezone

class Deck(Common_methods_db_model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), default=uuid.uuid4)
    name = db.Column(db.String(200))
    datetime = db.Column(db.DateTime, default = datetime.now(timezone.utc))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", back_populates="decks")
    terms = db.relationship("Term", secondary=deck_term_jointable, back_populates="decks")
