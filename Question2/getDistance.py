# import the necessary packages
from imutils import paths
import numpy as np
import imutils
import cv2


def find_marker(image):
    # 将图片转化为灰度图，进行模糊处理，并进行边缘检测
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 35, 125)
    # 找到图片中的众多轮廓，获取其中面积最大的轮廓，假设是目标物体的轮廓
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)

    # 反馈包含轮廓坐标、像素长度和像素宽度的边框
    return cv2.minAreaRect(c)

def distance_to_camera(knownWidth, focalLength, perWidth):
    # 传入物体的实际宽度，计算出的焦距和图片上目标的像素宽度，则可以通过小孔成像原理
    # 使用相似三角形获得目标到相机的距离
    return (knownWidth * focalLength) / perWidth


# 首先测量目标物体到相机的距离
KNOWN_DISTANCE = 29.7

# 再测量目标物体的宽度
KNOWN_WIDTH = 21.0


# 读取图片通过find_marker函数得到图片汇总目标物体的坐标和长宽信息,根据相似三角形得到相机焦距
image = cv2.imread("images29.7cm.jpg")
marker = find_marker(image)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH

# 再对一系列图片进行循环测距
for imagePath in sorted(paths.list_images("./")):
    # 读取图片,获取距离
    image = cv2.imread(imagePath)
    marker = find_marker(image)
    centimeters = distance_to_camera(KNOWN_WIDTH, focalLength, max(marker[1]))

    # 将距离标注在图片上
    box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
    box = np.int0(box)
    cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
    cv2.putText(image, "%.2fcm" % (centimeters),
                (image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                2.0, (0, 255, 0), 3)
    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    cv2.imshow("result", image)
    cv2.imwrite("images%.2fcm.jpg" % (centimeters), image)
    cv2.waitKey(0)