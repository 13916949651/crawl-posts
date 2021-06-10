from controller import facebook


@facebook.route('/', methods=['GET', 'POST'])
def search_media():
    return '请求根目录成功！'
