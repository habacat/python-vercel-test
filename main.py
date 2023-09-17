from flask import Flask, render_template, request, jsonify
# from mahjong import solve, hello_world2
import pandas as pd
import numpy as np
# from check import CheckWin
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
    list1,list2,list3 = solve("test1.csv")
      # 创建一个包含三个列表的字典
    data = {
        'array1': list1.tolist(),
        'array2': list2.tolist(),
        'array3': list3.tolist()
    }
    return jsonify(data)