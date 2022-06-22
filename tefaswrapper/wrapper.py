import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from .models import FundType, History, Fund, Property
import pandas as pd
from typing import Type, Mapping


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
              end_date=datetime.now().strftime(date_format)) -> Mapping[str, Type[Fund]]:

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

        fund_df = pd.merge(info_df, alloc_df, on=[Property.DATE, Property.CODE], suffixes=('', '_drop'))
        fund_df.drop([col for col in fund_df.columns if 'drop' in col], axis=1, inplace=True)

        result: Mapping[str, Type[Fund]] = {}
        for _, row in fund_df.iterrows():
            fund = result.get(row.get(Property.CODE))
            if fund is None:
                detail = self.fetch_detail(row.get(Property.CODE))
                result[row.get(Property.CODE)] = Fund({**row.to_dict(), **detail})
            else:
                fund.history.append(History(row.to_dict()))

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

    def __parse_detail(self, content):
        bs = BeautifulSoup(content, features="html.parser")
        return {
            Property.CATEGORY: bs.find_all(text="Kategorisi")[0].parent.span.contents[0],
            Property.RANK: bs.find_all(text="Son Bir Yıllık Kategori Derecesi")[0].parent.span.contents[0],
            Property.MARKET_SHARE: bs.find_all(text="Pazar Payı")[0].parent.span.contents[0],
            Property.ISIN_CODE: bs.find_all(text="ISIN Kodu")[0].parent.next_sibling.text,
            Property.START_TIME: bs.find_all(text="İşlem Başlangıç Saati")[0].parent.next_sibling.text,
            Property.END_TIME: bs.find_all(text="Son İşlem Saati")[0].parent.next_sibling.text,
            Property.VALUE_DATE: bs.find_all(text="Fon Alış Valörü")[0].parent.next_sibling.text,
            Property.BACK_VALUE_DATE: bs.find_all(text="Fon Satış Valörü")[0].parent.next_sibling.text,
            Property.STATUS: bs.find_all(text="Platform İşlem Durumu")[0].parent.next_sibling.text,
            Property.KAP_URL: bs.find_all(text="KAP Bilgi Adresi")[0].parent.get("href")
        }

    def _get_near_weekday(self, date):
        current_date = datetime.strptime(date, self.date_format)
        if current_date.weekday() > 4:
            result = self._get_near_weekday(
                (current_date - timedelta(days=1)).strftime(self.date_format))
        else:
            result = current_date.strftime(self.date_format)
        return result
