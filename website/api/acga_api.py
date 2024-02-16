import json
from flask import Blueprint, request
from website.helpers.require_role import require_role_system_name_on_current_user
from flask_login import current_user
from datetime import datetime
from website.models.evaluace import Evaluace
from acga.prumery import pocitani_prumeru


acga_api = Blueprint("acga_api", __name__)


@acga_api.route("/get_acga_jmeno")
@require_role_system_name_on_current_user("user")
def get_acga_jmeno():
    return current_user.acga_jmeno if current_user.acga_jmeno else ""


@acga_api.route("/get_evaluace_pro_seznam")
@require_role_system_name_on_current_user("user")
def get_evaluace_pro_seznam():
    return json.dumps([e.get_info_pro_seznam() for e in Evaluace.get_all() if e.ucitel == current_user])


@acga_api.route("/evaluace/<string:uuid>")
def evaluace_data(uuid):
    if e := Evaluace.get_by_uuid(uuid):
        return e.data_json
    else:
        return None
    
    
@acga_api.route("/evaluace_locked/<string:uuid>")
def evaluace_locked(uuid):
    if e := Evaluace.get_by_uuid(uuid):
        return e.locked_data()
    else:
        return None

@acga_api.route("/evaluace_statistiky_data", methods=["POST"])
@require_role_system_name_on_current_user("acga_ucitel")
def evaluace_statistiky_data():
    date = datetime.fromisoformat(request.form.get("date"))
    print(date)
    return request.form.to_dict()
 
@acga_api.route("/vytvorit_evaluace/<int:pocet>", methods=["GET","POST"])
@require_role_system_name_on_current_user("user")
def vytvorit_evlauace(pocet):
    result = Evaluace.vytvorit_evaluace(pocet)
    return result

@acga_api.route("/vazeny_prumer", methods=["POST"])
def vazeny_prumer():
    file = request.files["file"]
    data  = request.form.to_dict()
    result = pocitani_prumeru(file=file, data=data)
    return json.dumps(result, indent=3)