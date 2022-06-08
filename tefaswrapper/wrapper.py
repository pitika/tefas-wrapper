import requests
import js2xml
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from .models import Fund, FundType, Detail, Asset


class Wrapper:
    root_url = "https://www.tefas.gov.tr"
    detail_page = f"{root_url}/FonAnaliz.aspx"
    info_api = f"{root_url}/api/DB/BindHistoryInfo"
    allocation_api = f"{root_url}/api/DB/BindHistoryAllocation"

    date_format = "%d.%m.%Y"

    def __init__(self, fund_type=FundType.YAT):
        self.session = requests.Session()
        self.session.get(self.root_url)
        self.cookies = self.session.cookies.get_dict()

    def fetch(self, fund="", start_date=datetime.now().strftime(date_format),
              end_date=datetime.now().strftime(date_format)):

        # Get first page
        start_date = self._get_near_weekday(start_date)
        end_date = self._get_near_weekday(end_date)

        data = {
            "fontip": FundType.YAT,
            "bastarih": start_date,
            "bittarih": end_date,
            "fonkod": fund.upper()
        }

        response = self.session.post(
            url=self.info_api,
            data=data,
            cookies=self.cookies
        )

        # data = self.initial_form_data
        # for field in FORM_DATA_START_DATE_FIELDS:
        #     data[field] = start_date
        #
        # for field in FORM_DATA_END_DATE_FIELDS:
        #     data[field] = end_date
        #
        # for field in FORM_DATA_FUND_FIELDS:
        #     data[field] = fund
        #
        # # Get remaining pages
        # first_page = self.__get_first_page(data)
        # first_general_pages = self.__parse_table(first_page.text, GENERAL_TAB)
        # if first_general_pages and (
        #         first_general_pages[len(first_general_pages) - 1]["Tarih"] != start_date or len(fund) == 0):
        #     first_assets_pages = self.__parse_table(first_page.text, ASSETS_TAB)
        #
        #     next_general_pages = self.__get_next_pages(data, NEXT_BUTTON_GENEL_KEY_X, NEXT_BUTTON_GENEL_KEY_Y)
        #     next_assets_pages = self.__get_next_pages(data, NEXT_BUTTON_ASSET_KEY_X, NEXT_BUTTON_ASSET_KEY_Y)
        #
        #     parsed_general_pages = self.__parse_table(next_general_pages.text, GENERAL_TAB)
        #     parsed_assets_pages = self.__parse_table(next_assets_pages.text, ASSETS_TAB)
        #
        #     result_general = [*first_general_pages, *parsed_general_pages]
        #     result_assets = [*first_assets_pages, *parsed_assets_pages]
        #
        #     result = []
        #     for r in result_general:
        #         r["Portfoy Dagilimi"] = next(({k.replace("(%)", "").strip(): float(v.replace(",", ".")) for k, v in
        #                                        item.items() if
        #                                        k not in ["Tarih", "Fon Kodu", "Fon Adı"] and float(
        #                                            v.replace(",", ".")) > 0} for item in result_assets if
        #                                       (item["Tarih"] == r["Tarih"] and item["Fon Kodu"] == r["FonKodu"])), None)
        #         result.append(r)

        # return [Fund(data) for data in result]

        return response.json().get("data", {})

    def fetch_detail(self, fund):
        response = self.session.get(
            url=self.detail_page,
            params={"FonKod": fund},
            cookies=self.cookies
        )

        return self.__parse_detail(response.text)

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
            "start_time": bs.find_all(text="İşlem Başlangıç Saati")[0].parent.next_sibling.text,
            "end_time": bs.find_all(text="Son İşlem Saati")[0].parent.next_sibling.text,
            "value_date": bs.find_all(text="Fon Alış Valörü")[0].parent.next_sibling.text,
            "back_value_date": bs.find_all(text="Fon Satış Valörü")[0].parent.next_sibling.text,
            "status": bs.find_all(text="Platform İşlem Durumu")[0].parent.next_sibling.text,
            "assets": self.__get_asset_allocation(bs),
            "kap_url": bs.find_all(text="KAP Bilgi Adresi")[0].parent.get("href")
        })

    def _get_near_weekday(self, date):
        current_date = datetime.strptime(date, self.date_format)
        if current_date.weekday() > 4:
            result = self._get_near_weekday(
                (current_date - timedelta(days=1)).strftime(self.date_format))
        else:
            result = current_date.strftime(self.date_format)
        return result
