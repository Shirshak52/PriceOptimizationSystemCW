from app import db
from app.models.Branch.model import Branch


class BranchUserCrud:
    # READ
    @staticmethod
    def get_user_by_email(email):
        return Branch.query.filter_by(email=email).first()

    # UPDATE

    # DELETE
