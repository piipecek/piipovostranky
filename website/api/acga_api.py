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


@acga_api.route("/evaluace_statistiky_data", methods=["POST"])
@require_role_system_name_on_current_user("acga_ucitel")
def evaluace_statistiky_data():
    date = datetime.fromisoformat(request.form.get("date"))
    result = []
    # pripustna evaluace do shrnuti je 1) od spravnyho ucitele 2) odevzdana 3) novejsi nez dane datum
    pripustne_evaluace = [e for e in current_user.evaluace if e.datetime_vytvoreni > date and e.je_odevzdana]
    for e in pripustne_evaluace:
        e: Evaluace
        data_evaluace = json.loads(e.data_json)
        for otazka in data_evaluace:
            if otazka["id"] not in [entry["id"] for entry in result]: # pokud tohle ID ještě nemá histogramovou kategorii, zalozim ji
                # budu mit dva typy: histogram a otevrena. Do histogramu patri single, multiple i ciselna.
                if otazka["typ"] == "ciselna":
                    popisky = [str(i) for i in range(1, otazka["max"]+1)]
                    popisky[0] += ": Zcela souhlasím"
                    popisky[-1] += ": Vůbec neuhlasím"
                    typ = "histogram"
                elif otazka["typ"] == "single":
                    popisky = otazka["choices"]
                    typ = "histogram"
                elif otazka["typ"] == "multiple":
                    popisky = otazka["choices"]
                    typ = "histogram"
                else:
                    popisky = None
                    typ = "otevrena"
                    
                novy_zaznam = {
                        "id": otazka["id"],
                        "otazka": otazka["otazka"],
                        "typ": typ,
                    }    
                if typ == "histogram":
                    novy_zaznam["x"] = popisky
                    novy_zaznam["y"] = [0 for _ in popisky]
                else:
                    novy_zaznam["odpovedi"] = []
                
                result.append(novy_zaznam)
            # teď už záznam buď existoval předtim, nebo byl nově vytvořenej
            #najdu ten existujici zaaznam 
            zaznam = None
            for z in result:
                if z["id"] == otazka["id"]:
                    zaznam = z
                    break
            # a zapocitam.
            
            if otazka["typ"] == "ciselna" and otazka["value"]:
                zaznam["y"][otazka["value"]-1] += 1
            elif otazka["typ"] == "single" and otazka["value"] is not None:
                zaznam["y"][otazka["value"]] += 1
            elif otazka["typ"] == "multiple" and otazka["values"]:
                for value in otazka["values"]:
                    zaznam["y"][value] += 1
            elif otazka["typ"] == "otevrena":
                zaznam["odpovedi"].append(otazka["value"])
    return json.dumps(result, indent=4)