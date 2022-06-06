from models.admin import Admin
from data.data import Sessions


def get_user_by_email(email: str):
    with Sessions() as session:
        return session.query(Admin).filter_by(email=email).first()
