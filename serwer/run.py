from flask import Flask, render_template, request
from json import load as jsload
import sqlite3

from flask.wrappers import Response
app = Flask(__name__)

def getdb():
   return sqlite3.connect('baza.sqlite')

def insertdb(args):
   db = getdb()
   db.execute('INSERT INTO cechy(nazwa, uwagi, Alex, Alfred, Anita, Anne, Bernard, Bill, Charles, Claire, David, Eric, Frans, George, Herman, Joe, Maria, Max, Paul, Peter, Philip, Richard, Robert, Sam, Susan, Tom) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', args)
   db.commit()
   db.close()

with open('serwer/osoby.json') as f:
    OSOBY = jsload(f)

@app.route('/', methods=['POST'])
def form():
   print(request.form)
   if not request.form.get('cecha') or request.form.get('uwagi') is None:
      return "Brakuje pola cech i uwag", 400

   args = [request.form['cecha'], request.form['uwagi'].replace('\n','/')]
   for os in sum(OSOBY, []):
      if request.form.get(os, 'NIE').isnumeric():
         args.append(int(request.form[os]))
      else:
         return "brakuje wartości dla osobnika", 400

   insertdb(args)
   return render_template('podziekowanie.html')

@app.route('/', methods=['GET'])
def send():
   return render_template('main.html', osoby=OSOBY)

if __name__ == '__main__':
    app.run()