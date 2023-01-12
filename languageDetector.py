import fasttext
import os
from pathlib import Path
import re
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator

model = fasttext.load_model('Pdf-Proofing/lid.176.ftz')
file= "Sample/Trimble_different.pdf"
fp = open(file, 'rb')
rsrcmgr = PDFResourceManager()
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
pages = PDFPage.get_pages(fp)
counter=0
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
                if lang!='it' and odds>0.95:
                    print("page number : ",counter)
                    print("language : ",lang)
                    print("Text : ",text)
                    print("")
