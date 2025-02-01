from app import db
from app.models.Branch.model import Branch
from app.models.Branch.crud import BranchUserCrud
from werkzeug.security import check_password_hash


class LoginService:
    @staticmethod
    def verify_password(email, password):
        branch = BranchUserCrud.get_user_by_email(email)

        # Compare password
        if branch and check_password_hash(branch.password, password):
            return True

        return False
