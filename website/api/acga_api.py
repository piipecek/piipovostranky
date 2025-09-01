import json
from flask import Blueprint, request
from website.helpers.require_role import require_role_system_name_on_current_user
from website.helpers.pretty_date import pretty_datetime
from flask_login import current_user
from datetime import datetime, date, timedelta
from website.models.evaluace import Evaluace
from acga.prumery import pocitani_prumeru
from astrofyzika.generator import generator
from website.models.krouzek import Krouzek


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


@acga_api.route("/vazeny_prumer", methods=["POST"])
def vazeny_prumer():
    file = request.files["file"]
    data  = request.form.to_dict()
    result = pocitani_prumeru(file=file, data=data)
    return json.dumps(result, indent=3)


@acga_api.route("/evaluace_statistiky_data", methods=["POST"])
@require_role_system_name_on_current_user("acga_ucitel")
def evaluace_statistiky_data():
    form_date = datetime.fromisoformat(request.form.get("date"))
    otazky = []
    # pripustna evaluace do shrnuti je 1) od spravnyho ucitele 2) odevzdana 3) novejsi nez dane datum
    pripustne_evaluace = [e for e in current_user.evaluace if e.je_odevzdana]
    if request.form.get("type") == "odevzdane":
        pripustne_evaluace = [e for e in pripustne_evaluace if e.datetime_odevzdani > form_date]
    else:
        pripustne_evaluace = [e for e in pripustne_evaluace if e.datetime_vytvoreni > form_date]
        
    for e in pripustne_evaluace:
        e: Evaluace
        data_evaluace = json.loads(e.data_json)
        for otazka in data_evaluace:
            if otazka["id"] not in [entry["id"] for entry in otazky]: # pokud tohle ID ještě nemá histogramovou kategorii, zalozim ji
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
                
                otazky.append(novy_zaznam)
            # teď už záznam buď existoval předtim, nebo byl nově vytvořenej
            #najdu ten existujici zaaznam 
            zaznam = None
            for z in otazky:
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
                
    datetimes = []
    for e in pripustne_evaluace:
        datetimes.append(e.datetime_odevzdani.date())
        
    diff: timedelta = max(datetimes) - min(datetimes)
    diff_days = diff.days
    start_date = min(datetimes)
    datetimes_full = [{"date": start_date + timedelta(days=i), "count": datetimes.count(start_date + timedelta(days=i))} for i in range(diff_days+1)] # chci prvni i posledni
        
    result = {
        "otazky": otazky,
        "count": len(pripustne_evaluace),
        "dny": [pretty_datetime(d["date"]) for d in datetimes_full],
        "pocty_ve_dnech": [str(d["count"]) for d in datetimes_full]
    }
    return json.dumps(result, indent=4)

@acga_api.route("/astrofyzika/<string:prijmeni>", methods=["GET"])
def astrofyzika(prijmeni):
    cisla = generator(prijmeni)
    return json.dumps(cisla, indent=4)


@acga_api.route("/seznam_krouzku")
@require_role_system_name_on_current_user("acga_ucitel")
def seznam_krouzku():
    return json.dumps(Krouzek.get_data_for_list()), 200


@acga_api.route("/detail_krouzku/<int:id>")
@require_role_system_name_on_current_user("acga_ucitel")
def detail_krouzku(id):
    return json.dumps(Krouzek.get_by_id(id).get_data_for_detail()), 200


@acga_api.route("/student_krouzky")
def student_krouzky():
    if current_user.organizace != "acga.cz":
        return "", 403
    return json.dumps(Krouzek.get_data_for_current_user()), 200