from googletrans import Translator
import PyPDF2
from PyPDF2 import PdfFileWriter,PdfFileReader
from fpdf import FPDF 
import numpy as np

def translateWriteToPDF(fileName,transToLang):
	filePath = "filesToBeTranslated/"+fileName
	pdfFileObj = open(filePath, 'rb')
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

	testStr = ''
	# transToLang = 'hi'

	for i in range(pdfReader.numPages):
		pageObj = pdfReader.getPage(i)
		testStr = testStr + pageObj.extractText()
		# print(testStr)

	translator = Translator()
	test = testStr
	translator.translate(test)
	translated = translator.translate(test, dest=transToLang, encoding='utf-8')
	string01 = translated.origin
	string02 = translated.text
	print(string02)
	pdfFileObj.close()

	pdf = FPDF()
	pdf.add_page()
	if transToLang!='en':
		pdf.add_font('gargi', '', 'fonts/NotoSans-Regular.ttf', uni=True) 
	if transToLang=='en':
		pdf.add_font('gargi', '', 'fonts/NotoSans-Regular.ttf', uni=False) 
	pdf.set_font('gargi', '', 18)
	stringLength = len(string02.split())

	listStr = string02.split()
	print(listStr)
	tempStr = ''

	counter = 0
	index = 0
	maxLength = 50

	if transToLang=="hi":
		for i in range(len(listStr)):
			index = counter
			if(len(tempStr)<maxLength):
				tempStr = tempStr + listStr[i]+" "
			if(len(tempStr)>maxLength):
				# move to previous string
				tempStr.replace(listStr[index-1],'')
				# print(tempStr+"\n")
				i = i-1
				pdf.cell(w=0, h = 0, txt = tempStr, border = 0, ln = 0, align = 'L', fill = False, link = '')
				pdf.multi_cell(0,10,txt="\n",border=0,align='J',fill=False)
				tempStr = ''
			if(len(tempStr)==maxLength):
				pdf.cell(w=0, h = 0, txt = tempStr, border = 0, ln = 0, align = 'L', fill = False, link = '')
				pdf.multi_cell(0,10,txt="\n",border=0,align='J',fill=False)
				tempStr = ''
			counter = counter +1
		pdf.cell(w=0, h = 0, txt = tempStr, border = 0, ln = 0, align = 'L', fill = False, link = '')
		pdf.multi_cell(0,10,txt="\n",border=0,align='J',fill=False)
	# print(index,len(listStr))

	else:
		if transToLang=='en':
		# print(string02)
			pdf.write(12,string02)
		else:
			pdf.write(12,u''+string02)

	pdf.ln(0.5)
	pdf.output("translatedFiles/"+fileName+"_translated_"+transToLang+".pdf", 'F')
	pdf.close()
	return True