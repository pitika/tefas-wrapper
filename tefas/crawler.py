import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from .constants import *


class Crawler:
    def __init__(self):
        self.session = requests.Session()
        res = self.session.get(ENDPOINT)
        self.cookies = self.session.cookies.get_dict()
        self.initial_form_data = {**FORM_DATA, **
                                  self.__update_session_data(res, SESSION_DATA)}

    def fetch_from(self, start_date, fund):
        now = datetime.now()
        end_date = now.strftime(DATE_FORMAT)
        return self.fetch(start_date, end_date, fund)

    def fetch_single(self, date, fund):
        near_date = self._get_near_weekday(date)
        return self.fetch(start_date=near_date, end_date=near_date, fund=fund)

    def fetch(self, start_date, end_date, fund):
        # Get first page
        data = self.initial_form_data
        for field in FORM_DATA_START_DATE_FIELDS:
            data[field] = start_date

        for field in FORM_DATA_END_DATE_FIELDS:
            data[field] = end_date

        for field in FORM_DATA_FUND_FIELDS:
            data[field] = fund

        # Get remaining pages
        first_page = self.__get_first_page(data)
        first_page = self.__parse_table(first_page.text, HTML_TABLE_IDS[0])
        next_pages = self.__get_next_pages(data)
        next_pages = self.__parse_table(next_pages.text, HTML_TABLE_IDS[0])
        return [*first_page, *next_pages]

    def __do_post(self, data):
        # TODO: error handling
        response = self.session.post(
            url=ENDPOINT,
            data=data,
            cookies=self.cookies,
            headers=HEADERS,
        )
        return response

    def __get_first_page(self, data):
        mng = "ctl00$MainContent$UpdatePanel1|ctl00$MainContent$ButtonSearchDates"
        data["ctl00$MainContent$ScriptManager1"] = mng
        return self.__do_post(data)

    def __get_next_pages(self, data):
        mng = "ctl00$MainContent$UpdatePanel1|ctl00$MainContent$ImageButtonGenelNext"
        data["ctl00$MainContent$ScriptManager1"] = mng
        data["ctl00$MainContent$ImageButtonGenelNext.x"] = "1"
        data["ctl00$MainContent$ImageButtonGenelNext.y"] = "1"
        return self.__do_post(data)

    def _get_near_weekday(self, date):
        current_date = datetime.strptime(date, DATE_FORMAT)
        if(current_date.weekday() > 4):
            result = self._get_near_weekday(
                (current_date - timedelta(days=1)).strftime(DATE_FORMAT))
        else:
            result = current_date.strftime(DATE_FORMAT)
        return result

    def __update_session_data(self, res, data):
        soup = BeautifulSoup(res.text, features="html.parser")
        updated_data = {
            key: soup.find(attrs={"name": key}).get("value", "")
            if soup.find(attrs={"name": key})
            else data[key]
            for key in data
        }
        return updated_data

    def __parse_table(self, content, table_id):
        bs = BeautifulSoup(content, features="html.parser")
        table = bs.find("table", attrs={"id": table_id})
        data = []
        rows = table.find_all("tr")
        header = rows.pop(0).find_all("th")
        header = [ele.text.strip() for ele in header]
        for row in rows:
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            data.append(dict(zip(header, cols)))
        return data
