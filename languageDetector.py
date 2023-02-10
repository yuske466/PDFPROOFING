import fasttext
import re
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator

def generalFilter(lang,odds,language):
    if (language=='zh' or language=='ja'):
        return (lang!='zh' and lang!='ja') and odds>0.95
    else:
        return (lang!=language) and odds>0.95

def languageDetector(file,language):
    model = fasttext.load_model('lid.176.ftz')
    fp = open(file, 'rb')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = PDFPage.get_pages(fp)
    counter=0
    print('\n\nLOADING...')
    for page in pages:
        counter+=1
        interpreter.process_page(page)
        layout = device.get_result()
        for lobj in layout:
            if isinstance(lobj, LTTextBox):
                x, y, text = lobj.bbox[0], lobj.bbox[3], lobj.get_text()
                text = text.replace('\n','')
                pattern = r'[0-9]'
                text = re.sub(pattern, '', text).replace('.', '')
                if text !='':
                    lang = model.predict(text, k=1)[0][0].replace('__label__', '')
                    odds = model.predict(text, k=1)[1][0]
                    if generalFilter(lang,odds,language):
                        print("page number : ",counter)
                        print("language : ",lang)
                        print("Text : ",text)
                        print("")
    print('\n\nANALYSIS COMPLETE...')
    
def display(file,language):
    languageDetector(file,language)
try:
    path = input("enter path : ").replace('\\','/').replace('"', '')
    language = input("LANGUAGES:\n\nda = danish, de = german, en = english, es = Spanish, fr = french, it = italian, ja = japanese, ko = korean, no = norwegian, nl = dutch, pl = polish, pt = portuguese,  ru = russian, sv = swedish zh, = chinese\n\nEnter language : ")
    display(path,language.lower())
except:
    print("Error, wrong file name")
