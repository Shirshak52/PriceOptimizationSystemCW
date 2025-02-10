from flask_wtf import FlaskForm
from wtforms import SelectField, RadioField, IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange


class SegmentationParametersForm(FlaskForm):

    # Metric based on which to perform segmentation
    metric = SelectField(
        "Select a Metric",
        choices=[
            ("option1", "Option 1"),
            ("option2", "Option 2"),
            ("option3", "Option 3"),
        ],
        validators=[InputRequired()],
    )

    # Options for selecting number of groups
    number_choice = RadioField(
        "Select Option",
        choices=[("select_number", "Select a Number"), ("auto", "Auto")],
        default="auto",
        validators=[InputRequired()],
    )

    # Number selection (only when selecting custom number of groups)
    number = IntegerField(
        "Pick a Number",
        validators=[NumberRange(min=2, max=10)],
        render_kw={"disabled": True},  # Initially disabled
    )

    # Submit button
    submit = SubmitField("OK")
