from automation_scripts.common.driver import get_driver
import time


class CutShort:
    def __init__(self):
        self.driver = get_driver()

    def start(self):
        try:
            self.driver.get(url="https://cutshort.io/profile/all-jobs")
            time.sleep(300)
        except:
            pass



instance = CutShort()
instance.start()