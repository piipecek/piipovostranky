from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from website.models.user import get_roles
from website.models.suggestion import Suggestion


guest_views = Blueprint("guest_views",__name__)


@guest_views.route("/")
@guest_views.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", roles=get_roles(current_user))

@guest_views.route("/known_bugs")
def known_bugs():
    return render_template("zname_chyby.html", roles=get_roles(current_user))

@guest_views.route("/historie")
def historie():
    return render_template("historie_verzi.html", roles=get_roles(current_user))

@guest_views.route("/nahlasit_bug", methods=["GET","POST"])
def nahlasit_bug():
    if request.method == "GET":
        return render_template("nahlasit_chybu.html", roles=get_roles(current_user))
    else:
        autor = None
        if current_user.is_authenticated:
            autor = current_user if request.form.get("include_name") else None
        s = Suggestion(value = request.form.get("popis"), author = autor)
        s.update()
        return redirect(url_for("guest_views.known_bugs"))

@guest_views.route("/planovane_featury")
def planovane_featury():
    return render_template("planovane_featury.html", roles=get_roles(current_user))

@guest_views.route("/account", methods=["GET","POST"])
@login_required
def account():
    if request.method == "GET":
        return render_template("account.html", roles=get_roles(current_user))
    else:
         return request.form.to_dict()


@guest_views.route("/mutace")
def mutace():
    return render_template("jazykova_mutace.html", roles=get_roles(current_user))

@guest_views.route("/vydaje")
def vydaje():
    return render_template("vydaje.html", roles=get_roles(current_user))
