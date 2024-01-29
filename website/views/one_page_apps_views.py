from flask import Blueprint, render_template, send_file, request, flash, redirect, url_for
from website.paths import hadej_slova_db_path
from tomiem_ipsum.generator import get_tomiem
from catan.catan import generate_catan
from semihra.semihra import generate
from cernabila.cernabila import get_word
from website.models.user import get_roles
from flask_login import current_user
from acga.prumery import pocitani_prumeru
from website.models.evaluace import Evaluace
import json

one_page_apps_views = Blueprint("one_page_apps_views", __name__)

@one_page_apps_views.route("/rybicky")
def rybicky():
    return render_template("one_page_apps/rybicky.html", roles=get_roles(current_user))


@one_page_apps_views.route("/hadej_slova")
def hadej_slova():
    return render_template("one_page_apps/hadej_slova.html", roles=get_roles(current_user))


@one_page_apps_views.route("/hadej_slova_getter")
def hadej_slova_getter():
    return send_file(hadej_slova_db_path())


@one_page_apps_views.route("/tomiem_ipsum/<int:words>")
def tomiem_ipsum(words):
    return get_tomiem(words=words)


@one_page_apps_views.route("/matematika/popis_primky")
def popis_primky():
    return render_template("one_page_apps/popis_primky.html", roles=get_roles(current_user))


@one_page_apps_views.route("/matematika/trig")
def trig():
    return render_template("one_page_apps/trig.html", roles=get_roles(current_user))


@one_page_apps_views.route("/matematika/nacrty")
def nacrty():
    return render_template("one_page_apps/nacrty.html", roles=get_roles(current_user))


@one_page_apps_views.route("/catan",  methods=["GET","POST"])
def catan():
    if request.method == "GET":
        return render_template("one_page_apps/catan.html", roles=get_roles(current_user))
    else:
        got = json.loads(request.form["result"])
        return json.dumps(generate_catan(got))
    

@one_page_apps_views.route("/matlab")
def matlab():
    return render_template("one_page_apps/matlab.html", roles=get_roles(current_user))


@one_page_apps_views.route("/semihra", methods=["GET","POST"])
def semihra():
    if request.method == "GET":
        return render_template("one_page_apps/semihra.html", roles=get_roles(current_user))
    else:
        jmena = request.form["jmena"]
        indicie =  request.form["indicie"]
        return json.dumps(generate(string_jmen = jmena, string_indicii = indicie))


@one_page_apps_views.route("/frekvence", methods=["GET","POST"])
def frekvence():
    if request.method == "GET":
        return render_template("one_page_apps/frekvence.html", roles=get_roles(current_user))
    else:
        return "jeste neumim post"


@one_page_apps_views.route("/cernabila", methods=["GET","POST"])
def cernabila():
    if request.method == "GET":
        return render_template("one_page_apps/cernabila.html", roles=get_roles(current_user))
    else:
        return "jeste neumim post"


@one_page_apps_views.route("/cerna_bila_get_word")
def cerna_bila_get_word():
    return json.dumps({"slovo": get_word()})


@one_page_apps_views.route("/tabulky", methods=["GET","POST"])
def tabulky():
    if request.method == "GET":
        return render_template("one_page_apps/tabulky.html", roles=get_roles(current_user))
    else:
        return "jeste neumim post"
    

@one_page_apps_views.route("/mutace")
def mutace():
    return render_template("one_page_apps/jazykova_mutace.html", roles=get_roles(current_user))


@one_page_apps_views.route("/vydaje")
def vydaje():
    return render_template("one_page_apps/vydaje.html", roles=get_roles(current_user))


@one_page_apps_views.route("/acga_vazeny_prumer", methods=["GET","POST"])
def acga_vazeny_prumer():
    if request.method == "GET":
        return render_template("one_page_apps/acga_vazeny_prumer.html", roles=get_roles(current_user))
    else:
        file = request.files["file"]
        data  = request.form.to_dict()
        result = pocitani_prumeru(file=file, data=data)
        return json.dumps(result, indent=3)
    
@one_page_apps_views.route("/acga_statistika_ctvrtletky")
def acga_statistika_ctvrtletky():
    return render_template("one_page_apps/acga_statistika_ctvrtletky.html", roles=get_roles(current_user))

@one_page_apps_views.route("/acga_evaluace", methods=["GET","POST"])
def acga_evaluace():
    if request.method == "GET":
        return render_template("one_page_apps/acga_evaluace.html", roles=get_roles(current_user))
    else:
        if request.form.get("zadany_kod"):
            kod = request.form.get("kod")
            if e := Evaluace.get_by_kod(kod):
                return redirect(url_for("one_page_apps_views.acga_evaluace_formular", uuid=e.uuid))
            else:
                flash("Zadaný kód jsme nenašli. Pokud je to chyba na naší straně, dejte nám to vědět.", category="error")
                return redirect(url_for("one_page_apps_views.acga_evaluace"))
        else:
            return request.form.to_dict()
    

@one_page_apps_views.route("acga_cist_evaluace")
def acga_cist_evaluace():
    if "acga_ucitel" in get_roles():
        return redirect(url_for("user_views.acga_cist_evaluace_auth"))
    else:
        return render_template("one_page_apps/acga_cist_evaluace_bez_opravneni.html")
    
@one_page_apps_views.route("acga_evaluace/<string:uuid>", methods=["GET","POST"])
def acga_evaluace_formular(uuid):
    e = Evaluace.get_by_uuid(uuid)
    if not e:
        flash("Tohle UUID neexistuje.", category="error")
        return redirect(url_for("one_page_apps_vies.acga_evaluace"))
    else:
        
        if request.method == "GET":
            if e.je_odevzdana:
                return redirect(url_for("one_page_apps_views.acga_evaluace_locked", uuid=uuid))
            else:
                return render_template("one_page_apps/acga_evaluace_formular.html", uuid=uuid, name=Evaluace.get_by_uuid(uuid).ucitel.acga_jmeno)
        else:
            data = json.loads(request.form.get("result"))
            akce = data.get("akce")
            if akce == "ulozit": 
                e = Evaluace.get_by_uuid(uuid)
                e.ulozit_nova_data(data)
                flash("Vaše odpovědi byly uloženy.", category="success")
                return redirect(url_for("one_page_apps_views.acga_evaluace_formular", uuid = uuid))
            elif akce == "odevzdat":
                e = Evaluace.get_by_uuid(uuid)
                e.ulozit_nova_data(data)
                e.oznacit_za_odevzdane()
                flash("Vaše odpovědi byly odevzdány, děkujeme.", category="success")
                return redirect(url_for("one_page_apps_views.acga_evaluace_formular", uuid = uuid))
            return request.form.to_dict()
        
@one_page_apps_views.route("acga_evaluace_locked/<string:uuid>")
def acga_evaluace_locked(uuid):
    if not Evaluace.get_by_uuid(uuid):
        flash("Tohle UUID neexistuje.", category="error")
        return redirect(url_for("one_page_apps_vies.acga_evaluace"))
    else:
        e = Evaluace.get_by_uuid(uuid)
        if request.method == "GET":
            if e.je_odevzdana:
                return render_template("one_page_apps/acga_evaluace_locked.html", uuid=uuid)
            else:
                return redirect(url_for("one_page_apps_views.acga_evaluace_formular", uuid=uuid))
        else:
            return request.form.to_dict()