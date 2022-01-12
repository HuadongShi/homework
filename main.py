import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle

import randomMap
import aStar
import shutil
import os
shutil.rmtree('./Images')
os.mkdir('./Images')

plt.figure(figsize=(5, 5))

#创建一个随机地图
map = randomMap.RandomMap()

#设置图像的内容与地图大小一致
ax = plt.gca()
ax.set_xlim([0, map.size])
ax.set_ylim([0, map.size])

#绘制地图,对于障碍物绘制一个灰色的方块,其他区域绘制白色方块,每块的边线为灰色.
for i in range(map.size):
    for j in range(map.size):
        if map.IsObstacle(i,j):
            rec = Rectangle((i, j), width=1, height=1, color='gray')
            ax.add_patch(rec)
        else:
            rec = Rectangle((i, j), width=1, height=1, edgecolor='gray', facecolor='w')
            ax.add_patch(rec)

#绘制起点为蓝色方块.
rec = Rectangle((0, 0), width = 1, height = 1, facecolor='b')
ax.add_patch(rec)

#绘制终点为红色方块.
rec = Rectangle((map.size-1, map.size-1), width = 1, height = 1, facecolor='r')
ax.add_patch(rec)

#设置图像的坐标轴比例相等、隐藏坐标轴.
plt.axis('equal')
plt.axis('off')
plt.tight_layout()
#plt.show()

#调用算法查找路径.获得图片与结果.
a_star = aStar.AStar(map)
a_star.RunAndSaveImage(ax, plt)