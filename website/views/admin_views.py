from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from website.models.suggestion import Suggestion
from website.models.user import User
from website.logs import delete_app_logs
import json
import shutil
from website.helpers.require_role import require_role_system_name_on_current_user

admin_views = Blueprint("admin_views",__name__)


@admin_views.route("/")
@admin_views.route("/dashboard")
@require_role_system_name_on_current_user("admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")


@admin_views.route("/uprava_znamych_bugu", methods=["GET","POST"])
@require_role_system_name_on_current_user("editing_suggestions")
def uprava_znamych_bugu():
    if request.method == "GET":
        return render_template("admin_uprava_znamych_chyb.html")
    else:
        if _id := request.form.get("smazat_suggestion"):
            Suggestion.get_by_id(_id).delete()
            flash("Záznam smazán", category="success")
        elif _id := request.form.get("ulozit_stav"):
            popis = request.form.get(_id)
            s = Suggestion.get_by_id(_id)
            s.state = popis
            s.update()
            flash("Záznam upraven", category="success")
        return redirect(url_for("admin_views.uprava_znamych_bugu"))
    

@admin_views.route("/logs_file", methods=["GET","POST"])
@require_role_system_name_on_current_user("editing_app_logs")
def logs_file():
    if request.method == "GET":
        return render_template("admin_logs_file.html")
    else:
        delete_app_logs()
        flash("Logy úspěšně smazány", category="success")
        return redirect(url_for("admin_views.admin_dashboard"))


@admin_views.route("/edit_users", methods=["GET","POST"])
def edit_users():
    if current_user.is_authenticated:
        if is_admin(current_user.email):
            if request.method == "GET":
                return render_template("admin_edit_users.html")
            else:
                result = request.form.get("result")
                folder_to_delete = user_data_folder_path() / result
                shutil.rmtree(folder_to_delete)
                User.query.get(int(result)).odstranit()
                flash("User smazán", category="success")
                return redirect(url_for("admin_views.admin_dashboard"))
    
    flash("Na tuto stránku nemáte přístup.", "error")
    return redirect(url_for("guest_views.home"))