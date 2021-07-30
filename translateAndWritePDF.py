import PyPDF4
import re
import io
from googletrans import Translator
from fpdf import FPDF 
import numpy as np

def translateAndWriteToPDF(fileName,transToLang):
	# reading pdf file
	filePath = "filesToBeTranslated/"+fileName
	pdfFileObj = open(r''+filePath, 'rb')
	pdfReader = PyPDF4.PdfFileReader(pdfFileObj)

	# for writing pdf file
	pdf = FPDF()
	translator = Translator()
	toBeTranslatedStr  = ''

	for i in range(pdfReader.numPages):
		print(i)
		pageObj = pdfReader.getPage(i)
		pages_text = pageObj.extractText()

		# for writing
		pdf.add_page()
		pdf.add_font('gargi', '', 'fonts/NotoSans-Regular.ttf', uni=True) 
		pdf.set_font('gargi', '', 9)

		for line in pages_text.split('\n'):
			# print(line)
			# toBeTranslatedStr = toBeTranslatedStr + line+"\n"
			translated = translator.translate(line, dest=transToLang, encoding='utf-8')
			print(translated.text)
			pdf.cell(w=0, h = 0, txt = translated.text, border = 0, ln = 0, align = 'L', fill = False, link = '')
			pdf.multi_cell(0,10,txt="\n",border=0,align='J',fill=False)
		# print(toBeTranslatedStr)
	pdf.ln(0.5)
	pdf.output("translatedFiles/"+fileName+"_translated_"+transToLang+".pdf", 'F')
	pdf.close()
	pdfFileObj.close()
	return True
