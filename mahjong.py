#!/usr/bin/python
# 来源 https://github.com/habacat/mahjong_hw/tree/cloud GPL-3.0 license

from check import CheckWin
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def InitCards(df, player_names, player_flags_write, player_flags, cards): # 定义函数，用来重新生成13张牌组
	player_flags_write.fill(0) # 四个玩家的数据写入指针初始化
	for i,name in enumerate(player_names):
		if(player_flags[i]+12 <= df.shape[0]):
			cards[player_flags_write[i]+1: player_flags_write[i]+14, i] = df.iloc[player_flags[i]: player_flags[i]+13, i]
		else:
			return False
	player_flags+= 13 # 玩家读取和写入指针移动
	player_flags_write+= 13
	return True

def RepeatOnce(df, cards, pf, pfw, i, name, player_names, winner_names, winner_scores, pn):
	if(np.count_nonzero(cards[:,i]) == 13): # 如果已有13张牌，则摸取第14张并判别是否获胜。如获胜，返回；如没有获胜，则丢弃下一张牌。
		cards[pfw[i]+1, i] = df.iloc[pf[i], i]
		pf[i]+= 1; pfw[i]+= 1
		try:
			if(CheckWin(cards[1:,i].copy())):
				print(name, "is win!!!")
				WinStat = 1
				if(WinStat==1): winner_names=np.append(winner_names, name); winner_scores[i]+=1
				pf+= 1;pf[i]-= 1 # 调整玩家读取指针位置，除了当前i指向的玩家，其余指针均下移一个牌位
				cards = np.zeros([15,4], dtype=object)
				if(not InitCards(df, player_names, pfw ,pf, cards)):
					print("数组坐标越界，本局游戏中止。终止位置：",pf)
					return pn, winner_names, winner_scores
		except TypeError:
			print("发生错误，存在空数据或数据类型有误...程序仍将继续...")
			pass
		except:
			print("发生未知错误...程序终止！")
			return False, False, False

def solve(filename):
	with open(filename, 'r', encoding='utf-8') as file: # 读取文件
		dealer = file.readline().strip().replace("," , "") # 读取文件的第一行作为初始的dealer（摸牌者）
		# print("initial_dealer=",dealer)
	df = pd.read_csv(filename, encoding='utf-8', skiprows=1) # type(data) --> <class 'pandas.core.frame.DataFrame'>

	p1_name, p2_name, p3_name, p4_name = df.columns # 获得4个玩家的名字
	pn = player_names = np.array([p1_name, p2_name, p3_name, p4_name]) # 将四个名字存储在player_names中，方便取用
	pf = player_flags = np.zeros(4, dtype=int) # 四个玩家的数据读取指针
	pfw = player_flags_write = np.zeros(4, dtype=int) # 四个玩家的数据写入指针初始化
	winner_scores = np.zeros(4)
	winner_names = np.empty((0,))
	cards = np.zeros([15,4], dtype=object) # 生成空的玩家牌组表
	if(not InitCards(df, player_names, player_flags_write, player_flags, cards)): # 调用函数初始化牌组
		print("数组坐标越界，本局游戏中止。")
		print(pf)
		return pn, winner_names, winner_scores
	WinStat = 0
	pre_name = ""
	pre_index = ""
	while True:
		for i,name in enumerate(player_names):
			pre_name = name
			pre_index = i
			if(np.count_nonzero(cards[:,i]) == 13): # 如果已有13张牌，则摸取第14张并判别是否获胜。如获胜，返回；如没有获胜，则丢弃下一张牌。
				cards[pfw[i]+1, i] = df.iloc[pf[i], i]
				pf[i]+= 1; pfw[i]+= 1
				try:
					if(CheckWin(cards[1:,i].copy())):
						print(name, "is win!!!")
						WinStat = 1
						if(WinStat==1): winner_names=np.append(winner_names, name); winner_scores[i]+=1
						pf+= 1;pf[i]-= 1 # 调整玩家读取指针位置，除了当前i指向的玩家，其余指针均下移一个牌位
						cards = np.zeros([15,4], dtype=object)
						if(not InitCards(df, player_names, player_flags_write ,player_flags, cards)):
							print("数组坐标越界，本局游戏中止。终止位置：",pf)
							return pn, winner_names, winner_scores
						else:
							RepeatOnce(df, cards, pf, pfw, pre_index, pre_name, player_names, winner_names, winner_scores, pn)
				except TypeError:
					print("发生错误，存在空数据或数据类型有误...程序仍将继续...")
				except:
					print("发生未知错误...程序终止！")
					return False, False, False
			if(np.count_nonzero(cards[:,i]) >= 14): # 如果已有14张牌，则弃一张牌并从牌堆摸取一张牌然后判别是否获胜
				if(pf[i]+2 <= df.shape[0]): # 如果玩家读取指针不越界，则将下一张牌弃掉，下下一张牌替换到原位置
					try:
						cards[np.where(cards[:,i]== df.iloc[pf[i], i] )[0][0], i] = df.iloc[pf[i]+1, i]
					except:
						print("找不到元素---",pf)
					pf[i]+= 2
					try:
						if(CheckWin(cards[1:,i].copy())):
							print(name, "is win!!!",pf)
							WinStat = 1
							if(WinStat==1): winner_names=np.append(winner_names, name); winner_scores[i]+=1
							pf+= 1;pf[i]-= 1 # 调整玩家读取指针位置，除了当前i指向的玩家，其余指针均下移一个牌位
							cards = np.zeros([15,4], dtype=object)
							if(not InitCards(df, player_names, player_flags_write ,player_flags, cards)):
								print("数组坐标越界，本局游戏中止。终止位置：",pf)
								return pn, winner_names, winner_scores
							else:
								RepeatOnce(df, cards, pf, pfw, pre_index, pre_name, player_names, winner_names, winner_scores, pn)
					except TypeError:
						print("发生错误，存在空数据或数据类型有误...程序仍将继续...")
					except:
						print("发生未知错误...程序终止！")
						return False, False, False
				else: # 如果玩家指针越界，则抛出警告，中止程序，返回玩家指针位置
					print("数组坐标越界，本局游戏中止。终止位置：",pf)
					return pn, winner_names, winner_scores


