class Fund:

    def __init__(self, data):
        self.date = data["Tarih"]
        self.code = data["FonKodu"]
        self.name = data["Fon Adı"]
        self.price = data["Fiyat"]
        self.shares = data["TedavüldekiPaySayısı"]
        self.person= data["KişiSayısı"]
        self.aum = data["Fon Toplam Değer"]

    def __repr__(self):
        return str(self.__dict__)
