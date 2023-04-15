from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import sys


def csv_write(date, cena, otkr, maks, minn, obj, izm, file_name):
    with open(file_name, 'a', newline = '') as file:
        writer = csv.writer(file, delimiter = ';')
        writer.writerow([date, cena, otkr, maks, minn, obj, izm])


def rasparsing(html, file_name):
    soup = BeautifulSoup(html, "lxml")
    items = soup.find("table", class_ = "genTbl closedTbl historicalTbl").find("tbody").find_all("tr")

    for item in items:
        date = item.find_all("td")[0].text
        cena = item.find_all("td")[1].text
        otkr = item.find_all("td")[2].text
        maks = item.find_all("td")[3].text
        minn = item.find_all("td")[4].text
        obj = item.find_all("td")[5].text
        izm = item.find_all("td")[6].text
        csv_write(date, cena, otkr, maks, minn, obj, izm, file_name)


def pars_companys(html, company):
    host = "https://ru.investing.com/"
    hr = "-historical-data"
    soup = BeautifulSoup(html, "lxml")
    items = soup.find("div", class_ = "js-ga-on-sort marketInnerContent filteredMarketsDiv").find("tbody").find_all("tr")

    for item in items:
        title = item.find("td", class_ = "bold left noWrap elp plusIconTd").find('a').text

        if (title == company):
            href = item.find("td", class_ = "bold left noWrap elp plusIconTd").find('a').attrs["href"]
            ref = host + href + hr
            return ref
        else:
            continue


def main():
    birga = str(input("Введите название биржы: "))
    company = str(input("Введите название компании: "))
    date1 = str(input("Введите дату начала парсинга: "))
    date2 = str(input("Введите дату конца парсинга: "))
    file_name = birga + '_' + company + ".csv"

    with open(file_name, 'a', newline = '') as file:
        writer = csv.writer(file, delimiter = ';')
        writer.writerow(["Дата", "Цена", "Откр.", "Макс.", "Мин.", "Объём", "Изм.%"])

    driver = webdriver.Chrome(r"")

    if company == "Яндекс":
        ref = "https://ru.investing.com/equities/yandex-historical-data?cid=102063"
    else:
        driver.get(r"https://ru.investing.com/equities/")
        time.sleep(1)
        driver.find_element_by_id("stocksFilter").click()
        options = driver.find_element_by_id("stocksFilter").find_elements_by_tag_name("option")

        for option in options:
            if option.text == birga:
                option.click()
            else:
                continue

        time.sleep(1)
        html = driver.find_element_by_tag_name("body").get_attribute("innerHTML")
        ref = pars_companys(html, company)
        time.sleep(1)

    driver.get(ref)
    time.sleep(1)
    driver.find_element_by_id("widgetFieldDateRange").click()
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 800);")
    driver.find_element_by_id("startDate").click()
    driver.find_element_by_id("startDate").clear()
    driver.find_element_by_id("startDate").send_keys(date1)
    driver.find_element_by_id("endDate").click()
    driver.find_element_by_id("endDate").clear()
    driver.find_element_by_id("endDate").send_keys(date2)
    driver.find_element_by_id("applyBtn").click()
    time.sleep(0.5)
    html = driver.find_element_by_tag_name("body").get_attribute("innerHTML")
    rasparsing(html, file_name)
    driver.close()
    sys.exit()


if __name__ == "__main__":
    main()