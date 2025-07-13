import asyncio
import json
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

BASE_URL = "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"
OUTPUT_FILE = "output.json"
async def extract_listing_data(page):
    products = []
    cards = await page.query_selector_all('.card.thumbnail')

    for card in cards:
        try:
            title_el = await card.query_selector('a.title')
            title = await title_el.get_attribute('title')
            relative_url = await title_el.get_attribute('href')
            product_url = f"https://webscraper.io{relative_url}"

            price_el = await card.query_selector('[itemprop="price"]')
            price = await price_el.inner_text() if price_el else "N/A"

            review_count_el = await card.query_selector('[itemprop="reviewCount"]')
            reviews_count = int(await review_count_el.inner_text()) if review_count_el else 0

            star_elements = await card.query_selector_all('.ratings p span.ws-icon-star')
            rating = len(star_elements)

            products.append({
                "title": title.strip() if title else "N/A",
                "price": price.strip(),
                "rating": rating,
                "reviews_count": reviews_count,
                "product_url": product_url,
            })

        except Exception as e:
            print(f"Error parsing product card: {e}")
    return products


async def extract_description(page, url):
    try:
        await page.goto(url, timeout=10000)
        desc_el = await page.query_selector('.description')
        if desc_el:
            return (await desc_el.inner_text()).strip()
        return ""
    except PlaywrightTimeoutError:
        print(f"Timeout while loading {url}")
        return ""
    except Exception as e:
        print(f"Failed to get description for {url}: {e}")
        return ""

async def scrape():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(BASE_URL)

        all_products = []

        while True:
            print(f"Scraping page: {page.url}")
            listings = await extract_listing_data(page)
            print(len(listings))
            for product in listings:
                desc = await extract_description(page, product["product_url"])
                product["description"] = desc
                all_products.append(product)

            next_btn = await page.query_selector("li.next > a")
            if next_btn:
                try:
                    await next_btn.click()
                    await page.wait_for_load_state("load")
                except Exception as e:
                    print("Error clicking next button:", e)
                    break
            else:
                break

        await browser.close()

        # Write to JSON
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(all_products, f, indent=2)

        print(f"Scraping complete. {len(all_products)} products saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(scrape())

#
# import json
# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# BASE_URL = "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"
# OUTPUT_FILE = "laptops_data_selenium.json"
#

# def init_browser():
#     options = Options()
#     options.add_argument("--headless=new")  # For latest Chrome
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     return webdriver.Chrome(options=options)
#
# def extract_product_info(card):
#     try:
#         title_el = card.find_element(By.CSS_SELECTOR, 'a.title')
#         title = title_el.get_attribute("title")
#         product_url = "https://webscraper.io" + title_el.get_attribute("href")
#
#         price_el = card.find_element(By.CSS_SELECTOR, '[itemprop="price"]')
#         price = price_el.text.strip()
#
#         reviews_el = card.find_element(By.CSS_SELECTOR, '[itemprop="reviewCount"]')
#         reviews_count = int(reviews_el.text.strip())
#
#         stars = card.find_elements(By.CSS_SELECTOR, 'p[data-rating] span.ws-icon-star')
#         rating = len(stars)
#
#         return {
#             "title": title.strip(),
#             "price": price,
#             "rating": rating,
#             "reviews_count": reviews_count,
#             "product_url": product_url
#         }
#     except Exception as e:
#         print("Error extracting product info:", e)
#         return None

# def extract_description(driver, url):
#     try:
#         driver.get(url)
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CLASS_NAME, "description"))
#         )
#         desc = driver.find_element(By.CLASS_NAME, "description").text
#         return desc.strip()
#     except Exception as e:
#         print(f"Error getting description for {url}:", e)
#         return ""
#

# def scrape_site():
#     driver = init_browser()
#     driver.get(BASE_URL)
#     wait = WebDriverWait(driver, 10)
#     all_products = []
#
#     while True:
#         print(f"Scraping page: {driver.current_url}")
#         try:
#             wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "thumbnail")))
#             product_cards = driver.find_elements(By.CLASS_NAME, "thumbnail")
#         except TimeoutException:
#             print("Timeout loading products. Exiting.")
#             break
#
#         for card in product_cards:
#             product = extract_product_info(card)
#             if product:
#                 description = extract_description(driver, product["product_url"])
#                 product["description"] = description
#                 all_products.append(product)

#         try:
#             next_button = driver.find_element(By.CSS_SELECTOR, "li.next > a")
#             next_button.click()
#             time.sleep(2)
#         except NoSuchElementException:
#             break  # No more pages
#
#     driver.quit()
#
#     # Save to JSON
#     with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
#         json.dump(all_products, f, indent=2)
#
#     print(f"Scraping finished. {len(all_products)} products saved to {OUTPUT_FILE}")
#
# if __name__ == "__main__":
#     scrape_site()
