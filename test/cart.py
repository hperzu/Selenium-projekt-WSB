import unittest

from utils.base_command import BaseCommand
from utils.field import Field


class Cart(BaseCommand):
    def test_cart_happy_path(self):
        self.standard_login()

        self.click_element(Field.high_to_low)
        for _ in range(3):
            self.click_element(Field.add_to_cart)

        self.click_element(Field.shopping_chart_link)
        self.click_element(Field.checkout)

        self.clear_element(Field.first_name)
        self.send_text_to_element(Field.first_name, "Jan")

        self.clear_element(Field.last_name)
        self.send_text_to_element(Field.last_name, "Kowalski")

        self.clear_element(Field.postal_code)
        self.send_text_to_element(Field.postal_code, "95-100")

        self.click_element(Field.continue_button)

        self.display_products()

        item_total = self.get_price(Field.item_total)
        tax = self.get_price(Field.tax)
        total = self.get_price(Field.total)

        self.assertEqual(round(total - item_total, 2), tax)

        self.click_element("//button[@id='finish']")
        self.element_is_visible("//img[@alt='Pony Express']")


if __name__ == '__main__':
    unittest.main()
