from flask import Flask, render_template, request
from mahjong import solve

app = Flask(__name__)

@app.route('/index')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  app.run(port=5000)


@app.route('/hello')
def hello_world():
    return 'Hello from Flask Github!'

@app.route('/api')
def run_slove():
	solve("test1.py")