from flask import Flask,request,render_template
import numpy as np
import statistics as sc
import math

app = Flask(__name__)

def mean(data):
    n = len(data)
    result = sum(data) / n
    return result

def rls(n,Sxiyi,Sx,Sy,Sx2,Sy2,findY):
    r = ((n * Sxiyi) - (Sx * Sy)) / ((n * Sx2 - (Sx ** 2)) * (n * Sy2 - (Sy ** 2))) ** (1./2)
    b = ((n * Sxiyi) - (Sx * Sy)) / (n * Sx2 - (Sx ** 2))
    a = (Sy - b * Sx) / n
    result = a + b * findY
    return result,r

def sr(n,sigma):
    a = 1/n * sigma
    return a

def s(n,sigma):
    a = math.sqrt(1/n * sigma)
    return a

def sk(rerata,modus,sb):
    a = (rerata-modus)/sb
    return a

# home
@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

# mean modus median
@app.route("/mean-modus-median",methods=['GET','POST'])
def meanModeMedian():
    if request.method == "GET":
        return render_template('meanModeMedian.html')
    if request.method == "POST":
        inputValue = []
        inputData = request.form['data']
        inputValue += inputData.split(',')
        data = [eval(i) for i in inputValue]
        rata,median,mode = np.mean(data),np.median(data),sc.mode(data)
        return render_template('meanModeMedian.html',mean=rata,median=median,mode=mode,data=sorted(data))

# simpangan rata rata
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
        rerata = mean(datum)
        n = len(datum)
        for i in range(n):
            xixb += [abs(datum[i] - rerata)]
        sigma = sum(xixb)
        result = sr(n,sigma)
        return render_template('sr.html', n=n, sigma=sigma, result=result, datum=datum)

# simpangan baku
@app.route("/simpangan-baku", methods=['GET','POST'])
def simpanganBaku():
    if request.method == 'GET':
        return render_template('s.html')
    
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
        result = s(n,sigma)
        return render_template('s.html', n=n, sigma=sigma, result=result, datum=datum)

# ragam variasi
@app.route("/ragam-variasi", methods=['GET','POST'])
def ragamVariasi():
    if request.method == 'GET':
        return render_template('s2.html')
    
    if request.method == 'POST':
        datumSTR = []
        xixb = []

        if request.form['datum'] == "":
            return False
        else:
            data = request.form['datum']
            datumSTR += data.split(',')
            datum = [eval(i) for i in datumSTR]
            rerata = mean(datum)
            n = len(datum)
            for i in range(n):
                xixb += [(datum[i] - rerata) ** 2]
            sigma = sum(xixb)
            result = sr(n,sigma)

        return render_template('s2.html', n=n, sigma=sigma, result=result, datum=datum)

# ukuran kemiringan
@app.route("/ukuran-kemiringan",methods=['GET','POST'])
def ukuranKemiringan():
    if request.method == "GET":
        return render_template('sk.html')
    if request.method == 'POST':
        datumSTR = []
        xixb = []
        data = request.form['datum']
        datumSTR += data.split(',')
        datum = [eval(i) for i in datumSTR]
        n,rerata,modus = len(datum),np.mean(datum),sc.mode(datum)
        for i in range(n):
            xixb += [(datum[i] - rerata) ** 2]
        sigma = sum(xixb)
        sb = s(n,sigma)
        # jika rata2 lebih besar dari modus maka nilai cederung negatif
        # jika rata2 lebih kecil dari modus maka nilai cederung positif
        # jika rata2 sama dari modus maka nilai cederung simetris
        result = sk(2,1,2)
        finish = ""
        if result > 0:
            finish = "positif"
        elif result < 0:
            finish = "negatif"
        elif result == 0:
            finish = "simetris"
        return f"{finish}"

# regresi linier sederhana
@app.route("/regresi-linier-sederhana",methods=["GET","POST"])
def regresiLinierSederhana():
    if request.method == "GET":
        return render_template('rls.html')
    
    if request.method == "POST":
        castingX = []
        castingY = []
        x2 = []
        y2 = []
        xiyi = []

        dataX = request.form['dataX']
        dataY = request.form['dataY']
        findY = (int)(request.form['findY'])

        castingX += dataX.split(',')
        castingY += dataY.split(',')

        x = [eval(i) for i in castingX]
        y = [eval(i) for i in castingY]
        n = len(x)

        for i in range(n):
            x2 += [x[i] ** 2]
            y2 += [y[i] ** 2]
            xiyi += [x[i] * y[i]]

        Sx,Sy,Sx2,Sxiyi,Sy2 = sum(x),sum(y),sum(x2),sum(xiyi),sum(y2)
        result,r = rls(n,Sxiyi,Sx,Sy,Sx2,Sy2,findY)
        return render_template('rls.html',result=result,korelasi=r,dataX=x,dataY=y,n=n)

# progress regresi linier ganda
@app.route("/regresi-linier-ganda",methods=["GET","POST"])
def regresiLinierGanda():
    if request.method == "GET":
        return render_template('rlg.html')
    
    if request.method == "POST":
        castingX1 = []
        castingX2 = []
        x12 = []
        x22 = []
        castingY = []

        dataX1 = request.form['dataX1']
        dataX2 = request.form['dataX2']
        dataY = request.form['dataY']
        # preX1 = (int)(request.form['preX1'])
        # preX2 = (int)(request.form['preX2'])

        castingX1 += dataX1.split(',')
        castingX2 += dataX2.split(',')
        castingY += dataY.split(',')

        x1 = [eval(i)for i in castingX1]
        x2 = [eval(i)for i in castingX2]
        y = [eval(i)for i in castingY]

        for i in range(len(y)):
            x1y += [x1[i] * y[i]]
            x2y += [x2[i] * y[i]]
            x1x2 += [x1[i] * x2[i]]
            x12 += [x1[i] ** 2]
            x22 += [x2[i] ** 2]

        n = len(y)
        sx1,sx2,sx1y,sx2y,sx1x2,sx12,sx22 = sum(x1),sum(x2),sum(x1y),sum(x2y),sum(x1x2),sum(x12),sum(x22)
        return f"{sx1,sx2,sx1y,sx2y,sx1x2,sx12,sx22}"
        # return render_template('rlg.html')
        