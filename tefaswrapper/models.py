from enum import Enum
import datetime as dt

from typing import Dict, List

date_fmt = "%d-%m-%Y"


def isfloat(num):
    try:
        x = float(num)
        return x == x  # for "is not nan"
    except ValueError:
        return False


class FundType(str, Enum):
    YAT = "YAT"
    EMK = "EMK"


class Property(str, Enum):
    CODE = "FONKODU"
    TITLE = "FONUNVAN"
    DATE = "TARIH"
    PRICE = "FIYAT"
    MARKET_CAP = "PORTFOYBUYUKLUK"
    NUM_OF_SHARES = "TEDPAYSAYISI"
    NUM_OF_INVESTORS = "KISISAYISI"
    CATEGORY = "CATEGORY"
    RANK = "RANK"
    MARKET_SHARE = "MARKET_SHARE"
    ISIN_CODE = "ISIN_CODE"
    START_TIME = "START_TIME"
    END_TIME = "END_TIME"
    VALUE_DATE = "VALUE_DATE"
    BACK_VALUE_DATE = "BACK_VALUE_DATE"
    STATUS = "STATUS"
    KAP_URL = "KAP_URL"


class Asset:
    code: str
    name: str
    percent: float

    __asset_codes__ = {
        "R": "repo",
        "D": "other",
        "HS": "stock",
        "EUT": "eurobond",
        "BB": "bank bills",
        "T": "derivatives",
        "TR": "reverse repo",
        "VM": "term deposit",
        "HB": "treasury bill",
        "YHS": "foreign equity",
        "DT": "government bond",
        "KM": "precious metals",
        "FB": "commercial paper",
        "DB": "fx payable bills",
        "YMK": "foreign securities",
        "OST": "private sector bonds",
        "KH": "participation account",
        "DÖT": "foreign currency bills",
        "VDM": "asset backed securities",
        "GAS": "real estate certificate",
        "YBA": "foreign dept instrument",
        "KKS": "government lease certificates",
        "FKB": "fund participation certificate",
        "KBA": "government_bonds_and_bills_fx",
        "OSKS": "private_sector_lease_certificates",
        "VİNT": "",
        "VMTL": "",
        "VMAU": "",
        "BB": "",
        "BYF": "",
        "GSYKB": "",
        "GYKB": "",
        "KHAU": "",
        "KHD": "",
        "KHTL": "",
        "KKSD": "",
        "KKSTL": "",
        "KKSYD": "",
        "KMBYF": "",
        "KMKBA": "",
        "KMKKS": "",
        "KİBD": "",
        "TPP": "",
        "VM": "",
        "VMD": "",
        "YBKB": "",
        "YBOSB": "",
        "YBYF": "",
        "YYF": "",
        "ÖKSYD": "",
        "ÖSDB": ""
    }

    def __init__(self, code, percent) -> None:
        self.code = code
        self.percent = float(percent)
        self.name = self.__asset_codes__.get(code)

    @staticmethod
    def codes():
        return Asset.__asset_codes__.keys()

    def __repr__(self):
        return str(self.__dict__)


class History:
    date: dt.date
    timestamp: int
    price: float
    market_cap: float
    number_of_shares: int
    number_of_investors: int
    assets: List[Asset]

    def __init__(self, data: Dict) -> None:
        super().__init__()
        self.date = dt.datetime.fromtimestamp(int(data.get(Property.DATE)) / 1000).strftime(date_fmt)
        self.timestamp = int(data.get(Property.DATE))
        self.price = float(data.get(Property.PRICE))
        self.market_cap = float(data.get(Property.MARKET_CAP))
        self.number_of_shares = int(data.get(Property.NUM_OF_SHARES))
        self.number_of_investors = int(data.get(Property.NUM_OF_INVESTORS))
        self.assets = []
        for code in Asset.codes():
            if code in data and data.get(code) is not None and isfloat(data.get(code)):
                self.assets.append(Asset(code, data.get(code)))

    def __repr__(self):
        return str({**self.__dict__, **{"assets": self.assets}})


class Fund:
    code: str
    title: str
    category: str
    rank: str
    market_share: str
    isin_code: str
    start_time: str
    end_time: str
    value_date: str
    back_value_date: str
    status: str
    kap_url: str
    history: List[History]

    def __init__(self, data: dict) -> None:
        super().__init__()
        self.code = data.get(Property.CODE)
        self.title = data.get(Property.TITLE)
        self.category = data.get(Property.CATEGORY)
        self.rank = data.get(Property.RANK)
        self.market_share = data.get(Property.MARKET_SHARE)
        self.isin_code = data.get(Property.ISIN_CODE);
        self.start_time = data.get(Property.START_TIME)
        self.end_time = data.get(Property.END_TIME)
        self.value_date = data.get(Property.VALUE_DATE)
        self.back_value_date = data.get(Property.BACK_VALUE_DATE)
        self.status = data.get(Property.STATUS)
        self.kap_url = data.get(Property.KAP_URL)
        self.history = [History(data)]

    def __repr__(self):
        return str({**self.__dict__, **{"history": self.history}})
