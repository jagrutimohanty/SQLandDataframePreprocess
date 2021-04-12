#reference link https://www.askpython.com/python-modules/flask/flask-crud-application
#data reference https://www.kaggle.com/ajaypalsinghlo/world-happiness-report-2021?select=world-happiness-report-2021.csv
#https://stackoverflow.com/questions/51356402/how-to-upload-excel-or-csv-file-to-flask-as-a-pandas-data-frame/51361162

import flask
import os
import os.path
from os import path
from flask import Flask,render_template,request,redirect,flash
from models import db
from werkzeug.utils import secure_filename
import pandas as pd
import urllib.request
import sys
import pandas.io.formats.style

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import sqlite3 as sql
import pandas as pd
import shutil


from sqlalchemy import create_engine

sql_engine = create_engine('sqlite:///happy.db', echo=False)
connection = sql_engine.raw_connection()



app = Flask(__name__)
UPLOAD_FOLDER = '/Users/jagrutimohanty/HAPPINESS-APP/FILE-UPLOAD' 
app.secret_key = "jmjm"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.run(host='localhost', port=5000)
ALLOWED_EXTENSIONS = set(['csv', 'pdf', 'xls', 'txt'])
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
#reference https://tutorial101.blogspot.com/2020/02/python-flask-multiple-files-upload.html

@app.route('/')
def homepage():
    return render_template('home.html')

 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

 
@app.before_first_request
def create_table():
    db.create_all()

  


@app.route('/upload', methods=['GET','POST'])
def upload():  
    return render_template("upload.html" ,name=" ")  


fnamelist = []
@app.route('/success', methods = ['GET','POST'])  
def success():  
    if request.method == 'POST': 
               # check if the post request has the files part
        if 'files[]' not in request.files:
         flash('No file part')
         return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
          if file and allowed_file(file.filename):
            
                filename = secure_filename(file.filename)
                fnamelist.append(filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('File(s) successfully uploaded')
        return render_template("success.html" ,name=fnamelist)
    if request.method == 'GET': 
        if (not path.exists(file.filename)):   
           return render_template("success.html" ,name=fnamelist)  
    


@app.route('/display/<string:fname>' , methods = ['GET','POST'])
def display(fname):
    
        df3= pd.read_csv(UPLOAD_FOLDER+"/"+fname) 
        html = df3.head(2).to_html(header="true", table_id="table")
        shape = df3.shape
        with open('/Users/jagrutimohanty/HAPPINESS-APP/templates/backbutton.html','r') as firstfile, open('/Users/jagrutimohanty/HAPPINESS-APP/templates/displaydf.html','w') as secondfile:
                secondfile.truncate()
                secondfile.write(html)
             # read content from first file
                for line in firstfile:     
             # write content to second file
                           secondfile.write(line)                
                firstfile.close()
                secondfile.close()
        return render_template("displaydf.html" , shape=shape)



@app.route('/displayall' , methods = ['GET','POST'])
def displayall():
        name = os.listdir('/Users/jagrutimohanty/HAPPINESS-APP/FILE-UPLOAD/')
        return render_template("displaydflinks.html" ,name=name)  
  

### Code to list two dataframes and show the common elements 
#https://stackoverflow.com/questions/47704441/applying-styling-to-pandas-dataframe-saved-to-html-file

#####################


##Common Columns

@app.route('/commoncols/')
def common_cols():
    df1 = pd.read_csv(UPLOAD_FOLDER+"/"+'world-happiness-report-2021.csv')
    df2 = pd.read_csv(UPLOAD_FOLDER+"/"+'world-happiness-report.csv')
    com_col = common_columns(df1,df2)
    if com_col:
        return render_template('commoncol.html', common_columns  = com_col , df1_col = list(df1.columns)  ,df2_col = list(df2.columns))
    return f"Common Columns Does not exist"

def common_columns(df1,df2):
    common_columns = list(set(list(df1.columns) + list(df2.columns)))
    if common_columns:
        return common_columns
    return False

#####


@app.route('/createtablefromdf/')
def createtablefromdf():
    report21_df = pd.read_csv("/Users/jagrutimohanty/HAPPINESS-APP/FILE-UPLOAD"+"/"+"world-happiness-report-2021.csv")
    arr = list(report21_df.columns)
    sql_report_df = report21_df[arr[0:5]]
    sqlite_table = "report21dftosql"
    sql_report_df.to_sql(sqlite_table, sql_engine.raw_connection(), if_exists='replace')
    html = sql_report_df.head(2).to_html(header="true", table_id="table")
    shape = sql_report_df.shape
    with open('/Users/jagrutimohanty/HAPPINESS-APP/templates/shape.html','r') as firstfile, open('/Users/jagrutimohanty/HAPPINESS-APP/templates/displaydf.html','w') as secondfile:
                secondfile.truncate()
                secondfile.write(html)
             # read content from first file
                for line in firstfile:     
             # write content to second file
                           secondfile.write(line)
                
                firstfile.close()
                secondfile.close()

   # return render_template("displaydf.html")
    if(not sql_report_df.empty):
        operation = "Creation of Table from Dataframe is" 
        return render_template("displaydf.html" , shape=shape ,operation = operation)
    abort(404)
         

@app.route('/createdffromsql/')
def createdffromsql():
    report21_df = pd.read_csv("/Users/jagrutimohanty/HAPPINESS-APP/FILE-UPLOAD"+"/"+"world-happiness-report-2021.csv")
    arr = list(report21_df.columns)
    sql_report_df = report21_df[arr[0:5]]
    sql_torepor21_df = pd.read_sql_query("SELECT * from report21dftosql",sql_engine.raw_connection())

    html = sql_torepor21_df.head(2).to_html(header="true", table_id="table")
    shape = sql_torepor21_df.shape
    operation = "Creation of  Dataframe from SQL Table is"
    with open('/Users/jagrutimohanty/HAPPINESS-APP/templates/shape.html','r') as firstfile, open('/Users/jagrutimohanty/HAPPINESS-APP/templates/displaydf.html','w') as secondfile:
                secondfile.truncate()
                secondfile.write(html)
             # read content from first file
                for line in firstfile:     
             # write content to second file
                           secondfile.write(line)
                
                firstfile.close()
                secondfile.close()

   # return render_template("displaydf.html")
    if(not sql_report_df.empty):
        operation = "Creation of  Dataframe from SQL Table is"
        return render_template("displaydf.html" , shape=shape ,operation =  operation)
    abort(404)




###percentile

def quantile_disp(df,n :int):
    if(n<0 or n>100):
      return "Invalid Selection"
    else: 
       quan = n/100
       res_df = df.quantile([ quan], axis = 0)
       return res_df

@app.route('/quantilepercentile' , methods = ['GET','POST'])
def quantilepercentile():
    
    report21_df = pd.read_csv("/Users/jagrutimohanty/HAPPINESS-APP/FILE-UPLOAD"+"/"+"world-happiness-report-2021.csv")
    if request.method == 'POST':
       inp = request.form['inputnum']
       res_df = quantile_disp(report21_df,int(inp))
       return res_df.to_html(header="true", table_id="table")
    
    return render_template('percentileinput.html')



#https://www.askpython.com/python-modules/flask/flask-forms
#https://stackoverflow.com/questions/52644035/how-to-show-a-pandas-dataframe-into-a-existing-flask-html-table
#     

 
