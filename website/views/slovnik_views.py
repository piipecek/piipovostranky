from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from website.helpers.require_role import require_role_system_name_on_current_user
from website.models.user import get_roles
from website.models.term import Term
from website.models.deck import Deck
from flask_login import current_user
from website.helpers.pretty_date import pretty_datetime
import json

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
        return render_template("slovnik/term_list.html", roles=get_roles())
    else:
        if request.form.get("new_term"):
            front = request.form.get("front")
            back = request.form.get("back")
            t = Term(front=front, back=back)
            t.update()
            flash("Slovo vytvořeno!", "success")
            return redirect(url_for("slovnik_views.terms"))
        else:
            return request.form.to_dict()
    
    
@slovnik_views.route("/term/<int:term_id>", methods=["GET", "POST"])
@require_role_system_name_on_current_user("user")
def term_detail(term_id):
    term = Term.get_by_id(term_id)
    if not term:
        flash("Slovo nenalezeno!", "error")
        return redirect(url_for("slovnik_views.terms"))
    if term.author_id != current_user.id:
        flash("Nemáte oprávnění zobrazit toto slovo!", "error")
        return redirect(url_for("slovnik_views.terms"))
    if request.method == "POST":
        if request.form.get("delete_term"):
            term.delete()
            flash("Slovíčko smazáno!", "info")
            return redirect(url_for("slovnik_views.terms"))
        else:
            return request.form.to_dict()
    return render_template("slovnik/term_detail.html", roles=get_roles(), data = term.for_detail())


@slovnik_views.route("/term_edit/<int:term_id>", methods=["GET", "POST"])
@require_role_system_name_on_current_user("user")
def term_edit(term_id):
    if request.method == "GET":
        term = Term.get_by_id(term_id)
        if not term:
            flash("Slovo nenalezeno!", "error")
            return redirect(url_for("slovnik_views.terms"))
        if term.author_id != current_user.id:
            flash("Nemáte oprávnění upravovat toto slovo!", "error")
            return redirect(url_for("slovnik_views.terms"))
        return render_template("slovnik/term_edit.html", roles=get_roles(), front=term.front, back=term.back)
    else:
        if request.form.get("update_term"):
            term = Term.get_by_id(term_id)
            term.front = request.form.get("front")
            term.back = request.form.get("back")
            term.update()
            flash("Slovo upraveno!", "success")
            return redirect(url_for("slovnik_views.term_detail", term_id=term_id))
        else:
            return request.form.to_dict()
    
    
@slovnik_views.route("/decks", methods=["GET", "POST"])
@require_role_system_name_on_current_user("user")
def decks():
    if request.method == "GET":
        return render_template("slovnik/deck_list.html", roles=get_roles())
    else:
        if request.form.get("new_deck"):
            name = request.form.get("new_deck_name")
            d = Deck(name=name)
            d.update()
            flash("Balíček vytvořen!", "success")
            return redirect(url_for("slovnik_views.deck_edit", deck_id=d.id))
        else:
            return request.form.to_dict()
        
        
@slovnik_views.route("/deck/<int:deck_id>", methods=["GET", "POST"])
@require_role_system_name_on_current_user("user")
def deck_detail(deck_id):
    deck = Deck.get_by_id(deck_id)
    if not deck:
        flash("Balíček nenalezen!", "error")
        return redirect(url_for("slovnik_views.decks"))
    if deck.author_id != current_user.id:
        flash("Nemáte oprávnění zobrazit tento balíček!", "error")
        return redirect(url_for("slovnik_views.decks"))
    if request.method == "POST":
        if request.form.get("delete_deck"):
            deck.delete()
            flash("Balíček smazán, slovíčka ponechána ve slovnníku.", "info")
            return redirect(url_for("slovnik_views.decks"))
        elif request.form.get("delete_deck_and_words"):
            deck.delete_and_words()
            flash("Balíček a slovíčka smazány!", "info")
            return redirect(url_for("slovnik_views.decks"))
        elif request.form.get("edit_deck"):
            return redirect(url_for("slovnik_views.deck_edit", deck_id=deck_id))
        elif request.form.get("start_quiz_1"):
            number_of_terms = request.form.get("number_of_terms")
            return redirect(url_for("slovnik_views.quiz", deck_id=deck_id, quiz_type=1, number_of_terms=number_of_terms))
        elif request.form.get("start_quiz_2"):
            number_of_terms = request.form.get("number_of_terms")
            return redirect(url_for("slovnik_views.quiz", deck_id=deck_id, quiz_type=2, number_of_terms=number_of_terms))
        else:
            return request.form.to_dict()
    return render_template("slovnik/deck_detail.html", roles=get_roles(), data = deck.for_detail())
        

