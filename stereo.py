import cv2
import math
from tqdm import tqdm

import matplotlib.pyplot as plt

class depth_map:
    def __init__(self, left_file_name, right_file_name, strob_size, step):

        self.img_l = cv2.resize( cv2.imread(left_file_name, 0), (300,400))
        self.img_r = cv2.resize( cv2.imread(right_file_name, 0), (300,400))

        # self.img_l = cv2.imread(left_file_name, 0)
        # self.img_r = cv2.imread(right_file_name, 0)

        self.strob_size = strob_size
        self.strob_n = strob_size**2
        self.step = step

        self.height = self.img_l.shape[0]
        self.width = self.img_l.shape[1]    

        # Параметры камер
        self.alpha = 81 * math.pi / 180  # rad
        self.f = 5.23        # mm
        self.base = 200      # mm
        self.rad_na_pix = self.alpha/self.width  # rad/pixel
        self.mm_px = self.f * math.tan(math.radians(40.5)) / (self.width / 2)

    def MAD(self, Im1, Im2):
        '''Функция отклонений'''
        result = abs(Im1-Im2)
        result = result.sum()/self.strob_n
        return result
    
    def KOR(self, Im1, Im2):
        '''Корреляционная функция'''
        m1 = Im1.sum()/self.strob_n
        m2 = Im2.sum()/self.strob_n
        i1 = Im1 - m1
        i2 = Im2 - m2
        k = i1 * i2
        return k.sum()/self.strob_n

    def find_point_on_right(self, strob, row):
        '''Поиск строба с левого изображения на правом'''
        response = []
        
        min_value = math.inf
        idx = 0

        for j in range(self.strob_size // 2, self.width - self.strob_size // 2 - 1):
            
            right = self.img_r[row - self.strob_size // 2 : row + self.strob_size // 2 + 1, j - self.strob_size // 2: j + self.strob_size // 2 + 1]
            k = self.MAD(strob,right)     
            response.append(k)
            if (k <= min_value):
                    min_value = k
                    idx = len(response)-1

        return idx
    
    def calc_dist(self, row, i):
        '''Вычисление расстояния по координатам точки на двух изображениях'''
        strob = self.img_l[row - self.strob_size // 2 : row + self.strob_size // 2 + 1, i - self.strob_size // 2: i + self.strob_size // 2 + 1]
                
        idx = self.find_point_on_right(strob, row)

        pol_width = self.width// 2  
        d_l = (i - pol_width) * self.rad_na_pix
        d_p = (pol_width - idx) * self.rad_na_pix
        
        phi1 = math.atan(d_l)
        phi2 = math.atan(d_p)

        if (math.tan(phi1) + math.tan(phi2) != 0):
            ds = (self.base / (math.tan(phi1) + math.tan(phi2))) / 1000
            if ds <=0:
                ds = 1.5
            elif ds >=1.5:
                ds = 1.5
        else :
            ds = 1.5
        
        return ds

    def calc_depth_row(self, row):
        '''Вычисления расстояния проход по строчке'''

        dist = []

        for i in range(self.strob_size // 2, self.width - self.strob_size // 2, self.step):
            dist.append(self.calc_dist(row, i))
        return dist

    def show_map(self):
        '''Вывод карты глубины'''
        plt.scatter(x=self.x, y=self.y, c=self.d, cmap="summer")
        plt.colorbar(orientation="horizontal").set_label(label='Дальность',size=15,weight='bold')
        plt.show()

    def calc_depth_map(self):
        '''Вычисление карты глубины'''
        self.d = []
        self.x = []
        self.y = []
        for i in tqdm(range(self.strob_size//2, self.height-self.strob_size//2, self.step)):
            self.y[len(self.x):] =  [self.height-i for k in range(self.strob_size//2, self.width-self.strob_size//2,self.step)]
            self.x[len(self.y):] = [k for k in range(self.strob_size//2, self.width-self.strob_size//2, self.step)]
            self.d[len(self.d):] = self.calc_depth_row(i)
            # b = len(self.x)
            # v = len(self.y)
            # pp = len(self.d)

