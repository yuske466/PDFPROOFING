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

