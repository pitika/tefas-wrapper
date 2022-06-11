from tefaswrapper import Wrapper, FundType

if __name__ == '__main__':
    tefas = Wrapper()
    data_list = tefas.fetch("NNF",start_date="01.06.2022")

    print(data_list)


    # for data in data_list:
    #     detail = tefas.fetch_detail(data.code)
    #     print(data)
    #     print("-----------------------------")
    #     print(detail)
    #     print("-----------------------------")
    #     print("-----------------------------")
    #     print("-----------------------------")
    # detail = tefas.fetch_detail(data_list[0].code)

    # kap = tefas.fetch_kap(detail.kap_url)
    # print(detail)
