import os
from random import random
import cv2
import requests
from matplotlib import pyplot as plt


def download_video(url, path_name):
    headers = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36"
    }
    dispatch = '/Users/heavengifts/Desktop/tiktok/{}'.format(path_name)
    if not os.path.exists(dispatch):
        os.mkdir(dispatch)
        try:
            response = requests.get(url=url, headers=headers, timeout=10, verify=False)
            if response.status_code == 200:
                content = response.content
                # 判断后缀
                file_path = r'/Users/heavengifts/Desktop/tiktok/{path}/{name}.{mp4}'.format(path=path_name,
                                                                                            name='%04d' % random.randint(
                                                                                                0, 9999), mp4='mp4')
                with open(file_path, 'wb') as f:
                    f.write(content)
                    f.close()
            else:
                print('请求二进制流错误, 错误状态码：', response.status_code)
        except Exception as e:
            print(e)


def downloader(video_url, video_title):
    headers = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/90.0.4430.212 Safari/537.36"
    }
    path = '/Users/heavengifts/Desktop/tiktok/'
    if not os.path.exists(path):
        os.mkdir(path)
    file_name = os.path.join(path, video_title + ".mp4")
    response = requests.get(video_url, headers=headers, verify=False)
    with open(file_name, 'ab') as f:
        f.write(response.content)
        # 在文件关闭前，将缓存区的内容刷新到硬盘
        f.flush()
        print(file_name, '下载完毕')


# 安装pip3 install ffmpy
def delogo(video_title):
    # with open('1.mp4', 'wb') as fw:
    #     fw.write(requests.get(url).content)  # 为了把视频下载到本地
    video_path = '/Users/heavengifts/Desktop/tiktok/' + video_title + ".mp4"
    cap = cv2.VideoCapture(video_path)  # opencv读取视频对象

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取视频宽
    # 获取视频高度
    # frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(frame_width)
    delogo_x = frame_width - 310  # 京东水印宽大改300不过为了让他长度不超过边界这边故意多剪了10

    cmd = f'ffmpeg -i {video_path} -filter_complex "delogo=x={delogo_x}:y=1:w=300:h=70:show=0" 2.mp4'

    # -i 视频路径
    # delogo去除视频某处的logo。其实实现原理就是将给出区域进行高斯模糊处理。始x于y,wh为覆盖水印的长宽,band是模糊强度
    # show=1 便于调试他会出现一个绿色的框,去除水印的时候要把show改为0
    # 补充点:-vf:video_filter 滤镜 ；-filger_complex混合滤镜

    os.system(cmd)


def dovideo(video_title, newvideo):
    source = '/Users/heavengifts/Desktop/tiktok/' + video_title + ".mp4"
    tpl = '/Users/heavengifts/Desktop/tiktok/' + newvideo + ".mp4"

    img = cv2.imread(source, 0)
    img2 = img.copy()
    template = cv2.imread(tpl, 0)
    # 非1080*1920需要等比例缩放
    w, h = template.shape[::-1]

    ow, oh = img.shape[::-1]

    # # All the 6 methods for comparison in a list
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
               'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    #
    # methods = ['cv2.TM_CCOEFF_NORMED']
    for meth in methods:
        img = img2.copy()
        method = eval(meth)

        # Apply template Matching
        res = cv2.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(img, top_left, bottom_right, 255, 1)
        print('x={},y={},w={},h={}'.format(top_left[0], top_left[1], bottom_right[0] - top_left[0],
                                           bottom_right[1] - top_left[1]))

        plt.subplot(121), plt.imshow(res, cmap='gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(img, cmap='gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)

        plt.show()


def do_load_media(url, path):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/90.0.4430.212 Safari/537.36'}
        pre_content_length = 0
        # 循环接收视频数据
        while True:
            # 若文件已经存在，则断点续传，设置接收来需接收数据的位置
            if os.path.exists(path):
                headers['Range'] = 'bytes=%d-' % os.path.getsize(path)
            res = requests.get(url, stream=True, headers=headers)
            #res = requests.head(url, stream=True, headers=headers)
            #print(res.text)

            content_length = int(res.headers['content-length'])
            # 若当前报文长度小于前次报文长度，或者已接收文件等于当前报文长度，则可以认为视频接收完成
            if content_length < pre_content_length or (
                    os.path.exists(path) and os.path.getsize(path) == content_length) or content_length == 0:
                break
            pre_content_length = content_length

            # 写入收到的视频数据
            with open(path, 'ab') as file:
                file.write(res.content)
                file.flush()
                print('下载成功,file size : %d   total size:%d' % (os.path.getsize(path), content_length))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    url = 'https://www.tiktok.com/@c.0214/video/6953188339545640194?sender_device=mobile&sender_web_id=6969480573648569858&is_from_webapp=v1&is_copy_url=0'
    source = '/Users/heavengifts/Desktop/tiktok/999999' + ".mp4"
    #url = 'https://v16m.tiktokcdn.com/421a38ab4679b4b9c1ba33dbc8a7ddcc/60b9e5cb/video/tos/alisg/tos-alisg-pve-0037c001/de4c48eb88624b7393dbee12b079570d/?a=1233&br=3758&bt=1879&cd=0%7C0%7C1&ch=0&cr=0&cs=0&cv=1&dr=0&ds=3&er=&l=202106040235050101151531510F01C0F0&lr=tiktok_m&mime_type=video_mp4&net=0&pl=0&qs=0&rc=MzVrN2pyZTRnNTMzODczM0ApaDM1NWdkNWQ2N2dnOjRpaGcwc3IuMmUyaWpgLS1kMTRzc2JfMmMxLTMxMV80LjVeLy46Yw%3D%3D&vl=&vr='
    # url = 'https://v16-web.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/67883176cb5243c3bf970401407c175a/?a=1988&br=1752&bt=876&cd=0%7C0%7C1&ch=0&cr=0&cs=0&cv=1&dr=3&ds=3&er=&expire=1622727986&l=202106030746200101910630742800F160&lr=tiktok&mime_type=video_mp4&net=0&pl=0&policy=2&qs=0&rc=anR3PG9oPG1reTMzNTgzM0ApNTw1ZjdkOmVmNzY4PGczZ2dray4zaW1lYF9fLS1fLzRzc15eYzI0YDBeLjZhMTQyNDM6Yw%3D%3D&signature=e2f7ccd071db13f8ad57069de00dbef2&tk=tt_webid_v2&vl=&vr='
    # url = 'https://v77.tiktokcdn.com/51bd26f5e8c80f7c6dc59c5334fcd64d/60b89d8e/video/tos/useast2a/tos-useast2a-ve-0068c001/b62c2934c60b4b7980ea2903ed38e086/?a=1233&br=3144&bt=1572&cd=0%7C0%7C1&ch=0&cr=0&cs=0&cv=1&dr=0&ds=3&er=&l=202106030314400101910650242E09A0F3&lr=tiktok_m&mime_type=video_mp4&net=0&pl=0&qs=0&rc=M2V4b3E7dXB4NDMzNzczM0ApZDU3ZWc1O2RlNzc3O2k8ZmdiYjVsM2xmX21gLS1kMTZzczYuLl9jMjAyNS5hX14tNmM6Yw%3D%3D&vl=&vr='
    do_load_media(url, source)
