from wrapper import Tefas

if __name__ == '__main__':
    tefas = Tefas()
    data_list = tefas.fetch("AFT", "25.11.2020", "25.11.2020")
    
    for data in data_list:
        print(data)
    # print(len(data_list))
    # print(data_list[len(data_list)-1])
    # print(data_list[0])clear