from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.helpers.require_role import require_role_system_name_on_current_user
from website.models.user import get_roles

slovnik_views = Blueprint("slovnik_views",__name__)

@slovnik_views.route("/")
@require_role_system_name_on_current_user("user")
def slovnik_home():
    return render_template("slovnik/dashboard.html", roles=get_roles())


@slovnik_views.route("/docs")
@require_role_system_name_on_current_user("user")
def docs():
    return render_template("slovnik/docs.html", roles=get_roles())
    
    
@slovnik_views.route("/terms", methods=["GET", "POST"])
@require_role_system_name_on_current_user("user")
def terms():
    if request.method == "GET":
        return render_template("slovnik/terms.html", roles=get_roles())
    else:
        return request.form.to_dict()
    
    
@slovnik_views.route("/decks", methods=["GET", "POST"])
@require_role_system_name_on_current_user("user")
def decks():
    if request.method == "GET":
        return render_template("slovnik/decks.html", roles=get_roles())
    else:
        return request.form.to_dict()    
    
    
@slovnik_views.route("/new_terms", methods=["GET", "POST"])
@require_role_system_name_on_current_user("user")
def new_terms():
    if request.method == "GET":
        return render_template("slovnik/new_terms.html", roles=get_roles())
    else:
        return request.form.to_dict()