# -*- coding: utf-8 -*-
'''
Author：Jason
Create time： 2019-06-20
Description： 下载文件工具程序
'''
import requests
import os
import sys
import time
import contextlib
from Crypto.Cipher import AES
import logging

logging.basicConfig(format='%(asctime)s-[line:%(lineno)d]-%(levelname)s: %(message)s', level=logging.INFO)


def download_file(url: str, path: str, fileName=""):
    '''
    下载图片，下载过程显示进度条
    :param url: 图片链接
    :param path: 存放图片的路径
    :param fileName: 下载的文件名
    :return: True:下载成功  False:下载失败
    '''
    try:
        os.makedirs(path, exist_ok=True)  # 创建对应的目录，存在则忽略
        if fileName:
            file_name = path.rstrip('/') + '/' + fileName
        else:
            file_name = path.rstrip('/') + '/' + url.split('/')[-1]
        print('\nDownloading ' + url)
        print('[文件路径]: ' + file_name)
        done_size = 0  # 已下载文件大小
        progress_bar_length = 30  # 进度条长度
        start = time.time()  # 开始时间
        try:
            response = requests.get(url, stream=True)
        except Exception as e:
            logging.error("请求错误: {}".format(e))
            return False
        else:
            if response.status_code == 200:
                content_length = int(response.headers['Content-Length'])  # 总大小
                print('[文件大小]: %0.2f MB' % (content_length / 1024 / 1024))
                with contextlib.closing(response) as res:
                    with open(file_name, 'wb') as f:
                        for data in res.iter_content(chunk_size=1024 * 1024 * 2):
                            f.write(data)
                            f.flush()
                            done_size += len(data)  # 已经下载的大小
                            done = int(progress_bar_length * done_size / content_length)  # 已经下载的进度条长度
                            undone = progress_bar_length - done  # 未下载的进度条长度
                            percent = float(done_size / content_length * 100)  # 下载进度
                            sys.stdout.write('\r[下载进度]: %s%s %.2f%%' % ('●' * done, '○' * undone, percent))
                            sys.stdout.flush()
                print('\n' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ': 下载完成！ 用时%.2f 秒' % (
                        time.time() - start))
                return True
            else:
                logging.error("下载失败，返回响应码: {}".format(response.status_code))
                return False
    except Exception as e:
        logging.error(e)
        return False


def download_m3u8(url: str, path: str, fileName=""):
    '''
    下载m3u8视频流
    :param url: m3u8 URL
    :param path: 存放目录
    :param fileName: 下载的文件名
    :return: True:下载成功  False:下载失败
    '''
    try:
        print('\nDownloading .m3u8 ' + url)
        key = b""
        baseUrl = '/'.join(url.split('/')[:-1]) + '/'  # ts请求的前面部分
        m3u8_text = requests.get(url).text  # 获取m3u8
        file_line = m3u8_text.split("\n")
        if fileName:
            video_file = path.rstrip('/') + '/' + fileName + '.mp4'  # 把ts文件合成一个MP4
        else:
            video_file = path.rstrip('/') + '/' + url.split('/')[-1] + '.mp4'  # 把ts文件合成一个MP4
        m3u8_file = path.rstrip('/') + '/' + url.split('/')[-1]  # m3u8的文件目录
        ts_path = path.rstrip('/') + '/ts/'  # ts文件目录
        os.makedirs(ts_path, exist_ok=True)  # 创建对应的目录，存在则忽略
        with open(m3u8_file, 'w') as f:  # 把m3u8文件保存下来
            f.write(m3u8_text)
        logging.info("{} write success!".format(m3u8_file))
        for index, line in enumerate(file_line):
            if "EXT-X-KEY" in line:  # 找解密Key
                logging.info('the m3u8 have key')
                key_url = baseUrl + line[line.find("URI"):line.rfind('"')].split('"')[1]  # 拼出key解密密钥URL
                key = requests.get(key_url).content
                logging.info("the m3u8 key get success")
            if "EXTINF" in line:  # 找ts地址并下载
                ts_url = baseUrl + file_line[index + 1]  # 拼出ts片段的URL
                ts_file = ts_path + str(index + 2) + '.ts'
                while True:
                    ts_content = b''
                    try:
                        with contextlib.closing(requests.get(ts_url, stream=True)) as res:
                            for data in res.iter_content(chunk_size=1034 * 1024 * 2):
                                ts_content += data
                    except Exception as e:
                        logging.info(ts_url + "  重新请求")
                        continue
                    else:
                        break
                if len(key):  # AES 解密
                    cryptos = AES.new(key, AES.MODE_CBC, key)
                    ts_content = cryptos.decrypt(ts_content)
                with open(ts_file, 'ab') as f:  # 写入ts文件
                    f.write(ts_content)
                    f.flush()
                with open(video_file, 'ab') as f:  # 把合成的ts二进制写入文件
                    f.write(ts_content)
                    f.flush()
                logging.info("{} write success!".format(ts_file))
    except Exception as e:
        logging.error(e)
        return False
    else:
        return True


def download_thunder(url: str, path='D:\迅雷下载'):
    thunder_path = 'D:\Program Files\Thunder Network\Thunder\Program\ThunderStart.exe'  # 迅雷的安装目录
    xltd_file = os.path.join(path, url.split('/')[-1] + '.xltd')
    os.system('"{}" {}'.format(thunder_path, url))
    if 'http' in url[:5]:
        while not os.path.exists(xltd_file):
            continue
    else:
        time.sleep(5)
    logging.info("正在下载: {} ···".format(url))


if __name__ == '__main__':
    ...
