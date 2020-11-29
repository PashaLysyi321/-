from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, DateTimeField

class SignUpForm(FlaskForm):
    
    user_name = StringField("user_name: ")
    married = StringField("married: ")  
    dependents = StringField("dependents: ")
    education = StringField("education: ")
    self_employed = PasswordField("self_employed: ")
    income = StringField("income: ")
    Coapplicant_income = StringField("Coapplicant_income: ")
    loan = StringField("loan: ")
    term_loan = StringField("term_loan: ")
    Credit_history = StringField("Credit_history: ")
    Urban = StringField("Urban: ")
    Loan_approved = StringField("Loan_approved: ")
    submit = SubmitField("OK")
