import requests
import pandas as pd
import numpy as np
def solve(data_json):
	url = "https://python-vercel-test-one.vercel.app/api"
	df = pd.read_csv("test1.csv", encoding='utf-8', skiprows=1)
	df_json = df.to_json(orient='records')
	response = requests.post(url, data={"data": df_json})
	# 获取"finnal_csv"的数据
	final_csv_data = response["finnal_csv"]
	print(final_csv_data)
	# 将数据保存到winner.csv文件中
	np.savetxt("winner.csv", final_csv_data, delimiter=",", fmt="%s")
