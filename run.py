from tefas import Crawler

if __name__ == '__main__':
    tefas = Crawler()
    data_list = tefas.fetch_single(date="22.11.2020", fund="AFT")
    #for data in data_list:
    # print(len(data_list))
    # print(data_list[len(data_list)-1])
    print(data_list[0])