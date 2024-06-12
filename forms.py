from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired

class OrderForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired()])
    currency = StringField('Currency', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PaymentForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired()])
    currency = StringField('Currency', validators=[DataRequired()])
    submit = SubmitField('Submit')
