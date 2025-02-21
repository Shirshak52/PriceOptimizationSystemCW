from wtforms import FileField, SubmitField
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed


class FileUploadForm(FlaskForm):
    # File input field
    file = FileField(
        "Upload File",
        validators=[
            FileRequired("No file selected!"),
            FileAllowed(
                ["csv", "json", "sql", "xlsx", "xls"],
                "Only CSV, JSON, SQL, and Excel files are allowed!",
            ),
        ],
    )

    # Submit button
    submit = SubmitField("Upload")
