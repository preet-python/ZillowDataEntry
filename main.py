import re
import time

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://appbrewery.github.io/Zillow-Clone/"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0"}
response = requests.get(URL,headers)
zillow_web_page = response.text
soup = BeautifulSoup(zillow_web_page,"html.parser")
all_matching_items = soup.select("li:has(div.StyledPropertyCardDataWrapper)")

#Part 1 Web scrpaing
def clean_up(input):
    result = input
    result = input.strip().replace(" |",",")
    words = ["+1 bd","+ 1bd", "+ 1 bd","+/mo","/mo"]
    sorted_words = sorted(words, key=len, reverse=True)
    for word in sorted_words:
        if word in result:
            result = result.removesuffix(word).strip()
            break
    return result


all_links = []
all_prices = []
all_addresses = []
# You can loop through them just like a find_all list
for item in all_matching_items:
    anchor_tag = item.find(name = "a", attrs={"data-test":"property-card-link"})
    address_tag = anchor_tag.find(name="address", attrs={"data-test":"property-card-addr"})
    price = item.find(name="span", attrs={"data-test": "property-card-price"})
    all_links.append(anchor_tag.get_attribute_list("href"))
    all_prices.append(clean_up(address_tag.text))
    all_addresses.append(clean_up(price.text))

print(all_links)
print(all_prices)
print(all_addresses)

# Part 2 - Fill in the Google Form using Selenium

# Optional - Keep the browser open (helps diagnose issues if the script crashes)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

for n in range(len(all_links)):
    driver.get("https://forms.gle/TNDyHKuZPKVbeq9G8")
    time.sleep(3)
    address = driver.find_element(by=By.XPATH,
                                  value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(by=By.XPATH,
                                value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(by=By.XPATH,
                               value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(by=By.XPATH,
                                        value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    address.send_keys(all_addresses[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])
    submit_button.click()

