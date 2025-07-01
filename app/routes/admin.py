from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import AdminUser, ContactMessage, Event
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import markdown

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin login route
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = AdminUser.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['admin_logged_in'] = True
            session['admin_username'] = user.username
            session['admin_type'] = user.admin_type  # optional: used if you handle roles
            flash("Welcome, admin!", "success")
            return redirect(url_for('admin.dashboard'))
        else:
            flash("Invalid username or password.", "danger")

    return render_template('admin/login.html')

# Admin dashboard home
@admin_bp.route('/')
def dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    return render_template('admin/dashboard.html')

# Admin logout route
@admin_bp.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('admin.login'))

# Admins management page
@admin_bp.route('/admins')
def admins():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))

    if session.get('admin_type') != 'super':
        flash("You don't have permission to view this page.", "warning")
        return redirect(url_for('admin.dashboard'))

    admins = AdminUser.query.order_by(AdminUser.created_at.desc()).all()
    return render_template('admin/admins.html', admins=admins)

# Add new admin
@admin_bp.route('/add-admin', methods=['POST'])
def add_admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))

    if session.get('admin_type') != 'super':
        flash('Only super admins can add new admins.', 'danger')
        return redirect(url_for('admin.admins'))

    username = request.form['username']
    password = request.form['password']
    role = request.form.get('admin_type', 'middle')  # default to middle

    if AdminUser.query.filter_by(username=username).first():
        flash('Admin username already exists.', 'danger')
        return redirect(url_for('admin.admins'))

    new_admin = AdminUser(
        username=username,
        password_hash=generate_password_hash(password),
        admin_type=role,
        created_at=datetime.utcnow()
    )
    db.session.add(new_admin)
    db.session.commit()
    flash('New admin added successfully!', 'success')
    return redirect(url_for('admin.admins'))

# Delete admin
@admin_bp.route('/delete-admin/<int:admin_id>', methods=['POST'])
def delete_admin(admin_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    admin = AdminUser.query.get_or_404(admin_id)
    db.session.delete(admin)
    db.session.commit()
    flash('Admin deleted successfully.', 'info')
    return redirect(url_for('admin.admins'))

# Blog post management
@admin_bp.route('/manage-blog')
def manage_blog():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    return render_template('admin/manage_blog.html')

# Site statistics view
@admin_bp.route('/site-stats')
def site_stats():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    return render_template('admin/site_stats.html')

# Learning materials management
@admin_bp.route('/learning-materials')
def learning_materials():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    return render_template('admin/learning_materials.html')

# Events management
@admin_bp.route('/events', methods=['GET', 'POST'])
def manage_events():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))

    if request.method == 'POST':
        title = request.form['title']
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        description = request.form['description']

        if start_date > end_date:
            flash("End date cannot be earlier than start date.", "danger")
            return redirect(url_for('admin.manage_events'))

        new_event = Event(
            title=title,
            start_date=start_date,
            end_date=end_date,
            description=description
        )
        db.session.add(new_event)
        db.session.commit()
        flash("Event added successfully.", "success")
        return redirect(url_for('admin.manage_events'))

    events = Event.query.order_by(Event.start_date.desc()).all()
    return render_template('admin/events.html', events=events)

# Delete event
@admin_bp.route('/delete-event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash("Event deleted successfully.", "info")
    return redirect(url_for('admin.manage_events'))

# Edit event details
@admin_bp.route('/events/edit/<int:event_id>', methods=['POST'])
def edit_event(event_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))

    event = Event.query.get_or_404(event_id)
    event.title = request.form['title']
    event.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
    event.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
    event.description = request.form['description']

    db.session.commit()
    flash('Event updated successfully.', 'success')
    return redirect(url_for('admin.manage_events'))

# Contact messages management
@admin_bp.route('/messages')
def messages():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    msgs = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=msgs)

# Delete contact message
@admin_bp.route('/delete-message/<int:msg_id>', methods=['POST'])
def delete_message(msg_id):
    if not session.get('admin_logged_in'):
        flash("Login required to perform this action.", "danger")
        return redirect(url_for('admin.login'))

    message = ContactMessage.query.get_or_404(msg_id)
    db.session.delete(message)
    db.session.commit()
    flash("Message deleted successfully.", "info")
    return redirect(url_for('admin.messages'))