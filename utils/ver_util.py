import cv2  # cv2 图像处理库
import numpy as np  # numpy 数学函数库
import pandas as pd  # pandas 数据分析库
import math


# x方向一阶导中值
def get_dx_median(dx, x, y, w, h):
    return np.median(dx[y:(y + h), x])


# 预处理
def pre_process(img_path):
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR) # 从指定的文件中加载图像并返回,1 为彩色图像
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转成灰度图像

    _, binary = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)  # 将灰度图像转成二值图像

    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 查找轮廓

    rect_area = []
    rect_arc_length = []
    cnt_infos = {}

    for i, cnt in enumerate(contours):
        if cv2.contourArea(cnt) < 5000 or cv2.contourArea(cnt) > 25000:
            continue

        x, y, w, h = cv2.boundingRect(cnt)
        cnt_infos[i] = {'rect_area': w * h,  # 矩形面积
                        'rect_arclength': 2 * (w + h),  # 矩形周长
                        'cnt_area': cv2.contourArea(cnt),  # 轮廓面积
                        'cnt_arclength': cv2.arcLength(cnt, True),  # 轮廓周长
                        'cnt': cnt,  # 轮廓
                        'w': w,
                        'h': h,
                        'x': x,
                        'y': y,
                        'mean': np.mean(np.min(img[y:(y + h), x:(x + w)], axis=2)),  # 矩形内像素平均
                        }
        rect_area.append(w * h)
        rect_arc_length.append(2 * (w + h))
    dx = cv2.Sobel(img, -1, 1, 0, ksize=5)

    return img, dx, cnt_infos

# 计算移动的距离
def calculate_distance(img_path):
    img, dx, cnt_infos = pre_process(img_path)
    df = pd.DataFrame(cnt_infos).T
    df.head()
    df['dx_mean'] = df.apply(lambda x: get_dx_median(dx, x['x'], x['y'], x['w'], x['h']), axis=1)
    df['rect_ratio'] = df.apply(lambda v: v['rect_arclength'] / 4 / math.sqrt(v['rect_area'] + 1), axis=1)
    df['area_ratio'] = df.apply(lambda v: v['rect_area'] / v['cnt_area'], axis=1)
    df['score'] = df.apply(lambda x: abs(x['rect_ratio'] - 1), axis=1)

    result = df.query('x>0').query('area_ratio<2').query('rect_area>5000').query('rect_area<20000').sort_values(
        ['mean', 'score', 'dx_mean']).head(2)
    return result.x.values[0]

