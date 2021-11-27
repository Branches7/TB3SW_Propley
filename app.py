from typing import Optional

from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, json
import requests
app = Flask(__name__)
app.secret_key = 'secret-string'

@app.route('/',methods=['GET', 'POST'])
def registrar():
     return render_template('index.html')

@app.route('/registrar', methods=['GET', 'POST'])
def registrar1():
    if request.method == "POST":
        attempted_username = request.form['username']
        attempted_password = request.form['password']

        dados = {"user": "", "pass": ""}
        with open('./data.json', 'r') as outfile:
            data = json.load(outfile)

        dados['user']= attempted_username
        dados['pass']= attempted_password

        data.append(dados)
        with open('./data.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

        if request.form['username'] == '' or request.form['password'] == '':
            return render_template('registrar.html', error=True)
        else:
            return render_template('index.html')
    else:
        return render_template('registrar.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        with open('./data.json', 'r') as outfile:
            dados = json.load(outfile)

        for user in dados:
            if request.form['username'] == user['user'] and request.form['password'] == user['pass']:
                return redirect('/home')

    return render_template('index.html', error=True)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/home', methods=['POST'])
def my_form_post():
    text = request.form['text']
    #processed_text = text.upper()

    url = "https://api.unsplash.com/search/photos?client_id=Cerx1ZVlv5T7ZKOs94DHPmSB-CqOwOTTT5n4AS-N7Zk"
    querystring = {"query": text}

    response = requests.request("GET", url, params=querystring)
    data = response.json()
    result = data['results']

    return render_template('imagem.html', result=result)

@app.route('/imagem')
def imagem():
    return render_template('imagem.html')


if __name__ == '__main__':
    app.run(debug=True)
