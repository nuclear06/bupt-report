def get_logindata(user, pswd, mode=True,execution = None):
    if mode:
        data = {
            'username': '{}'.format(user),
            'password': '{}'.format(pswd)
        }
        return data
    else:
        data = {
            "username": "{}".format(user),
            "password": "{}".format(pswd),
            'execution': '{}'.format(execution),
            'submit': '登录',
            'type': 'username_password',
            '_eventId': 'submit'
        }
        return data


def get_log():
    with open('Running_log', 'r') as f:
        temp = f.readlines()
        print('log is {}'.format(temp))
        return temp
