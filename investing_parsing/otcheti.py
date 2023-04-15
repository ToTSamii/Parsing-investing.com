from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import sys


with open("otcheti.csv", 'a', newline = '') as file:
    writer = csv.writer(file, delimiter = ';')
    writer.writerow(["Дата", "Страна", "Компания", "Аббвиатура", "Время"])


def csv_write(date, countrys, company, abv, pps):
    with open("otcheti.csv", 'a', newline = '') as file:
        writer = csv.writer(file, delimiter = ';')
        writer.writerow([date, countrys, company, abv, pps])


def rasparsing(html):
    soup = BeautifulSoup(html, "lxml")
    items = soup.find("table", class_ = "genTbl closedTbl ecoCalTbl earnings persistArea js-earnings-table").find("tbody").find_all("tr")

    for item in items:

        if item.attrs:
            date = item.find("td", class_ = "theDay").text
        else:
            countrys = item.find("td", class_ = "flag").find("span").attrs["title"]
            company = item.find("td", class_ = "left noWrap earnCalCompany").find("span").text
            abv = item.find("td", class_ = "left noWrap earnCalCompany").find('a').text
            ks = item.find("td", class_ = "right time").attrs["data-value"]

            if ks == '1':
                pps = "До открытия рынка"
            elif ks == '2':
                pps = "Во время открытия рынка"
            elif ks == '3':
                pps = "После закрытия рынка"
            else:
                pps = ""
 
            csv_write(date, countrys, company, abv, pps)


def main():
    d1 = int(input("Введите начальный день: "))
    m1 = int(input("Введите начальный месяц: "))
    y1 = int(input("Введите начальный год: 20"))
    nm = int(input("Введите конечный месяц: "))
    ny = int(input("Введите конечный год: 20"))
    m2 = m1
    y2 = y1
    driver = webdriver.Chrome(r"")
    driver.get(r"https://ru.investing.com/earnings-calendar/")
    
    while True:
        d2 = d1 + 1

        if (m2 == 4 or m2 == 6 or m2 == 9 or m2 == 11) and d2 == 31:
            d2 = 30
                
        if not (m2 == 4 or m2 == 6 or m2 == 9 or m2 == 11 or m2 == 2) and d1 == 29:
            d2 = 31

        if m1 == 13:
            m2 = 1
            m1 = 1
            y2 += 1
            y1 += 1
            d1 = 1  
            
        driver.find_element_by_id("datePickerToggleBtn").click()
        driver.find_element_by_id("startDate").click()
        driver.find_element_by_id("startDate").clear()
        driver.find_element_by_id("startDate").send_keys(f"{d1}/{m1}/20{y1}")
        driver.find_element_by_id("endDate").click()
        driver.find_element_by_id("endDate").clear()
        driver.find_element_by_id("endDate").send_keys(f"{d2}/{m2}/20{y2}")
        driver.find_element_by_id("applyBtn").click()
        time.sleep(1)

        d1 += 2      

        time.sleep(3)
        html = driver.find_element_by_tag_name("body").get_attribute("innerHTML")
        rasparsing(html)

        if (d2 == 30 or d2 == 31) or (m2 == 2 and d2 == 28):
            m2 += 1
            m1 += 1
            d1 = 1

        if y2 == ny and m2 == nm:
            break 

    driver.close()
    sys.exit()


if __name__ == "__main__":
    main()