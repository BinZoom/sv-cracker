import os
import imghdr
import random
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.request import urlretrieve

from utils.PositionalPID import get_pid_track

LESS_WAIT_SECOND = 2
MIN_WAIT_SECOND = 5
MAX_WAIT_SECOND = 10


def init_chrome_driver(is_headless):
    """
    初始化一个 chrome Driver
    :param is_headless:  是否开启无头模式
    :return: chrome Driver
    """
    chrome_options = Options()
    # 设置屏幕器宽高
    chrome_options.add_argument("--window-size=1440,750");
    # 最大化，防止失去焦点
    chrome_options.add_argument("--start-maximized")
    # 消除安全校验 可以直接无提示访问http网站
    chrome_options.add_argument("--allow-running-insecure-content")
    if is_headless:
        chrome_options.add_argument('--headless')

    # 实例化驱动
    driver = webdriver.Chrome(executable_path=r'D:\Program Files\chromeDriver\chromedriver.exe',
                              options=chrome_options)
    return driver


def is_visibility_by_xpath(driver, seconds, xpathExpressions):
    '''
    在指定时间内判断 xpath 元素是否存在
    :param driver:
    :param seconds:  等待时机（秒）
    :param xpathExpressions:  元素 xpath 路径
    :return:
    '''
    try:
        wait = WebDriverWait(driver, seconds, 1)
        wait.until(EC.visibility_of_element_located((By.XPATH, xpathExpressions)))
    except Exception:
        return False
    return True


def is_element_exit(driver, by, value):
    '''
    判断指定元素是否存在
    '''
    try:
        if by == 'id':
            driver.find_element(by=By.ID, value=value)
        else:
            driver.find_element(by=By.XPATH, value=value)
        return True
    except Exception:
        return False


def save_image(driver, xpathExpression, path, filename):
    '''
    下载并保存图片
    :param driver: 驱动
    :param xpathExpression:  元素 xpath 路径
    :param path:  保存的目录
    :param filename:  保存的文件名
    :return:
    '''
    validateBlockUrl = driver.find_element(by=By.XPATH, value=xpathExpression).get_attribute("src")
    img_path = os.path.join(path, filename)
    # 将图片下载到本地
    urlretrieve(validateBlockUrl, img_path)
    if imghdr.what(img_path):
        return True
    else:
        return False


def slide_verify(driver, expression, distance):
    '''
    滑动验证码
    :param driver: 驱动
    :param expression:  滑块元素表达式
    :param path:  滑动距离
    '''
    slider_element = driver.find_element(by=By.CLASS_NAME, value=expression)

    # 生成 PID 轨迹，可对 P、I、D 三个参数进行调参，如先控制 0.1，之后以试错法增加减少值大小以达到最佳效果
    track = get_pid_track(0.1, 0.1, 0.1,distance)

    webdriver.ActionChains(driver).click_and_hold(slider_element).perform()
    for x in track:
        if (x != 0):
            # 模拟抖动
            offset_y = random.uniform(-2, 2)
            webdriver.ActionChains(driver).move_by_offset(xoffset=x, yoffset=offset_y).perform()
    time.sleep(0.5)
    webdriver.ActionChains(driver).release().perform()
