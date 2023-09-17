from flask import Flask, render_template, request, jsonify
# from mahjong import solve, hello_world2
import pandas as pd

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
	# 读取CSV文件
	df = pd.read_csv("test1.csv", encoding='utf-8', skiprows=1)
	# 将DataFrame转换为JSON字符串
	json_data = df.to_json(orient="records")
	# 打印JSON数据
	return jsonify(json_data)