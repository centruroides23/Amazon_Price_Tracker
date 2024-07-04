import pandas as pd
import requests
from bs4 import BeautifulSoup
import smtplib
import os

USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
URL = "https://www.amazon.com.mx/bilbil-computadora-el%C3%A9ctrico-ajustable-elevadora/dp/B0B5RCV367/ref=sr_1_27?crid=9N5ZW9KS0RTH&dib=eyJ2IjoiMSJ9._BsUOz0rgizvIcOoUzQxmtWcu201WP7b0_S3ZXrBJZALn4cHEdsFW8grdAIlh-NlgtfpXqT4s9kOjXcMeOVDUlAUUyJVwVhZsXwdPJ-tz5YeWSnPAjMz_cqoyB5oBRxbvUsOnsMkdgDJa295hQWEs_gGGf9I7ry3oBysGqQUY2ZEc7R5B4Bj8LerXVFIV90f9zzDz2epxd5KkmTXcG_ftIkJxU1b6DmtURciks96EuBr5kPBU79BWZzWTDuBk3wLXeSoglFi9M10yHxKt9jl5cprVYQeZaOBOZ0JXg0NScA.5KQtr_3PmYaXV1uWAmpW0JWIfhSL1H2_w-iIX1i-2OE&dib_tag=se&keywords=escritorio%2Belevable&qid=1713567540&sprefix=Escritorio%2Bele%2Caps%2C172&sr=8-27&ufe=app_do%3Aamzn1.fos.4e545b5e-1d45-498b-8193-a253464ffa47&th=1"
HEADERS = {"User-Agent": "Defined"}


def update_price_in_csv(csv_file, index, new_price):
    csv_file.at[index, 'Price'] = new_price
    csv_file.to_csv("price_file.csv", index=False)


# ---------------------------------- Scrape Amazon for the specified product ----------------------------------- #
price_csv = pd.read_csv("price_file.csv")
for index, row in price_csv.iterrows():
    price_tag = None
    while price_tag is None:
        website = requests.get(url=row["Link"], headers=HEADERS).text
        soup = BeautifulSoup(website, "html.parser")
        price_tag = soup.find(name="span", class_="a-price-whole")
    price = float(price_tag.text.split(".")[0].replace(",", ""))
    print(price)

    if row["Price"] > price:
        subject = "Subject: Python PriceTracker: Price Drop in Product\n\n"
        body = f"Price Drop Alert! The {row['Product']} has its price lowered form ${row['Price']} to ${price}."
        message = f"{subject}{body}"

        with smtplib.SMTP("SMTP.gmail.com") as connection:
            connection.starttls()
            connection.login(user=USERNAME, password=PASSWORD)
            connection.sendmail(to_addrs="oscar.bejarano503@gmail.com",
                                from_addr=USERNAME,
                                msg=message)

        update_price_in_csv(price_csv, index, price)
