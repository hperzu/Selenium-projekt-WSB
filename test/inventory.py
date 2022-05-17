import unittest

from selenium.webdriver.common.by import By

from utils.base_command import BaseCommand, get_image_sources
from utils.field import Field


class Inventory(BaseCommand):
    def test_compare_inventory_images(self):
        self.standard_login()
        images = self.driver.find_elements(By.XPATH, Field.inventory_images)
        standard_img_src = get_image_sources(images)

        self.driver.get(Field.url)
        self.problem_user_login()
        images = self.driver.find_elements(By.XPATH, Field.inventory_images)
        problem_img_src = get_image_sources(images)
        self.maxDiff = 1100
        self.assertEqual(standard_img_src, problem_img_src)


if __name__ == '__main__':
    unittest.main()
