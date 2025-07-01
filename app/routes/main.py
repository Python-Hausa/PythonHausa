from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
import markdown
from math import ceil
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
@main_bp.route("/home")
def index():
    from app.models import Event

    today = datetime.today().date()
    upcoming_events = (
        Event.query
        .filter(Event.end_date >= today)
        .order_by(Event.start_date.asc())
        .limit(3)
        .all()
    )
    return render_template("index.html", upcoming_events=upcoming_events)

@main_bp.route("/about")
def about():
    return render_template("about.html")

@main_bp.route("/learn")
def learn():
    return render_template("learn.html")

@main_bp.route("/events")
def events():
    from app.models import Event
    
    page = int(request.args.get("page", 1))
    per_page = 10

    all_events = Event.query.order_by(Event.start_date.desc()).all()

    active_events = [e for e in all_events if e.status != 'past']
    past_events = [e for e in all_events if e.status == 'past']
    sorted_events = active_events + past_events

    total_pages = ceil(len(sorted_events) / per_page)
    paginated = sorted_events[(page - 1) * per_page : page * per_page]

    return render_template("events.html", events=paginated, page=page, total_pages=total_pages)

@main_bp.route("/events/<int:event_id>")
def event_detail(event_id):
    from app.models import Event

    event = Event.query.get_or_404(event_id)
    event.description_html = markdown.markdown(event.description)
    return render_template("event_detail.html", event=event)


@main_bp.route("/blog")
def blog():
    return render_template("blog.html")

@main_bp.route("/contact", methods=['GET', 'POST'])
def contact():
    from app.models import ContactMessage

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form.get('subject', '')
        message = request.form['message']

        new_msg = ContactMessage(name=name, email=email, subject=subject, message=message)
        db.session.add(new_msg)
        db.session.commit()
        flash("Your message has been sent. Thank you!", "success")
        return redirect(url_for('main.contact'))

    return render_template("contact.html")

@main_bp.route("/conduct")
def conduct():
    return render_template("conduct.html")

@main_bp.route("/health")
def health():
    return render_template("health.html")

@main_bp.route("/donate")
def donate():
    return render_template("donate.html")
