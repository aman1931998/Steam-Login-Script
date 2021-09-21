# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 12:00:48 2021

@author: aman1
"""

import os
from PIL import Image, ImageGrab
import cv2
import numpy as np
import time

x1, y1 = 863, 744
x2, y2 = 905, 756

time.sleep(5)
image = ImageGrab.grab([x1, y1, x2, y2]).convert('RGB')
image_array = np.array(image)

accepted_colors = [114, 142, 15]
time.sleep(5)
haystack = ImageGrab.grab([x1 - 10, y1 - 10, x2 + 10, y2 + 10]).convert("RGB")

def find_matches_green(haystack, x1, y1, x2, y2, accepted_colors):
    arr_h = np.array(np.asarray(haystack)[:, :, :3], 'uint8')

    y_h, x_h = arr_h.shape[:2]
    y_n, x_n = y2-y1, x2-x1

    xstop = x_h - x_n + 1
    ystop = y_h - y_n + 1
    for xmin in range(0, xstop):
        for ymin in range(0, ystop):
            xmax = xmin + x_n
            ymax = ymin + y_n

            arr_s = arr_h[ymin:ymax, xmin:xmax]     # Extract subimage
            avg_red, avg_green, avg_blue = np.average(arr_s[:, :, 0]), np.average(arr_s[:, :, 1]), np.average(arr_s[:, :, 2])
            print(avg_red, avg_green, avg_blue, sep = "     ")
            if avg_red in range(accepted_colors[0] - 1, accepted_colors[0] + 2) and \
                avg_green in range(accepted_colors[1] - 1, accepted_colors[1] + 2) and \
                    avg_blue in range(accepted_colors[2] - 1, accepted_colors[2] + 2):
                return xmin, ymin
    return None, None

np.save(os.path.join('email_snippets', 'steam_profile_privacy_options_options.npy'), image_array)

