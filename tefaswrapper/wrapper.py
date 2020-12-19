import requests
import js2xml
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from .constants import *
from .models import Fund, FundType, Detail, Asset


class Wrapper:
    def __init__(self, fund_type=FundType.YAT):
        self.session = requests.Session()
        res = self.session.get(ENDPOINT)
        self.cookies = self.session.cookies.get_dict()
        self.initial_form_data = {**FORM_DATA, **self.__update_session_data(res, SESSION_DATA)}
        self.initial_form_data[FORM_DATA_FUND_TYPE_KEY] = fund_type

    def fetch(self, fund="", start_date=datetime.now().strftime(DATE_FORMAT),
              end_date=datetime.now().strftime(DATE_FORMAT)):
        # Get first page
        start_date = self._get_near_weekday(start_date)
        end_date = self._get_near_weekday(end_date)
        data = self.initial_form_data
        for field in FORM_DATA_START_DATE_FIELDS:
            data[field] = start_date

        for field in FORM_DATA_END_DATE_FIELDS:
            data[field] = end_date

        for field in FORM_DATA_FUND_FIELDS:
            data[field] = fund

        # Get remaining pages
        first_page = self.__get_first_page(data)
        first_general_pages = self.__parse_table(first_page.text, GENERAL_TAB)
        if first_general_pages and (
                first_general_pages[len(first_general_pages) - 1]["Tarih"] != start_date or len(fund) == 0):
            first_assets_pages = self.__parse_table(first_page.text, ASSETS_TAB)

            next_general_pages = self.__get_next_pages(data, NEXT_BUTTON_GENEL_KEY_X, NEXT_BUTTON_GENEL_KEY_Y)
            next_assets_pages = self.__get_next_pages(data, NEXT_BUTTON_ASSET_KEY_X, NEXT_BUTTON_ASSET_KEY_Y)

            parsed_general_pages = self.__parse_table(next_general_pages.text, GENERAL_TAB)
            parsed_assets_pages = self.__parse_table(next_assets_pages.text, ASSETS_TAB)

            result_general = [*first_general_pages, *parsed_general_pages]
            result_assets = [*first_assets_pages, *parsed_assets_pages]

            result = []
            for r in result_general:
                r["Portfoy Dagilimi"] = next(({k.replace("(%)", "").strip(): float(v.replace(",", ".")) for k, v in
                                               item.items() if
                                               k not in ["Tarih", "Fon Kodu", "Fon Adı"] and float(
                                                   v.replace(",", ".")) > 0} for item in result_assets if
                                              (item["Tarih"] == r["Tarih"] and item["Fon Kodu"] == r["FonKodu"])), None)
                result.append(r)

        return [Fund(data) for data in result]

    def fetch_detail(self, fund):
        response = self.session.get(
            url=ENDPOINT_DETAIL,
            params={"FonKod": fund},
            cookies=self.cookies,
            headers=HEADERS,
        )

        return self.__parse_detail(response.text)

    def __do_post(self, data):
        # TODO: error handling
        response = self.session.post(
            url=ENDPOINT,
            data=data,
            cookies=self.cookies,
            headers=HEADERS,
        )
        return response

    def __get_asset_allocation(self, bs):
        assets = []
        script = bs.find_all("script", text=re.compile("Highcharts.Chart"))[
            0].contents[0].replace("//<![CDATA[", "").replace("//]]>", "")
        data = js2xml.parse(script).xpath(
            '/program/functioncall[2]/arguments/funcexpr/body/assign['
            '@operator="="]/right/new/arguments/object/property[10]/array/object//property[3]')[0]
        data = js2xml.jsonlike.make_dict(data)[1]
        for d in data:
            assets.append(Asset(d[0], d[1]))
        return assets

    def __parse_detail(self, content):
        bs = BeautifulSoup(content, features="html.parser")
        return Detail({
            "category": bs.find_all(text="Kategorisi")[0].parent.span.contents[0],
            "rank": bs.find_all(text="Son Bir Yıllık Kategori Derecesi")[0].parent.span.contents[0],
            "market_share": bs.find_all(text="Pazar Payı")[0].parent.span.contents[0],
            "isin_code": bs.find_all(text="ISIN Kodu")[0].parent.next_sibling.text,
            "start_time": bs.find_all(text="TEFAS İşlem Başlangıç Saati")[0].parent.next_sibling.text,
            "end_time": bs.find_all(text="TEFAS Son İşlem Saati")[0].parent.next_sibling.text,
            "value_date": bs.find_all(text="Fon Alış Valörü")[0].parent.next_sibling.text,
            "back_value_date": bs.find_all(text="Fon Satış Valörü")[0].parent.next_sibling.text,
            "status": bs.find_all(text="TEFAS İşlem Durumu")[0].parent.next_sibling.text,
            "assets": self.__get_asset_allocation(bs),
            "kap_url": bs.find_all(text="KAP Bilgi Adresi")[0].parent.get("href")
        })

    def __get_first_page(self, data):
        data[PAGE_SCRIPT_KEY] = FIRST_PAGE_SCRIPT
        return self.__do_post(data)

    def __get_next_pages(self, data, keyx, keyy):
        data[PAGE_SCRIPT_KEY] = NEXT_PAGES_SCRIPT
        data[keyx] = "1"
        data[keyy] = "1"
        return self.__do_post(data)

    def _get_near_weekday(self, date):
        current_date = datetime.strptime(date, DATE_FORMAT)
        if (current_date.weekday() > 4):
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

    def __parse_table(self, content, tab):
        bs = BeautifulSoup(content, features="html.parser")
        table = bs.find("table", attrs={"id": tab})
        data = []
        rows = table.find_all("tr")
        header = rows.pop(0).find_all("th")
        header = [ele.text.strip() for ele in header]
        for row in rows:
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            data.append(dict(zip(header, cols)))

        return data
