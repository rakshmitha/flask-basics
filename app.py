
#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 

Course work: 

@author: FLASK-INTERN-TEAM

Source:
    https://stackoverflow.com/questions/13279399/how-to-obtain-values-of-request-variables-using-python-and-flask
'''

from flask import Flask, render_template, request, make_response
from PyPDF2 import PdfFileReader,PdfFileWriter
import sqlite3
from sqlite3 import Error
import requests
from PIL import Image, ImageDraw, ImageFont
import textwrap



from werkzeug.utils import secure_filename
import os

app = Flask(__name__)


database = 'test.db'


def generate_meme(image_path, top_text, bottom_text='', font_path='./fonts/impact/impact.ttf', font_size=9):
	# load image
	im = Image.open(image_path)
	draw = ImageDraw.Draw(im)
	image_width, image_height = im.size
	
	# load font
	font = ImageFont.truetype(font=font_path, size=int(image_height*font_size)//100)

	# convert text to uppercase
	top_text = top_text.upper()
	bottom_text = bottom_text.upper()

	# text wrapping
	char_width, char_height = font.getsize('A')
	chars_per_line = image_width // char_width
	top_lines = textwrap.wrap(top_text, width=chars_per_line)
	bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line)

	# draw top lines
	y = 10
	for line in top_lines:
	    line_width, line_height = font.getsize(line)
	    x = (image_width - line_width)/2
	    draw.text((x,y), line, fill='yellow', font=font)
	    y += line_height

	# draw bottom lines
	y = image_height - char_height * len(bottom_lines) - 15
	for line in bottom_lines:
	    line_width, line_height = font.getsize(line)
	    x = (image_width - line_width)/2
	    draw.text((x,y), line, fill='yellow', font=font)
	    y += line_height

	# save meme
	im.save('./static/uploads/' + 'meme-' + im.filename.split('/')[-1])

def get_last_record(conn):
    sql = '''SELECT * FROM flask1 ORDER BY id DESC LIMIT 1'''
    cur = conn.cursor()
    cur.execute(sql)
    row = cur.fetchall()

    if(len(row) <= 0):
        print('No Data available')
        return 1
    
    current_id = row[0][0]
    return current_id+1

def select_all(conn):
    """
    Query all rows in the flask1 table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM flask1")
 
    rows = cur.fetchall()
    
    print('rows count : '+str(len(rows)))
    
    if(len(rows) <= 0):
        print('No Data available')
 
    item_list = []
    for row in rows:
        print(row) 

        current_id = row[0]
        current_name = row[1]
        current_dept = row[2]

        current_dict = {
            'id' : current_id,
            'name' : current_name,
            'dept' : current_dept
        }

        item_list.append(current_dict)

    return item_list


def update_db(conn,update_obj):
    """
    Query all rows in the flask1 table
    :param conn: the Connection object
    :return:
    """
    sql = ''' UPDATE flask1 SET name = :name, dept = :dept where id = :id'''
    cur = conn.cursor()
    cur.execute(sql,update_obj)
    conn.commit()
    cur.execute("SELECT * FROM flask1")
 
    rows = cur.fetchall()
    
    print('rows count : '+str(len(rows)))
    
    if(len(rows) <= 0):
        print('No Data available')
 
    item_list = []
    for row in rows:
        print(row) 

        current_id = row[0]
        current_name = row[1]
        current_dept = row[2]

        current_dict = {
            'id' : current_id,
            'name' : current_name,
            'dept' : current_dept
        }

        item_list.append(current_dict)

    return item_list

def insert_into_db(conn,insert_obj):

    sql = ''' INSERT INTO flask1 (id,name,dept) 
            VALUES (:id, :name, :dept) '''

    cur = conn.cursor()
    cur.execute(sql, insert_obj)
    conn.commit()
    cur.execute("SELECT * FROM flask1")
 
    rows = cur.fetchall()
    
    print('rows count : '+str(len(rows)))
    
    if(len(rows) <= 0):
        print('No Data available')
 
    item_list = []
    for row in rows:
        print(row) 

        current_id = row[0]
        current_name = row[1]
        current_dept = row[2]

        current_dict = {
            'id' : current_id,
            'name' : current_name,
            'dept' : current_dept
        }

        item_list.append(current_dict)

    return item_list

def delete_from_db(conn,delete_obj):
    
    sql = ''' DELETE FROM flask1 WHERE id = :id '''

    cur = conn.cursor()
    cur.execute(sql, delete_obj)
    conn.commit()
    cur.execute("SELECT * FROM flask1")
 
    rows = cur.fetchall()
    
    print('rows count : '+str(len(rows)))
    
    if(len(rows) <= 0):
        print('No Data available')
 
    item_list = []
    for row in rows:
        print(row) 

        current_id = row[0]
        current_name = row[1]
        current_dept = row[2]

        current_dict = {
            'id' : current_id,
            'name' : current_name,
            'dept' : current_dept
        }

        item_list.append(current_dict)

    return item_list



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    
    name = None

    if request.method == 'POST':
        name = request.values.get("name")

    return name

'''
    http://127.0.0.1:5000/api/base
