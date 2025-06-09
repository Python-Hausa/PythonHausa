from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/about")
def about():
    return render_template("about.html")

@main_bp.route("/learn")
def learn():
    return render_template("learn.html")

@main_bp.route("/events")
def events():
    return render_template("events.html")

@main_bp.route("/blog")
def blog():
    return render_template("blog.html")

@main_bp.route("/contact")
def contact():
    return render_template("contact.html")
