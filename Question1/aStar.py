import sys
import time

import numpy as np

from matplotlib.patches import Rectangle

import point
import randomMap

class AStar:
    def __init__(self, map):
        self.map=map
        self.open_set = []
        self.close_set = []

    #BaseCost,节点到起点的移动代价
    def BaseCost(self, p):
        x_dis = p.x
        y_dis = p.y
        # Distance to start point
        return x_dis + y_dis + (np.sqrt(2) - 2) * min(x_dis, y_dis)

    #HeuritsticCost,节点到终点的启发函数
    def HeuristicCost(self, p):
        x_dis = self.map.size - 1 - p.x
        y_dis = self.map.size - 1 - p.y
        # Distance to end point
        return x_dis + y_dis + (np.sqrt(2) - 2) * min(x_dis, y_dis)

    #TotalCost,代价总和
    def TotalCost(self, p):
        return self.BaseCost(p) + self.HeuristicCost(p)

    #IsValidPoint,判断点是否有效
    def IsValidPoint(self, x, y):
        if x < 0 or y < 0:
            return False
        if x >= self.map.size or y >= self.map.size:
            return False
        return not self.map.IsObstacle(x, y)

    #IsInPointList,判断点是否在某个集合中
    def IsInPointList(self, p, point_list):
        for point in point_list:
            if point.x == p.x and point.y == p.y:
                return True
        return False

    #IsInOpenList, 判断点是否在open set中
    def IsInOpenList(self, p):
        return self.IsInPointList(p, self.open_set)

    #IsInCloseList, 判断点是否在close set中
    def IsInCloseList(self, p):
        return self.IsInPointList(p, self.close_set)

    #IsStartPoint,判断点是否为起点.
    def IsStartPoint(self, p):
        return p.x == 0 and p.y ==0

    #IsEndPoint,判断点是否为终点.
    def IsEndPoint(self, p):
        return p.x == self.map.size-1 and p.y == self.map.size-1

    def RunAndSaveImage(self, ax, plt):
        start_time = time.time()

        start_point = point.Point(0, 0)
        start_point.cost = 0
        self.open_set.append(start_point)

        while True:
            index = self.SelectPointInOpenList()
            if index < 0:
                print('No path found, algorithm failed!!!')
                return
            p = self.open_set[index]
            rec = Rectangle((p.x, p.y), 1, 1, color='c')
            ax.add_patch(rec)
            self.SaveImage(plt)

            if self.IsEndPoint(p):
                return self.BuildPath(p, ax, plt, start_time)

            del self.open_set[index]
            self.close_set.append(p)

            # Process all neighbors
            x = p.x
            y = p.y
            self.ProcessPoint(x - 1, y + 1, p)
            self.ProcessPoint(x - 1, y, p)
            self.ProcessPoint(x - 1, y - 1, p)
            self.ProcessPoint(x, y - 1, p)
            self.ProcessPoint(x + 1, y - 1, p)
            self.ProcessPoint(x + 1, y, p)
            self.ProcessPoint(x + 1, y + 1, p)
            self.ProcessPoint(x, y + 1, p)

    #SaveImage, 将当前状态保存到图片中,以当前的时间戳命名,表唯一性和先后顺序.
    def SaveImage(self, plt):
        millis = int(round(time.time() * 1000))
        filename = 'Images/' + str(millis) + '.png'
        plt.savefig(filename)

    #ProcessPoint, 针对每一节点进行处理
    def ProcessPoint(self, x, y, parent):
        if not self.IsValidPoint(x, y):
            return  # Do nothing for invalid point
        p = point.Point(x, y)
        if self.IsInCloseList(p):
            return  # Do nothing for visited point
        print('Process Point [', p.x, ',', p.y, ']', ', cost: ', p.cost)
        if not self.IsInOpenList(p):
            p.parent = parent
            p.cost = self.TotalCost(p)
            self.open_set.append(p)

    #SelectPointInOpenList, 从open set中找到优先级最高的节点, 返回其索引.
    def SelectPointInOpenList(self):
        index = 0
        selected_index = -1
        min_cost = sys.maxsize
        for p in self.open_set:
            cost = self.TotalCost(p)
            if cost < min_cost:
                min_cost = cost
                selected_index = index
            index += 1
        return selected_index

    #BuildPath, 从终点往回沿着parent路线构造结果路径.然后从起点开始绘制结果,通过绿色方块，每次测绘便保存一个图片.
    def BuildPath(self, p, ax, plt, start_time):
        path = []
        while True:
            path.insert(0, p)  # Insert first
            if self.IsStartPoint(p):
                break
            else:
                p = p.parent
        for p in path:
            rec = Rectangle((p.x, p.y), 1, 1, color='g')
            ax.add_patch(rec)
            plt.draw()
            self.SaveImage(plt)
        end_time = time.time()
        print('===== Algorithm finish in', int(end_time - start_time), ' seconds')