ENDPOINT = "https://www.tefas.gov.tr/TarihselVeriler.aspx"
ENDPOINT_DETAIL = "https://www.tefas.gov.tr/FonAnaliz.aspx"
MAX_FETCH = 10000
DATE_FORMAT = "%d.%m.%Y"
FORM_DATA = {
    # variable data
    "ctl00$MainContent$ScriptManager1": "",
    "ctl00$MainContent$TextBoxStartDate": "",
    "ctl00$MainContent$TextBoxEndDate": "",
    "ctl00$MainContent$HTarihselBitTarih": "",
    "ctl00$MainContent$HTarihselBasTarih": "",
    "ctl00$MainContent$HGeneralBasSira": "0",
    "ctl00$MainContent$HGeneralBitSira": str(MAX_FETCH),
    "ctl00$MainContent$HAllocationBasSira": "0",
    "ctl00$MainContent$HAllocationBitSira": str(MAX_FETCH),
    "ctl00$MainContent$ImageButtonGenelNext.x": "",
    "ctl00$MainContent$ImageButtonGenelNext.y": "",
    "ctl00$MainContent$HiddenFieldFundId": "",
    "ctl00$MainContent$HTarihselFonKod": "",
    "ctl00$MainContent$RadioButtonListFundMainType": "",
    # fixed data
    "ctl00$MainContent$ButtonSearchDates": "G\xF6r\xFCnt\xFCle",
    "ctl00$MainContent$TextBoxOtherFund": "",
    "ctl00$MainContent$TextBoxWatermarkExtenderFund_ClientState": "",
    "ctl00$MainContent$DropDownListExtraFundType": "T\xFCm\xFC",
    "ctl00$MainContent$DropDownListFundTypeExplanation": "",
    "ctl00$MainContent$TextBoxWatermarkExtenderStartDate_ClientState": "",
    "ctl00$MainContent$TextBoxWatermarkExtenderEndDate_ClientState": "",
    "ctl00$MainContent$HTarihselFonTip": "YAT",
    "ctl00$MainContent$hdnSelectedTab": "0",
    "ctl00$MainContent$HTarihselFonTurKod": "",
    "ctl00$MainContent$HTarihselFonExtraTur": "",
    "ctl00$MainContent$HSortDirection": "Descending",
    "ctl00$MainContent$HGeneralSortExpression": "Descending",
    "ctl00$MainContent$HAllocationSortExpression": "Descending",
    "hiddenInputToUpdateATBuffer_CommonToolkitScripts": "1"
}

PAGE_SCRIPT_KEY = "ctl00$MainContent$ScriptManager1"
NEXT_BUTTON_KEY_1 = "ctl00$MainContent$ImageButtonGenelNext.x"
NEXT_BUTTON_KEY_2 = "ctl00$MainContent$ImageButtonGenelNext.y"
FIRST_PAGE_SCRIPT = "ctl00$MainContent$UpdatePanel1|ctl00$MainContent$ButtonSearchDates"
NEXT_PAGES_SCRIPT = "ctl00$MainContent$UpdatePanel1|ctl00$MainContent$ImageButtonGenelNext"

SESSION_DATA = {
    "__EVENTTARGET": "",
    "__EVENTARGUMENT": "",
    "__LASTFOCUS": "",
    "__VIEWSTATE": "",
    "__VIEWSTATEGENERATOR": "",
    "__VIEWSTATEENCRYPTED": "",
    "__EVENTVALIDATION": "",
    "__ASYNCPOST": "",
}

HTML_TABLE_IDS = ["MainContent_GridViewGenel", "MainContent_GridViewDagilim"]

FORM_DATA_START_DATE_FIELDS = [
    "ctl00$MainContent$HTarihselBasTarih",
    "ctl00$MainContent$TextBoxStartDate"
]

FORM_DATA_END_DATE_FIELDS = [
    "ctl00$MainContent$TextBoxEndDate",
    "ctl00$MainContent$HTarihselBitTarih"
]

FORM_DATA_FUND_FIELDS = [
    "ctl00$MainContent$HiddenFieldFundId",
    "ctl00$MainContent$HTarihselFonKod"
]

FORM_DATA_FUND_TYPE_KEY = "ctl00$MainContent$RadioButtonListFundMainType"

HEADERS = {
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "DNT": "1",
    "X-Requested-With": "XMLHttpRequest",
    "X-MicrosoftAjax": "Delta=true",
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    ),
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "*/*",
    "Origin": "https://www.tefas.gov.tr",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://www.tefas.gov.tr/TarihselVeriler.aspx",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6",
}
