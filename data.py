from parameter import find


def get_logindata(user, pswd):
    data = {
        'username': '{}'.format(user),
        'password': '{}'.format(pswd)
    }
    return data


def get_postdata(data_dict):
    null = None
    true = True
    # 修正eval(dict['geo_api_info'])中的变量

    data = {
        'sfzx': '{}'.format(data_dict['sfzx']),
        'tw': '{}'.format(data_dict['tw']),
        'area': '{}'.format(data_dict['area']),
        'city': '{}'.format(data_dict['city']),
        'province': '{}'.format(data_dict['province']),
        'address': '{}'.format(data_dict['address']),
        'sfcyglq': '{}'.format(data_dict['sfcyglq']),
        'sfyzz': '{}'.format(data_dict['sfyzz']),
        'qtqk': '',
        'askforleave': '{}'.format(data_dict['askforleave']),

        'geo_api_info': eval(data_dict['geo_api_info'])
    }
    # print(data)
    return data



def get_log():
    with open('Running_log','r') as f:
        temp = f.readlines()
        print('log is {}'.format(temp))
        return temp
