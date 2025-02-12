from flask_wtf import FlaskForm
from wtforms import SelectField, RadioField, IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange


class SegmentationParametersForm(FlaskForm):

    # Metric based on which to perform segmentation
    metric = SelectField(
        "On what basis do you want to group your customers?",
        choices=[
            ("total_visits", "Total Visits"),
            ("total_sales", "Total Sales"),
            ("total_qty", "Total Quantity"),
            ("avg_weekly_visits", "Average Weekly Visits"),
            ("avg_weekly_sales", "Average Weekly Sales"),
            ("avg_weekly_qty", "Average Weekly Quantity"),
            ("avg_monthly_visits", "Average Monthly Visits"),
            ("avg_monthly_sales", "Average Monthly Sales"),
            ("avg_monthly_qty", "Average Monthly Quantity"),
            ("avg_quarterly_visits", "Average Quarterly Visits"),
            ("avg_quarterly_sales", "Average Quarterly Sales"),
            ("avg_quarterly_qty", "Average Quarterly Quantity"),
        ],
        validators=[InputRequired()],
    )

    # Options for selecting number of groups
    number_choice = RadioField(
        "How many groups do you want to form?",
        choices=[("custom", "Custom"), ("auto", "Auto")],
        default="auto",
        validators=[InputRequired()],
    )

    # Number selection (only when selecting custom number of groups)
    number = IntegerField(
        "Select a Number",
        validators=[
            NumberRange(min=2, max=10),
        ],
        render_kw={"disabled": True},  # Initially disabled
    )

    # Submit button
    submit = SubmitField("OK")
