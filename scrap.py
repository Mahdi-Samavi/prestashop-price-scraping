#! venv/Scripts/python

import sqlite3
import logging
import re
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep

class Scrap():
    def __init__(self):
        logging.basicConfig(filename='.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)
        self.con = sqlite3.connect('database')
        self.cur = self.con.cursor()
        self.initBrowser()

    def initBrowser(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--start-maximized')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(executable_path=r'.\driver\chromedriver.exe', options=options)

    def run(self):
        admins = self.cur.execute('SELECT * FROM admins')
        for admin in admins:
            products = self.cur.execute('SELECT * FROM products WHERE admin_id = ?', str(admin[0])).fetchall()

            self.goToProductsPage(admin)

            for product in products:
                self.crawl(admin, product)
                logging.info(f'The {product[3]} => {product[2]} updated.')

            self.switchToAdminTab()

    def goToProductsPage(self, admin):
        self.driver.get(admin[2])

        # Email field
        email = self.driver.find_element(By.ID, 'email')
        email.send_keys(admin[3])

        # Passwd field
        passwd = self.driver.find_element(By.ID, 'passwd')
        passwd.send_keys(admin[4])
        passwd.submit()

        # Click on catalog link
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#subtab-AdminCatalog > .link'))
        ).click()

        # Click on products link
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#subtab-AdminProducts > .link'))
        ).click()

        # Reset catagory filter
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#product_catalog_category_tree_filter'))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#product_catalog_category_tree_filter_reset'))
        ).click()

    def crawl(self, admin, product):
        self.driver.execute_script('window.open("about:blank", "scrapTab")')
        self.driver.switch_to.window('scrapTab')
        self.driver.get(product[4])
        price = re.sub("[^0-9]", "", self.driver.find_element(By.XPATH, product[5]).text)

        # Switch to admin products page
        self.switchToAdminTab()

        # Filter product
        self.filterProduct(product[3])

        # Open editing product page
        productUrl = self.driver.find_element(By.CSS_SELECTOR, 'a.product-edit').get_attribute('href')
        self.driver.execute_script('window.open("about:blank", "productEdit")')
        self.driver.switch_to.window('productEdit')
        self.driver.get(productUrl)

        priceField = self.driver.find_element(By.ID, 'form_step1_price_ttc_shortcut')
        priceField.clear()
        priceField.send_keys(price)

        submitBtn = self.driver.find_element(By.CSS_SELECTOR, '#submit')
        if submitBtn.is_displayed():
            submitBtn.click()
        else:
            self.driver.find_element(By.CSS_SELECTOR, '#form button.btn-primary[type="submit"]').click()

        sleep(1)

        self.driver.close()

    def switchToAdminTab(self):
        self.driver.switch_to.window(self.driver.window_handles[0])

    def filterProduct(self, id):
        reset = self.driver.find_element(By.CSS_SELECTOR, 'button[name="products_filter_reset"]')
        if reset.is_displayed():
            reset.click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'filter_column_id_product_min'))
        ).send_keys(id)

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'filter_column_id_product_max'))
        ).send_keys(id)

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[name="products_filter_submit"]'))
        ).click()

if __name__ == '__main__':
    scrap = Scrap()
    while True:
        scrap.run()
        sleep(30 * 60)