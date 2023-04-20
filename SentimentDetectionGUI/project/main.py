
import sys
import json
import ast
import time
import os
#input = sys.argv[1]



import subprocess



subprocess.check_call([sys.executable, "-m", "pip", "install", 'joblib'])
subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "scikit-learn"])
subprocess.check_call([sys.executable, "-m", "pip", "install", 'pandas'])
subprocess.check_call([sys.executable, "-m", "pip", "install", 'Flask'])
subprocess.check_call([sys.executable, "-m", "pip", "install", 'selenium'])
subprocess.check_call([sys.executable, "-m", "pip", "install", 'werkzeug'])
subprocess.check_call([sys.executable, "-m", "pip", "install", 'pywin32'])
subprocess.check_call([sys.executable, "-m", "pip", "install", 'plyer'])

from flask import Flask, render_template, request
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import *
import numpy as np
import webbrowser
import win32api
import win32com.client
import pythoncom
from plyer import notification


Folder = os.getcwd()

X_train = pd.read_csv("data/X_train.csv")
y_train = pd.read_csv("data/y_train.csv")
y_train = y_train['sentiment']
X_train = X_train.text
loaded_model = loaded_model = joblib.load("data/LinearSVC.joblib")

print("Please wait! Don't close the programe[0/1]")
vect = TfidfVectorizer(ngram_range=(1, 3)).fit(X_train)
print("Please wait! Don't close the programe[1/1]")
loaded_model.fit(vect.transform(X_train), y_train)
app = Flask(__name__, template_folder='')

def check_pos_neg(sentiment):
  if (sentiment == [1]):
    return "This is a negative review."
  else:
    return "This is a positive review."

@app.route('/')

def index():
    return render_template('./index.html')


@app.route('/ans', methods = ['POST'])
def ans():
    if request.method == 'POST':
        print(request.form)
        ls = list(request.form.lists())
        value = ls[0][1]
        result = loaded_model.predict(vect.transform(value))
        message = check_pos_neg(result)
        notification.notify(title = "RESULT", message = message, timeout = 10)
        result = win32api.MessageBox(None, message, "Result", 1)
        if result == 1:
            print('Ok')
        elif result == 2:
            print('cancel')
        print("result", message)
        return ('', 204)
    


if __name__ == '__main__':
    print("Please go to the website 127.0.0.1:5001")
    try:
       subprocess.check_call('explorer "http://127.0.0.1:5001"', shell=True)
    except:
       print("Done try Win")
    try:
       subprocess.check_call('open http://127.0.0.1:5001', shell=True)
    except:
       print("Done try Mac")
    app.run(
        host = '127.0.0.1',
        port = 5001,
        debug= False
    )


