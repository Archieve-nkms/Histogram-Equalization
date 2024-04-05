# 입력영상, 입력영상의 히스토그램, 입력영상의 누적 히스토그램
# 출력영상, 출력영상의 히스토그램, 출력영상의 누적 히스토그램

import matplotlib.pyplot as plt
import cv2
from cv2.typing import MatLike

def clamp(value:float, min:float, max:float):
    if value < min:
        return min
    elif value > max:
        return max
    return value

def equalizeHist(image:MatLike) -> MatLike:
    height, width, channel = image.shape
    total_pixels = height * width
    hist = [0] * 256
    sum_of_hist = [0] * 256
    sum = 0

    ycbcrImg = convertBGR2YCbCr(image)

    y = ycbcrImg[..., 0]

    for i in range(height):
        for j in range(width):
            hist[y[i][j]]+=1

    for i in range(256):
        sum += hist[i]
        sum_of_hist[i] = sum

    for i in range(height):
        for j in range(width):
            y[i][j] = sum_of_hist[y[i][j]] * (255 / total_pixels)
    
    ycbcrImg[..., 0] = y

    bgrImage = convertYCbCrToBGR(ycbcrImg)
    return bgrImage

def convertBGR2YCbCr(image:MatLike) -> MatLike:
    resultImage = image.copy()
    height, width, channel = image.shape
    b = image[..., 0]
    g = image[..., 1]
    r = image[..., 2]

    for i in range(height):
        for j in range(width):
            y = 0.299 * r[i][j] + 0.587 * g[i][j] + 0.114 * b[i][j]
            cb = (r[i][j] - y) * 0.713 + 128
            cr = (b[i][j] - y) * 0.564 + 128 
            resultImage[i][j] = (y, cr, cb) 

    return resultImage

def convertYCbCrToBGR(image:MatLike) -> MatLike:
    resultImage = image.copy()
    height, width, channel = image.shape
    y = image[..., 0]
    cr = image[..., 1]
    cb = image[..., 2]

    for i in range(height):
        for j in range(width):
            b = clamp(y[i][j] + 1.773 * (cb[i][j] - 128), 0, 255)
            g = clamp(y[i][j] - 0.714 * (cr[i][j] - 128) - 0.344 * (cb[i][j] - 128), 0, 255)
            r = clamp(y[i][j] + 1.403 * (cr[i][j] - 128), 0, 255)
            resultImage[i][j] = (r, g, b) 

    return resultImage

def calcHist(image: MatLike):
    height, width, channel = image.shape
    hist = [0] * 256
    for i in range(height):
        for j in range(width):
            b = image[i][j][0]
            g = image[i][j][1]
            r = image[i][j][2]
            y =  (int)(0.114 * b + 0.299 * r + 0.587 * g)
            hist[y] += 1
            
    return hist

def calcCumulativeHist(image:MatLike):
    hist = calcHist(image)
    sum_of_hist = [0] * 256
    sum = 0
    for i in range(256):
        sum += hist[i]
        sum_of_hist[i] = sum

    return sum_of_hist    
# main

image = cv2.imread("image.bmp", cv2.IMREAD_COLOR)
result = equalizeHist(image)
cv2.imshow('original', image)
cv2.imshow('result', result)

imageHist = calcHist(image)
resultHist = calcHist(result)

imageCumHist = calcCumulativeHist(image)
resultCumHist = calcCumulativeHist(result)

plt.figure(figsize=(6,8))
plt.subplot(211)
plt.title("histogram")
plt.plot(imageHist, color='r')
plt.plot(resultHist, color='b')
plt.xlim([0, 256])

plt.subplot(212)
plt.title("Cumulative histogram")
plt.plot(imageCumHist, color='r')
plt.plot(resultCumHist, color='b')
plt.xlim([0, 256])

plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()