import json
from flask import Blueprint, request
from website.helpers.require_role import require_role_system_name_on_current_user
from flask_login import current_user
from website.models.term import Term
from website.models.deck import Deck


slovnik_api = Blueprint("slovnik_api", __name__)


@slovnik_api.route("/terms")
@require_role_system_name_on_current_user("user")
def get_terms():
    return json.dumps(Term.get_all_for_user_list())


@slovnik_api.route("/decks")
@require_role_system_name_on_current_user("user")
def get_decks():
    return json.dumps(Deck.get_all_for_user_list())


@slovnik_api.route("/deck/<int:deck_id>")
@require_role_system_name_on_current_user("user")
def get_terms_in_deck(deck_id):
    deck = Deck.get_by_id(deck_id)
    if deck.author_id != current_user.id:
        return json.dumps({"error": "Nemáte oprávnění zobrazit tento balíček!"})
    return json.dumps(deck.for_detail())