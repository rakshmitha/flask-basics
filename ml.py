from flask import Flask, render_template, request, make_response
from PyPDF2 import PdfFileReader,PdfFileWriter
from werkzeug.utils import secure_filename
app = Flask(__name__)
'''
    http://127.0.0.1:5000/show_pdf
'''
@app.route('/show_pdf',methods = ['GET', 'POST'])
def show_pdf():
    UPLOAD_FOLDER = './static/uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    pdf_path=None
    error_msg=None
    pdf=None
    if request.method == 'POST':
        file = request.files['pdf']
        if file.filename == '':
            error_msg="Please Upload Any PDF"
        else:
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pdf_path="./static/uploads/{}".format(filename)
            
            pdfFileObj = open(filename, 'r')  
            pdfReader = PdfFileReader(filename)  
            print(pdfReader.numPages)  
            pageObj = pdfReader.getPage(0)  
            s=[]
            s.append((pageObj.extractText()) )
            
            f=open('hi.txt','w')
            for ele in s:
                f.write(ele+'\n')
            f.close()
            pdfFileObj.close()
    return render_template("show_pdf.html",pdf_path=pdf_path,error_msg=error_msg)
    '''pdfFileObj = open(filename, 'r')  
            pdfReader = PdfFileReader(filename)  
            print(pdfReader.numPages)  
            pageObj = pdfReader.getPage(0)  
            s=[]
            s.append((pageObj.extractText()) )
            print(s)
            f=open('hi1.txt','w')
            for ele in s:
                f.write(ele+'\n')
            f.close()
            pdfFileObj.close()'''

