import os
import time
import traceback
from selenium.webdriver.common.by import By
from utils import driver_util
from utils import ver_util
from PIL import Image
import tempfile
from utils.driver_util import is_visibility_by_xpath, MIN_WAIT_SECOND

LOGIN_URL = '<LOGIN_URL>'
USERNAME = '<USERNAME>'
PASSWORD = '<PASSWORD>'

def login(driver):
    """
    登录逻辑
    """
    driver.get(LOGIN_URL)
    driver.find_element(by=By.XPATH, value="//input[@name='email']").send_keys(USERNAME)
    driver.find_element(by=By.XPATH, value="//input[@type='password']").send_keys(PASSWORD)
    driver.find_element(by=By.CLASS_NAME, value="account-center-action-button").click()
    return validate(driver, 3)


def validate(driver, tryNum):
    """
    滑块处理逻辑
    1. cv2 分析滑块背景图计算滑动距离
    2. 生成滑动轨迹
    3. 拖动滑块
    """
    i = 0
    while i < tryNum:
        i += 1
        img_xpath = "//*[@id='captcha-verify-image']"
        filename = "validate-big_" + str(i) + ".png"
        img_path = os.path.join(tempfile.gettempdir(), filename)
        if not is_visibility_by_xpath(driver, MIN_WAIT_SECOND, img_xpath):
            raise Exception("找不到滑块背景图！")
        # 保存滑块背景图片
        is_finish = driver_util.save_image(driver, img_xpath, tempfile.gettempdir(), filename)
        if is_finish:
            time.sleep(1)
            # 获取缩放比
            img_element = driver.find_element(by=By.XPATH, value=img_xpath)
            w1 = img_element.size.get('width')
            img = Image.open(img_path)  # type: Image.Image
            w2 = img.width
            # 计算滑块移动距离
            track = ver_util.calculate_distance(img_path)
            hold_btn = "//div[@id='secsdk-captcha-drag-wrapper']/div[2]"
            # 根据缩放比例计算真正的滑动距离
            track = (track * w1 / w2)
            if driver_util.is_visibility_by_xpath(driver, driver_util.MIN_WAIT_SECOND, hold_btn):
                # 滑动滑块
                driver_util.slide_verify(driver, hold_btn, track)
                # 判断是否登录成功
                if (not is_visibility_by_xpath(driver, MIN_WAIT_SECOND, "//*[@id='captcha-verify-image']")):
                    return True
    return False


# 实例化驱动
driver = driver_util.init_chrome_driver(is_headless=False)
driver.maximize_window()
try:
    login(driver)
except Exception:
    traceback.print_exc()
finally:
    driver.close()
