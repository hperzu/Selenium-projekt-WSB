from unittest import TestLoader, TestSuite
from HtmlTestRunner import HTMLTestRunner
from test import login, inventory, cart

login_tests = TestLoader().loadTestsFromModule(login)
inventory_tests = TestLoader().loadTestsFromModule(inventory)
cart_tests = TestLoader().loadTestsFromModule(cart)

suite = TestSuite([
    login_tests,
    inventory_tests,
    cart_tests
])


runner = HTMLTestRunner(
    output='reports',
    combine_reports=True,
    report_name='report'
)


if __name__ == '__main__':
    runner.run(suite)
