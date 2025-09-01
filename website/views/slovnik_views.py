from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.helpers.require_role import require_role_system_name_on_current_user
from website.models.user import get_roles

slovnik_views = Blueprint("slovnik_views",__name__)

@slovnik_views.route("/")
@require_role_system_name_on_current_user("user")
def slovnik_home():
    if request.method == "GET":
        return render_template("slovnik/dashboard.html", roles=get_roles())
    else:
        return request.form.to_dict()
    
@slovnik_views.route("/slovnik")
@require_role_system_name_on_current_user("user")
def slovnik():
    if request.method == "GET":
        return render_template("slovnik/slovnik.html", roles=get_roles())
    else:
        return request.form.to_dict()
    
@slovnik_views.route("/nova_slovicka")
@require_role_system_name_on_current_user("user")
def nova_slovicka():
    if request.method == "GET":
        return render_template("slovnik/nova_slovicka.html", roles=get_roles())
    else:
        return request.form.to_dict()