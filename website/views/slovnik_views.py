from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.helpers.require_role import require_role_system_name_on_current_user

slovnik_views = Blueprint("slovnik_views",__name__)

@slovnik_views.route("/")
@require_role_system_name_on_current_user("user")
def slovnik_home():
    if request.method == "GET":
        return render_template("slovnik/slovnik_home.html")
    else:
        return request.form.to_dict()