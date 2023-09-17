from flask import Flask, render_template, request
# from mahjong import solve, hello_world2

app = Flask(__name__)

@app.route('/index')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  app.run(port=5000)


@app.route('/hello')
def hello_world():
    return 'Hello from Flask Github!'

# @app.route('/api')
# def run_slove():
#     solve("test1.py")
    
@app.route('/hello2')
def run_slove():
    print("test111")
    return 'test222'