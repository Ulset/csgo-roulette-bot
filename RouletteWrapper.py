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

    def get_current_holding(self):
        # Gets the users current money
        elem = self.driver.find_element_by_xpath(
            "//*[@id='app']/div[1]/div[2]/div[1]/div/div[3]/div[2]/div[3]/div/div/span/span")
        return float(elem.get_attribute("innerHTML"))

    def get_least_betted_side(self):
        left_side_amount = float(self.driver.find_element_by_xpath(
            "//*[@id='page-scroll']/div[1]/div/div/div[6]/div[1]/div/div[1]/div[2]/span").get_attribute(
            "innerHTML").replace(",", "."))
        right_side_amount = float(self.driver.find_element_by_xpath(
            "//*[@id='page-scroll']/div[1]/div/div/div[6]/div[3]/div/div[1]/div[2]/span").get_attribute(
            "innerHTML").replace(",", "."))
        if left_side_amount < right_side_amount:
            return "Left"
        else:
            return "Right"

    def get_timer(self):
        return self.timerEl.get_attribute("innerHTML").replace(",", ".")

    def get_winner(self):
        while float(self.get_timer()) < 20:
            # Waits for the next rund to start to find winnder
            pass
        last_win_el = self.driver.find_element_by_xpath(
            "//*[@id='page-scroll']/div[1]/div/div/div[3]/div/div[1]/div[2]/div[10]/div")
        class_list = last_win_el.get_attribute("className").split(" ")
        if "coin-ct" in class_list:
            return "Left"
        if "coin-t" in class_list:
            return "Right"
        else:
            return "Joker"
