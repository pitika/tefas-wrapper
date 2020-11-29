from enum import Enum

class Base:
    def __repr__(self):
        return str(self.__dict__)

class FundType(str, Enum):
    YAT = "YAT"
    EMK = "EMK"

class Fund(Base):
    def __init__(self, data):
        self.date = data["Tarih"]
        self.code = data["FonKodu"]
        self.name = data["Fon Adı"]
        self.price = data["Fiyat"]
        self.shares = data["TedavüldekiPaySayısı"]
        self.person= data["KişiSayısı"]
        self.aum = data["Fon Toplam Değer"]
        

class Detail(Base):
    def __init__(self, data):
        self.category = data["category"]
        self.rank = data["rank"]
        self.market_share = data["market_share"]
        self.isin_code = data["isin_code"]
        self.start_time = data["start_time"]
        self.end_time = data["end_time"]
        self.value_date = data["value_date"]
        self.back_value_date = data["back_value_date"]
        self.status = data["status"]
        self.assets = data["assets"]
        self.kap_url = data["kap_url"]


class Asset(Base):
    def __init__(self, name, percent):
        self.name = name
        self.percent = percent