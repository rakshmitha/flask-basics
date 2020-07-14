from flask import Flask, render_template, request

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)