import os
from flask import current_app, redirect, flash, request, url_for
from flask_login import login_user

# from app import db
# from app.models.Branch.model import Branch
# from app.models.Branch.crud import BranchUserCrud


class DatasetFileService:
    @staticmethod
    def validate_datasetfile(file):
        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        flash("File uploaded successfully!", "success")
        return True  # Return True to indicate success
