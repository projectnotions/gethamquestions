"""
  https://etienned.github.io/posts/extract-text-from-word-docx-simply/
  Module that extract text from MS XML Word document (.docx).
  (Inspired by python-docx <https://github.com/mikemaccana/python-docx>)
"""

try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import zipfile

WORDNAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORDNAMESPACE + 'p'
TEXT = WORDNAMESPACE + 't'
SYM = WORDNAMESPACE + 'sym'
CHAR = WORDNAMESPACE + 'char'
SYMDICT = {
    'F0B4' : 'x',
    '0000' : 'u\\unkn'
}

def get_docx_text(path):
    """
    Take the path of a docx file as argument, return the text in unicode.
    """

    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = XML(xml_content)

    paragraphs = []
    # https://stackoverflow.com/questions/25228106/
    #      how-to-extract-text-from-an-existing-docx-file-using-python-docx
    # replace .getiterator with .iter
    texts = []
    paragraphs = []
    for elt in tree.iter():
        if elt.tag == PARA:
            if texts:
                paragraphs.append(''.join(texts))
            texts = []
        elif elt.tag == SYM:
            sym = elt.attrib[CHAR].upper()
            sym = SYMDICT.get(sym, 'u\\unkn')
            texts.append(sym)
        elif elt.tag == TEXT:
            texts.append(elt.text)

    if texts:
        paragraphs.append(''.join(texts))
        texts = []

    return paragraphs
