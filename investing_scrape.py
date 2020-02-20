import ctypes
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver
import time

class Forex():
    def __init__(self,begin,end):
        source_code =self.driver(begin,end)
        self.extract(source_code)

    def driver(self,begin_date,end_date):
        chrome_options = Options()
        user32 = ctypes.windll.user32  # necessary for resolution
        screensize = ("window-size={}x{}").format(user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
        chrome_options.add_argument("--headless")  # hide browser
        chrome_options.add_argument(screensize)
        self.driver = webdriver.Chrome(chrome_options=chrome_options)  # web driver
        self.driver.get("https://www.investing.com/economic-calendar")  # to go to the web site
        time.sleep(1)  # wait
        self.driver.find_element_by_id("datePickerToggleBtn").click()  # clicked
        time.sleep(2)  # wait
        self.driver.find_element_by_id("startDate").clear()  # cleaned
        self.driver.find_element_by_id("startDate").send_keys(begin_date)  # we have entered the start date
        self.driver.find_element_by_id("endDate").clear()  # cleaned
        self.driver.find_element_by_id("endDate").send_keys(end_date)  # we have entered the end date
        self.driver.execute_script("document.getElementById('applyBtn').click()")  # click apply button
        time.sleep(2)  # Wait 2 seconds
        return self.driver.page_source # page source code

    def extract(self,source_code):
        soup = BeautifulSoup(source_code, "lxml")
        table = soup.find("table", attrs={"id": "economicCalendarData"})  # we get the source code for the table
        tbody = table.find('tbody')  # we get the source code for the table
        rows = tbody.findAll('tr', {"class": "js-event-item"})  # we get the source code for the rows

        for row in rows:
            impact = row.find('td', {"class": "flagCur"}).text
            event_row_code = row.find('td', {"class": "event"})
            event_row = event_row_code.find('a').text
            event = event_row.strip()

            curr = row.findAll("link", {"class": "grayFullBullishIcon"})
            currency = len(curr)

            actual = row.find("td", {"class": "bold"}).text
            forecast = row.find('td', {"class": "fore"}).text
            previous = row.find('td', {"class": "prev"}).text

            date_time = row.attrs['data-event-datetime']
            date_and_time = date_time.split()
            date = date_and_time[0]
            time = date_and_time[1]

            if "'" in event:
                finished_event = event.replace("'", "")
            else:
                finished_event = event
            print(" {} /  {} /{} / {} / {} / {} / {} / {}".format(date, time, impact, currency, finished_event, actual,
                                                                  forecast, previous))
        self.driver.close()

if __name__ == "__main__":
    begin_date = "MM/DD/YYYY"
    end_date = "MM/DD/YYYY"
    investing = Forex(begin_date,end_date)
