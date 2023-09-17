import requests
import pandas as pd
import numpy as np
def solve():
	url = "https://python-vercel-test-one.vercel.app/api"
	df = pd.read_csv("test1.csv", encoding='utf-8', skiprows=1)
	df_json = df.to_json(orient='records')
	response = requests.post(url, data={"data": df_json})
	if response.status_code == 200:  # 确保请求成功
		data = response.json()  # 将Response对象转换为JSON格式
		final_csv_data = data["finnal_csv"]  # 对JSON对象进行索引操作，获取"finnal_csv"的数据

		# 在这里可以继续处理final_csv_data
		print(final_csv_data)
	else:
		print("请求失败")
	# 将数据保存到winner.csv文件中
	try:
		np.savetxt("winner.csv", final_csv_data, delimiter=",", fmt="%s")
		print("已保存文件winner.csv")
	except:
		print("保存文件失败...")

if __name__ == "__main__":
	solve()