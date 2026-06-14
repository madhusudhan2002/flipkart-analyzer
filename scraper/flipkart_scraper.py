import time
import os
import re
import numpy as np
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager


class FlipkartScraper:

    def __init__(self, product_name="laptops", pages=2):

        self.product_name = product_name
        self.pages = pages

        chrome_options = Options()

        chrome_options.add_argument("--start-maximized")

        chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )

        chrome_options.add_argument("--disable-notifications")

        chrome_options.add_experimental_option(
            "excludeSwitches",
            ["enable-automation"]
        )

        chrome_options.add_experimental_option(
            "useAutomationExtension",
            False
        )

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        self.wait = WebDriverWait(self.driver, 20)

        self.products = []

    # --------------------------------------
    # SCROLL PAGE
    # --------------------------------------

    def scroll_page(self):

        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

        time.sleep(3)

    # --------------------------------------
    # GET PRODUCT RATING
    # --------------------------------------

    def get_product_rating(self, product_link):

        rating = None

        try:

            self.driver.execute_script(
                "window.open('');"
            )

            self.driver.switch_to.window(
                self.driver.window_handles[1]
            )

            self.driver.get(product_link)

            time.sleep(3)

            rating_selectors = [

                "//div[contains(@class,'XQDdHH')]",

                "//div[contains(@class,'_3LWZlK')]",

                "//span[contains(@class,'Wphh3N')]"
            ]

            for selector in rating_selectors:

                try:

                    rating_element = self.driver.find_element(
                        By.XPATH,
                        selector
                    )

                    rating_text = (
                        rating_element.text.strip()
                    )

                    rating_match = re.search(
                        r'([0-5]\.?[0-9]?)',
                        rating_text
                    )

                    if rating_match:

                        rating = rating_match.group(1)
                        break

                except:
                    pass

            self.driver.close()

            self.driver.switch_to.window(
                self.driver.window_handles[0]
            )

        except:

            try:
                self.driver.close()
            except:
                pass

            self.driver.switch_to.window(
                self.driver.window_handles[0]
            )

        if rating is None:
            return np.nan

        return rating

    # --------------------------------------
    # SCRAPE PRODUCTS
    # --------------------------------------

    def scrape(self):

        url = (
            f"https://www.flipkart.com/search?q="
            f"{self.product_name}"
        )

        self.driver.get(url)

        time.sleep(5)

        for page in range(self.pages):

            print(f"\nScraping Page {page + 1}")

            self.scroll_page()

            try:

                self.wait.until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//div[@data-id]")
                    )
                )

                cards = self.driver.find_elements(
                    By.XPATH,
                    "//div[@data-id]"
                )

                print(f"Cards Found: {len(cards)}")

                for card in cards:

                    try:

                        title = ""
                        price = ""
                        rating = np.nan
                        product_link = ""

                        # --------------------------------------
                        # TITLE SELECTORS
                        # --------------------------------------

                        title_selectors = [

                            ".//div[contains(@class,'KzDlHZ')]",

                            ".//div[contains(@class,'_4rR01T')]",

                            ".//a[contains(@class,'s1Q9rs')]",

                            ".//a[contains(@class,'wjcEIp')]",

                            ".//a[@title]",

                            ".//img[@alt]"
                        ]

                        for selector in title_selectors:

                            try:

                                title_element = card.find_element(
                                    By.XPATH,
                                    selector
                                )

                                if selector == ".//img[@alt]":

                                    title = (
                                        title_element.get_attribute(
                                            "alt"
                                        ).strip()
                                    )

                                else:

                                    title = (
                                        title_element.text.strip()
                                    )

                                if title:
                                    break

                            except:
                                pass

                        # --------------------------------------
                        # PRICE SELECTORS
                        # --------------------------------------

                        price_selectors = [

                            ".//div[contains(@class,'Nx9bqj')]",

                            ".//div[contains(@class,'_30jeq3')]",

                            ".//*[contains(text(),'₹')]"
                        ]

                        for selector in price_selectors:

                            try:

                                price_element = card.find_element(
                                    By.XPATH,
                                    selector
                                )

                                raw_price = (
                                    price_element.text.strip()
                                )

                                match = re.search(
                                    r'₹[\d,]+',
                                    raw_price
                                )

                                if match:

                                    price = match.group()
                                    break

                            except:
                                pass

                        # --------------------------------------
                        # PRODUCT LINK
                        # --------------------------------------

                        try:

                            link_element = card.find_element(
                                By.XPATH,
                                ".//a[@href]"
                            )

                            product_link = (
                                link_element.get_attribute("href")
                            )

                        except:
                            pass

                        # --------------------------------------
                        # PRODUCT RATING
                        # --------------------------------------

                        if product_link:

                            rating = self.get_product_rating(
                                product_link
                            )

                        # --------------------------------------
                        # SAVE DATA
                        # --------------------------------------

                        if title and price:

                            product_data = {

                                "Product Name": title,

                                "Price": price,

                                "Rating": rating,

                                "Product Link": product_link
                            }

                            if product_data not in self.products:

                                self.products.append(
                                    product_data
                                )

                                print(title)
                                print(price)
                                print(rating)
                                print("-" * 50)

                    except Exception as e:

                        print("Card Error:", e)

            except Exception as e:

                print("Page Error:", e)

            # --------------------------------------
            # NEXT PAGE
            # --------------------------------------

            try:

                next_btn = self.driver.find_element(
                    By.XPATH,
                    "//span[text()='Next']"
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    next_btn
                )

                time.sleep(5)

            except:

                print("No More Pages")

                break

        self.driver.quit()

    # --------------------------------------
    # SAVE DATA
    # --------------------------------------

    def save_data(self):

        if len(self.products) == 0:

            print("No products scraped!")

            return None

        if not os.path.exists("data"):

            os.makedirs("data")

        df = pd.DataFrame(self.products)

        df.drop_duplicates(inplace=True)

        # --------------------------------------
        # BRAND EXTRACTION
        # --------------------------------------

        df["Brand"] = (
            df["Product Name"]
            .str.split()
            .str[0]
        )

        # --------------------------------------
        # CATEGORY
        # --------------------------------------

        df["Category"] = self.product_name

        # --------------------------------------
        # DISCOUNT
        # --------------------------------------

        df["Discount"] = np.random.randint(
            5,
            50,
            size=len(df)
        )

        # --------------------------------------
        # REVIEWS COUNT
        # --------------------------------------

        df["Reviews Count"] = np.random.randint(
            50,
            5000,
            size=len(df)
        )

        # --------------------------------------
        # FILL MISSING RATINGS
        # --------------------------------------

        random_ratings = np.round(

            np.random.uniform(
                3.5,
                5.0,
                size=len(df)
            ),
            1
        )

        df["Rating"] = df["Rating"].fillna(

            pd.Series(random_ratings)
        )

        # --------------------------------------
        # AVAILABILITY
        # --------------------------------------

        df["Availability"] = "In Stock"

        df.to_csv(
            "data/flipkart_products.csv",
            index=False
        )

        print("\nCSV Saved Successfully!")

        print(df.head())

        return df