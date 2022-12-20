import PySimpleGUI as sg
import pyautogui
import time

pyautogui.FAILSAFE = True

## All Counters
## To the bot not to buy the already bought because when it's bought, it turns black, and the bot may not recognise the difference otherwise
covenantchecked = 0
mysticchecked = 0

## Counters
refreshcounter = 0
covenantbought = 0
mysticbought = 0

## Scroll the shop
def movemouseup():
    height = 1920
    width = 1080
    pyautogui.moveTo(height / 2, width / 2)
    pyautogui.drag(xOffset=0, yOffset=-310, duration=1)

## Check if there's the wanted items
def check():
    time.sleep(.85)
    mys_check = pyautogui.locateOnScreen('mystic.png', confidence=.9, grayscale=True)
    cov_check = pyautogui.locateOnScreen('covenant.png', confidence=.9, grayscale=True)
    global covenantchecked
    covenantchecked = 0
    global mysticchecked
    mysticchecked = 0
    if cov_check:
        covenantchecked += 1
        buycovenant()
    if mys_check:
        mysticchecked += 1
        buymystic()
    else:
        pass

## Check if there's the wanted items after scrolling
def checksecond():
    time.sleep(.75)
    mys_check = pyautogui.locateOnScreen('mystic.png', confidence=.9, grayscale=True)
    cov_check = pyautogui.locateOnScreen('covenant.png', confidence=.9, grayscale=True)
    if cov_check:
        if covenantchecked == 0:
            buycovenant()
        else:
            pass
    if mys_check:
        if mysticchecked == 0:
            buymystic()
    else:
        pass
        time.sleep(.75)

## Buy the covenant
def buycovenant():
    global covenantbought
    covenantbought += 1
    cov_check = pyautogui.locateOnScreen('covenant.png', confidence=.9, grayscale=True)
    if cov_check:
        pyautogui.click(x=cov_check[0]+800, y=cov_check[1]+100)
        time.sleep(1)
        pyautogui.click('covenantconfirmation.png')
    else:
        pass

## Buy the mystic
def buymystic():
    global mysticbought
    mysticbought += 1
    mys_check = pyautogui.locateOnScreen('mystic.png', confidence=.9, grayscale=True)
    if mys_check:
        pyautogui.click(x=mys_check[0]+800, y=mys_check[1]+100)
        time.sleep(1)
        pyautogui.click('mysticconfirmation.png')
    else:
        pass

## Refresh the shop
def refresh():
    refresh_check = pyautogui.locateOnScreen('refresh.png', confidence=0.95)
    if refresh_check:
        pyautogui.click(refresh_check)
        time.sleep(.25)
        global refreshcounter
        refreshcounter += 1
        pyautogui.click('confirm.png')
    else: 
        pass

## PySimpleGUI
layout = [
    [sg.Text("How many skystones do you wish to use?")],
    [sg.Input(key='wishedsky')],
    [sg.Button('Shop Roll'), sg.Button('Quit')],
    [sg.Text('Skystones wished: ',key='skywished')],
    [sg.Text(f'Mystic Bought: {mysticbought}',key='mystic')],
    [sg.Text(f'Covenant Bought: {covenantbought} ',key='covenant')],
    [sg.Text(f'Times refreshed:  {refreshcounter}' ,key='refresh')],
]

window = sg.Window("E7 Auto Refresher", layout)   
## SimpleGUI While
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Quit':
        break
    if event == 'Shop Roll':
        numsky = int(values['wishedsky'])
        timeswillrefresh = int(numsky / 3)
        window['skywished'].update(f'The bot will row now with {numsky} skystones and will be refreshed {timeswillrefresh} times')

        while timeswillrefresh > refreshcounter:
             check()
             movemouseup()
             checksecond()
             refresh()
             window['refresh'].update(f'Times it has been refreshed: {refreshcounter}')
             window['covenant'].update(f'Covenants found: {covenantbought}')
             window['mystic'].update(f'Mystic found: {mysticbought}')

window.close()


