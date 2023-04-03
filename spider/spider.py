import os
import time
import traceback
from selenium.webdriver.common.by import By
from utils import driver_util
from utils import ver_util
from PIL import Image
from utils.driver_util import is_visibility_by_xpath, MIN_WAIT_SECOND, LESS_WAIT_SECOND


# 头条登录账号
username = '<username>'
password = '<password>'
# 截图根目录
validate_pic_path = "<validate_pic_path>"
# 登录地址
LOGIN_URL = 'https://business.oceanengine.com/site/login/'

def login(driver):
    """
    登录
    """
    driver.get(LOGIN_URL)
    time.sleep(LESS_WAIT_SECOND)
    driver.find_element(by=By.XPATH, value="//input[@name='email']").send_keys(username)
    driver.find_element(by=By.XPATH, value="//input[@type='password']").send_keys(password)
    driver.find_element(by=By.CLASS_NAME,value="check-box-container").click()
    loginBtn = driver.find_element(by=By.CLASS_NAME, value="account-center-action-button")
    loginBtn.click()
    time.sleep(LESS_WAIT_SECOND)
    return validate(driver, 3)

def validate(driver, tryNum):
    """
    # 分析滑块验证码并移动滑块过验证
    """
    if not (driver.current_url == LOGIN_URL):
        return True
    # 判断滑动弹窗是否出现
    is_sliderpop = is_visibility_by_xpath(driver, MIN_WAIT_SECOND, "//*[@id='captcha-verify-image']")
    is_loginpage = is_visibility_by_xpath(driver, LESS_WAIT_SECOND, "//input[@name='service']/parent::div")
    if ((not is_loginpage) and (not is_sliderpop)):
        return True
    if (is_loginpage and (not is_sliderpop)):
        raise Exception("登录失败！可能账号密码错误，账号：" + username + " 密码：" + password)
    if is_sliderpop:
        i = 0
        while i < tryNum:
            i += 1
            img_xpath = "//*[@id='captcha-verify-image']"
            filename = "validate-big_" + str(i) + ".png"
            img_path = os.path.join(validate_pic_path, filename)
            if not is_visibility_by_xpath(driver, MIN_WAIT_SECOND, img_xpath):
                raise Exception("找不到滑块背景图！")
            # 下载滑块背景图
            is_finish = driver_util.save_image(driver, img_xpath, validate_pic_path, filename)
            if is_finish:
                time.sleep(1)
                img_element = driver.find_element(by=By.XPATH, value=img_xpath)
                w1 = img_element.size.get('width')
                img = Image.open(img_path)  # type: Image.Image
                w2 = img.width
                # 计算滑块移动距离
                track = ver_util.calculate_distance(img_path)
                hold_btn = "//div[@id='secsdk-captcha-drag-wrapper']/div[2]"
                # 根据缩放比例计算真正的滑动距离
                track = (track * w1 / w2) - 7
                if driver_util.is_visibility_by_xpath(driver, driver_util.MIN_WAIT_SECOND, hold_btn):
                    # 根据轨迹移动滑块
                    if driver_util.slide_verify(driver, hold_btn, track):
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

