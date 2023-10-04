from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from website.models.user import get_roles


noauth_views = Blueprint("noauth_views",__name__)


@noauth_views.route("/")
@noauth_views.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", roles=get_roles(current_user))

@noauth_views.route("/known_bugs")
def known_bugs():
    chyby  = Chyba.get_all()
    return render_template("zname_chyby.html", chyby=chyby)

@noauth_views.route("/historie")
def historie():
    return render_template("historie_verzi.html", roles=get_roles(current_user))

@noauth_views.route("/nahlasit_bug", methods=["GET","POST"])
def nahlasit_bug():
    if request.method == "GET":
        return render_template("nahlasit_chybu.html")
    else:
        if current_user.is_authenticated:
            autor = current_user.email if request.form.get("include_name") else "Anonym"
        else:
            autor = "user_not_logged_in"
        c = Chyba(
        autor = autor,
        popis = request.form.get("popis")
        )
        c.pridat_do_chyb()
        return redirect(url_for("noauth_views.known_bugs"))

@noauth_views.route("/planovane_featury")
def planovane_featury():
    return render_template("planovane_featury.html", roles=get_roles(current_user))

@noauth_views.route("/account", methods=["GET","POST"])
@login_required
def account():
    if request.method == "GET":
        return render_template("account.html", roles=get_roles(current_user))
    else:
         return request.form.to_dict()


@noauth_views.route("/mutace")
def mutace():
    return render_template("jazykova_mutace.html", roles=get_roles(current_user))

@noauth_views.route("/vydaje")
def vydaje():
    return render_template("vydaje.html", roles=get_roles(current_user))
