# -*- coding: utf-8 -*-
'''
使用requests方式下载文件
'''
import requests
import os
from tqdm import tqdm
import logging
from fake_useragent import UserAgent

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO)
ua = UserAgent()


def getLocalFileSize(file):
    '''返回本地文件大小'''
    if os.path.isfile(file):
        return os.path.getsize(file)
    return 0


def req_file(url, offset=None):
    '''请求'''
    headers = {'User-Agent': ua.random}
    if offset:
        headers['Range'] = 'bytes=%d-' % offset
    try:
        response = requests.get(url=url, stream=True, headers=headers, timeout=30)
        status_code = response.status_code
        if status_code in [200, 206]:
            return response
        elif status_code == 404:
            print("%s 链接有误,status_code:%s" % (url, status_code))
            return 404
        elif status_code == 416:
            print("%s 文件数据请求区间错误,status_code:%s" % (url, status_code))
        else:
            print("%s 链接有误,status_code:%s" % (url, status_code))
    except Exception as e:
        print("无法链接:{},e:{}".format(url, e))


def download(url, local_path=r'D:\迅雷下载', file=None):
    '''
    下载
    :param url: 链接
    :param local_path: 本地地址
    :param file: 需要更改的文件名
    :return: 404：文件不存在  True
    '''
    max_file_size = -1
    if file is None:
        file = os.path.join(local_path, url.split('/')[-1])
    else:
        file = os.path.join(local_path, file)
    while True:
        local_file_size = int(getLocalFileSize(file))
        if local_file_size != 0 and max_file_size == local_file_size and max_file_size >= 0:
            print("---文件已在本地: [path：{}] [size: {:.2f}MB]\n".format(file, local_file_size / 1024 / 1024))
            return True
        if max_file_size < 0:
            response = req_file(url=url)
        else:
            response = req_file(url=url, offset=local_file_size)
        if response:
            if response == 404:
                return 404
            if max_file_size < 0:
                max_file_size = int(response.headers['Content-Length'])
                if max_file_size == local_file_size:
                    print("---文件已在本地: [path：{}] [size: {:.2f}MB]\n".format(file, local_file_size / 1024 / 1024))
                    return True
            pbar = tqdm(total=max_file_size, initial=local_file_size, desc=file, unit='B', unit_scale=True)
            try:
                with open(file, 'ab') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            pbar.update(1024)
            except Exception as e:
                print("{} 文件写入失败:{}".format(file, e))
            else:
                pbar.close()
                return True


if __name__ == '__main__':
    ...