def hello_world():
    return '仅支持post请求...'


# @app.route('/<path:path>', methods=['GET', 'POST'])
# def main():
# 	filename = "test1.csv"
# 	try:
# 		filename = f"{path}"
# 		if(filename is None):
# 			raise IndexError
# 	except IndexError:
# 		print("缺少输入参数，请正确引用文件名 *.csv\n示例：/test1.csv\n")
# 		print("本次将使用main函数内的filename默认值启动...")
# 		pass
# 	except:
# 		print("发生未知错误...程序终止！"); exit()
# 	try:
# 		player_names, winner_names, winner_scores = solve(filename)
# 		if(player_names or winner_names or winner_scores == False):
# 			print("返回值错误，程序退出！")
# 		else:
# 			print("正在为您生成winner.csv文件...")
# 	except:
# 		print("solve(filename)无法返回预期的值...程序强制退出...")
# 		exit()
# 	try:
# 		if os.path.exists("winner.csv"):
# 			os.rename("winner.csv", "winner.bak.csv")
# 			print("原目录中已存在winner.csv文件，已经将原文件重命名为winner.bak.csv，请及时保存。")
# 		if(np.all(winner_scores) == 0): # 如果没有人获胜（winner_scores全是0），则输出Draw
# 			with open('winner.csv', 'w', encoding='utf-8') as file:
# 				file.writelines("Draw\n")
# 				for name, score in zip(player_names, winner_scores): # 遍历player_names数组和winner_scores列表
# 					file.write(f'{name},{score*100:.2f}%\n') # 将每个元素的名称和得分以指定格式写入文件
# 			print("无人获胜（Draw）时的winner.csv成功生成。")
# 		else:
# 			winner_scores = winner_scores/np.sum(winner_scores)
# 			np.savetxt('winner.csv', winner_names, fmt='%s', encoding='utf-8')
# 			with open('winner.csv', 'a', encoding='utf-8') as file:
# 				for name, score in zip(player_names, winner_scores): # 遍历player_names数组和winner_scores列表
# 					file.write(f'{name},{score*100:.2f}%\n') # 将每个元素的名称和得分以指定格式写入文件
# 			print("有玩家获胜，winner.csv成功生成。")
# 	except:
# 		print("保存文件时出错！")
# 		exit()
