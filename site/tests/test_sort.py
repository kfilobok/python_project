import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import unittest

class ProductCatalogTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_sorting(self):
        driver = self.driver
        driver.get("http://localhost:5000/catalog")

        sort_asc_button = driver.find_element(By.LINK_TEXT, "Цена ↑")
        sort_asc_button.click()
        time.sleep(2)


        product_prices = driver.find_elements(By.CSS_SELECTOR, ".product-card .card-body p")
        prices = []

        for price in product_prices:
            try:
                price_text = price.text.replace("Цена:", "").strip()
                price_value = re.sub(r"[^\d]", "", price_text)
                if price_value:
                    prices.append(int(price_value))
            except ValueError:
                continue

        self.assertEqual(prices, sorted(prices), "Товары должны быть отсортированы по возрастанию цены")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
