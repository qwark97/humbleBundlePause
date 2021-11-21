import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

HUMBLE_BUNDLE_ENTRYPOINT = 'https://www.humblebundle.com/user/pause-subscription/confirm'
CHROMEDRIVER_PATH = os.getenv("HBP_CHROMEDRIVER_PATH", "chromedriver")
BROWSER_PROFILE_PATH = os.getenv("HBP_BROWSER_PROFILE_PATH")
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'


def run():
    driver = run_browser()
    pause_subscription(driver)


def notify_about_error(msg: str):
    now = datetime.now().strftime("%d.%m.%Y-%H:%M")
    print(msg)


def run_browser() -> webdriver.Chrome:
    o = webdriver.ChromeOptions()
    o.headless = True
    o.add_argument(f"user-data-dir={BROWSER_PROFILE_PATH}")
    o.add_argument(f"user-agent={USER_AGENT}")
    driver = webdriver.Chrome(
        executable_path=CHROMEDRIVER_PATH,
        options=o,
    )
    driver.set_window_size(1920, 1080)
    return driver


def pause_subscription(driver: webdriver.Chrome) -> bool:
    try:
        # load page
        driver.get(HUMBLE_BUNDLE_ENTRYPOINT)
        print('loaded main URL')

        # click pause button
        WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//a[contains(text(), 'Pause my membership')]"))).click()
        print('clicked first pause button')

        # click another pause button
        WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(), 'Pause my membership')]"))).click()
        print('clicked second pause button')

        # confirm pause
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//h1[contains(text(), 'Enjoy the month long break!')]")))
        print('confirm pausing subscription')

    except Exception as ex:
        notify_about_error(str(ex))

    else:
        return True
    finally:
        if driver:
            driver.quit()


if __name__ == '__main__':
    run()
