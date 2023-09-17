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

@app.route('/api', methods=['POST'])
def run_slove():
	if request.method == 'POST':
		data = request.form.get('data')  # 获取名为"data"的POST参数

		# 在这里处理接收到的数据
		# ...

		return "Received POST data: " + data
	list1,list2,list3 = solve("test1.csv")
	# 创建一个包含三个列表的字典
	data = {
		'winner_names': list1.tolist(),
		'player_names': list2.tolist(),
		'player_scores': list3.tolist()
	}
	return jsonify(data)