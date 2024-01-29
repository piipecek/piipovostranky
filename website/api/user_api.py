import json
from flask import Blueprint
from website.helpers.require_role import require_role_system_name_on_current_user
from flask_login import current_user
from website.models.evaluace import Evaluace

user_api = Blueprint("user_api", __name__)

@user_api.route("/detail_usera")
@require_role_system_name_on_current_user("user")
def detail_usera():
    return json.dumps(current_user.get_info_for_detail_usera())


@user_api.route("/jazyky")
@require_role_system_name_on_current_user("user")
def jazyky():
    return json.dumps(current_user.get_info_for_detail_usera())


@user_api.route("/vytvorit_evaluace/<int:pocet>", methods=["GET","POST"])
@require_role_system_name_on_current_user("user")
def vytvorit_evlauace(pocet):
    result = Evaluace.vytvorit_evaluace(pocet)
    return result

@user_api.route("/get_acga_jmeno")
@require_role_system_name_on_current_user("user")
def get_acga_jmeno():
    return current_user.acga_jmeno if current_user.acga_jmeno else ""

@user_api.route("/get_evaluace_pro_seznam")
@require_role_system_name_on_current_user("user")
def get_evaluace_pro_seznam():
    return json.dumps([e.get_info_pro_seznam() for e in Evaluace.get_all() if e.ucitel == current_user])
