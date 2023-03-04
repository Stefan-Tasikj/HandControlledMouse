import pyautogui
from threading import Thread
#kwargs={'duration': 0.001}
def movement(x,y):
    threaded = Thread(target=pyautogui.moveTo, args=(x, y),kwargs={'duration': 0.0001} )
    movethread(threaded)
def movethread(recieving):
     recieving.start()