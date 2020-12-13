# tefas-wrapper
Fetch funds data from https://www.tefas.gov.tr

    pip install tefas-wrapper


usage:

    from tefaswrapper import Wrapper, FundType
    
    # ...
    
    tefas = Wrapper(FundType.YAT)
    # single day
    result = tefas.fetch("AFT", "25.11.2020", "25.11.2020")
    
    # between two dates
    result = tefas.fetch("AFT", "15.11.2020", "20.11.2020")
    
    # from a cetain day until today
    result = tefas.fetch("AFT", "15.11.2020")                
    
    # latest value
    result = tefas.fetch("AFT")
    
    # latest values of all funds
    result = tefas.fetch()
    
    # fetch detail a specific fund
    detail = tefas.fetch_detail("AFT")

    # ...
    
