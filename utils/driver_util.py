import os
import imghdr
import random
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from urllib.request import urlretrieve

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
    driver = webdriver.Chrome(executable_path='D:\\Program Files\\chromeDriver\\chromedriver.exe',
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


def slide_verify(driver, xpathExpression, distance):
    '''
    模拟人工拖动滑块
    :param driver: 驱动
    :param xpathExpression: 元素 xpath 路径
    :param distance: 需要拖动的距离
    :return:
    '''
    element = driver.find_element(by=By.XPATH, value=xpathExpression)
    actionchains = ActionChains(driver)
    actionchains.click_and_hold(element).perform()
    # 单位时间内，前面滑动距离长些(速度快)，后面则速度慢性，模拟人手操作（y轴设置偏移量，模拟人手操作）
    y = int(random.random() * (4 - 2) + 1)
    actionchains.move_by_offset(distance / 2, y)
    y = int(random.random() * (4 - 2) + 1)
    actionchains.move_by_offset(distance / 3, y)
    y = int(random.random() * (4 - 2) + 1)
    actionchains.move_by_offset(distance / 7, y)
    # 计算余留的距离
    remain = distance - (distance / 2 + distance / 3 + distance / 7)
    y = int(random.random() * (4 - 2) + 1)
    actionchains.move_by_offset(remain, y)
    time.sleep(1)
    # 释放
    actionchains.release(element).perform()
    time.sleep(3)
    return not is_visibility_by_xpath(driver, LESS_WAIT_SECOND, xpathExpression)
