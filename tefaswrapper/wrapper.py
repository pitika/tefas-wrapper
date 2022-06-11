import requests
import js2xml
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from .models import FundType, Asset
from .schema import History, Fund
import pandas as pd


class Wrapper:
    root_url = "https://www.tefas.gov.tr"
    detail_page = f"{root_url}/FonAnaliz.aspx"
    info_api = f"{root_url}/api/DB/BindHistoryInfo"
    allocation_api = f"{root_url}/api/DB/BindHistoryAllocation"

    date_format = "%d.%m.%Y"

    fund_type = FundType.YAT

    def __init__(self):
        self.session = requests.Session()
        self.session.get(self.root_url)
        self.cookies = self.session.cookies.get_dict()

    def set_fund_type(self, fund_type: FundType):
        self.fund_type = fund_type

    def fetch(self,
              fund_code="",
              start_date=datetime.now().strftime(date_format),
              end_date=datetime.now().strftime(date_format)):

        # Get first page
        start_date = self._get_near_weekday(start_date)
        end_date = self._get_near_weekday(end_date)

        data = {
            "fontip": self.fund_type,
            "bastarih": start_date,
            "bittarih": end_date,
            "fonkod": fund_code.upper()
        }

        info_resp = self.__do_post(self.info_api, data)
        alloc_resp = self.__do_post(self.allocation_api, data)

        info_df = pd.DataFrame.from_records(info_resp)
        alloc_df = pd.DataFrame.from_records(alloc_resp)

        fund_df = pd.merge(info_df, alloc_df, on=["TARIH", "FONKODU"], suffixes=('', '_drop'))
        fund_df.drop([col for col in fund_df.columns if 'drop' in col], axis=1, inplace=True)

        result = {}
        for _, row in fund_df.iterrows():
            fund = result.get(row.get("FONKODU"))
            if fund is None:
                detail = self.fetch_detail(row.get("FONKODU"))
                result[row.get("FONKODU")] = Fund().load({**row.to_dict(), **detail})
            else:
                history = fund.get("history")
                history.append(History().load(row.to_dict()))

        return result

    def fetch_detail(self, fund):
        response = self.session.get(
            url=self.detail_page,
            params={"FonKod": fund},
            cookies=self.cookies
        )

        return self.__parse_detail(response.text)

    def __do_post(self, url, data):
        response = self.session.post(
            url=url,
            data=data,
            cookies=self.cookies
        )

        return response.json().get("data", {})

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
        return {
            "category": bs.find_all(text="Kategorisi")[0].parent.span.contents[0],
            "rank": bs.find_all(text="Son Bir Yıllık Kategori Derecesi")[0].parent.span.contents[0],
            "market_share": bs.find_all(text="Pazar Payı")[0].parent.span.contents[0],
            "isin_code": bs.find_all(text="ISIN Kodu")[0].parent.next_sibling.text,
            "start_time": bs.find_all(text="İşlem Başlangıç Saati")[0].parent.next_sibling.text,
            "end_time": bs.find_all(text="Son İşlem Saati")[0].parent.next_sibling.text,
            "value_date": bs.find_all(text="Fon Alış Valörü")[0].parent.next_sibling.text,
            "back_value_date": bs.find_all(text="Fon Satış Valörü")[0].parent.next_sibling.text,
            "status": bs.find_all(text="Platform İşlem Durumu")[0].parent.next_sibling.text,
            # "assets": self.__get_asset_allocation(bs),
            "kap_url": bs.find_all(text="KAP Bilgi Adresi")[0].parent.get("href")
        }

    def _get_near_weekday(self, date):
        current_date = datetime.strptime(date, self.date_format)
        if current_date.weekday() > 4:
            result = self._get_near_weekday(
                (current_date - timedelta(days=1)).strftime(self.date_format))
        else:
            result = current_date.strftime(self.date_format)
        return result
