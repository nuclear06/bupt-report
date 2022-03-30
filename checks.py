def message_check(message):
    if message != '操作成功':
        raise RuntimeWarning(message)


