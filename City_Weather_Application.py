#------------------------------------------------------------------------
# City Weather Application

import pyowm

temperature = ""
tempc = ""
cityw = ""
tempInC =""

#getWeather method receives a city as an input parameter and fetches the weather details of the
#particular city from the open weather map server and returns it back with all the details
def getWeather(city):
     #global variables
     global temperature
     global tempc
     global cityw
     global tempInC

     owm = pyowm.OWM('450e64430978f09103b1e868a68315af') # init class with unique key
     mgr = owm.weather_manager()  
     observation  = mgr.weather_at_place(city)  
     w = observation.weather    
     tempInC = w.temperature('celsius')     # in degrees c
     tempInF = w.temperature('fahrenheit')  # in degrees f
     temp = w.temperature()                 
     
     values_view_celsius = tempInC.values()
     value_iterator_celsius = iter(values_view_celsius)
     first_value_celsius = next(value_iterator_celsius)
     
     tempc = str(first_value_celsius)+" °C"
     tempcdetailed = str(tempInC)+" °C"

     values_view_fahrenheit = tempInF.values()
     value_iterator_fahrenheit = iter(values_view_fahrenheit)
     first_value_fahrenheit = next(value_iterator_fahrenheit)
     
     tempf = str(first_value_fahrenheit)+" °F"
     tempfdetailed = str(tempInF)+" °F"
   
     result = []
     result.append(tempc)  
     result.append(tempf)

     status = w.detailed_status

     result.append(f"In {city} it is currently " + str(int(tempInC['temp'])) + " degrees and " + status)
     result.append(w.weather_icon_name)
     result.append(f"City:{city} = {tempcdetailed}")  
     result.append(f"City:{city} = {tempfdetailed}")
     return result
#------------------------------------------------------------------------

import PySimpleGUI as sg

from PIL import Image, ImageTk

import time

# definition area
sg.theme('Black')   # Color Theme
fonts1 = ('Any', 30)

# All the elements inside the window
output3 = sg.Text()
output4 = sg.Text()
output5 = sg.Text()
output6 = sg.Text()
layout = [  [sg.Text('                      Welcome to City Weather Application')],
            [sg.Text('Input City to find the current weather forecast'), sg.InputText()],
            [sg.Text(size=(70, 2), key='output1')],
            [sg.Text(size=(70, 2), key='output2')],
            [output5],
            [output6],
            [output3],       
            [sg.Image(size=(300, 300), key='-IMAGE-')],
            [output4],
            [sg.Text(size=(100, 1), key='-OUT-')],
            [sg.Button('Find it'), sg.Button('Cancel')] ]

# Creating the Window
window = sg.Window('City Weather Application', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])  
    result = getWeather(values[0])
    print("Calling weather again")
    print("\nresult ",result)
    window['output1'].update(value="Temperature in Degree Celsius : "+result[0])
    window['output2'].update(value="Temperature in Degree Fahrenheit : "+result[1])
    output5.update(value="Detailed Temperature specifications in Degree Celsius : "+result[4])
    output6.update(value="Detailed Temperature specifications in Degree Fahrenheit : "+result[5])
    output3.update(value=result[2])
    im = Image.open(result[3]+".png")
    # Convert im to ImageTk.PhotoImage after window finalized
    image = ImageTk.PhotoImage(image=im)
    # Update image in sg.Image
    window['-IMAGE-'].update(data=image)
    #Timer Logic to fetch the weather details after an interval of 30 minutes
    counter = 1800
    output4.update("Count Down Started! The Weather will get automatically updated after 30 minutes...")
    while True:
         event, values = window.read(timeout=11)
         if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
              break
         window['-OUT-'].update(counter)
         counter = counter-1
         time.sleep(1)
         if counter<1:
              break
     
window.close()

