from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import current_user
from website.models.user import get_roles
from website.helpers.require_role import require_role_system_name_on_current_user, require_acga_ucitel_role_on_current_user
from website.models.evaluace import Evaluace
import json
from datetime import datetime, date
from google.oauth2 import id_token
from google.auth.transport import requests
from website.models.user import User
from website.paths import acga_students_xlsx_path
from acga.db_studentu import get_students_from_xlsx, get_classes, get_students_by_class
from website.models.krouzek import Krouzek
from website.models.role import Role
from website.helpers.pretty_date import pretty_datetime


acga_views = Blueprint("acga_views",__name__)


@acga_views.route("/")
@acga_views.route("/student_dashboard")
def student_dashboard():
    return render_template("acga/student_dashboard.html", roles=get_roles())


@acga_views.route("/teacher_dashboard")
def teacher_dashboard():
    return render_template("acga/teacher_dashboard.html", roles=get_roles(current_user))


@acga_views.route("/vazeny_prumer", methods=["GET"])
def vazeny_prumer():
    if request.method == "GET":
        return render_template("acga/vazeny_prumer.html", roles=get_roles())
    
    
@acga_views.route("/statistika_ctvrtletky")
def statistika_ctvrtletky():
    return render_template("acga/statistika_ctvrtletky.html", roles=get_roles(current_user))


@acga_views.route("/evaluace", methods=["GET","POST"])
def evaluace():
    if request.method == "GET":
        return render_template("acga/evaluace.html", roles=get_roles(current_user))
    else:
        if request.form.get("zadany_kod"):
            kod = request.form.get("kod").strip()
            if e := Evaluace.get_by_kod(kod):
                return redirect(url_for("acga_views.evaluace_formular", uuid=e.uuid))
            else:
                flash("Zadaný kód jsme nenašli. Pokud je to chyba na naší straně, dejte nám to vědět.", category="error")
                return redirect(url_for("acga_views.evaluace"))
        else:
            return request.form.to_dict()
        

@acga_views.route("/cist_evaluace", methods=["GET", "POST"])
@require_acga_ucitel_role_on_current_user()
def cist_evaluace():
    if request.method == "GET":
        return render_template("acga/cist_evaluace.html", roles=get_roles())
    else:
        if request.form.get("acga_jmeno_button"):
            jmeno = request.form.get("acga_jmeno")
            current_user.acga_jmeno = jmeno
            current_user.update()
            flash("Změna ACGA Jména proběhla v pořádku.", category="success")
            return redirect(url_for("acga_views.cist_evaluace_auth"))
        elif id := request.form.get("smazat_evaluaci"):
            e = Evaluace.get_by_id(id)
            e.delete()
            flash("Evaluace úspěšně smazána", category="success")
            return redirect(url_for("acga_views.cist_evaluace_auth"))
        elif id := request.form.get("detail"):
            e = Evaluace.get_by_id(id)
            return redirect(url_for("acga_views.evaluace_locked", uuid=e.uuid))
        elif date := request.form.get("smazat_starsi_nez"):
            date = datetime.fromisoformat(date)
            for e in current_user.evaluace:
                e: Evaluace
                if e.datetime_vytvoreni < date:
                    e.delete()
            flash("Starší formuláře promazány.", category="success")
            return redirect(url_for("acga_views.cist_evaluace_auth"))
        elif request.form.get("tisk_neodevzdane"):
            result = []
            for e in current_user.evaluace:
                e: Evaluace
                if not e.je_odevzdana:
                    result.append(e)
            if len(result) == 0:
                flash("Nejsou žádné neodevzdané evaluace k tisku.", category="error")
                return redirect(url_for("acga_views.cist_evaluace_auth"))
            else:
                result = Evaluace.vytvorit_kody_k_tisku(result)
                return render_template("acga/tisk_kodu.html", kody = result)
        elif request.form.get("pocet_kodu"):
            pocet = int(request.form.get("pocet_kodu"))
            result = Evaluace.vytvorit_evaluace(pocet)
            result = Evaluace.vytvorit_kody_k_tisku(result)
            return render_template("acga/tisk_kodu.html", kody = result)
        return request.form.to_dict()


