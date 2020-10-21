# Self-Driving-RC-Car
Built a self driving RC car that can detect traffic lights, stop signs, obstacles and acts accordingly while keeping itself in the lane. For both object detction and lane keeping, deep learning models have been used.

![](https://github.com/Rami97rgb/Self-Driving-RC-Car/blob/master/images/car1.jpg)

## Hardware
The following hardware has been used:
* Raspberry Pi 3 b+
* Arduino Uno
* USB Webcam
* DC motors
* A powerbank and some AA battries
* Ultrasonic sensor
* A PC

## Software
We used the following languages and software tools:
* Python
* C/C++
* OpenCV
* Tensorflow
* Keras
* Numpy
* Pickle
* Socket
* imutils

## How The Self Driving System Functions
* The USB Webcam mounted in front of the vehicule captures frames.
* The frames are fed to the lane keeping model which runs locally: it is a deep learning model developed by Nvidia that outputs the direction that the vehicule should take (forward, left, or right)
* The frames are also sent to a PC via a socket connection where they are being fed to an obeject detection model based on the sliding window algorithm. This model should detect if there is a stop sign, a red light, a green light in the frame and return the result back to the Raspberry SBC. The task is being run on dedicated a computer because, unlike lane keeping, it is computionally heavy.
* The system can also detect obstacles using an ultrasonic sensor.
* All actions are being handeled by the Arduino.

## Lane keeping
![](https://github.com/Rami97rgb/Self-Driving-RC-Car/blob/master/images/car2.gif)

## Stop Sign Detection
![](https://github.com/Rami97rgb/Self-Driving-RC-Car/blob/master/images/car3.gif)

## Traffic Lights Detection
![](https://github.com/Rami97rgb/Self-Driving-RC-Car/blob/master/images/car4.gif)
![](https://github.com/Rami97rgb/Self-Driving-RC-Car/blob/master/images/car5.gif)

## Obstacle Detection
![](https://github.com/Rami97rgb/Self-Driving-RC-Car/blob/master/images/car6.gif)

## Resources
A huge help and inspiration for this project: https://github.com/jawilk/Self-Driving-RC-Car-Payment

Also inspired by: https://github.com/hamuchiwa/AutoRCCar

Lane keeping: https://developer.nvidia.com/blog/deep-learning-self-driving-cars/

Object Detection: https://www.coursera.org/lecture/convolutional-neural-networks/convolutional-implementation-of-sliding-windows-6UnU4
