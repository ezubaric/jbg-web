
import sys
from CoreGraphics import *
from glob import glob

def pageCount(pdfPath):
    "Return the number of pages for some PDF file."

    pdf = CGPDFDocumentCreateWithProvider (CGDataProviderCreateWithFilename (pdfPath))
    return pdf.getNumberOfPages()

if __name__ == "__main__":
    for pp in glob("pubs/*"):
        src = open(pp).read()
        try:
            pdf = [x.split()[-1] for x in src.split('\n') if "~~ url" in x.lower()][0]
            pdf = pdf.replace("docs", "src_docs")
            print pdf
        except IndexError:
            continue
        src = "\n".join(x for x in src.split('\n') if not x.startswith("~~NumPages"))
        pages = pageCount(pdf)
        text = "%s\n~~ NumPages | %i\n" % (src.strip(), pages)

        with open(pp, 'w') as output:
            output.write(text)
