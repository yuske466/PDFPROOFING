from pdfminer.high_level import extract_pages
from pdfminer.layout import LTFigure,LTImage


def noImages(path):
    counter = 0 
    for page_layout in extract_pages(path):
        for element in page_layout:
            if isinstance(element, LTFigure) or isinstance(element, LTImage) :
                counter+=1
    return counter

def display(no1,no2):
    if no1!=no2:
        print("not the same, we have ")
    else:
        print("same number of images")

