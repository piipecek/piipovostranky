from website import db

user_role_jointable = db.Table("user_role_jointable",
                               db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                               db.Column("role_id", db.Integer, db.ForeignKey("role.id"))
                               )

deck_term_jointable = db.Table("deck_term_jointable",
                               db.Column("deck_id", db.Integer, db.ForeignKey("deck.id")),
                               db.Column("term_id", db.Integer, db.ForeignKey("term.id"))
                               )

editors_jointable = db.Table("editors_jointable",
                                 db.Column("deck_id", db.Integer, db.ForeignKey("deck.id")),
                                 db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
                                 )

subscribers_jointable = db.Table("subscribers_jointable",
                                 db.Column("deck_id", db.Integer, db.ForeignKey("deck.id")),
                                 db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
                                 )

editor_candidates_jointable = db.Table("editor_candidates_jointable",
                                 db.Column("deck_id", db.Integer, db.ForeignKey("deck.id")),
                                 db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
                                 )
