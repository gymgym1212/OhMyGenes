from flask import  Flask,request,render_template
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
import math
import time
import os

app = Flask(__name__)


@app.route('/',methods = ['POST','GET'])
def omg():
    if request.method == 'POST':
        print("get file from the request.")
        file = request.files['file']
        print("try to..save file.")
        path = os.path.dirname(__file__)
        upload_path = os.path.join(path, 'static/upload', secure_filename(file.filename))
        file.save(upload_path)

        print("try to..check the validity of file")
        if check(upload_path)=='wrong':
            return '<h1>Wrong Format!</h1><p>the correct format should be like:<br>gene_id	ControlSample' \
                   '	KnockOutSample<br> AT1G01010	1.198558083	2.036161827<br> AT1G01020	13.75736234	13.370796<br>'

        return getResult(upload_path)
    return render_template('index.html')

def check(path):
    file = open(path)
    lines = file.readlines()
    for eachline in lines:
        if len(eachline.split()) != 3:
            return 'wrong'

def getResult(path):
    result = '<table><thead><th>gene_Id</th><th>control_Sample</th><th>treatment_Sample</th><th>log_2[FC]</th></thead><tbody>'
    file = open(path)
    lines = file.readlines()
    plt.xlabel('control_sample')
    plt.ylabel('treatment_sample')
    linenum = 0
    for eachline in lines:
        linenum += 1
        if linenum == 1 :continue
        splited = eachline.split()
        print(splited)
        gene_id = splited[0]
        if isfloat(splited[1]) == False or isfloat(splited[2]) == False:
            return '<h1>Wrong Format!</h1><h2>Not Number!</h2><p>the correct format should be like:<br>gene_id	ControlSample' \
                   '	KnockOutSample<br> AT1G01010	1.198558083	2.036161827<br> AT1G01020	13.75736234	13.370796<br>'
        control_sample = float(splited[1])
        treatment_sample = float(splited[2])

        if control_sample == treatment_sample:
            logFC = 0
        elif control_sample == 0:
            logFC = 'divided  by zero'
            color = 'black'
        else:
            logFC = math.log2(treatment_sample/control_sample)
            if logFC > 0:
                color = 'red'
            elif logFC == 0:
                color = 'yellow'
            else:
                color = 'blue'
        plt.scatter(control_sample,treatment_sample, c=color)

        result += '<tr><td>' + gene_id + \
                  '</td><td>' + str(control_sample) \
                  + '</td><td>' + str(treatment_sample) + \
                  '</td><td>' + str(logFC) +\
                  '</td></tr><br>'
#in memory of John D. Hunter
    pic_name = str(int(time.time() * 1000))
    plt.savefig('static/img/' + pic_name + '.png')
    result += '</tbody></table><br><img src="/static/img/' + pic_name + '.png">'+ '<a href="/">Back</a>'
    return result;

def isfloat(x):
    pointnum = 0
    for i in range(len(x)):
        if x[i] == '.':
            pointnum += 1
        elif x[i] <= '9' and x[i] >= '0' :
            pass
        else:
            return False
    if pointnum >1:
        return False
    return True


if __name__ == '__main__':
    app.run()