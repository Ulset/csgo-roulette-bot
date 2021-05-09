import time

from selenium import webdriver


class RouletteWrapper:
    def __init__(self, log_in=True):
        self.driver = webdriver.Chrome()
        self.driver.get("https://csgoempire.com/")

        if log_in:
            # Waits for the user to log in to the site.
            print("Venter på log in")
            while True:
                user = self.driver.find_elements_by_class_name("avatar")
                if len(user) > 0:
                    break
                time.sleep(3)
            print("Bruker logget inn.")

        time.sleep(4)
        self.timerEl = self.driver.find_element_by_xpath(
            "//*[@id='page-scroll']/div[1]/div/div/div[2]/div[3]/div/div[2]")

    def wait_for_timer(self, timer_value: float):
        timer_value_now = float(self.get_timer())
        if timer_value_now > timer_value:
            time.sleep(timer_value_now - timer_value)

    def get_current_holding(self):
        # Gets the users current money
        elem = self.driver.find_element_by_xpath(
            "//*[@id='app']/div[1]/div[2]/div[1]/div/div[3]/div[2]/div[3]/div/div/span/span")
        return float(elem.get_attribute("innerHTML"))

    def get_bet_side(self):
        left_side_amount = float(self.driver.find_element_by_xpath(
            "//*[@id='page-scroll']/div[1]/div/div/div[6]/div[1]/div/div[1]/div[2]/span").get_attribute(
            "innerHTML").replace(",", ".").replace("1&nbsp;", ""))
        right_side_amount = float(self.driver.find_element_by_xpath(
            "//*[@id='page-scroll']/div[1]/div/div/div[6]/div[3]/div/div[1]/div[2]/span").get_attribute(
            "innerHTML").replace(",", ".").replace("1&nbsp;", ""))
        if left_side_amount * 2 < right_side_amount:
            return "Left"
        elif right_side_amount * 2 < left_side_amount:
            return "Right"
        else:
            return None

    def get_timer(self):
        return self.timerEl.get_attribute("innerHTML").replace(",", ".")

    def get_winner(self):
        self.wait_for_timer(0)
        while float(self.get_timer()) == 0:
            # Waits for the next rund to start to find winnder
            time.sleep(0.5)
        last_win_el = self.driver.find_element_by_xpath(
            "//*[@id='page-scroll']/div[1]/div/div/div[3]/div/div[1]/div[2]/div[10]/div")
        class_list = last_win_el.get_attribute("className").split(" ")
        if "coin-ct" in class_list:
            return "Left"
        if "coin-t" in class_list:
            return "Right"
        else:
            return "Joker"
