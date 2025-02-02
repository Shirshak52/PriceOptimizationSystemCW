from app import db
from app.models.Branch.model import Branch
from werkzeug.security import check_password_hash, generate_password_hash


class BranchUserCrud:
    # READ
    @staticmethod
    def get_user_by_email(email):
        return Branch.query.filter_by(email=email).first()

    @staticmethod
    def check_password(user, password):
        return check_password_hash(user.password, password)

    # UPDATE
    @staticmethod
    def set_password(user, password):
        user.password = generate_password_hash(password, method="sha256")
