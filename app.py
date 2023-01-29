from flask import Flask,request,render_template
import numpy as np

app = Flask(__name__)

def sr(n,sigma):
    a = 1/n * sigma
    return a

@app.route('/',methods=['GET'])
def home():
    return render_template('home.html')

@app.route("/simpangan-rerata", methods=['GET','POST'])
def simpanganRerata():
    if request.method == 'GET':
        return render_template('sr.html')
    
    if request.method == 'POST':
        datumSTR = []
        xixb = []
        data = request.form['datum']
        datumSTR += data.split(',')
        datum = [eval(i) for i in datumSTR]
        rerata = np.mean(datum)
        n = len(datum)
        for i in range(n):
            xixb += [abs(datum[i] - rerata)]
        sigma = sum(xixb)
        result = sr(n,sigma)
        return render_template('sr.html', n=n, sigma=sigma, result=result, datum=datum)

@app.route("/ragam-variasi", methods=['GET','POST'])
def ragamVariasi():
    if request.method == 'GET':
        return render_template('s2.html')
    
    if request.method == 'POST':
        datumSTR = []
        xixb = []
        data = request.form['datum']
        datumSTR += data.split(',')
        datum = [eval(i) for i in datumSTR]
        rerata = np.mean(datum)
        n = len(datum)
        for i in range(n):
            xixb += [(datum[i] - rerata) ** 2]
        sigma = sum(xixb)
        result = sr(n,sigma)
        return render_template('s2.html', n=n, sigma=sigma, result=result, datum=datum)

if __name__ == '__main__':
	app.run(debug=1)