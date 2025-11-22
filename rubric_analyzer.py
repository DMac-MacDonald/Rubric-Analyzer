import pymupdf
import pytesseract
import os

tesspath = "C:\\Program Files\\Tesseract-OCR\\tessdata"  # path to tessdata. DO NOT CHANGE
infile = "sample_ocr.jpg"
tempfile = "temp.pdf"
out = open("output.txt", "wb")
zoom_4x = pymupdf.Matrix(2.0, 2.0)  # zoom factor 2 in each dimension

print("running....")

for page in pymupdf.open(infile): # iterate the document pages
    # if os.path.splitext(infile)[1] != ".pdf":
    page.get_pixmap().pdfocr_save(tempfile, tessdata=tesspath)  # converts current pdf page to pixmap, then back to pdf with ocr layer
    tempfile = pymupdf.open(tempfile)  # opens the temp ocr pdf
    text = tempfile[0].get_text().encode("utf8")  # gets text from ocr layer of pdf
    print(text)  # prints extracted text to terminal (for easier debugging). can be removed if you want
    out.write(text) # write text of page to output.txt file
    
out.close()

print("done!")