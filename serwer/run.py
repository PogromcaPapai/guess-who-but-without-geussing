from flask import Flask, render_template
from json import load as jsload
app = Flask(__name__)

with open('serwer/osoby.json') as f:
    OSOBY = jsload(f)

@app.route('/', methods=['POST'])
def form():
   return render_template('podziekowanie.html')

@app.route('/', methods=['GET'])
def send():
   return render_template('main.html', osoby=OSOBY)

if __name__ == '__main__':
    app.run()