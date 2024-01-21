import json
from flask import Blueprint
from website.models.suggestion import Suggestion
from website.models.user import User

guest_api = Blueprint("guest_api", __name__)

@guest_api.route("/suggestions")
def suggestions():
    return json.dumps([s.info_for_guest() for s in Suggestion.get_all()])