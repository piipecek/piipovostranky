import json
from flask import Blueprint
from website.models.suggestion import Suggestion
from website.models.user import User

guest_api = Blueprint("guest_api", __name__)

@guest_api.route("/suggestions")
def suggestions():
    return json.dumps([s.info_for_guest() for s in Suggestion.get_all()])


@guest_api.route("ucitele_na_evaluaci")
def ucitele_na_evaluaci():
    return json.dumps([u.acga_jmeno for u in User.get_all() if u.acga_jmeno])


