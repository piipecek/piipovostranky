from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from website.models.user import User
from website.models.role import Role
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, current_user
from website.mail_handler import mail_sender
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os
import requests


auth_views = Blueprint("auth_views",__name__, template_folder="auth")

# helper pro registrační endpoint
def validate_turnstile(token, secret, remoteip=None):
    url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'

    data = {
        'secret': secret,
        'response': token
    }

    if remoteip:
        data['remoteip'] = remoteip

    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Turnstile validation error: {e}")
        return {'success': False, 'error-codes': ['internal-error']}


@auth_views.route("/login", methods=["GET","POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("guest_views.dashboard"))
	if request.method == "GET":
		return render_template("auth/auth_login.html", site_url=current_app.config["SITE_URL"])
	else:
		email = request.form.get("email")
		password = request.form.get("password")
		if len(email) > 100:
			flash("Zadaný e-mail byl určitě přiliš dlouhý.", category="error")
			return redirect(url_for("auth_views.login"))
		if len(password) > 300:    
			flash("Zadané heslo bylo určitě příliš dlouhé.", category="error")
			return redirect(url_for("auth_views.login"))
		user = User.get_by_email(email=email)
		try:
			if user and check_password_hash(user.password, password):
				user.login()
				flash("úspěšné přihlášení", category="success")
				return redirect(url_for("guest_views.dashboard"))
			else:
				flash("E-mail nebo heslo byly špatně", category="error")
			return redirect(url_for("auth_views.login"))
		except ValueError:
			flash("Vaše heslo bylo zastaralé, prosíme, nastavte si nové heslo pomocí odkazu pro obnovu hesla.", category="error")
			return redirect(url_for("auth_views.request_reset"))


@auth_views.route("/register", methods=["GET","POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for("guest_views.dashboard"))
	if request.method == "GET":
		cloudflare_site_key = os.environ.get("CLOUDFLARE_SITE_KEY")
		return render_template("auth/auth_register.html", site_url=current_app.config["SITE_URL"], cloudflare_site_key=cloudflare_site_key)
	else:
		token = request.form.get("cf-turnstile-response")
		secret = os.environ.get("CLOUDFLARE_SECRET_KEY")
		validation_result = validate_turnstile(token, secret)
  
		if not validation_result.get("success"):
			flash("Ověření Turnstile selhalo. Prosím zkuste to znovu.", category="error")
			return redirect(url_for("auth_views.register"))

		email = request.form.get("email")
		password = request.form.get("password")

		user = User.get_by_email(email=email)
		if user:
			flash("Tento email je už zaregistrovaný. Použij prosím jiný", category="error")
			return redirect(url_for("auth_views.register"))
		else:
			new_user = User(email=email, password=generate_password_hash(password, method="scrypt"))
			new_user.roles.append(Role.get_by_system_name("user"))
			new_user.update()
			new_user.login()
			mail_sender(mail_identifier = "potvrzeni_emailu", target = new_user.email, data=new_user.get_reset_token())
			flash("Úspěšná registrace.", category="success")
			return redirect(url_for("guest_views.dashboard"))

@auth_views.route("/logout")
@login_required
def logout():
	logout_user()
	flash("Odhlášení proběhlo úspěšně.", category="info")
	return redirect(url_for("guest_views.dashboard"))


@auth_views.route("/reset_password", methods=["GET","POST"])
def request_reset():
	if current_user.is_authenticated:
		return redirect(url_for("guest_views.home"))
	if request.method == "GET":
		return render_template("auth/auth_request_reset.html")
	else:
		email = request.form.get("email")
		if len(email) > 100:
			flash("Zadaný e-mail byl určitě moc dlouhý.", category="error")
			return redirect(url_for("auth_views.request_reset"))
		user = User.get_by_email(email=email)
		if user:
			mail_sender(mail_identifier="reset_password", target=email, data=user.get_reset_token())
		flash("Pokud existuje uživatel s tímto e-mailem, byl mu odeslán ověřovací e-mail.", category="info")
		return redirect(url_for("auth_views.login"))


@auth_views.route("/reset_password/<token>", methods=["GET","POST"])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for("guest_views.home"))
	user = User.verify_reset_token(token)
	if user is None:
		flash("Obnovovací link vypršel, nebo je jinak neplatný.", category="info")
		return redirect(url_for("auth_views.request_reset"))
	if request.method == "GET":
		return render_template("auth/auth_reset_password.html")
	else:
		user.password = generate_password_hash(request.form.get("password"), method="scrypt")
		user.update()
		flash("Heslo změněno, můžete se nyní přihlásit:", category="info")
		return redirect(url_for("auth_views.login"))


@auth_views.route("/google_auth_receiver", methods=["POST"])
def google_auth_receiver():
    token = request.form.get("credential")
    idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), current_app.config["GOOGLE_CLIENT_ID"], clock_skew_in_seconds=2)
    User.manage_google_login(idinfo)
    return redirect(url_for("guest_views.dashboard"))


