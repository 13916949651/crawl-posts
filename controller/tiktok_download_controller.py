from flask import request

from service.tiktok_crawl_service import TikTokCrawl
from controller import tiktok


@tiktok.route('/search', methods=['GET', 'POST'])
def search_media():
    if request.method == 'POST':
        count = request.form.get('count')
        user_name = request.form.get('name')
        hashtag = request.form.get('hashtag')

    else:
        count = request.args.get('count')
        user_name = request.args.get('name')
        hashtag = request.args.get('hashtag')

    if count is None:
        return 'count cannot be empty'

    tik = TikTokCrawl(n_videos=int(count), user_name=user_name, hashtag=hashtag, post_id=None, target=None, share_url=None)
    if user_name is not None:
        return str(tik.by_user_name())
    elif hashtag is not None:
        return str(tik.by_post_hashtag())
    else:
        return str(tik.by_post_trending())


@tiktok.route('/user/download', methods=['GET', 'POST'])
def download_by_user():
    if request.method == 'POST':
        count = request.form.get('count')
        user_name = request.form.get('name')
    else:
        count = request.args.get('count')
        user_name = request.args.get('name')
    if count is None or user_name is None:
        return 'count and name cannot be empty'

    target = '/Users/heavengifts/Desktop/tiktok/'

    tik = TikTokCrawl(n_videos=int(count), user_name=user_name, hashtag=None, post_id=None, target=target, share_url=None)

    result = tik.by_user_name()
    tik.get_load_media(result)
    # executor.submit(tik.get_load_media, result, name, target)

    return 'download success ~~~~~'


@tiktok.route('/download', methods=['GET', 'POST'])
def download_media():
    if request.method == 'POST':
        post_id = request.form.get('post_id')
        user_name = request.form.get('name')

    else:
        post_id = request.args.get('post_id')
        user_name = request.args.get('name')

    if post_id is None or user_name is None:
        return 'name and post_id cannot be empty'
    target = '/Users/heavengifts/Desktop/tiktok/'

    tik = TikTokCrawl(n_videos=None, user_name=user_name, hashtag=None, post_id=post_id, target=target, share_url=None)

    tik.by_post_id_download()
    # executor.submit(tik.by_post_id_download, post_id, user_name, target)
    return 'download success'
