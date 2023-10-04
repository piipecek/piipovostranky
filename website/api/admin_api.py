import json
from flask import Blueprint
from website.helpers.require_role import require_role_system_name_on_current_user
from website.logs import get_app_logs
from website.models.suggestion import Suggestion

admin_api = Blueprint("admin_api", __name__)


@admin_api.route("/app_logs")
@require_role_system_name_on_current_user("editing_app_logs")
def app_logs():
    return json.dumps(get_app_logs())

@admin_api.route("/suggestions")
@require_role_system_name_on_current_user("editing_suggestions")
def suggestions():
    return json.dumps([s.info_for_admin() for s in Suggestion.get_all()])