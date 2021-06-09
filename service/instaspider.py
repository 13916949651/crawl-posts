import requests
import re
import time
import random
import os


class InstaSpider(object):

    def __init__(self, user_name, path_name=None):
        # 初始化要传入ins用户名和保存的文件夹名
        self.path_name = path_name if path_name else user_name
        # 不能多余链接
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接

        # self.url = 'https://www.instagram.com/real__yami/'
        self.url = 'https://www.instagram.com/{}/?__a=1'.format(user_name)
        self.headers = {
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/90.0.4430.212 Safari/537.36",
            'cookie': 'mid=YLSLtQAEAAHgPW_faw2aohVfu0BE; ig_did=6CCD78B6-3BD8-4295-A201-F725AB558E2E; ig_nrcb=1; '
                      'csrftoken=CeGwQ9Nnwx3khhN8G8AEkpmfE1RqHt8I; rur=NAO; ds_user_id=33471139089; '
                      'sessionid=33471139089%3ApqOKxVJTasNXzV%3A8 '
        }
        # 保存所有的图片和视频地址
        self.img_url_list = []
        self.uri = 'https://www.instagram.com/graphql/query/?query_hash=f2405b236d85e8296cf30347c9f08c2a&variables' \
                   '=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A12%2C%22after%22%3A%22{cursor}%22%7D '

    def parse_html(self):
        try:
            next_html_str = requests.get(url=self.url, headers=self.headers).text
            # 获取12条图片地址
            next_url_list = re.findall('''display_url":(.*?),''', next_html_str)
            video_list = re.findall('"video_url":(.*?),', next_html_str)
            if len(video_list) > 0:
                next_url_list.extend(video_list)
            self.img_url_list.extend(next_url_list)
            time.sleep(random.random())
        except Exception as e:
            print(e)
        print(len(self.img_url_list))
        self.img_url_list = list(set(self.img_url_list))
        print('去重后', len(self.img_url_list))
        self.download_img()

    def download_img(self):
        # 开始下载图片，生成文件夹再下载
        dirpath = '/Users/heavengifts/Desktop/insimg/{}'.format(self.path_name)
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        for i in range(len(self.img_url_list)):
            print('\n正在下载第{0}张：'.format(i), '还剩{0}张'.format(len(self.img_url_list) - i - 1))
            try:
                response = requests.get(self.img_url_list[i].replace('"', ''), headers=self.headers, timeout=10)
                if response.status_code == 200:
                    content = response.content
                    # 判断后缀
                    endw = 'mp4' if r'mp4?_nc_ht=scontent.cdninstagram.com' in self.img_url_list[i] else 'jpg'
                    file_path = r'/Users/heavengifts/Desktop/insimg/{path}/{name}.{jpg}'.format(path=self.path_name,
                                                                                                name='%04d' % random.randint(
                                                                                                    0, 9999), jpg=endw)
                    with open(file_path, 'wb') as f:
                        print('第{0}张下载完成： '.format(i))
                        f.write(content)
                        f.close()
                else:
                    print('请求照片二进制流错误, 错误状态码：', response.status_code)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    # 输入用户名和保存的文件夹名，如果没有文件夹名就和用户名同名
    ins_spider = InstaSpider(user_name='katyperry')
    ins_spider.parse_html()
