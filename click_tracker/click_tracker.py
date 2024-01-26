# 一个用来维护鼠标移动轨迹的类

import cv2

class ClickTracker(object):
    def __init__(self):
        self.track = [(0, 0)]
        self.dx = 0
        self.dy = 0
    
    def add_point(self, x, y):
        self.dx += x - self.track[-1][0]
        self.dy += y - self.track[-1][1]
        self.track.append((x, y))

    def add_move(self, _dx, _dy):
        self.dx += _dx
        self.dy += _dy
        self.track.append((self.track[-1][0] + _dx, self.track[-1][1] + _dy))
    
    def go_back(self, n):
        self.add_point(self.track[-1])
    
    def goto_start(self):
        self.add_point(self.track[0])
    
    def draw_track(self, img, color=(255,0,0), thickness=1):
        for i in range(len(self.track) - 1):
            cv2.line(img, self.track[i], self.track[i+1], color=color, thickness=thickness)

    def get_dx(self):
        return self.dx
    
    def get_dy(self):
        return self.dy