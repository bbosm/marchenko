
import os, sys
import docx

def docx_to_str(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def docx_to_txt(filename, path_to = None):
    txt_name = os.path.splitext(os.path.basename(filename))[0] + '.txt'
    if path_to is not None:
        txt_name = os.path.join(path_to, txt_name)
    s = docx_to_str(filename).encode('utf8')
    print(s)
##    with open(txt_name, 'w') as f:
##        f.write(s)

docx_to_txt('24zt0or4H232jBA2405Xs0.docx')


            
