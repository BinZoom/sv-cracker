<p align="center">
  <a href="https://github.com/senlizishi/sv-cracker">
    <img width="100" src="https://github.com/senlizishi/sv-cracker/blob/main/spider.png">
  </a>
</p>
<h1 align="center">sv-cracker</h1>
<div align="center">
滑块验证码破解
</div>

### 概述
使用 cv2 + numpy 分析滑块背景图片并计算所需滑动的距离，使用 PID 控制算法生成轨迹，使用 Selenium 模拟手工拖动滑块行为。 

<img src="https://p3.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/5c7e57c89e3742359b604b3c67f75365?from=pc" width="300px">

### 关于 cv2 库
OpenCV 是一个跨平台的计算机视觉库，cv2 提供了对 OpenCV C++ 库的 Python 封装，使得可以通过 Python 方便地调用 OpenCV 中的各种函数和方法，从而进行图像处理、物体检测、计算机视觉算法等操作。

### 关于 PID 控制算法
PID（Proportional-Integral-Derivative）算法是一种常用的控制算法，主要用于对各种系统和过程进行自动控制。它基于对系统当前状态的反馈信息，通过计算误差信号的比例、积分和导数部分，来决定控制器输出的大小和方向，从而实现对系统的稳定控制。

具体来说，PID算法包括三个部分：
- 比例控制（P）：根据当前误差信号的大小，直接产生一个与误差成正比的控制输出，用于快速响应系统的变化。
- 积分控制（I）：将误差信号在一段时间内积累起来，并产生一个与误差积分值成正比的控制输出，用于消除系统的静态误差。
- 导数控制（D）：根据误差信号的变化率，产生一个与误差变化率成正比的控制输出，用于减小系统的超调和振荡。

这三个控制部分共同作用于系统，使得控制器输出的值能够及时、准确地跟随系统的变化，达到对系统的精确控制。

### 环境
- chrome + chromedriver
- requirements.txt 相关依赖

### 免责声明
本代码仅供学习交流之用，只提供大致实现思路，并不针对特定渠道的滑块验证码进行破解，禁止用于任何违法行为。
