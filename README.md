# Object-Detection-and-Avoidance-using-Arduino

# Materials Required:
1. Arduino Mega 2560
2. 2 Wheel Chassis
3. Two DC Motors
4. Two Dual Channel Relay Modules
5. HC-SR04 Ultrasonic Sensor
6. HC-05 Bluetooth Module
7. 400 points Breadboard
8. 5V adapter for external power supply for Arduino
9. 12V adapter for external power supply for DC Motors

# Verification of Components
To verify that all components are in working condition, upload the following codes one by one to check and test the working of each part.
1. Upload ```Blink.ino``` code to test the Arduino.
2. Upload ```DC_Motor.ino``` code to test the working of Two Channel Relay Module and DC Motors
3. Upload the ```Sensor.ino``` Code to test the working of the HC-SR04 Ultrasonic Sensor.
4. Upload the ```Bluetoooth_inbuilt_LED.ino``` code to test the working of HC-05 Bluetooth module

# Connections
Connect the components with the Arduino as shown in the images below. You can use breadboard for common connections.

Interfacing HC-SR04 Ultrasonic sensor with Arduino:

![image](https://github.com/vvpai9/Object-Detection-and-Avoidance-using-Arduino/assets/162291797/6d469aaf-43de-45a4-a4bb-98600294b6fc)


Interfacing HC-05 Bluetooth Module with Arduino:

![image](https://github.com/vvpai9/Object-Detection-and-Avoidance-using-Arduino/assets/162291797/bbe472e4-8737-44dc-a351-a9837b34a41a)


Interfacing DC Motor using Two Channel relay Module with Arduino:

![image](https://github.com/vvpai9/Object-Detection-and-Avoidance-using-Arduino/assets/162291797/a0814eeb-66e9-416b-af93-e09457d255be)


# Controlling
The bot can be controlled by using an android app developed using MIT App Inventor. Download and install ```BOT.apk``` to install the MIT App.

Upload ```Object_Avoidance.ino``` code to the Arduino.

This code will receive user inputs from the MIT App via the HC-05 Bluetooth Module to move around in the direction specified by the user. When the bot detects any object or obstacle via the HC-SR04 Ultrasonic sensor, it stops within 10 cm of the object. The bot will again move only if the obstacle is removed and an input is given via the app.

For the bot to move in its previous path as soon as the obstacle is removed, upload the ```Object_Avoidance_Refined.ino``` code to the Arduino.




