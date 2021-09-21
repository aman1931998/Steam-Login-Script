import pyautogui as pg
import time
pg.FAILSAFE = False

while True:
    print(pg.position())
    time.sleep(1)