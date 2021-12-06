import Gamepad
import subprocess


def listener():

    gamepad = Gamepad.Gamepad()

    if Gamepad.available():
        gamepad = Gamepad.Gamepad()
    else:
        print('Controller not connected :(')


    keys = []
    while True:
        event = gamepad.getNextEvent()
        if event[1] in [6,7,10,11] and event[0]=='BUTTON':
            if event[2]==True:
                keys.append(event[1])
        if event[1] in [6,7,10,11] and event[0]=='BUTTON':
            if event[2]==False and event[1] in keys:
                keys.remove(event[1])
        keys.sort()
        if keys==[6,7,10,11]:
            pidd = ''
            result = subprocess.run(['ps', '-a'], capture_output=True, text=True).stdout
            for item in result.split("\n"):
                if "snes9x" in item:
                    pidd = item.split(' ')
                    if pidd[0]=='':
                        pidd = pidd[1]
                    else:
                        pidd = pidd[0]
            subprocess.run(['kill', pidd])
