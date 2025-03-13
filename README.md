# sv-cracker
Using cv2 and numpy to analyze the background image of the slider and calculate the sliding distance, using PID algorithm to generate trajectories, and using Selenium simulation to manually drag the slider to crack the verification code.

<img src="https://p3.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/5c7e57c89e3742359b604b3c67f75365?from=pc" width="300px">

## Install
1. Install dependencies：
```bash
pip install -r requirements.txt
```

2. Install chrome and chromedriver


## About PID
PID (Proportional-Integral-Derivative) algorithm is a commonly used control algorithm, mainly used for automatic control of various systems and processes. It is based on the feedback information of the current state of the system, and determines the size and direction of the controller output by calculating the proportional, integral and derivative parts of the grating signal, thereby achieving stable control of the system.

The PID algorithm consists of three parts:
- Proportional control (P): Based on the size of the current error signal, a control output proportional to the error is directly generated to quickly respond to system changes.
- Integral control (I): The error signal is accumulated over a period of time and a control output proportional to the integral value of the error is generated to eliminate the static error of the system.
- Derivative control (D): Based on the rate of change of the error signal, a control output proportional to the rate of change of the error is generated to reduce the overshoot and oscillation of the system.

These three control parts work together on the system so that the value output by the controller can follow the changes of the system in a timely and accurate manner, thereby achieving precise control of the system.


### Declaration
This repository is for learning and research purposes only, and is strictly prohibited from being used for illegal, irregular, or infringing activities. Users shall bear all responsibilities arising from the use of the code on their own.
