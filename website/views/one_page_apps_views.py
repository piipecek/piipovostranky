from flask import Blueprint, render_template, send_file, request
from website.paths import hadej_slova_db_path
from tomiem_ipsum.generator import get_tomiem
from catan.catan import generate_catan
from semihra.semihra import generate
from cernabila.cernabila import get_word
from website.models.user import get_roles
from flask_login import current_user
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

@one_page_apps_views.route("/two_of_these_people_are_lying")
def two_of_these_people_are_lying():
    return render_template("one_page_apps/two_of_these_people_are_lying.html", roles=get_roles(current_user))

@one_page_apps_views.route("/marsjosefac")
def marsjosefac():
    return render_template("one_page_apps/marsjosefac.html", roles=get_roles(current_user))

@one_page_apps_views.route("/jeopardy")
def jeopardy():
    return render_template("one_page_apps/jeopardy.html", roles=get_roles(current_user))
