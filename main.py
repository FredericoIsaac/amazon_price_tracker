import requests
from bs4 import BeautifulSoup
import smtplib
import email
import os


URL = "https://www.amazon.com/Instant-Pot-Duo-Evo-Plus/dp/B07W55DDFB/ref=sr_1_1?qid=1597662463"
E_MAIL = "fredericogago@hotmail.com"
PASS_MAIL = os.environ["PASS_MAIL"]

headers = {
    "Accept-Language": "pt-PT,pt;q=0.9,pt-BR;q=0.8,en;q=0.7,en-US;q=0.6,en-GB;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                  " (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36 Edg/89.0.774.45"
}


response = requests.get(url=URL, headers=headers)
response.raise_for_status()
web_data = response.text

"""
HINT: If you get an error that says "bs4.FeatureNotFound: Couldn't find a tree builder with the features you requested:
 html-parser." Then it means you're not using the right parser, you'll need to import lxml at the top and install
 the module then use "lxml" instead of "html.parser" when you make soup.
"""
soup = BeautifulSoup(web_data, "html.parser")

title_product = soup.find(name="span", id="productTitle").getText().strip()

price_tag = soup.find(name="span", id="priceblock_ourprice")
price = float(price_tag.getText().split("$")[1])

title_product = title_product.encode("utf-8")

if price < 100:
    msg = email.message_from_string(f"{title_product} is now ${price}\n{URL}")
    msg['From'] = E_MAIL
    msg['To'] = E_MAIL
    msg['Subject'] = "Warning price drop down"

    server = smtplib.SMTP("smtp.live.com", 587)
    server.ehlo()  # Hostname to send for this command defaults to the fully qualified domain name of the local host.
    server.starttls()  # Puts connection to SMTP server in TLS mode
    server.ehlo()
    server.login(E_MAIL, PASS_MAIL)
    server.sendmail(E_MAIL, E_MAIL, msg.as_string())
    server.quit()
