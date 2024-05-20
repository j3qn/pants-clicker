import eel
import time
import win32gui
import win32api
import win32con
import threading
import random
import os
import winsound



os.system('cls')
username = input("user: ")


delay_cps = 10

eel.init('web')

@eel.expose                    
def say_hello_py(x):
 
    print('Hello from %s' % x)


   

@eel.expose
def set_cps(cps):
    global delay_cps
    print('CPS set to %s' % cps)
    delay_cps = int(cps)


eel.say_hello_js(username)   

runningLeft = False
workInMenus = False
shakeEffect = False
shakeEffectValue = 20
runningRight = False
sound = False
soundInput = ""
delay_cps_right = 10

window = win32gui.FindWindow("LWJGL", None)

@eel.expose
def toggleSound():
    global sound
    if sound:
        sound = False
    else:
        sound = True
    print('Sound toggled to %s' % sound)

@eel.expose
def setSound(soundInput1):
    global soundInput
    soundInput = soundInput1
    print('Sound set to %s' % sound)



@eel.expose
def toggleRightClicker():
    global runningRight
    if runningRight:
        runningRight = False
        print('Right clicker toggled to %s' % runningRight)
    else:
        runningRight = True
        rightClicker_thread = threading.Thread(target=rightClicker, daemon=True)
        rightClicker_thread.start()
        print('Right clicker toggled to %s' % runningRight)
    
@eel.expose
def set_cpsRight(cps):
    global delay_cps_right
    print('CPS set to %s' % cps)
    delay_cps_right = int(cps)

@eel.expose
def workInMenusToggle():
    global workInMenus
    if workInMenus:
        workInMenus = False
    else:
        workInMenus = True
    print('Work in menus toggled to %s' % workInMenus)

@eel.expose
def shakeEffectValueSet(value):
    global shakeEffectValue
    shakeEffectValue = int(value)
    print('Shake effect value set to %s' % shakeEffectValue)

@eel.expose
def shakeEffectToggle():
    global shakeEffect
    if shakeEffect:
        shakeEffect = False
    else:
        shakeEffect = True
    print('Shake effect toggled to %s' % shakeEffect)

@eel.expose
def destruct():
   
    global runningLeft
    runningLeft = False

@eel.expose
def toggleLeftClicker():
    global runningLeft
    if runningLeft:
        runningLeft = False
        print('Left clicker toggled to %s' % runningLeft)
    else:
        runningLeft = True
        leftClicker_thread = threading.Thread(target=leftClicker, daemon=True)
        leftClicker_thread.start()
        

    
    
@eel.expose
def leftClicker():
    global window, workInMenus
    while runningLeft:
        currentWindow = win32gui.GetForegroundWindow()
        if currentWindow != window:
            window = win32gui.FindWindow("LWJGL", None)

        if not workInMenus:
            cursorInfo = win32gui.GetCursorInfo()[1]
            if cursorInfo > 50000 and cursorInfo < 100000:
                            time.sleep(1 / delay_cps)

                            continue
        if win32api.GetAsyncKeyState(0x01):
        

            if sound and not soundInput == "":
                winsound.PlaySound(f"./assets/{soundInput}", winsound.SND_ASYNC)
            else:
                pass
            start_time = time.time()

            time.sleep(random.uniform(0.0100, 0.0200))

            delay = delay_cps / 1000

            random_drops = random.uniform(40 / 1000, 10 / 1000)

            win32api.SendMessage(window, win32con.WM_LBUTTONDOWN, 0, 0)
            time.sleep(random_drops)
            win32api.SendMessage(window, win32con.WM_LBUTTONUP, 0, 0)

            elapsed_time = time.time() - start_time
            remaining_delay = max(0, delay - elapsed_time)
            time.sleep(remaining_delay)

            if elapsed_time + remaining_delay < 1 / delay_cps:
                time.sleep((1 / delay_cps) - (elapsed_time + remaining_delay))
            if shakeEffect and currentWindow == window:
                currentPos = win32api.GetCursorPos()
                direction = random.randint(0, 3)
                pixels = random.randint(-shakeEffectValue, shakeEffectValue)

                if direction == 0:
                    win32api.SetCursorPos((currentPos[0] + pixels, currentPos[1] - pixels))
                elif direction == 1:
                        win32api.SetCursorPos((currentPos[0] - pixels, currentPos[1] + pixels))
                elif direction == 2:
                    win32api.SetCursorPos((currentPos[0] + pixels, currentPos[1] + pixels))
                elif direction == 3:
                    win32api.SetCursorPos((currentPos[0] - pixels, currentPos[1] - pixels))

            else:
                 pass
                 
            
              
@eel.expose
def rightClicker():
    global window
    while runningRight:
        currentWindow = win32gui.GetForegroundWindow()
        if currentWindow != window:
            window = win32gui.FindWindow("LWJGL", None)

        if win32api.GetAsyncKeyState(0x02):


            delay = 1 / delay_cps_right


            win32api.SendMessage(window, win32con.WM_RBUTTONDOWN, 0, 0)
            time.sleep(delay)
            win32api.SendMessage(window, win32con.WM_RBUTTONUP, 0, 0)

options = {
      'mode': "chrome",
     'borderless': True,
     'size': (700, 440)
}

eel.start('gui.html', options=options, suppress_error=True)  





