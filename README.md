This application is designed for Praxis III Team 0104B (Winter 2023-2024)
Key functions include:
    1. Measure soil moisture levels and read from lcd screen / leds, instantaneously 
    2. Store several soil moisture values into the Arduino EEPROM memory
    3. Upload stored soil moisture to database in order to compare to past data

Frequently Asked Questions (FAQ):

    Q: I can't open the python application.
    A: Ensure that the entire package is downloaded, including folder build and dist

    Q: When testing the connection, it shows the Ardiuno is not found.
    A: Check the port and baudrate(serial output):
       1. The port is shown on 'my computer', or open Arduino IDE and it will appear.
          Remember to close Arduino IDE after opening it.
       2. The serial output for the Arduino is set to 57600, not 9600.

    Q: When testing the connection, it shows Access Denied.
    A: Arduino IDE must be closed to allow Python access to Arduino board. 
       Also check no other application is interacting with the Arduino board.

    Q: When inputting the data, somehow it doesn't work.
    A: Check the following:
       1. past_data.txt is closed.
       2. past_data.txt is under the same folder with the application.(should be in folder dist)
       3. If any stored value is 0(ie. [0,25] ; [25,0] ; [0,0]), this set won't be recored. 

    Q: I'm trying to modify the Python code, but there are bugs;
       I'm trying to run the code through VS code, but it doesn't work;
    A: Check the following:
       1. The python functions is programmed under Python 3.8.6
       2. The application is programmed using package Pyside2, not Pyside6
       3. The application is programmed without external UI.
       4. The interaction with Arduino uses package Serial2.
     
    Q: I'm trying to modify the Arduino code, but there are bugs;
    A: Check the following:
       1. Change the serial output to 57600 so output messages are readable.
       2. The voltage for LEDs are set reversely (using 256-certain values)
       3. Button detections are programmed without vibrational detections
       4. Check that your Arduino board has EEPROM.
       5. The code serves primarily for Arduino UNO R3


past_data.txt: 
    Stores all past data in txt form: 
    before  after   date 
    287     321     2024-03-23
    It shall not be externally edited unless doing testing.
    Read/Write is implemented via Afunc.py


Afunc.py:
    Include all core python functions which interact with the database.
    Include graphing functions and data analysis functions.
    Internal data(read from txt) is converted to dict type: {date:[[be,af],[be,af],[be,af]]}

arduino_initialize.ino: (Not a part of actual program)
    Arduino code that sets the EEPROM memory to all 0 values

arduino_input.py:
    Include all core python functions which interact with the Arduino EEPROM.
    Allows checking connection, reading memory, and data convertion to python dict.

arduino_storage.ino:
    Arduino code that shall be uploaded to Arduino Uno R3 boards.
    Include all functions for arduino:
        1. instant moisture level reading from lcd and leds 
        2. recording moisture level using buttons
        3. clear internal memory using buttons
        4. power on/off mode change using buttons

arduino_test.ino: (Not a part of actual program)
    Arduino code that reads the EEPROM memory and prints them in the serial output
    It is the primary testing via Arduino IDE before python interactions for debugging

moisture_level.py:
    Main application page