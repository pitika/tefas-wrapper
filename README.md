# Tefas Crawler

Crawl public fund information from [Tefas](https://www.tefas.gov.tr) with ease.

"""Fetch public fund information from ``https://www.tefas.gov.tr``.

    Attributes:

    Examples:

    >>> tefas = Crawler()
    >>> data = tefas.fetch(date="2020-11-20")
    >>> data = tefas.fetch(date="2020-11-20", fund="AAK")
    >>> data = tefas.fetch(start_date="2020-11-19", end_date="2020-11-20")
    >>> data = tefas.fetch(start_date="2020-11-19", end_date="2020-11-20", fund="AAK")
    >>> print(data[0])
    {
        'Tarih': '20.11.2020',
        'FonKodu': 'AAK',
        'Fon Adı': 'ATA PORTFÖY ÇOKLU VARLIK DEĞİŞKEN FON',
        'Fiyat': '41,302235',
        'TedavüldekiPaySayısı': '1.898.223,00',
        'KişiSayısı': '422',
        'Fon Toplam Değer': '78.400.851,68'},
        'Banka Bonosu (%)': '0,00',
        ...
    }
    """