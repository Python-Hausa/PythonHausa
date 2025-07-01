from app import create_app, db
from app.models import AdminUser

app = create_app()
with app.app_context():
    db.create_all()
    admin = AdminUser(username="admin", password="admin123")
    db.session.add(admin)
    db.session.commit()


