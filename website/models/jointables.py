from website import db

user_role_jointable = db.Table("user_role_jointable",
                               db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                               db.Column("role_id", db.Integer, db.ForeignKey("role.id"))
                               )

deck_term_jointable = db.Table("deck_term_jointable",
                               db.Column("deck_id", db.Integer, db.ForeignKey("deck.id")),
                               db.Column("term_id", db.Integer, db.ForeignKey("term.id"))
                               )