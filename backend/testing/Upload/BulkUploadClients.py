# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest


class UntitledTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=r"../chromedriver.exe")
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_untitled_test_case(self):
        driver = self.driver
        driver.get("http://3.144.105.249:3000/")
        driver.find_element_by_xpath(
            "//div[@id='root']/div/div/div[2]/div[4]/div[2]/div/div/button"
        ).click()
        driver.find_element_by_xpath(
            "//div[@id='root']/div/div/div[2]/div[4]/div/div/div/input"
        ).click()
        driver.find_element_by_xpath(
            "//div[@id='root']/div/div/div[2]/div[4]/div/div/div/input"
        ).clear()
        driver.find_element_by_xpath(
            "//div[@id='root']/div/div/div[2]/div[4]/div/div/div/input"
        ).send_keys("C:\\fakepath\\RandomAddresses.xlsx")
        driver.find_element_by_xpath(
            "//div[@id='root']/div/div/div[2]/div[4]/div[2]/div/div/button"
        ).click()
        driver.find_element_by_xpath(
            "//div[@id='root']/div/div/div[2]/div/div/div/div[2]/div/input"
        ).click()
        driver.find_element_by_xpath(
            "//div[@id='root']/div/div/div[2]/div/div/div/div[2]/div/input"
        ).click()
        driver.find_element_by_xpath(
            "//div[@id='root']/div/div/div[2]/div/div/div/div[2]/div/input"
        ).clear()
        driver.find_element_by_xpath(
            "//div[@id='root']/div/div/div[2]/div/div/div/div[2]/div/input"
        ).send_keys("juan")
        driver.find_element_by_xpath(
            "//div[@id='root']/div/div/div[2]/div/div/div"
        ).click()
        driver.find_element_by_xpath(
            "//div[@id='root']/div/div/div[2]/div/div/div/div[2]/div/input"
        ).clear()
        driver.find_element_by_xpath(
            "//div[@id='root']/div/div/div[2]/div/div/div/div[2]/div/input"
        ).send_keys("vonny")
        driver.find_element_by_xpath(
            "//div[@id='root']/div/div/div[2]/div/div/div"
        ).click()
        driver.find_element_by_xpath(
            "//div[@id='root']/div/div/div[2]/div/div/div/div[2]/div/input"
        ).clear()
        driver.find_element_by_xpath(
            "//div[@id='root']/div/div/div[2]/div/div/div/div[2]/div/input"
        ).send_keys("")
        driver.find_element_by_xpath(
            "//div[@id='root']/div/div/div[2]/div/div/div/div[2]/div/input"
        ).clear()
        driver.find_element_by_xpath(
            "//div[@id='root']/div/div/div[2]/div/div/div/div[2]/div/input"
        ).send_keys("p")
        driver.find_element_by_xpath(
            "//div[@id='root']/div/div/div[2]/div/div/div"
        ).click()
        driver.find_element_by_xpath(
            "//div[@id='root']/div/div/div[2]/div/div/div/div[2]/div/input"
        ).clear()
        driver.find_element_by_xpath(
            "//div[@id='root']/div/div/div[2]/div/div/div/div[2]/div/input"
        ).send_keys("")

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
