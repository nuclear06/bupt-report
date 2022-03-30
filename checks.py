def message_check(message):
    if not (message == '操作成功' or message ==r"call_user_func() expects parameter 1 to be a valid callback, function '/a_bupt/api/sso/cas' not found or invalid function name"):
        raise RuntimeWarning(message)

