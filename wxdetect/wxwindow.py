import cv2

class WXWindow:
    def __init__(self, x = None, y = None, w = None, h = None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw_boundary(self, img, color=(255,0,0), thickness=1):
        cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h), color=color, thickness=thickness)