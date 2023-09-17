import requests
import pandas as pd
url = "https://python-vercel-test-one.vercel.app/api"
df = pd.read_csv("test1.csv", encoding='utf-8', skiprows=1)
df_json = df.to_json(orient='records')
data = {"data": df_json}

response = requests.post(url, data=data)
print(response.text)
