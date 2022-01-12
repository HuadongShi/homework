import numpy as np

import point

class RandomMap:
    #初始化函数
    def __init__(self, size=20):
        self.size = size
        self.obstacle = size//5
        self.GenerateObstacle()

    #障碍生成函数,建立一个数组并将障碍点放置其中
    def GenerateObstacle(self):
        self.obstacle_point = []
        self.obstacle_point.append(point.Point(self.size//2, self.size//2))
        self.obstacle_point.append(point.Point(self.size//2, self.size//2-1))

        # 生成位于地图中间的某个障碍体，宽度为2
        for i in range(self.size//2-2, self.size//2):
            self.obstacle_point.append(point.Point(i, self.size-i))
            self.obstacle_point.append(point.Point(i, self.size-i-1))
            self.obstacle_point.append(point.Point(self.size-i, i))
            self.obstacle_point.append(point.Point(self.size-i, i-1))

        #随机生成障碍物
        for i in range(self.obstacle-1):
            x = np.random.randint(0, self.size)
            y = np.random.randint(0, self.size)
            self.obstacle_point.append(point.Point(x, y))

            if (np.random.rand() > 0.5): # 随机方向
                for l in range(self.size//4):
                    self.obstacle_point.append(point.Point(x, y+l))
                    pass
            else:
                for l in range(self.size//4):
                    self.obstacle_point.append(point.Point(x+l, y))
                    pass

    #判断某个平面中的点是否为障碍
    def IsObstacle(self, i ,j):
        for p in self.obstacle_point:
            if i==p.x and j==p.y:
                return True
        return False