from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from website.models.user import get_roles
from website.helpers.require_role import require_role_system_name_on_current_user


user_views = Blueprint("user_views",__name__)


@user_views.route("/ucet", methods=["GET","POST"])
@require_role_system_name_on_current_user("user")
def ucet():
    if request.method == "GET":
        return render_template("ucet.html", roles=get_roles(current_user))
    else:
         return request.form.to_dict()