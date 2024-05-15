from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from website.models.user import get_roles
from website.helpers.require_role import require_role_system_name_on_current_user
from website.models.evaluace import Evaluace
from acga.prumery import pocitani_prumeru
import json
from datetime import datetime

acga_views = Blueprint("acga_views",__name__)


@acga_views.route("/")
@acga_views.route("/home")
def home():
    return render_template("acga/dashboard.html")


@acga_views.route("/vazeny_prumer", methods=["GET"])
def vazeny_prumer():
    if request.method == "GET":
        return render_template("acga/vazeny_prumer.html", roles=get_roles())
    
    
@acga_views.route("/statistika_ctvrtletky")
def statistika_ctvrtletky():
    return render_template("acga/statistika_ctvrtletky.html", roles=get_roles(current_user))


@acga_views.route("/evaluace", methods=["GET","POST"])
def evaluace():
    if request.method == "GET":
        return render_template("acga/evaluace.html", roles=get_roles(current_user))
    else:
        if request.form.get("zadany_kod"):
            kod = request.form.get("kod").strip()
            if e := Evaluace.get_by_kod(kod):
                return redirect(url_for("acga_views.evaluace_formular", uuid=e.uuid))
            else:
                flash("Zadaný kód jsme nenašli. Pokud je to chyba na naší straně, dejte nám to vědět.", category="error")
                return redirect(url_for("acga_views.evaluace"))
        else:
            return request.form.to_dict()
        

@acga_views.route("cist_evaluace")
def cist_evaluace():
    if "acga_ucitel" in get_roles():
        return redirect(url_for("acga_views.cist_evaluace_auth"))
    else:
        return render_template("acga/cist_evaluace_bez_opravneni.html")
     

@acga_views.route("/cist_evaluace_auth", methods=["GET", "POST"])
@require_role_system_name_on_current_user("acga_ucitel")
def cist_evaluace_auth():
    if request.method == "GET":
        return render_template("acga/cist_evaluace.html")
    else:
        if request.form.get("acga_jmeno_button"):
            jmeno = request.form.get("acga_jmeno")
            current_user.acga_jmeno = jmeno
            current_user.update()
            flash("Změna ACGA Jména proběhla v pořádku.", category="success")
            return redirect(url_for("acga_views.cist_evaluace_auth"))
        elif id := request.form.get("smazat_evaluaci"):
            e = Evaluace.get_by_id(id)
            e.delete()
            flash("Evaluace úspěšně smazána", category="success")
            return redirect(url_for("acga_views.cist_evaluace_auth"))
        elif id := request.form.get("detail"):
            e = Evaluace.get_by_id(id)
            return redirect(url_for("acga_views.evaluace_locked", uuid=e.uuid))
        elif date := request.form.get("smazat_starsi_nez"):
            date = datetime.fromisoformat(date)
            for e in current_user.evaluace:
                e: Evaluace
                if e.datetime_vytvoreni < date:
                    e.delete()
            flash("Starší formuláře promazány.", category="success")
            return redirect(url_for("acga_views.cist_evaluace_auth"))
        elif request.form.get("tisk_neodevzdane"):
            result = []
            for e in current_user.evaluace:
                e: Evaluace
                if not e.je_odevzdana:
                    result.append(e)
            if len(result) == 0:
                flash("Nejsou žádné neodevzdané evaluace k tisku.", category="error")
                return redirect(url_for("acga_views.cist_evaluace_auth"))
            else:
                result = Evaluace.vytvorit_kody_k_tisku(result)
                return render_template("acga/tisk_kodu.html", kody = result)
        elif request.form.get("pocet_kodu"):
            pocet = int(request.form.get("pocet_kodu"))
            result = Evaluace.vytvorit_evaluace(pocet)
            result = Evaluace.vytvorit_kody_k_tisku(result)
            return render_template("acga/tisk_kodu.html", kody = result)
        return request.form.to_dict()


@acga_views.route("evaluace/<string:uuid>", methods=["GET","POST"])
def evaluace_formular(uuid):
    e = Evaluace.get_by_uuid(uuid)
    if not e:
        flash("Tohle UUID neexistuje.", category="error")
        return redirect(url_for("acga_views.evaluace"))
    else:
        if request.method == "GET":
            if e.je_odevzdana:
                return redirect(url_for("acga_views.evaluace_locked", uuid=uuid))
            else:
                return render_template("acga/evaluace_formular.html", uuid=uuid, name=Evaluace.get_by_uuid(uuid).ucitel.acga_jmeno)
        else:
            data = json.loads(request.form.get("result"))
            akce = data.get("akce")
            if akce == "ulozit": 
                e = Evaluace.get_by_uuid(uuid)
                e.ulozit_nova_data(data)
                flash("Vaše odpovědi byly uloženy.", category="success")
                return redirect(url_for("acga_views.evaluace_formular", uuid = uuid))
            elif akce == "odevzdat":
                e = Evaluace.get_by_uuid(uuid)
                e.ulozit_nova_data(data)
                e.oznacit_za_odevzdane()
                flash("Vaše odpovědi byly odevzdány, děkujeme.", category="success")
                return redirect(url_for("acga_views.evaluace_formular", uuid = uuid))
            return request.form.to_dict()
        

@acga_views.route("evaluace_locked/<string:uuid>")
def evaluace_locked(uuid):
    if not Evaluace.get_by_uuid(uuid):
        flash("Tohle UUID neexistuje.", category="error")
        return redirect(url_for("acga_views.evaluace"))
    else:
        e = Evaluace.get_by_uuid(uuid)
        if request.method == "GET":
            if e.je_odevzdana:
                return render_template("acga/evaluace_locked.html", uuid=uuid)
            else:
                return redirect(url_for("acga_views.evaluace_formular", uuid=uuid))
        else:
            return request.form.to_dict()


#TODO tohle jeste neni converted, check vsechny html a js soubory na neobvyklych mistech, check oba dashboardy


@acga_views.route("/evaluace_statistiky")
@require_role_system_name_on_current_user("acga_ucitel")
def evaluace_statistiky():
    return render_template("acga/evaluace_statistiky.html")


@acga_views.route("/astrofyzika")
def astrofyzika():
    return render_template("acga/astrofyzika.html")