@acga_views.route("evaluace/<string:uuid>", methods=["GET","POST"])
def evaluace_formular(uuid):
    e = Evaluace.get_by_uuid(uuid)
    if not e:
        flash("Tohle UUID neexistuje.", category="error")
        return redirect(url_for("acga_views.evaluace"))
    else:
        if request.method == "GET":
            if e.je_odevzdana:
                return redirect(url_for("acga_views.evaluace_locked", uuid=uuid))
            else:
                return render_template("acga/evaluace_formular.html", uuid=uuid, name=Evaluace.get_by_uuid(uuid).ucitel.acga_jmeno)
        else:
            data = json.loads(request.form.get("result"))
            akce = data.get("akce")
            if akce == "ulozit": 
                e = Evaluace.get_by_uuid(uuid)
                e.ulozit_nova_data(data)
                flash("Vaše odpovědi byly uloženy.", category="success")
                return redirect(url_for("acga_views.evaluace_formular", uuid = uuid))
            elif akce == "odevzdat":
                e = Evaluace.get_by_uuid(uuid)
                e.ulozit_nova_data(data)
                e.oznacit_za_odevzdane()
                flash("Vaše odpovědi byly odevzdány, děkujeme.", category="success")
                return redirect(url_for("acga_views.evaluace_formular", uuid = uuid))
            return request.form.to_dict()
        

@acga_views.route("evaluace_locked/<string:uuid>")
def evaluace_locked(uuid):
    if not Evaluace.get_by_uuid(uuid):
        flash("Tohle UUID neexistuje.", category="error")
        return redirect(url_for("acga_views.evaluace"))
    else:
        e = Evaluace.get_by_uuid(uuid)
        if request.method == "GET":
            if e.je_odevzdana:
                return render_template("acga/evaluace_locked.html", uuid=uuid)
            else:
                return redirect(url_for("acga_views.evaluace_formular", uuid=uuid))
        else:
            return request.form.to_dict()


@acga_views.route("/evaluace_statistiky")
@require_acga_ucitel_role_on_current_user()
def evaluace_statistiky():
    return render_template("acga/evaluace_statistiky.html", roles=get_roles())


@acga_views.route("/astrofyzika")
def astrofyzika():
    return render_template("acga/astrofyzika.html", roles=get_roles())


@acga_views.route("/google_auth_receiver_acga_student", methods=["POST"])
def google_auth_receiver_acga_student():
    token = request.form.get("credential")
    idinfo = id_token.verify_oauth2_token(token, requests.Request(), current_app.config["GOOGLE_CLIENT_ID"], clock_skew_in_seconds=2)
    User.manage_google_login(idinfo)
    return redirect(url_for("acga_views.student_dashboard"))


@acga_views.route("/google_auth_receiver_acga_teacher", methods=["POST"])
def google_auth_receiver_acga_teacher():
    token = request.form.get("credential")
    idinfo = id_token.verify_oauth2_token(token, requests.Request(), current_app.config["GOOGLE_CLIENT_ID"], clock_skew_in_seconds=2)
    User.manage_google_login(idinfo)
    return redirect(url_for("acga_views.teacher_dashboard"))



@acga_views.route("/krouzky", methods=["GET", "POST"])
def krouzky():
    if request.method == "GET":
        if current_user.is_authenticated:
            if current_user.organizace == "acga.cz":
                return render_template("acga/krouzky.html", roles=get_roles(current_user))
            else:
                return render_template("acga/krouzky_mimo_acga.html", roles=get_roles(current_user))
        else:
            return render_template("acga/krouzky_student_login.html", roles=get_roles(), site_url=current_app.config["SITE_URL"])
    else:
        if request.form.get("save"):
            krouzky_ids = [int(id) for id in request.form.getlist("krouzky")]
            Krouzek.manage_incoming_zapis(krouzky_ids)
            flash("Kroužky byly úspěšně uloženy.", category="success")
            return redirect(url_for("acga_views.krouzky"))
        else:
            return request.form.to_dict()
        

# sem směřuje ten decorator require_acga_ucitel_role_on_current_user
@acga_views.route("/krouzky_bez_role_ucitele")
def krouzky_bez_role_ucitele():
    return render_template("acga/krouzky_bez_role_ucitele.html", roles=get_roles(current_user))


# sem smxěřuje ten decorator require_acga_ucitel_role_on_current_user
@acga_views.route("/teacher_login")
def teacher_login():
    return render_template("acga/teacher_login.html", roles=get_roles(), site_url=current_app.config["SITE_URL"])


@acga_views.route("/sprava_krouzku", methods=["GET", "POST"])
@require_acga_ucitel_role_on_current_user()
def sprava_krouzku():
    if request.method == "GET":
        return render_template("acga/sprava_krouzku.html", roles=get_roles(current_user), krouzky=Krouzek.get_all_for_seznam())
    else:
        if request.form.get("novy_krouzek"):
            if name := request.form.get("nazev_krouzku"):
                krouzek = Krouzek(name=name)
                krouzek.update()
                flash("Kroužek byl úspěšně vytvořen.", category="success")
            else:
                flash("Kroužek musí mít název.", category="error")
            return redirect(url_for("acga_views.sprava_krouzku"))
        elif request.form.get("delete_all"):
            for k in Krouzek.get_all():
                k.delete()
            flash("Všechny kroužky byly úspěšně smazány.", category="success")
            return redirect(url_for("acga_views.sprava_krouzku"))
        return request.form.to_dict()


