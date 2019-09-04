import ctypes
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver
import time

print("Please enter the start date and end date. For example (MM/DD/YYYY)\n")
begin_date = input("Start date :  ")
end_date = input("End date :  ")

chrome_options = Options()
user32 = ctypes.windll.user32  # necessary for resolution
screensize = ("window-size={}x{}").format(user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
chrome_options.add_argument("--headless")  # hide browser
chrome_options.add_argument(screensize)
driver = webdriver.Chrome(chrome_options=chrome_options)  # web driver
driver.get("https://www.investing.com/economic-calendar")  # to go to the web site
time.sleep(1)  # wait
driver.find_element_by_id("datePickerToggleBtn").click()  # clicked
time.sleep(2)  # wait
driver.find_element_by_id("startDate").clear()  # cleaned
driver.find_element_by_id("startDate").send_keys(begin_date)  # we have entered the start date
driver.find_element_by_id("endDate").clear()  # cleaned
driver.find_element_by_id("endDate").send_keys(end_date)  # we have entered the end date
driver.execute_script("document.getElementById('applyBtn').click()")  # click apply button
time.sleep(2)  # Wait 2 seconds

source_code = driver.page_source
soup = BeautifulSoup(source_code, "lxml")
table = soup.find("table", attrs={"id": "economicCalendarData"})  # we get the source code for the table
tbody = table.find('tbody')  # we get the source code for the table
rows = tbody.findAll('tr', {"class": "js-event-item"})  # we get the source code for the rows


for row in rows:
    ############## event zone
    impact = row.find('td', {"class": "flagCur"}).text
    event_row_code = row.find('td', {"class": "event"})
    event_row = event_row_code.find('a').text
    event = event_row.strip()

    ############### currency zone
    curr = row.findAll("link", {"class": "grayFullBullishIcon"})
    currency = len(curr)

    ############## actual, forecast, previous zone
    actual = row.find("td", {"class": "bold"}).text
    forecast = row.find('td', {"class": "fore"}).text
    previous = row.find('td', {"class": "prev"}).text

    ############## date and time  zone
    date_time = row.attrs['data-event-datetime']
    date_and_time = date_time.split()
    date = date_and_time[0]
    time = date_and_time[1]

    if "'" in event:
        finished_event = event.replace("'", "")
    else:
        finished_event = event
    print(" {} /  {} /{} / {} / {} / {} / {} / {}".format(date, time, impact, currency, finished_event, actual,forecast, previous))

driver.close()
