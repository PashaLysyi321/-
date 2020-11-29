from flask import Flask, redirect, url_for, request, session, render_template
from forms.forms import SignUpForm
from datetime import datetime
import numpy as np
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'project'

@app.route("/", methods = ['GET'])
def hello():
    return render_template('Page0.html')
    
@app.route('/registration', methods=["GET"])
def regis():
    return render_template('registration.html')

@app.route('/registration', methods=["POST"])
def regiss():
    gender = request.form['gender']
    married = request.form['married']
    dependents = request.form['dependents']
    education = request.form['education']
    employed = request.form['employed']
    Applicant_income = request.form['Applicant_income']
    Coapplicant_income = request.form['Coapplicant_income']
    LoanAmount = request.form['LoanAmount']
    Loan_Amount_Term = request.form['Loan_Amount_Term']
    History = request.form['History']
    Property_Area = request.form['Property_Area']
    user_data = [gender,married,dependents,education,employed,Applicant_income,Coapplicant_income,LoanAmount,Loan_Amount_Term,History,Property_Area]
    session['my_gender'] = gender
    session['my_married'] = married
    session['my_dependents'] = dependents
    session['my_education'] = education
    session['my_employed'] = employed
    session['my_Applicant_income'] = Applicant_income
    session['my_Coapplicant_income'] = Coapplicant_income
    session['my_LoanAmount'] = LoanAmount
    session['my_Loan_Amount_Term'] = Loan_Amount_Term
    session['my_History'] = History
    session['my_Property_Area'] = Property_Area
    return redirect(url_for('answerr'))

@app.route('/answer', methods=['GET', "POST"])
def answerr():
    my_gender = session.get('my_gender', None)
    my_married = session.get('my_married', None)
    my_dependents = session.get('my_dependents', None)
    my_education = session.get('my_education', None)
    my_employed = session.get('my_employed', None)
    my_Applicant_income = session.get('my_Applicant_income', None)
    my_Coapplicant_income = session.get('my_Coapplicant_income', None)
    my_LoanAmount = session.get('my_LoanAmount', None)
    my_Loan_Amount_Term = session.get('my_Loan_Amount_Term', None)
    my_History = session.get('my_History', None)
    my_Property_Area = session.get('my_Property_Area', None)

    import pandas as pd
    train_df = pd.read_csv('C:/Users/lysyi/Desktop/универ/бд/dbis/source/train_ctrUa4K.csv')
    train_df = train_df.drop(columns=['Loan_ID'])
    train_df_encoded = pd.get_dummies(train_df,columns=['Gender', 'Married', 'Dependents','Education','Self_Employed','Property_Area','Loan_Status'])
    X = train_df_encoded.drop(columns=['Loan_Status_Y','Loan_Status_N'])
    y = train_df_encoded['Loan_Status_Y']
    X = X.fillna(0)
    print(X.columns)
    from sklearn.linear_model import LogisticRegression
    
    logreg_clf = LogisticRegression(solver='liblinear')
    logreg_clf.fit(X,y)
    thresh = 0.5
    y_pred_test_thresh = logreg_clf.predict_proba(X)[:,1]
    y_pred = (y_pred_test_thresh > thresh).astype(int)
    print(y_pred)

    from sklearn.metrics import accuracy_score,f1_score
    print("Test Accuracy: ",accuracy_score(y.values,y_pred))
    print("Test F1 Score: ",f1_score(y.values,y_pred))

    train_df.loc[len(train_df)] = [my_gender,my_married,my_dependents,my_education,my_employed,my_Applicant_income,my_Coapplicant_income,my_LoanAmount,my_Loan_Amount_Term,my_History,my_Property_Area,'Y']
    train_df_encoded = pd.get_dummies(train_df,columns=['Gender', 'Married', 'Dependents','Education','Self_Employed','Property_Area','Loan_Status'])
    X = train_df_encoded.drop(columns=['Loan_Status_Y','Loan_Status_N'])
    X = X.fillna(0)
    print(X.columns)
    y_pred_test_thresh = logreg_clf.predict_proba(X)[:,1]
    y_pred = (y_pred_test_thresh > thresh).astype(int)
    print(y_pred)
    print(y_pred[-1])

    if y_pred[-1] == 1:
        param = 1
    else:
        param = 0
    return render_template('answer.html', param = param)   


@app.route('/description', methods=["GET"])
def description():
    return render_template('description.html')


if __name__ == "__main__":
        app.run(debug = True)