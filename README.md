# 巨量纵横滑块验证码识别
通过 selenium + chromeDriver + python 库实现通过单缺口滑块验证码，并登录账号

![](https://media.giphy.com/media/Mh1UOn40nFImRGvQZ5/giphy.gif)
![](https://media.giphy.com/media/Mh1UOn40nFImRGvQZ5/giphy.gif)
![](https://media.giphy.com/media/Mh1UOn40nFImRGvQZ5/giphy.gif)

##主要步骤
- 下载滑块背景图片并借助 cv2、np 等库计算距离
- 根据缩放比例计算实际滑动所需移动距离
- 根据制定的滑动轨迹移动滑块

## 注
代码仅供学习交流之用，禁止用于任何违法行为
