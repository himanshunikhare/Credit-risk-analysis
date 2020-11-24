from flask import Flask, render_template, request, redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from _datetime import datetime
import pandas as pd
import numpy as np
from wtforms import Form, TextField,RadioField,SelectField,validators
from wtforms.fields.html5 import DecimalRangeField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db =SQLAlchemy(app)
data=pd.read_csv("./temp.csv")
#print(data.keys())
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class UserForm(Form):
    for i in data:
        # print(data[i])
        if data[i][0] == 'textbox':
            exec("%s=%s" % (i,'TextField(i,validators=[validators.required()], default="please add content")'))
        elif data[i][0] == 'radio':
            choice = list(data[i][1:].dropna().unique().tolist())
            # choice.remove('X')
            choiceStr=''
            for k in choice:
                choiceStr +="('"+k+"','"+k+"')," 
            print(choiceStr)
            exec("%s=%s" % (i,'RadioField(i,validators=[validators.required()],choices=[%s], default="%s")' %(choiceStr, choice[0])))

            pass
        elif data[i][0] == 'dropdown':
            choice = list(data[i][1:].dropna().unique().tolist())
            # choice.remove('X')
            choiceStr=''
            for k in choice:
                choiceStr +="('"+k+"','"+k+"')," 
            print(choiceStr)
            exec("%s=%s" % (i,'SelectField(i,validators=[validators.required()],choices=[%s])' %(choiceStr)))
            pass
        else:
            age = DecimalRangeField('Age',default=0)
            pass

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        formData = {}
        for i in request.form:
            formData[i] = request.form[i]
        print(formData)
        pass

    if form.validate():
        # Save the comment here.
        flash('Succesfully submitted')
        return render_template('result.html')
    else:
        flash('All the form fields are required. ')
    #if request.method == 'POST':
        #return redirect('/other-details')
    return render_template('index.html',values=data,form=form)

@app.route('/other-details', methods=['GET', 'POST'])
def otherdetails():
    if request.method == 'POST':
        return redirect('/result')
    return render_template('form2.html')

@app.route('/result')
def results():
    return render_template('result.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
