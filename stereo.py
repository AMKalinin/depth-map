import cv2
import math
import numpy as np

import matplotlib.pyplot as plt


def MAD(Im1, Im2):
    size = len(Im1) # Размер стробов
    N = size*size
    result = abs(Im1-Im2)
    result = result.sum()/N
    return result

def KOR(Im1, Im2):
    size = len(Im1)
    N = size*size
    m1 = Im1.sum()/N
    m2 = Im2.sum()/N
    i1 = Im1 - m1
    i2 = Im2 - m2
    k = i1 * i2
    return k.sum()/N

def Row(ImL, ImR, size, row, step):

    hight = ImL.shape[0]
    width = ImL.shape[1]

    alpha = 81 * math.pi / 180  # rad
    f = 5.23        # mm
    base = 200      # mm
    rad_na_pix = alpha/width  # rad/pixel
    mm_px = f * math.tan(math.radians(40.5)) / (width / 2)

    dist = []

    for i in range(size // 2, width - size // 2 - 1, step):

        

        strob = ImL[row - size // 2 : row + size // 2 + 1, i - size // 2: i + size // 2 + 1]
        response = []

        
        for j in range(size // 2, width - size // 2 - 1):
            
            right = ImR[row - size // 2 : row + size // 2 + 1, j - size // 2: j + size // 2 + 1]
            k = MAD(strob,right)     
            response.append(k)
        # plt.plot(response)
        # plt.show()
        m = response[0]
        ind = 0
        for t in range(len(response)):
            if (response[t] <= m):
                m = response[t]
                ind = t
        #print(i)

        pol_width = width// 2  
        d_l = (i - pol_width) * rad_na_pix
        d_p = (pol_width - ind) * rad_na_pix

        

        phi1 = math.atan(d_l)
        phi2 = math.atan(d_p)

        

        if (math.tan(phi1) + math.tan(phi2) != 0):
            ds = (base / (math.tan(phi1) + math.tan(phi2))) / 1000
            if ds <=0:
                dist.append(1.5)
            elif ds >=1.5:
                dist.append(1.5)
            else:
                dist.append(ds)
        else :
            dist.append(1.5)
        
    return dist


Left = cv2.imread('img/L.jpg', 0);
Right = cv2.imread('img/R.jpg', 0);
strob_size = 5 
row_number = 725
step = 3

# 605, 1080 книга угол
#660 980 корона

h = Left.shape[0]
w = Left.shape[1]

#d = Row(Left, Right, strob_size, row_number, step)
d = []
x = []
y = []
for i in range(strob_size//2, h-strob_size//2, step):
    print(i)
    y[len(x):] =  [h-i for k in range(strob_size//2,w-strob_size//2,step)]
    x[len(y):] = [k for k in range(strob_size//2, w-strob_size//2, step)]
    d[len(d):] = Row(Left, Right, strob_size, i, step)

plt.scatter(x=x, y=y, c=d, cmap="summer")
plt.colorbar(orientation="horizontal").set_label(label='Дальность',size=15,weight='bold')
plt.show()

