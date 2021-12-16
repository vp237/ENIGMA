import PySimpleGUI as sg
# on linux:
# sudo pip3 install pyserial
# /home/bruce/.local/lib/python3.5
# sudo python3.5 pic_target_3.py
#
# you can find out more about PySimleGUI at
# https://pysimplegui.readthedocs.io/en/latest/
#
# --event format to PIC--
# Four sharacters for each non-string event:
# pushbutton event 'b' + 2 digit button number + value (1,0)
# toggle sw event 't' + 2 digit button number + value (1,0)
# slider event 's' + 1-digit slider number + n digit value
# listbox event 'l' + + 1-digit listbox number + 1 digit selection number
# radio button 'r' + 1 digit group number + 1 digit selection numbr
# -- string --
# strings typed in the input line are sent in their entirety.
# -- reset --
# RESET has NO code on PIC!
# serial reset event sends a rs-232 BREAK which is connected
# through a filter to MCLR pin
#
# Python_TX_pin--(100ohm)--(+Schottky Diode-)------>(target MCLR pin)
#                                             |
#                                     (10uf)------(1kohm)
#                                        |           |
#                                        -------------
#                                             |
#                                         (PIC gnd)
#
import time
import serial
# open microcontroller serial port
# For windows the device will be 'COMx'
ser = serial.Serial('COM4', 115200, timeout=0.001)  # open serial port 38400

# sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
# This a heirachical list of items to be displayd in the window
# First list is first row controls, etc
# Buttons:
#   Realtime buttons respond to push-events
#   After the window is defined below, release events may be bound to each realtime button
#   The 'key' for each button must be of the form 'pushbutNN',
#   where 'NN' are digits 0-9 defining the button number
# Toggles:
#   Toggle switches are actually checkboxes
#   The 'key' for each checkbox must be of the form 'toggleNN',
#   where 'NN' are digits 0-9 defining the checkbox number
# Sliders
#   The 'key' for each slider must be of the form 'sliderN',
#   where 'N' is a digit 0-9 defining the slider number
#   Sliders can have any integer range which is handy for the application
# Text
#   The text input field acts like the one-line Arduino serial send box.
#   The multiline output box receives serial from the PIC. text typed here is ignored.
# Listbox
#   The 'key' for each listbox must be of the form 'listN',
#   where 'N' is a digit 0-9 defining the listbox number
#   Listbox as implemented can have only one selected value
# [sg.Text('LED Control',  background_color=heading_color)],
#             [sg.RealtimeButton('LED', key='pushbut01', font='Helvetica 12')],
#             #
#             [sg.Text('TFT LCD', background_color=heading_color)],
#             [sg.RealtimeButton('CLR LCD', key='pushbut02', font='Helvetica 12'),
#              sg.Checkbox('Dot Color', key='toggle01', font='Helvetica 12',enable_events=True)],
#             [sg.Text('Line Position'),
#             sg.Slider(range=(0,200), default_value=0, size=(22,15), key='slider1',
#              orientation='horizontal', font=('Helvetica', 12),enable_events=True)],
#             #
#             [sg.Text('Direct Digital Synthesis', background_color=heading_color)],
#             [sg.Radio('DDS', "radio1", default=True, key='radio1_1', enable_events=True),
#              sg.Radio('Vout', "radio1", key='radio1_2', enable_events=True),
#             sg.Listbox(values=['Sine', 'Square', 'Triangle'], key='list1', size=(10, 1),
#               select_mode='LISTBOX_SELECT_MODE_SINGLE', enable_events=True)],
#             #
#             [sg.Text('DDS Freq'),
#              sg.Slider(range=(20,1000), default_value=400, size=(22,15), key='slider2',
#              orientation='horizontal', font=('Helvetica', 12),enable_events=True)],
#             #
#             [sg.Text('   Vout   '),
#              sg.Slider(range=(0,2.00), default_value=0, size=(22,15), key='slider3', resolution=0.01,
#              orientation='horizontal', font=('Helvetica', 12),enable_events=True)],
#             #
#             [sg.Text('Serial data to PIC', background_color=heading_color)],
#             [sg.InputText('', size=(40,10), key='pic_input', do_not_clear=False,
#                 enable_events=False, focus=True),
#              sg.Button('Send', key='pic_send', font='Helvetica 12')],
#             #
#             [sg.Text('Serial data from PIC', background_color=heading_color)],
#             [sg.Multiline('', size=(50,10), key='console',
#                autoscroll=True, enable_events=False)],
#             #
#             [sg.Text('System Controls', background_color=heading_color)],
#             [sg.Button('Exit', font='Helvetica 12')],
#             [ sg.Checkbox('reset_enable', key='r_en',
#                         font='Helvetica 8', enable_events=True),
#              sg.Button('RESET PIC', key='rtg', font='Helvetica 8')
#             ]
font_spec = 'Courier 24 bold'
heading_color = '#2FB8AD'
alphabet_list = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
layout = [
    [sg.Text('Please Input Characters', background_color=heading_color)],
    [sg.InputText('', size=(40, 10), key='pic_input', do_not_clear=False,
                  enable_events=False, focus=True),
     sg.Button('Send', key='pic_send', font='Helvetica 12')],
    [sg.Text('Rotor 1 is the rightmost rotor, Rotor 3 is the leftmost rotor',
             background_color=heading_color)],
    [sg.Text('Rotor 1 encoding', background_color=heading_color)],
    [sg.InputText('', size=(40, 10), key='rotor1_input', do_not_clear=False,
                  enable_events=False, focus=True),
     sg.Button('Send', key='rotor1_send', font='Helvetica 12')],
    [sg.Text('Rotor 2 encoding', background_color=heading_color)],
    [sg.InputText('', size=(40, 10), key='rotor2_input', do_not_clear=False,
                  enable_events=False, focus=True),
     sg.Button('Send', key='rotor2_send', font='Helvetica 12')],
    [sg.Text('Rotor 3 encoding', background_color=heading_color)],
    [sg.InputText('', size=(40, 10), key='rotor3_input', do_not_clear=False,
                  enable_events=False, focus=True),
     sg.Button('Send', key='rotor3_send', font='Helvetica 12')],
    [sg.Text('Plugboard', background_color=heading_color)],
    [sg.InputText('', size=(40, 10), key='plugboard_input', do_not_clear=False,
                  enable_events=False, focus=True),
     sg.Button('Send', key='plugboard_send', font='Helvetica 12')],
    [sg.Text('Rotor 1 Letter', background_color=heading_color, size=(10, 1)), sg.Text('Rotor 2 Letter',
                                                                                      background_color=heading_color, size=(10, 1)), sg.Text('Rotor 3 Letter', background_color=heading_color, size=(10, 1))],
    [sg.Listbox(values=alphabet_list, key='list1', size=(10, 5),
                select_mode='LISTBOX_SELECT_MODE_SINGLE', enable_events=True), sg.Listbox(values=alphabet_list, key='list2', size=(10, 5),
                                                                                          select_mode='LISTBOX_SELECT_MODE_SINGLE', enable_events=True), sg.Listbox(values=alphabet_list, key='list3', size=(10, 5),
                                                                                                                                                                    select_mode='LISTBOX_SELECT_MODE_SINGLE', enable_events=True)],
    [sg.Text('Serial data from PIC', background_color=heading_color)],
    [sg.Multiline('', size=(50, 10), key='console',
                  autoscroll=True, enable_events=False)]
]

# change the colors in any way you like.
sg.SetOptions(background_color='#9FB8AD',
              text_element_background_color='#9FB8AD',
              element_background_color='#475841',  # '#9FB8AD',
              scrollbar_color=None,
              input_elements_background_color='#9FB8AD',  # '#F7F3EC',
              progress_meter_color=('green', 'blue'),
              button_color=('white', '#475841'),
              )

# Create the Window
window = sg.Window('ECE4760 Interface', layout, location=(0, 0),
                   return_keyboard_events=True, use_default_focus=True,
                   element_justification='c', finalize=True)

# Bind the realtime button release events <ButtonRelease-1>
# https://github.com/PySimpleGUI/PySimpleGUI/issues/2020
# window['pushbut01'].bind('<ButtonRelease-1>', 'r')

