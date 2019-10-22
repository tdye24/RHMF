# ！usr/bin/python
# -*- coding:utf-8 -*-#
# @date:2019/10/22 15:37
# @name:图像分割
# @author:TDYe
import cv2
import numpy as np

path = "D:\\MyProjects\\DC\\dataset\\formula.png"
root = "D:\\MyProjects\\DC\\dataset\\"
size = 28		# 归一化处理的图像大小
img = cv2.imread(path)
data = np.array(img)
len_y = data.shape[0]		# 高度95
len_x = data.shape[1]		# 宽度261
print("高度：" + str(len_y))
print("宽度：" + str(len_x))
min_height = 10		# 设置最小的文字像素高度，防止切分噪音字符

start_j = -1
end_j = -1
rowPairs = []		# 存放每行的起止点坐标
# 行分割
for j in range(len_y):
	"""
	[255, 255, 255]	黑色像素点
	[0, 0, 0]		白色像素点
	a = [[255, 255, 255], [255, 255, 255], [255, 255, 255]		#空白行
	a.all() === True
	a = [[0, 0, 0], [0, 0, 0], [255, 255, 255], [0, 0, 0]]		#非空白行
	a.all() == False
	"""
	if not data[j].all() and start_j < 0:		# 非空白行，起行
		start_j = j
	elif not data[j].all():		# 非空白行，终行，动态更新
		end_j = j
	elif data[j].all() and start_j >= 0:		# 找到完整一行
		if end_j - start_j >= min_height:		# 设置最小的文字像素高度，防止切分噪音字符
			rowPairs.append((start_j, end_j))
		start_j, end_j = -1, -1

print(rowPairs)

# 列分割
start_i = -1
end_i = -1
min_width = 5		# 最小文字像素长度
number = 0 		# 分割后保存编号
for start_j, end_j in rowPairs:
	for i in range(len_x):
		if not data[start_j: end_j, i].all() and start_i < 0:
			start_i = i
		elif not data[start_j: end_j, i].all():
			end_i = i
		elif data[start_j: end_j, i].all() and start_i >= 0:
			if end_i - start_i >= min_width:
				tmp = data[start_j: end_j, start_i: end_i]
				im2save = cv2.resize(tmp, (size, size))		# 归一化处理
				cv2.imwrite(root + '%d.png' % number, im2save)
				print(root + '%d.png' % number)
				number += 1
				start_i, end_i = -1, -1



