from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter#process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from io import StringIO
from pdfminer.layout import LAParams, LTTextBox, LTTextLine,LTChar

from googletrans import Translator
from fpdf import FPDF 

import shutil
import os

def translateWriteWithFormatToPDF(fileName,transToLang):

    filePath = "filesToBeTranslated/"+fileName
    filePathWithoutExt = filePath.replace('.pdf','')
    # copy file
    shutil.copyfile(filePath, filePathWithoutExt+"imDuplicate.pdf")
    pdf_file = open(filePathWithoutExt+"imDuplicate.pdf", 'rb')

    # PDFMiner boilerplate
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    translator = Translator()
    pageNum = 0

    pdf = FPDF()
    pdf.set_auto_page_break(False, margin = 0.0)

    if transToLang=='hi' or transToLang=='es' or transToLang=="pt" or transToLang=="ru" or transToLang=="jw" or transToLang=="de" or transToLang=="fr" or transToLang=='tr':
        pdf.add_font('gargi', '', 'fonts/NotoSans-Regular.ttf', uni=True)
    if transToLang=='ar':
        pdf.add_font('gargi', '', 'fonts/Almarai-Regular.ttf', uni=True)
    if transToLang=='ja':
        pdf.add_font('gargi', '', 'fonts/yugothil.ttf', uni=True)
    if transToLang=='ko':
        pdf.add_font('gargi', '', 'fonts/BMEULJIROTTF.ttf', uni=True)
        
    # Extract text
    fp = open(filePath, 'rb')
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        pageNum = pageNum+1
        data = sio.getvalue()
        print(pageNum)
        # print(data)
        
        pdf.add_page()
        for i in data.split('\n'):
            font_size = get_fontsize_and_fontname_for_word(filePathWithoutExt+"imDuplicate.pdf",pageNum,i.strip(),pdf_file)
            print(font_size)
            print(i)
            pdf.set_font('gargi', '', font_size)
            translated = translator.translate(i, dest=transToLang, encoding='utf-8')
            print(translated.text)
            pdf.cell(w=0, h = 0, txt = translated.text, border = 0, ln = 0, align = 'L', fill = False, link = '')
            pdf.multi_cell(0,4,txt="\n",border=0,align='J',fill=False)
        data = ''
        sio.truncate(0)
        sio.seek(0)
    pdf.ln(0.5)
    pdf.output("translatedFiles/"+fileName+"_translated_"+transToLang+".pdf", 'F')
    pdf.close()
    pdf_file.close()
    fp.close()
    device.close()
    os.remove(filePathWithoutExt+"imDuplicate.pdf")
    return True

def get_fontsize_and_fontname_for_word( pdf_path, page_number,word,pdf_file):
    resource_manager = PDFResourceManager()
    layout_params = LAParams()
    device = PDFPageAggregator(resource_manager, laparams=layout_params)
    # pdf_file = open(pdf_path, 'rb')
    pdf_page_interpreter = PDFPageInterpreter(resource_manager, device)
    actual_font_size_pt=0
    actual_font_name=0

    for current_page_number, page in enumerate(PDFPage.get_pages(pdf_file)):
        if current_page_number == int(page_number) - 1:
            pdf_page_interpreter.process_page(page)
            layout = device.get_result()
            for textbox_element in layout:
                if isinstance(textbox_element, LTTextBox):
                    for line in textbox_element:
                        word_from_textbox = line.get_text().strip()
                        if word in word_from_textbox:
                            for char in line:
                                if isinstance(char, LTChar):
                                    # convert pixels to points
                                    actual_font_size_pt = int(char.size) * 72 / 96
                                    # remove prefixed font name, such as QTBAAA+
                                    actual_font_name = char.fontname[7:]
    device.close()
    return actual_font_size_pt

translateWriteWithFormatToPDF('inEnglish_2.pdf','hi')
