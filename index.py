# -*- coding: utf-8 -*-    
from cv2 import cv2

from captcha.solveCaptcha import solveCaptcha

from os import listdir
from src.logger import logger, loggerMapClicked
from random import randint
from random import random
import pygetwindow
import numpy as np
import mss
import pyautogui
import time
import sys

import yaml


msg = """
                                                _

>>---> Bot começou a rodar!

>>---> Acesse: https://github.com/sCryptoHelp/zodiacs-bot

>>---> Pressione ctrl + c para parar o bot.

>>---> Abra o navegador com o Zodiacs conectado

"""


print(msg)
time.sleep(5)


if __name__ == '__main__':
    stream = open("config.yaml", 'r')
    c = yaml.safe_load(stream)

ct = c['threshold']
ch = c['home']

pause = c['time_intervals']['interval_between_moviments']
pyautogui.PAUSE = pause

pyautogui.FAILSAFE = False
hero_clicks = 0
login_attempts = 0
last_log_is_progress = False



def addRandomness(n, randomn_factor_size=None):
    if randomn_factor_size is None:
        randomness_percentage = 0.1
        randomn_factor_size = randomness_percentage * n

    random_factor = 2 * random() * randomn_factor_size
    if random_factor > 5:
        random_factor = 5
    without_average_random_factor = n - randomn_factor_size
    randomized_n = int(without_average_random_factor + random_factor)

    return int(randomized_n)

def moveToWithRandomness(x,y,t):
    pyautogui.moveTo(addRandomness(x,10),addRandomness(y,10),t+random()/2)


def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

def load_images():
    file_names = listdir('./targets/')
    targets = {}
    for file in file_names:
        path = 'targets/' + file
        targets[remove_suffix(file, '.png')] = cv2.imread(path)

    return targets

images = load_images()

def show(rectangles, img = None):

    if img is None:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            img = np.array(sct.grab(monitor))

    for (x, y, w, h) in rectangles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255,255), 2)

    cv2.imshow('img',img)
    cv2.waitKey(0)





def clickBtn(img,name=None, timeout=3, threshold = ct['default']):
    logger(None, progress_indicator=True)
    if not name is None:
        pass

    start = time.time()
    while(True):
        matches = positions(img, threshold=threshold)
        if(len(matches)==0):
            hast_timed_out = time.time()-start > timeout
            if(hast_timed_out):
                if not name is None:
                    pass

                return False
            continue

        x,y,w,h = matches[0]
        pos_click_x = x+w/2
        pos_click_y = y+h/2

        moveToWithRandomness(pos_click_x,pos_click_y,1)
        pyautogui.click()
        return True


def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))

        return sct_img[:,:,:3]

def positions(target, threshold=ct['default'],img = None):
    if img is None:
        img = printSreen()
    result = cv2.matchTemplate(img,target,cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)


    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def scroll(clickAndDragAmount):

    flagScroll = positions(images['scroll-bar'], threshold = ct['base_position'])
    
    if (len(flagScroll) == 0):
        return
    x,y,w,h = flagScroll[len(flagScroll)-1]

    logger("Scroll")
    moveToWithRandomness(x+10,y,1)

    pyautogui.dragRel(0,clickAndDragAmount,duration=1, button='left')

def scrollMax(clickAndDragAmount):

    flagScroll = positions(images['scroll-bar-max'], threshold = ct['base_position'])
    
    if (len(flagScroll) == 0):
        return
    x,y,w,h = flagScroll[len(flagScroll)-1]

    logger("ScrollMax")
    moveToWithRandomness(x+20,y+100,1)

    pyautogui.dragRel(0,clickAndDragAmount,duration=1, button='left')


def goToRace():

    scrollMax(200)
    gasBar = ''
    typeRace = ''

    if ct['type_race'] == 'quickRace':
        typeRace = 'quick-race'
    else:
        typeRace = 'comun-race'

    if(len(positions(images['racing-time'], threshold=ct['commom_position'])) == 0):
        if len(positions(images['gas-bar5'], threshold=ct['commom_position'])) > 0:
            gasBar = 'gas-bar5'
        else:
            if len(positions(images['gas-bar4'], threshold=ct['commom_position'])) > 0:
                gasBar = 'gas-bar4'
            else:
                if len(positions(images['gas-bar3'], threshold=ct['commom_position'])) > 0:
                    gasBar = 'gas-bar3'
                else:
                    if len(positions(images['gas-bar2'], threshold=ct['commom_position'])) > 0:
                        gasBar = 'gas-bar2'
                    else:
                        if len(positions(images['gas-bar1'], threshold=ct['commom_position'])) > 0:
                            gasBar = 'gas-bar1'
        if gasBar != '':
            logger("Located car")

            if clickBtn(images[gasBar], name='commom_position', timeout=1):
                if len(positions(images['Expired'], threshold=ct['commom_position'])) == 0:
                    if len(positions(images[typeRace], threshold=ct['commom_position'])) > 0:
                        if clickBtn(images[typeRace], name='commom_position', timeout=1):
                            
                            time.sleep(1)
                            if typeRace == 'quick-race':
                                time.sleep(1)
                                clickBtn(images['QR-Start'], name='commom_position', timeout=1)
                                time.sleep(1)

                            time.sleep(2)
                            while True:
                                if len(positions(images['racing-time'], threshold=ct['commom_position'])) <= 0:
                                    break
                                else:
                                    time.sleep(3)
                                    logger("Waiting... ...")
                
        else:
            logger("Car not found")
            scroll(50)

def checkResult():
    time.sleep(1)
    clickBtn(images['check-result'], name='commom_position', timeout=1)   

def claimRace():
    time.sleep(1)
    clickBtn(images['claim-race'], name='commom_position', timeout=1)   

def CheckOk():
    clickBtn(images['ok-btn'], name='commom_position', timeout=1)    




def main():
    time.sleep(3)
    t = c['time_intervals']
    

    windows = []

    for w in pygetwindow.getWindowsWithTitle('zodiacs'):
        windows.append({
            "window": w,
            "lessPosition":[],            
            })

    while True:
        now = time.time()
        logger("Starting action")
        goToRace()
        checkResult()
        claimRace()
        CheckOk()
            
main()



