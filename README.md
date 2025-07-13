"# WebAutomationandScrapingAssessment" 
# Selenium Laptop Scraper

This project scrapes laptop product data from [webscraper.io test site](https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops) using Selenium. It collects product details including title, price, rating, review count, description, and saves the results to a JSON file.

---

## Features

- Scrapes multiple pages of laptop listings
- Extracts product title, price, rating, reviews count, product URL
- Navigates to each product page to get detailed description
- Saves all data into `output.json`

---

## Requirements

- Python 3.7+
- Selenium
- WebDriver for your browser (e.g., ChromeDriver for Chrome)

---

## Setup

1. Clone the repository or download the source code.

2. Install required Python packages:

```bash
pip install -r requirements.txt
