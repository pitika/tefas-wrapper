from wrapper import Tefas
from wrapper.fund_type import FundType

if __name__ == '__main__':
    tefas = Tefas(FundType.YAT)
    data_list = tefas.fetch("AFT")
    
    for data in data_list:
        print(data)
    # print(len(data_list))
    # print(data_list[len(data_list)-1])
    # print(data_list[0])clear