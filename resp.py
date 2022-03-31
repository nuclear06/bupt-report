from parameter import backup_login_url


class Head:
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    }
    backup_head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
        'cookie': '_7da9a=d9660f87cdb3a76c'
    }

    @staticmethod
    def get_head(_dict):
        my_head = Head.head
        my_cookie = ''
        for i in _dict:
            my_cookie += '{0}={1}'.format(i, _dict[i])
        my_head['cookie'] = my_cookie
        return my_head


class Resp:
    resp_dict = dict()

    def add_resp(self, name, response):
        self.resp_dict[name] = response


# def backup_gethead(session):
#     resp1 = session.get(backup_login_url, headers=Head.head)
#     resp1 = session.post(backup_login_url, headers=Head.backup_head, data=login_data)
#     # print(resp1.text)