'''
@app.route('/api/base')
def api_base():
    
    result = {
        'food' : 'Poori',
        'name' : 'Rakshmitha'
    }

    return result

'''
    http://127.0.0.1:5000/api/student?name=gokul
'''
@app.route('/api/student')
def api_get_param():

    name = request.values.get("name")
    
    result = {
        'name' : name
    }

    return result

'''
    http://127.0.0.1:5000/api/path/test/chennai/tamilnadu
'''
@app.route('/api/path/test/<city>/<state>')
def api_get_path_variable(city, state):
    
    result = {
        'food' : 'Poori',
        'name' : 'Rakshmitha',
        'city' : city,
        'state' : state
    }

    return result

'''
    http://127.0.0.1:5000/api/db/vanilla/select
'''
@app.route('/api/db/vanilla/select')
def api_db_vanilla_select():

    item_list = None
    with sqlite3.connect("test.db") as conn:
        item_list = select_all(conn)

    result = {
        'users' : item_list
    }

    return render_template("show_db_table.html", result=result)

'''
    http://127.0.0.1:5000/show_image
'''
@app.route('/show_image',methods = ['GET', 'POST'])
def show_image():
    UPLOAD_FOLDER = './static/uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    img_path=None
    error_msg=None
    if request.method == 'POST':
        file = request.files['image']
        if file.filename == '':
            error_msg="Please Upload Any Image"
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_path="./static/uploads/{}".format(filename)
    return render_template("show_image.html",img_path=img_path,error_msg=error_msg)

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
            pdfFileObj = open(pdf_path, 'r')  
            pdfReader = PdfFileReader(pdf_path)  
            print(pdfReader.numPages)  
            pageObj = pdfReader.getPage(0) 
            s=[] 
            s.append((pageObj.extractText()))
            print("third print",s)
            f=open('demo.txt','w')
            for ele in s:
                f.write(ele+'\n')
            f.close()
            pdfFileObj.close()
            
    return render_template("show_pdf.html",pdf_path=pdf_path,error_msg=error_msg)
    
'''
    http://127.0.0.1:5000/api/db/vanilla/update
'''
@app.route('/api/db/vanilla/update/<id>/<name>/<dept>',methods = ['GET','POST'])
def api_db_vanilla_update(id,name,dept):
    id = int(id)
    if request.method == "POST":
        name = request.form['name']
        dept = request.form['dept']
        item_list = None
        with sqlite3.connect("test.db") as conn:
            update_obj = {
                "id": id,
                "name": name,
                "dept": dept
            }
        item_list = update_db(conn,update_obj)
        result = {
        'users' : item_list
        }
        return render_template("insert_into_db.html", result=result)

    return render_template("update_db.html",id=id,name=name,dept=dept)


'''
    http://127.0.0.1:5000/api/db/vanilla/insert
'''
@app.route('/api/db/vanilla/insert',methods = ['GET', 'POST'])
def api_db_vanilla_insert():
    if request.method == 'POST':
        #id = request.form['id']
        
        name = request.form['name']
        dept = request.form['dept']
        item_list = None
        with sqlite3.connect("test.db") as conn:
            id = get_last_record(conn)
            print("LAST RECORD ID ::: ",id)
            insert_obj = {
                "id": id,
                "name": name,
                "dept": dept
            }
        item_list = insert_into_db(conn,insert_obj)
        result = {
        'users' : item_list
        }

        return render_template("insert_into_db.html", result=result)
    
    item_list = None
    with sqlite3.connect("test.db") as conn:
        item_list = select_all(conn)

    result = {
        'users' : item_list
    }
    
    return render_template("insert_into_db.html", result=result)

'''
    http://127.0.0.1:5000/api/db/vanilla/delete/107
'''
@app.route('/api/db/vanilla/delete/<id>')
def api_db_vanilla_delete(id):

    item_list = None
    with sqlite3.connect("test.db") as conn:
        delete_obj = {
            "id": id,
        }
        item_list = delete_from_db(conn,delete_obj)

    result = {
        'users' : item_list
    }

    return render_template("insert_into_db.html",result=result)

'''
    http://127.0.0.1:5000/pub_api_request
'''
    
@app.route('/pub_api_request')
def pub_api_req():
    req = requests.get('https://reqres.in/api/users/2')
    result = json.loads(req.content)
    data = result.get('data')
    print(data)
    return render_template("api_data.html", data=data)


'''
    http://127.0.0.1:5000/meme_gen/img_filename
'''

@app.route('/meme_gen/<img_path>',methods=['GET','POST'])
def meme_gen(img_path):
    img_path = './static/uploads/' + img_path
    if request.method == 'POST':
        top_text = request.form['top_text']
        bottom_text = request.form['bottom_text']
        print("inside post method",img_path)
        
        generate_meme(img_path, top_text=top_text, bottom_text=bottom_text)
        meme_path = '../static/uploads/' + 'meme-' + img_path.split('/')[-1]
        print("Meme path :::",meme_path)
        return render_template("display_meme.html",meme_path=meme_path)
    return render_template("gen_meme.html",img_path=img_path)

if __name__ == "__main__":
    app.run(debug=True)