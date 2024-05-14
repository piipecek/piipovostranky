import json
from flask import Blueprint, request, make_response, redirect
from website.models.suggestion import Suggestion
from website.paths import gangy_path
from datetime import datetime
import io
import csv

guest_api = Blueprint("guest_api", __name__)

@guest_api.route("/suggestions")
def suggestions():
    return json.dumps([s.info_for_guest() for s in Suggestion.get_all()])


"""

Co všechno přibylo kvůli gangům:
- tento endpoint
- gangy_path
- gangy.json
- endpoint co vrací csv se sloupečky "cas", "jmeno", "email", "gang"
- endpoint co vrací počty lidí v gangu

"""

@guest_api.route("/novy_ucastnik_gangu", methods=["GET", "POST"])
def novy_ucastnik_gangu():
    with open(gangy_path()) as f:
        gangy = json.load(f)
    gangy.append(
        {
            "cas": datetime.now().isoformat(),
            "jmeno": request.form["jmeno"],
            "email": request.form["email"],
            "gang": request.form["gang"],
            "gang_2": request.form["gang_2"],
        }
    )
    with open(gangy_path(), "w") as f:
        json.dump(gangy, f, indent=4)
    return redirect("http://gangy.podsveti.cz?ulozeni=ok")

@guest_api.route("/gangy_csv")
def gangy_csv():
    with open(gangy_path()) as f:
        gangy_data = json.load(f)

    
    csv_data = [["cas", "jmeno", "email", "gang"]]
    for entry in gangy_data:
        csv_data.append([entry["cas"], entry["jmeno"], entry["email"], entry["gang"]])

    # Create a CSV string
    csv_string = io.StringIO()
    csv_writer = csv.writer(csv_string)
    csv_writer.writerows(csv_data)

    # Create a response with the CSV string
    response = make_response(csv_string.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=gangy.csv"
    response.headers["Content-type"] = "text/csv"

    return response

@guest_api.route("/pocet_lidi_v_gangu/<string:gang>", methods=["GET"])
def pocet_lidi_v_gangu(gang):
    with open(gangy_path()) as f:
        gangy_data = json.load(f)
    
    pocet_lidi = len([entry for entry in gangy_data if entry["gang"] == gang])

    return json.dumps({"count": pocet_lidi})