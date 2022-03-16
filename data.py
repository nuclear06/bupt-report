from parameter import find


def get_logindata(user, pswd):
    data = {
        'username': '{}'.format(user),
        'password': '{}'.format(pswd)
    }
    return data


def get_postdata(text):
    dict = screen(text)

    null = None
    true = True
    # 修正eval(dict['geo_api_info'])中的变量

    data = {
        'sfzx': '{}'.format(dict['sfzx']),
        'tw': '{}'.format(dict['tw']),
        'area': '{}'.format(dict['area']),
        'city': '{}'.format(dict['city']),
        'province': '{}'.format(dict['province']),
        'address': '{}'.format(dict['address']),
        'sfcyglq': '{}'.format(dict['sfcyglq']),
        'sfyzz': '{}'.format(dict['sfyzz']),
        'qtqk': '',
        'askforleave': '{}'.format(dict['askforleave']),

        'geo_api_info': eval(dict['geo_api_info'])
    }
    # print(data)
    return data


def screen(screen_text):
    data_dict = {}
    re_iter = find.finditer(screen_text)
    for j in re_iter:
        key = j.group('key')
        value = j.group('value')
        dict[key] = value
    return data_dict


def get_log():
    with open('./Running_log') as f:
        return f.read()
