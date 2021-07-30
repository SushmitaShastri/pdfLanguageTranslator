from flask import Flask, render_template, request
from pdfminerCode import *
app = Flask(__name__)

@app.route('/')
def student():
   return render_template('selectLanguage.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      # result = request.form
      transToLang = request.form['transToLang']
      filePath = request.form['fileToTranslate']
      success = translateWriteWithFormatToPDF(filePath,transToLang)
      return render_template("selectLanguage.html",succcessFlag='Translated Succesfully!',fileName = filePath+"_translated_"+transToLang+".pdf")

if __name__ == '__main__':
   app.run(debug = True)