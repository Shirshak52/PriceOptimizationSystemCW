from wtforms import SelectField, RadioField, SubmitField
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm


class SegmentationParametersForm(FlaskForm):

    # Metric based on which to perform segmentation
    metric = SelectField(
        "On what basis do you want to group your customers?",
        choices=[
            ("Total Visits", "Total Visits"),
            ("Total Sales", "Total Sales"),
            ("Total Quantity", "Total Quantity"),
            ("Average Weekly Visits", "Average Weekly Visits"),
            ("Average Weekly Sales", "Average Weekly Sales"),
            ("Average Weekly Quantity", "Average Weekly Quantity"),
            ("Average Monthly Visits", "Average Monthly Visits"),
            ("Average Monthly Sales", "Average Monthly Sales"),
            ("Average Monthly Quantity", "Average Monthly Quantity"),
            ("Average Quarterly Visits", "Average Quarterly Visits"),
            ("Average Quarterly Sales", "Average Quarterly Sales"),
            ("Average Quarterly Quantity", "Average Quarterly Quantity"),
        ],
        validators=[InputRequired()],
    )

    # Options for selecting number of groups
    number_choice = RadioField(
        "How many groups do you want to form?",
        choices=[
            ("auto", "Auto"),
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5"),
            (6, "6"),
            (7, "7"),
            (8, "8"),
            (9, "9"),
            (10, "10"),
        ],
        default="auto",
        validators=[InputRequired()],
    )

    # Submit button
    submit = SubmitField("OK")
