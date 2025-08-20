import time, random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from promts.promts import PROMPTS
from services.ask_ollama import analyze_with_ollama, get_embedding
from sqlalchemy.orm import Session
from models import Products
from database import SessionLocal
from selenium.webdriver.chrome.service import Service

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    return webdriver.Chrome(
        service=Service("/usr/bin/chromedriver"),
        options=chrome_options,
    )

def url_list(url: str, num_pages: int):
    driver = get_driver()

    products_list = []

    try:
        for page in range(1, num_pages):
            url_with_page = f"{url}&page={page}"
            driver.get(url_with_page)

            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-result-item[data-asin]")))

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            product_divs = soup.find_all("div", {"data-component-type": "s-search-result"})

            for product in product_divs:
                title_tag = product.find("h2")

                name = title_tag.get_text(strip=True)
                a_tag = product.find("a", class_= "a-link-normal s-line-clamp-2 s-link-style a-text-normal")
                link = "https://www.amazon.com" + a_tag["href"] if a_tag else "Not available"

                image = product.find("img", {"class": "s-image"})
                image = image["src"] if image else "Not available"

                price_whole = product.find("span", {"class": "a-price-whole"})
                price_fraction = product.find("span", {"class": "a-price-fraction"})
                price_symbol = product.find("span", {"class": "a-price-symbol"})
                review_tag = product.find("i", {"data-cy": "reviews-ratings-slot"})
                colors_container = product.find("div", class_="s-color-swatch-container-list-view")

                colors = []

                if colors_container:
                    color_links = colors_container.find_all("a", {"aria-label": True})
                    for color_link in color_links:
                        color_name = color_link["aria-label"].strip()
                        color_href = color_link["href"].strip()
                        full_color_link = "https://www.amazon.com" + color_href if color_href else "Not available"
                        colors.append({"name": color_name, "link": full_color_link})


                price_whole_text = price_whole.get_text(strip=True) if price_whole else ""
                price_fraction_text = price_fraction.get_text(strip=True) if price_fraction else ""
                price_symbol_text = price_symbol.get_text(strip=True) if price_symbol else "Not available"
                review_text = review_tag.span.get_text(strip=True) if review_tag and review_tag.span else "0 reviews"


                if price_whole_text:
                    price_str = f"{price_whole_text}{price_fraction_text}" if price_fraction_text else price_whole_text
                    try:
                        price_complete = float(price_str.replace(',', ''))
                    except ValueError:
                        price_complete = None
                else:
                    price_complete = None

                
                products_list.append({
                    "name": name,
                    "link": link,
                    "image": image,
                    "price_complete": price_complete,
                    "price_symbol": price_symbol_text,
                    "reviews": review_text,
                    "colors": colors if colors else ["No especificado"]
                })

            time.sleep(random.uniform(3, 10))

    finally:
        driver.quit()

    return analyze_with_ollama(products_list, "highest_lowest_rating")

def url_single(url: str):
    driver = get_driver()
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.a-container")))

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find_all("div", {"role": "main"})

        title_tag = content[0].find("span", {"id": "productTitle"})
        title = title_tag.get_text(strip=True) if title_tag else "Not available"

        price_whole = content[0].find("span", {"class": "a-price-whole"})
        price_fraction = content[0].find("span", {"class": "a-price-fraction"})
        about_item = content[0].find("ul", {"class": "a-unordered-list a-vertical a-spacing-mini"})
        review_tag = content[0].find("i", {"class": "cm-cr-review-stars-spacing-big"})
        colors_container = content[0].find("div", {"id": "twister_feature_div"})

        # Procesar colores
        colors = []
        seen = set()
        if colors_container:
            button_groups = colors_container.find_all(attrs={"data-a-button-group": True})
            for group in button_groups:
                options_in_group = group.find_all("span", {"class": "a-button-toggle"})
                for option in options_in_group:
                    text_span = option.find("span", {"class": "a-size-base swatch-title-text-display swatch-title-text"})
                    name = text_span.get("aria-label") if text_span else None
                    if not name and text_span:
                        name = text_span.get_text(strip=True)
                    img = option.find("img")
                    alt = img["alt"].strip() if img and img.has_attr("alt") else None
                    display_name = alt if alt else name
                    if display_name and display_name not in seen:
                        seen.add(display_name)
                        colors.append({"display_name": display_name})

        price_complete = None
        if price_whole:
            price_str = f"{price_whole.get_text(strip=True)}{price_fraction.get_text(strip=True) if price_fraction else ''}"
            try:
                price_complete = float(price_str.replace(',', ''))
            except:
                price_complete = None

        review_text = review_tag.span.get_text(strip=True) if review_tag and review_tag.span else "0 reviews"
        about_item_text = about_item.get_text(strip=True) if about_item else "Not available"

        single_product = {
            "name": title,
            "price_complete": price_complete,
            "reviews": review_text,
            "about_item": about_item_text,
            "colors": colors,
            "link": url
        }

        analysis_result = analyze_with_ollama(single_product, "detailed_product_analysis")
        summary = analysis_result.get("answer", "")

        db: Session = SessionLocal()
        try:
            asin = url.split("/dp/")[1].split("/")[0]
            existing_product = db.query(Products).filter(Products.asin == asin).first()
            #text_for_embedding = f"{title}. price: {price_complete if price_complete is not None else 'N/A'} {about_item_text}. {summary}"
            text_for_embedding = f"{title}. Price: {price_complete if price_complete else 'N/A'}. {about_item_text}"

            embedding = get_embedding(text_for_embedding)

            if existing_product:
                existing_product.name = title
                existing_product.price = price_complete
                existing_product.description = about_item_text
                existing_product.json_scraped = single_product
                existing_product.summary = summary
                existing_product.vector = embedding
                db.commit()
                db.refresh(existing_product)
                product_to_return = existing_product
            else:
                new_product = Products(
                    asin=asin,
                    name=title,
                    url=url,
                    price=price_complete,
                    description=about_item_text,
                    json_scraped=single_product,
                    summary=summary,
                    vector=embedding
                )
                db.add(new_product)
                db.commit()
                db.refresh(new_product)
                product_to_return = new_product
        finally:
            db.close()

        return {
            "id": product_to_return.id,
            "asin": product_to_return.asin,
            "name": product_to_return.name,
            "url": product_to_return.url,
            "price": product_to_return.price,
            "description": product_to_return.description,
            "summary": product_to_return.summary,
            "colors": product_to_return.json_scraped.get("colors", []),
            "link": product_to_return.json_scraped.get("link", ""),
        }

    finally:
        driver.quit()