@slovnik_views.route("/deck_edit/<int:deck_id>", methods=["GET", "POST"])
@require_role_system_name_on_current_user("user")
def deck_edit(deck_id):
    if request.method == "GET":
        deck = Deck.query.get(deck_id)
        if deck.author_id != current_user.id:
            flash("Nemáte oprávnění upravovat tento balíček!", "error")
            return redirect(url_for("slovnik_views.decks"))
        return render_template("slovnik/deck_edit.html", roles=get_roles(), deck_id = deck_id, deck_name=deck.name, deck_datetime=pretty_datetime(deck.datetime), deck_term_count=len(deck.terms))
    else:
        if data :=request.form.get("result"):
            data = json.loads(data) 
            name = data["deck_name"]
            
            deck = Deck.get_by_id(deck_id)
            deck.name = name
            
            for term in data["terms"]:
                if term["is_new"]:
                    t = Term(front=term["front"], back=term["back"])
                    t.update()
                    deck.terms.append(t)
                else:
                    t = Term.get_by_id(term["id"])
                    if t.author_id != current_user.id:
                        continue
                    t.front = term["front"]
                    t.back = term["back"]
                    t.update()
                    if t not in deck.terms:
                        deck.terms.append(t)
            deck.update()
            flash("Balíček upraven!", "success")
            return redirect(url_for("slovnik_views.deck_detail", deck_id=deck_id))
        else:
            return request.form.to_dict()
        
        
@slovnik_views.route("/quiz/<int:deck_id>/<int:quiz_type>/<int:number_of_terms>", methods=["GET", "POST"])
@require_role_system_name_on_current_user("user")
def quiz(deck_id, quiz_type, number_of_terms):
    if request.method == "GET":
        deck = Deck.get_by_id(deck_id)
        if not deck:
            flash("Balíček nenalezen!", "error")
            return redirect(url_for("slovnik_views.decks"))
        if deck.author_id != current_user.id:
            flash("Nemáte oprávnění zobrazit tento balíček!", "error")
            return redirect(url_for("slovnik_views.decks"))
        return render_template("slovnik/quiz.html", roles=get_roles(), deck_id=deck_id, quiz_type=quiz_type, number_of_terms=number_of_terms)
    else:
        if data := request.form.get("result"):
            data = json.loads(data)
            print(data)
            for ans_dict in data:
                term = Term.get_by_id(ans_dict["id"])
                if term.author_id != current_user.id:
                    continue
                term.times_tested += 1
                if ans_dict["correct"]:
                    term.times_correct += 1
                else:
                    # only recording wrong answers
                    term.add_answer(ans_dict["answer"])
                term.update()
            flash("Kvíz dokončen!", "success")
            return redirect(url_for("slovnik_views.deck_detail", deck_id=deck_id))
        else:
            return request.form.to_dict()
        
        
@slovnik_views.route("/export", methods=["GET", "POST"])
@require_role_system_name_on_current_user("user")
def export():
    if request.method == "GET":
        return render_template("slovnik/export.html", roles=get_roles())
    else:
        if request.form.get("import"):
            file = request.files.get("import_file")
            if not file:
                flash("Soubor se nepodařilo načíst!", "error")
                return redirect(url_for("slovnik_views.export"))
            result = Deck.import_from_xlsx(file)
            if result["success"]:
                flash(f"Import dokončen!", "success")
                return redirect(url_for("slovnik_views.deck_edit", deck_id=result["deck_id"]))
            else:
                flash(f"Při importu došlo k chybě: {result['error']}", "error")
                return redirect(url_for("slovnik_views.export"))
        elif request.form.get("pdf_export"):
            deck_id = request.form.get("pdf_deck")
            return redirect(url_for("slovnik_views.export_pdf", deck_id=deck_id))
        else:
            return request.form.to_dict()
        

@slovnik_views.route("/export_pdf/<int:deck_id>", methods=["GET"])
@require_role_system_name_on_current_user("user")
def export_pdf(deck_id):
    deck = Deck.get_by_id(deck_id)
    if not deck:
        flash("Balíček nenalezen!", "error")
        return redirect(url_for("slovnik_views.export"))
    if deck.author_id != current_user.id:
        flash("Nemáte oprávnění zobrazit tento balíček!", "error")
        return redirect(url_for("slovnik_views.export"))
    data = deck.for_pdf()
    return render_template("slovnik/deck_pdf.html", data=data)