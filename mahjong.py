#!/usr/bin/python
# 来源 https://github.com/habacat/mahjong_hw/tree/cloud GPL-3.0 license

from check import CheckWin
import pandas as pd
import numpy as np
from io import StringIO

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

def solve(data_json):
	data_io = StringIO(data_json)
	df = pd.read_json(data_io, encoding='utf-8') # type(data) --> <class 'pandas.core.frame.DataFrame'>

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
