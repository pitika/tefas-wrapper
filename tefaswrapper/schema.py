from datetime import date as dt
from marshmallow import Schema, fields, EXCLUDE, post_load

date_fmt = "%d-%m-%Y"

class Allocation(Schema):
    tmm = fields.Float(data_key="TMM (%)", allow_none=True)
    repo = fields.Float(data_key="R", allow_none=True)
    other = fields.Float(data_key="D", allow_none=True)
    stock = fields.Float(data_key="HS", allow_none=True)
    eurobonds = fields.Float(data_key="EUT", allow_none=True)
    bank_bills = fields.Float(data_key="BB", allow_none=True)
    derivatives = fields.Float(data_key="T", allow_none=True)
    reverse_repo = fields.Float(data_key="TR", allow_none=True)
    term_deposit = fields.Float(data_key="VM", allow_none=True)
    treasury_bill = fields.Float(data_key="HB", allow_none=True)
    foreign_equity = fields.Float(data_key="YHS", allow_none=True)
    government_bond = fields.Float(data_key="DT", allow_none=True)
    precious_metals = fields.Float(data_key="KM", allow_none=True)
    commercial_paper = fields.Float(data_key="FB", allow_none=True)
    fx_payable_bills = fields.Float(data_key="DB", allow_none=True)
    foreign_securities = fields.Float(data_key="YMK", allow_none=True)
    private_sector_bond = fields.Float(data_key="OST", allow_none=True)
    participation_account = fields.Float(data_key="KH", allow_none=True)
    foreign_currency_bills = fields.Float(data_key="DÖT", allow_none=True)
    asset_backed_securities = fields.Float(data_key="VDM", allow_none=True)
    real_estate_certificate = fields.Float(data_key="GAS", allow_none=True)
    foreign_debt_instruments = fields.Float(data_key="YBA", allow_none=True)
    government_lease_certificates = fields.Float(data_key="KKS", allow_none=True)
    fund_participation_certificate = fields.Float(data_key="FKB", allow_none=True)
    government_bonds_and_bills_fx = fields.Float(data_key="KBA", allow_none=True)
    private_sector_lease_certificates = fields.Float(data_key="OSKS", allow_none=True)

    @post_load(pass_original=True)
    def post_load_hool(self, data, orig_data, **kwargs):
        # Replace None values with 0 for float fields
        data = {
            k: v
            if not (isinstance(self.fields[k], fields.Float) and v is None)
            else 0.0
            for k, v in data.items()
        }
        # Fill missing fields with default None
        data = {f: data.setdefault(f) for f in self.fields}
        return data

    # pylint: enable=no-self-use
    # pylint: enable=unused-argument

    class Meta:
        unknown = EXCLUDE

class History(Schema):
    date = fields.Date()
    timestamp = fields.Number(data_key="TARIH", allow_none=True)
    price = fields.Float(data_key="FIYAT", allow_none=True)
    market_cap = fields.Float(data_key="PORTFOYBUYUKLUK", allow_none=True)
    number_of_shares = fields.Number(data_key="TEDPAYSAYISI", allow_none=True)
    number_of_investors = fields.Number(data_key="KISISAYISI", allow_none=True)
    allocation = fields.Nested(Allocation)

    @post_load(pass_original=True)
    def post_load_hool(self, data, orig_data, **kwargs):
        data["date"] = dt.fromtimestamp(int(orig_data["TARIH"]) / 1000).strftime(date_fmt)
        data["allocation"] = Allocation().load(orig_data)
        # Fill missing fields with default None
        data = {f: data.setdefault(f) for f in self.fields}
        return data

    class Meta:
        unknown = EXCLUDE

class Fund(Schema):
    code = fields.String(data_key="FONKODU", allow_none=True)
    title = fields.String(data_key="FONUNVAN", allow_none=True)
    category = fields.String(data_key="category", allow_none=True)
    rank = fields.String(data_key="rank", allow_none=True)
    market_share = fields.String(data_key="market_share", allow_none=True)
    isin_code = fields.String(data_key="isin_code", allow_none=True)
    start_time = fields.String(data_key="start_time", allow_none=True)
    end_time = fields.String(data_key="end_time", allow_none=True)
    value_date = fields.String(data_key="value_date", allow_none=True)
    back_value_date = fields.String(data_key="back_value_date", allow_none=True)
    status = fields.String(data_key="status", allow_none=True)
    kap_url = fields.String(data_key="kap_url", allow_none=True)
    history = fields.Nested(fields.Nested(History))

    @post_load(pass_original=True)
    def post_load_hool(self, data, orig_data, **kwargs):
        data["history"] = [History().load(orig_data)]
        # Fill missing fields with default None
        data = {f: data.setdefault(f) for f in self.fields}
        return data

    class Meta:
        unknown = EXCLUDE

