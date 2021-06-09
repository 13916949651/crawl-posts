import requests
import re
import random
import os


class InstagramGrab(object):

    def __init__(self, user_name, path_name=None):
        # 初始化要传入ins用户名和保存的文件夹名
        self.path_name = path_name if path_name else user_name
        # 不能多余链接
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接

        self.url = 'https://www.instagram.com/{}/?__a=1'.format(user_name)
        self.headers = {
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/90.0.4430.212 Safari/537.36",
            'cookie': 'mid=YLSLtQAEAAHgPW_faw2aohVfu0BE; ig_did=6CCD78B6-3BD8-4295-A201-F725AB558E2E; ig_nrcb=1; '
                      'csrftoken=CeGwQ9Nnwx3khhN8G8AEkpmfE1RqHt8I; rur=NAO; ds_user_id=33471139089; '
                      'sessionid=33471139089%3ApqOKxVJTasNXzV%3A8 '
        }
        # 保存所有的图片和视频地址
        self.video_url_list = []

    def parse_html(self):
        try:
            html_str = requests.get(url=self.url, headers=self.headers).text
            self.video_url_list = re.findall('"video_url":"(.*?)",', html_str)
        except Exception as e:
            print(e)
        self.download_img()

    def download_img(self):
        dirpath = '/Users/heavengifts/Desktop/insimg/{}'.format(self.path_name)
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        print('len : ', len(self.video_url_list))
        for i in range(len(self.video_url_list)):
            print('\n正在下载第{0}个：'.format(i), '还剩{0}个'.format(len(self.video_url_list) - i - 1))
            try:
                response = requests.get(self.video_url_list[i], headers=self.headers, timeout=10)
                if response.status_code == 200:
                    content = response.content
                    # 判断后缀
                    file_path = r'/Users/heavengifts/Desktop/insimg/{path}/{name}.{mp4}'.format(path=self.path_name,
                                                                                                name='%04d' % random.randint(
                                                                                                    0, 9999), mp4='mp4')
                    with open(file_path, 'wb') as f:
                        print('第{0}个下载完成： '.format(i))
                        f.write(content)
                        f.close()
                else:
                    print('请求二进制流错误, 错误状态码：', response.status_code)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    # 输入用户名和保存的文件夹名，如果没有文件夹名就和用户名同名
    ins_spider = InstagramGrab(user_name='katyperry')
    ins_spider.parse_html()
