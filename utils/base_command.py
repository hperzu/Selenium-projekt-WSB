import unittest
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager

from utils.field import Field
from utils.user import User


def get_image_sources(images):
    sources = []
    for img in images:
        img_src = img.get_attribute("src")
        sources.append(img_src)
    return sources


class BaseCommand(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.set_window_size(1280, 800)
        self.driver.get(Field.url)
        self.wait = WebDriverWait(self.driver, 3)
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(levelname)7s %(asctime)s [%(filename)13s:%(lineno)4d] %(message)s",
        )
        self.log = logging.getLogger()

    def tearDown(self):
        self.driver.quit()

    def click_element(self, element):
        self.wait.until(ec.element_to_be_clickable((By.XPATH, element)))
        self.driver.find_element(By.XPATH, element).click()

    def clear_element(self, element):
        self.wait.until(ec.visibility_of_element_located((By.XPATH, element)))
        self.driver.find_element(By.XPATH, element).clear()

    def send_text_to_element(self, element, text):
        self.wait.until(ec.visibility_of_element_located((By.XPATH, element)))
        self.driver.find_element(By.XPATH, element).send_keys(text)

    def element_is_visible(self, element):
        self.wait.until(ec.visibility_of_element_located((By.XPATH, element)))

    def get_element_text(self, element):
        self.wait.until(ec.visibility_of_element_located((By.XPATH, element)))
        return self.driver.find_element(By.XPATH, element).text

    def get_price(self, element):
        self.wait.until(ec.visibility_of_element_located((By.XPATH, element)))
        price = self.get_element_text(element)
        price = float(price.split("$", 1)[1])
        return price

    def display_products(self):
        items_list = self.driver.find_elements(By.XPATH, Field.inventory_item_name)
        quantity_list = self.driver.find_elements(By.XPATH, Field.item_cart_quantity)
        prices_list = self.driver.find_elements(By.XPATH, Field.inventory_item_price)

        for i in range(len(items_list)):
            self.log.info(
                f"Item: {items_list[i].text}, "
                f"Quantity: {quantity_list[i].text}, "
                f"Price: {prices_list[i].text}"
            )

    def standard_login(self):
        self.clear_element(Field.username_textfield)
        self.send_text_to_element(Field.username_textfield, User.standard_user_login)

        self.clear_element(Field.username_password_field)
        self.send_text_to_element(Field.username_password_field, User.password)

        self.click_element(Field.login_button)

        self.element_is_visible(Field.product_label)
        product_label_text = self.get_element_text(Field.product_label)
        self.assertEqual(Field.product_label_text.upper(), product_label_text)

    def problem_user_login(self):
        self.clear_element(Field.username_textfield)
        self.send_text_to_element(Field.username_textfield, User.problem_user)

        self.clear_element(Field.username_password_field)
        self.send_text_to_element(Field.username_password_field, User.password)

        self.click_element(Field.login_button)

        self.element_is_visible(Field.product_label)
        product_label_text = self.get_element_text(Field.product_label)
        self.assertEqual(Field.product_label_text.upper(), product_label_text)

    def login_locked_out_user(self):
        self.clear_element(Field.username_textfield)
        self.send_text_to_element(Field.username_textfield, User.locked_out_user_login)

        self.clear_element(Field.username_password_field)
        self.send_text_to_element(Field.username_password_field, User.password)

        self.click_element(Field.login_button)

        for i in range(3):
            self.element_is_visible(f"({Field.error_mark})[{i+1}]")

        self.element_is_visible(Field.error_message_container)
        self.element_is_visible(Field.error_message)
        message = self.get_element_text(Field.error_message)
        self.assertEqual(Field.error_message_text, message)


if __name__ == '__main__':
    unittest.main()