@acga_views.route("/zobrazit_studenty", methods=["GET", "POST"])
@require_acga_ucitel_role_on_current_user()
def zobrazit_studenty():
    if request.method == "GET":
        return render_template("acga/zobrazit_studenty.html", students_uploaded = acga_students_xlsx_path().exists(), students=get_students_from_xlsx(), roles=get_roles(current_user))
    else:
        if request.form.get("submit_students"):
            students_xlsx = request.files.get("import_file_input")
            if students_xlsx:
                students_xlsx.save(acga_students_xlsx_path())
                flash("Data byla úspěšně nahrána.", category="success")
            else:
                flash("Nepodařilo se nahrát data.", category="error")
            return redirect(url_for("acga_views.zobrazit_studenty"))
        

@acga_views.route("/detail_krouzku/<int:id>", methods=["GET", "POST"])
@require_acga_ucitel_role_on_current_user()
def detail_krouzku(id):
    krouzek = Krouzek.get_by_id(id)
    if request.method == "GET":
        if not krouzek:
            flash("Kroužek nebyl nalezen.", category="error")
            return redirect(url_for("acga_views.sprava_krouzku"))
        return render_template("acga/detail_krouzku.html", id=id, roles=get_roles(current_user))
    else:
        if request.form.get("ulozit_krouzek"):
            krouzek.name = request.form.get("nazev_krouzku")
            krouzek.description = request.form.get("popis_krouzku")
            krouzek.update()
            return redirect(url_for("acga_views.detail_krouzku", id=id))
        if request.form.get("pridat_studenta"):
            email = request.form.get("manual_email").strip()
            if not email:
                flash("Musíte napsat nějaký e-mail.", category="error")
                return redirect(url_for("acga_views.detail_krouzku", id=id))
            emails = json.loads(krouzek.enrolled_emails)
            if email  in [e["email"] for e in emails]:
                flash("Tento e-mail je již zapsaný.", category="error")
            else:
                emails.append({
                    "email": email,
                    "timestamp": pretty_datetime(datetime.now())
                })
                krouzek.enrolled_emails = json.dumps(emails)
                krouzek.update()
                flash("Student byl úspěšně přidán.", category="success")
            return redirect(url_for("acga_views.detail_krouzku", id=id))
        if request.form.get("delete"):
            email = request.form.get("delete")
            emails = json.loads(krouzek.enrolled_emails)
            if email in [e["email"] for e in emails]:
                emails.remove(next(e for e in emails if e["email"] == email))
                krouzek.enrolled_emails = json.dumps(emails)
                krouzek.update()
                flash("Student byl úspěšně odstraněn.", category="success")
            else:
                flash("Tento e-mail není zapsaný.", category="error")
            return redirect(url_for("acga_views.detail_krouzku", id=id))
        if request.form.get("delete_identifier"):
            if request.form.get("delete_identifier") == "all":
                krouzek.enrolled_emails = json.dumps([])
                krouzek.update()
                flash("Všichni studenti byli úspěšně odebráni.", category="success")
                return redirect(url_for("acga_views.detail_krouzku", id=id))
            elif request.form.get("delete_identifier") == "krouzek":
                krouzek.delete()
                flash("Kroužek byl úspěšně smazán.", category="success")
                return redirect(url_for("acga_views.sprava_krouzku"))
        else:
            return request.form.to_dict()
        

@acga_views.route("/jmenne_seznamy", methods=["GET", "POST"])
@require_acga_ucitel_role_on_current_user()
def jmenne_seznamy():
    if request.method == "GET":
        return render_template("acga/jmenne_seznamy.html", roles=get_roles(current_user), classes = get_classes())
    else:
        return redirect(url_for("acga_views.jmenny_seznam", class_name=request.form.get("trida")))
    

@acga_views.route("/jmenny_seznam/<class_name>", methods=["GET"])
@require_acga_ucitel_role_on_current_user()
def jmenny_seznam(class_name):
    students = get_students_by_class(class_name)
    return render_template("acga/jmenny_sezam.html", roles=get_roles(current_user), class_name=class_name, students=students)


@acga_views.route("/get_students_for_jmenny_seznam/<class_name>", methods=["GET"])
@require_acga_ucitel_role_on_current_user()
def get_students_for_jmenny_seznam(class_name):
    students = get_students_by_class(class_name)
    return json.dumps(students)
