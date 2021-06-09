from TikTokApi import TikTokApi


class TikTokCrawl:
    def __init__(self, n_videos, user_name, hashtag, post_id, target, share_url):
        self.api = TikTokApi()
        self.n_videos = n_videos
        self.user_name = user_name
        self.hashtag = hashtag
        self.post_id = post_id
        self.target = target
        self.share_url = share_url

    # 收集用户发布的视频
    def by_user_name(self):
        return self.api.byUsername(self.user_name, count=self.n_videos)

    # 收集用户喜欢的视频
    def by_user_like(self):
        return self.api.userLikedbyUsername(self.user_name, count=self.n_videos)

    # 收集由包括hashtag视频
    def by_post_hashtag(self):
        return self.api.byHashtag(self.hashtag, count=self.n_videos)

    # 收集热门视频
    def by_post_trending(self):
        return self.api.trending(count=self.n_videos)

    # 通过帐户收集用户列表
    def by_post_suggested(self):
        user_id = self.api.getUser(self.user_name)['userInfo']['user']['id']
        return self.api.getSuggestedUsersbyID(count=self.n_videos, user_id=user_id)

    # 通过url获取当前页面的所有json数据
    def get_tiktok_by_html(self, path):
        return self.api.get_tiktok_by_html(url=path)

    # 通过url获取当前页面的所有html
    def by_download_url(self, download_url):
        return self.api.get_video_by_download_url(download_url=download_url)

    # 根据分享的URL/转译的URL生成可下载文件
    def video_by_url(self, video_url):
        return self.api.get_video_by_url(video_url=video_url)

    # 根据【用户和post_id】下载
    def by_post_id_download(self):
        # result = self.by_post_trending()
        url = 'https://www.tiktok.com/@' + self.user_name + '/video/' + self.post_id
        try:
            download_url = self.video_by_url(url)
        except Exception as e:
            return 'Download resource does not exist'
        target_source = self.target + self.post_id + ".mp4"
        try:
            self.do_download_media(download_url, target_source)
            return target_source
        except Exception:
            return 'download failed'

    # 根据【用户/hashtag等查询需要下载的资源】，并下载
    def get_load_media(self, result):
        # result = self.by_post_trending()
        for i in range(len(result)):
            video = result[i]
            post_id = video['id']
            url = 'https://www.tiktok.com/@' + self.user_name + '/video/' + post_id
            download_url = self.video_by_url(url)
            try:
                self.do_download_media(download_url, self.target + post_id + ".mp4")
            except Exception:
                print('download failed')

    # 根据分享的URL下载
    def get_share_media(self):
        result = self.get_tiktok_by_html(self.share_url)
        post_id = result['key']
        download_url = self.video_by_url(self.share_url)
        self.do_download_media(download_url, self.target + post_id + ".mp4")

    # 下载二进制文件内容
    def do_download_media(self, download_source, target):
        try:
            with open(target, 'ab') as file:
                file.write(download_source)
                file.flush()
        except Exception as e:
            print(e)

#
# if __name__ == '__main__':
#     share_url = 'https://www.tiktok.com/@c.0214/video/6953188339545640194?sender_device=mobile&sender_web_id' \
#                 '=6969480573648569858&is_from_webapp=v1&is_copy_url=0 '
#     tiktok = TikTokCrawl(n_videos=1, username='riwww')
#     result = tiktok.by_post_trending()
#     target = '/Users/heavengifts/Desktop/tiktok/'
#     tiktok.get_load_media(result, target)
#     tiktok.get_share_media(share_url, target)
# print(tiktok.get_tiktok_by_html(share_url))
