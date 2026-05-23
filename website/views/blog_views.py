from flask import Blueprint, render_template
from website.models.user import get_roles


blog_views = Blueprint("blog_views",__name__, template_folder="blog")


@blog_views.route("/blog")
def blog():
    return render_template("blog/blog.html", roles=get_roles())


@blog_views.route("/expedice-banat-2026")
def expedice_banat_2026():
    return render_template("blog/expedice_banat_2026.html", roles=get_roles())