import json
from flask import Blueprint
from website.models.suggestion import Suggestion
from website.models.evaluace import Evaluace

guest_api = Blueprint("guest_api", __name__)

@guest_api.route("/suggestions")
def suggestions():
    return json.dumps([s.info_for_guest() for s in Suggestion.get_all()])

@guest_api.route("/evaluace/<string:uuid>")
def evaluace_data(uuid):
    if e := Evaluace.get_by_uuid(uuid):
        return e.data_json
    else:
        return None
    
@guest_api.route("/evaluace_locked/<string:uuid>")
def evaluace_locked(uuid):
    if e := Evaluace.get_by_uuid(uuid):
        return e.locked_data()
    else:
        return None