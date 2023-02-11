import threading
import time

import keyboard
import pyautogui
import PySimpleGUI as sg

pyautogui.FAILSAFE = True

## Counters to PyAutoGUI
refresh_counter = 0
bought_covenant = 0
bought_mystic = 0

## Check if they stop key was pressed
keyboard_pressed = False

def on_keyboard_press(e):
    global keyboard_pressed
    keyboard_pressed = True

keyboard.on_press_key("f5", on_keyboard_press)

## Check if the purchase was made or not
purchased_items = []

## Scroll the shop
def scroll_mouse_upwards():
    height = 1920
    width = 1080
    pyautogui.moveTo(height / 2, width / 2)
    pyautogui.drag(xOffset=0, yOffset=-310, duration=1)

## Inner function to check if the item is already bought or not
def check_purchase(check_image, buy_image):
    global bought_mystic
    global bought_covenant
    item_check = pyautogui.locateOnScreen(check_image, confidence=.9, grayscale=True)
    if item_check and check_image not in purchased_items:
        purchased_items.append(check_image)
        time.sleep(.35)
        if check_image == 'images/covenant.png':
            bought_covenant += 1
        elif check_image == 'images/mystic.png':
            bought_mystic += 1
        time.sleep(.5)
        pyautogui.click(x=item_check[0]+800, y=item_check[1]+100)
        time.sleep(1)
        pyautogui.click(buy_image)

## First check
def check():
    time.sleep(.95)
    check_purchase('images/covenant.png', 'images/covenantconfirmation.png')
    check_purchase('images/mystic.png', 'images/mysticconfirmation.png')

## Restart check
def restart_check():
    purchased_items.clear()

## Refresh the shop
def refresh():
    refresh_check = pyautogui.locateOnScreen('images/refresh.png', confidence=0.95)
    if refresh_check:
        pyautogui.click(refresh_check)
        time.sleep(.4)
        global refresh_counter
        refresh_counter += 1
        pyautogui.click('images/confirm.png')

## PySimpleGUI
sg.theme('DarkBlack')
layout = [
    [sg.Text('!!!!!!!!! The key to pause the refresher is "F5" !!!!!!!!!', text_color='red')],
    [sg.Text("How many skystones do you wish to use?", text_color='lightblue')],
    [sg.Input(key='wished_sky')],
    [sg.Button('Shop Roll'), sg.Button('Quit')],
    [sg.Text('Skystones wished: ',key='sky_wished')],
    [sg.Text(f'Mystic Bought: {bought_mystic}',key='mystic')],
    [sg.Text(f'Covenant Bought: {bought_covenant} ',key='covenant')],
    [sg.Text(f'Times refreshed:  {refresh_counter}' ,key='refresh')],
]

## Main Function
def main_function(times_will_refresh, window):
    global keyboard_pressed
    while times_will_refresh > refresh_counter:
        if keyboard_pressed:
            break
        check()
        scroll_mouse_upwards()
        check()
        refresh()
        window['refresh'].update(f'Times it has been refreshed: {refresh_counter}')
        window['covenant'].update(f'Covenants found: {bought_covenant}')
        window['mystic'].update(f'Mystic found: {bought_mystic}')

window = sg.Window("E7 Auto Refresher", layout)


## SimpleGUI While
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Quit':
        break
    if event == 'Shop Roll':
        num_of_sky = int(values['wished_sky'])
        times_will_refresh = int(num_of_sky / 3)
        window['sky_wished'].update(f'The bot will row now with {num_of_sky} skystones and will be refreshed {times_will_refresh} times')

        t = threading.Thread(target=main_function, args=(times_will_refresh, window))
        t.start()
            

window.close()