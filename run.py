from wrapper import Tefas
from wrapper.fund_type import FundType

if __name__ == '__main__':
    tefas = Tefas(FundType.YAT)
    data_list = tefas.fetch("AFT")
    
    for data in data_list:
        detail = tefas.fetch_detail(data.code)
        print(data)
        print("-----------------------------")
        print(detail)
        print("-----------------------------")
        print("-----------------------------")
        print("-----------------------------")