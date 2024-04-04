# 입력영상, 입력영상의 히스토그램, 입력영상의 누적 히스토그램
# 출력영상, 출력영상의 히스토그램, 출력영상의 누적 히스토그램
# 그래프 그리는데 라이브러리 사용 불가능

"""
예제

int k = 0, sum = 0, total_pixels = 0;
int hist[256];
int sum_of_hist[256];

for (int z = 0; z<256; z++)
{
    hist[z] = 0;
    sum_of_hist[z] = 0;
    for(int i = 0; i<256; i++)
    {
       k = m_openImg[i][z]
       hist[k]++;
    }
    for(int i = 0; i<256; i++)
    {
        sum += hist[i];
        sum_of_hist[i] = sum;
    }
    total_pixels = 256 * 256;
    for(int i = 0; i<256; i++)
    {
        k = m_openImg[i][z]
        m_resultImg[i][z] = sum_of_hist[k] * (255 / total_pixels);
    }
}

"""

import math
import cv2
from cv2.typing import MatLike

def equalizeHist_Gray(image:MatLike):
    result = image.copy()
    height = image.shape[0]
    width = image.shape[1]
    total_pixels = height * width
    hist = [0] * 256
    sum_of_hist = [0] * 256

    for i in range(height):
        for j in range(width):
            k = image[i][j]
            hist[k] += 1

    sum = 0
    for i in range(256):
        sum += hist[i]
        sum_of_hist[i] = sum

    for i in range(height):
        for j in range(width):
            k = image[i][j]
            result[i][j] = sum_of_hist[k] * (255.0 / total_pixels)

    return result

def equalizeHist(image:MatLike) -> MatLike:
    result = image.copy()
    height = image.shape[0]
    width = image.shape[1]
    total_pixels = height * width
    hist = [0] * 256
    sum_of_hist = [0] * 256
    sum = 0

    
    return result

def histogramEQ(image):
    img_y_cr_cb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(img_y_cr_cb)

    y_eq = cv2.equalizeHist(y)

    img_y_cr_cb_eq = cv2.merge((y_eq, cr, cb))
    img_rgb_eq = cv2.cvtColor(img_y_cr_cb_eq, cv2.COLOR_YCR_CB2BGR)

    return img_rgb_eq

def convertBGRToHSI(BGR): 
    B = BGR[0] / 255.0
    G = BGR[1] / 255.0
    R = BGR[2] / 255.0

    num1 = 0.5 * ((R - G) + (R - B))
    num2 = math.sqrt((R - G)**2 + (R - B) * (G - B)) + 0.00001
    H = math.acos(num1 / num2)
    H = math.degrees(H)
    if B > G:
        H = 360.0 - H
    H /= 360.0
     
    S = 1.0 - (3.0 / (B + G + R + 0.00001)) * min(R, G, B)
    I = (B + G + R) / 3.0

    return (H, S, I)

def convertHSIToBGR(HSI):
    H = HSI[0] * 360.0
    S = HSI[1]
    I = HSI[2]

    if 0 <= H < 120.0:  # RG
        B = I * (1.0 - S)
        R = I * (1.0 + (S * math.cos(math.radians(H))) / math.cos(math.radians(60 - H)))
        G = 3.0 * I - (R + B)
    elif 120.0 <= H < 240:  # GB
        H -= 120.0
        R = I * (1.0 - S)
        G = I * (1.0 + (S * math.cos(math.radians(H))) / math.cos(math.radians(60 - H)))
        B = 3.0 * I - (R + G)
    else:  # BR
        H -= 240.0
        G = I * (1.0 - S)
        B = I * (1.0 + (S * math.cos(math.radians(H))) / math.cos(math.radians(60 - H)))
        R = 3.0 * I - (G + B)

    B *= 255.0
    G *= 255.0
    R *= 255.0
    return (B, G, R)

image = cv2.imread("image.bmp", cv2.IMREAD_COLOR)
result = histogramEQ(image)
cv2.imshow('original', image)
cv2.imshow('result', result)

cv2.waitKey(0)
cv2.destroyAllWindows()