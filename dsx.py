import requests
from bs4 import BeautifulSoup
import sqlite3
import time

connection = sqlite3.connect("weather.db")
cur = connection.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS weather_dz (weath TEXT);")
connection.commit()

for x in range(10):
    response = requests.get("https://www.gismeteo.md/weather-zaporizhia-5093")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, features="html.parser")
        soup_list_timestamp = soup.find_all('div', {'class': 'temperature'})
        if soup_list_timestamp:
            res_timestamp = soup_list_timestamp[0].find("span")
        else:
            res_timestamp = "weath"

        print(res_timestamp.text)

        soup_list = soup.find_all('div', {'class': 'temperature'})
        res = soup_list[0].find("span")
        print("Температура - " + res.text)

        cur.execute("INSERT INTO weather_dz (weath) VALUES (?);", (res_timestamp.text + " " + res.text,))
        time.sleep(1800)

cur.execute("SELECT weath FROM weather_dz;")
res = cur.fetchall()
print(res)

connection.close()
