from parameter import backup_login_url


class Head:
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
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