# # Event Loop to process "events"
# # event is set by window.read
# event = 0
# #
# #  button state machine variables
# button_on = 0
# button_which = '0'
#
#
while True:

    # time out paramenter makes the system non-blocking
    # If there is no event the call returns event  '__TIMEOUT__'
    event, values = window.read(timeout=20)  # timeout=10
    #
    # print(event)  # for debugging
    # if user closes window using windows 'x' or clicks 'Exit' button
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
#     #
#    #  # pushbutton events state machine
#     if event[0:3]  == 'pus' and button_on == 0 :
#        # 'b' for button, two numeral characters, a '1' for pushed, and a terminator
#        ser.write(('b' + event[7:9] + '1' + '\r').encode())
#        button_on = 1
#        button_which = event[7:9]
#     # releaase event signalled by the 'r'
#     elif (button_on == 1 and event[7:10] == button_which +'r') :
#        ser.write(('b'  + button_which + '0' + '\r').encode())
#        button_on = 0
#        button_which = ' '
    #
    # listbox
    if event[0:3] == 'lis':
        # get the list box index#
        listbox_value = window.Element(event).GetIndexes()
        ser.write(('l0' + event[4] + str(listbox_value[0]) + '\r').encode())
    #  #
    #  # radio button
    #  if event[0:3]  == 'rad'  :
    #     #print(event)
    #     # get the radio group ID and group-member ID radio1_2
    #     ser.write(('r0' + event[5] + event[7] + '\r').encode())

    #  # toggle switches
    #  if event[0:3]  == 'tog'  :
    #     # read out the toggle switches
    #     switch_state = window.Element(event).get()
    #     ser.write(('t' + event[6:8] + str(switch_state) + '\r').encode())
    #
    # # silder events
    # if event[0:3]  == 'sli'  :
    #    ser.write(('s ' + event[6] + " {:f}".format((values[event])) + '\r').encode())
    #
    # reset events
    # switch_state = window.Element('r_en').get()
    # if event[0:3] == 'rtg' and switch_state == 1 :
    #    # drops the data line for 100 mSec
    #    ser.send_break() #optional duration; duration=0.01
    #  #
    # The one-line text input button event
    if event == 'pic_send':
        # The text from the one-line input field
        input_state = window.Element('pic_input').get()
        # add <cr> for PIC
        input_state = '$p' + input_state + '\r'
        # zero the input field
        window['pic_input'].update('')
        # send to PIC protothreads
        ser.write((input_state).encode())
        #
    if event == "rotor1_send":
        # The text from the one-line input field
        input_state = window.Element('rotor1_input').get()
        # add <cr> for PIC
        input_state = '$i' + input_state + '\r'
        # zero the input field
        window['rotor1_input'].update('')
        # send to PIC protothreads
        ser.write((input_state).encode())
    if event == "rotor2_send":
        # The text from the one-line input field
        input_state = window.Element('rotor2_input').get()
        # add <cr> for PIC
        input_state = '$j' + input_state + '\r'
        # zero the input field
        window['rotor2_input'].update('')
        # send to PIC protothreads
        ser.write((input_state).encode())
    if event == "rotor3_send":
        # The text from the one-line input field
        input_state = window.Element('rotor3_input').get()
        # add <cr> for PIC
        input_state = '$k' + input_state + '\r'
        # zero the input field
        window['rotor3_input'].update('')
        # send to PIC protothreads
        ser.write((input_state).encode())
    if event == "plugboard_send":
        # The text from the one-line input field
        input_state = window.Element('plugboard_input').get()
        # add <cr> for PIC
        input_state = '$l' + input_state + '\r'
        # zero the input field
        window['plugboard_input'].update('')
        # send to PIC protothreads
        ser.write((input_state).encode())
    # character loopback from PIC
    while ser.in_waiting > 0:
        #serial_chars = (ser.read().decode('utf-8'));
        #window['console'].update(serial_chars+'\n', append=True)
        pic_char = chr(ser.read(size=1)[0])
        if (pic_char) == '\r':
            window['console'].update('\n', append=True)
        else:
            window['console'].update((pic_char), append=True)

# close port and Bail out
ser.close()
window.close()
