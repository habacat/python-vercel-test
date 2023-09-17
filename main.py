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

@app.route('/api', methods=['GET','POST'])
def run_slove():
	if request.method == 'POST':
		data = request.form.get('data')  # 获取名为"data"的POST参数
		winner_names, player_names, winner_scores = solve(data)
		fin = np.empty((0,))
		if(np.all(winner_scores) == 0):
			fin = np.append(fin, 'Draw')
			for name, score in zip(player_names, winner_scores): # 遍历player_names数组和winner_scores列表
				fin = np.append(fin, f'{name},{score*100:.2f}%\n') # 将每个元素的名称和得分以指定格式写入文件
		else:
			winner_scores = winner_scores/np.sum(winner_scores)
			fin = np.append(fin, winner_names)
			for name, score in zip(player_names, winner_scores): # 遍历player_names数组和winner_scores列表
				fin = np.append(fin, f'{name},{score*100:.2f}%\n')
		fin_2d = np.expand_dims(fin, axis=0)
		transposed_fin = fin_2d.T
		# 创建一个包含三个列表的字典
		data = {
			'winner_names': winner_names.tolist(),
			'player_names': player_names.tolist(),
			'winner_scores': winner_scores.tolist(),
			'finnal_csv': transposed_fin.tolist()
		}
		return jsonify(data)
		# else:
		# 	data = {
		# 		'data' : '传递的数据有误'
		# 	}
		# 	return jsonify(data)

	if request.method == 'GET':
		return '请使用POST方法，向 https://python-vercel-test-one.vercel.app/api 传递data(json格式)<br>\
				data需要为使用df.to_json(orient=\'records\')将dataframe转换为json。<br>\
				具体方法为：df = pd.read_csv("test1.csv", encoding=\'utf-8\', skiprows=1)<br>'

