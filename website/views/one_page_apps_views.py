from flask import Blueprint, render_template, send_file, request, flash, redirect, url_for
from website.paths import hadej_slova_db_path
from tomiem_ipsum.generator import get_tomiem
from catan.catan import generate_catan
from semihra.semihra import generate
from cernabila.cernabila import get_word
from website.models.user import get_roles
from flask_login import current_user
from acga.prumery import pocitani_prumeru
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

@one_page_apps_views.route("/acga_evaluace")
def acga_evaluace():
    return render_template("one_page_apps/acga_evaluace.html", roles=get_roles(current_user))
    