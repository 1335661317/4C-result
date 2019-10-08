import os
import time
import sys
import numpy as np
import cv2
from PIL import Image

# 1280 * 720
# screen_x = 720
# screen_y = 1280
# recording_x = 360
# recording_y = 1170
# start_x = 355
# start_y = 834

# 1920 * 1080
screen_x = 1080
screen_y = 1920
recording_x = 541
recording_y = 1816
start_x = 526
start_y = 1086


def pull_screenshot():
    os.system('adb shell screencap -p /sdcard/autojump.png')
    os.system('adb pull /sdcard/autojump.png ./autojump.png')

fa = None

def init(n):
    global fa
    fa = list(range(n))
    pass

def find_set(x):
    global fa
    if fa[x] != x:
        fa[x] = find_set(fa[x])
    return fa[x]

def union_set(x,y):
    global fa
    x = find_set(x)
    y = find_set(y)
    fa[x] = y

def start_recording():
    os.system('adb shell input tap {} {}'.format(recording_x,recording_y))
    time.sleep(2)
    os.system('adb shell input tap {} {}'.format(recording_x,recording_y))

def touch(pos):
    print('adb shell input tap {} {}'.format(pos[1],pos[0]))
    os.system('adb shell input tap {} {}'.format(pos[1],pos[0]))

def get_means(poss):
    # 因为只是为了触控需要，直接 random 算了
    # res = np.random.choice(poss)
    # return [res // screen_x, res % screen_x]

    # # 求一些点的平均值
    x = 0
    y = 0
    le = len(poss)
    for i in poss:
        x += i // screen_x
        y += i % screen_x
    return [x // le, y // le]

def get_button_pos(vis):
    mv = [[-1,0],[1,0],[0,-1],[0,1]]
    init(vis.shape[0] * vis.shape[1])
    n = vis.shape[0]
    m = vis.shape[1]
    for i in range(n):
        for j in range(m):
            if vis[i][j]:
                for k in mv:
                    xx = i + k[0]
                    yy = j + k[1]
                    if xx >= n or xx < 0 or yy >= m or yy < 0 or vis[xx][yy] == False:
                        continue
                    union_set(i * m + j,xx * m + yy)
    pos = []
    for i in range(n * m):
        pos.append([])
    for i in range(n * m):
        pos[find_set(i)].append(i)
    res = []
    for i in range(n * m):
        le = len(pos[i])
        if le > 300:
            res.append(get_means(pos[i]) + [le])
    return res


def find_nextbutton():
    pull_screenshot()

    button_color = [100, 50, 60]        # next 右箭头颜色
    next_button_color = [112, 67, 75]   # 多选题 下一题的按钮颜色
    end_button_color = [103, 54, 63]    # 完成学习 颜色
    path = './autojump.png'
    image = cv2.imread(path)

    vis = np.all(image == next_button_color,axis=2) | np.all(image == button_color,axis=2) | np.all(image == end_button_color,axis=2)
    pos = get_button_pos(vis)
    exec_button(image, pos)


def exec_button(image, pos):
    print(pos)
    for i in pos:
        if i[2] == 4552 or i[2] == 4549 or i[2] == 4504:
            # 4554 4549 为暂停播放 4504 为提示
            start_recording()
            time.sleep(2)
            break
    for i in pos:
        if i[2] == 4955:
            # 右箭头
            touch(i)
            return
        if i[2] == 5565:
            # 完成学习
            touch(i)
            exit()

    for i in pos:
        # 填词
        touch(i)
        time.sleep(0.01)


if __name__ == '__main__':
    # 设置系统最大递归深度 3000
    sys.setrecursionlimit(3000)
    total_time = time.time()

    touch((start_y, start_x))
    time.sleep(.5)

    while True:
        start_time = time.time()
        find_nextbutton()
        time.sleep(.5)
        print('time: ',time.time() - start_time)
    print('total time: ',time.time() - total_time)
