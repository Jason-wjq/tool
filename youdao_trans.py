# -*- coding: utf-8 -*-
'''
author: Jason
有道翻译自定义功能
来自网页版有道翻译
'''

import requests
import time
import logging
import hashlib


# 加密算法
# "fanyideskweb" + i + salt + "n%A-rKaT5fb[Gy?;N5@Tj"


def MD5(md5List: list):
    # 生成一个md5对象
    m1 = hashlib.md5()
    for value in md5List:
        if (value is not None) and (not isinstance(value, bool)):
            # 使用md5对象里的update方法md5转换
            m1.update(str(value).encode("utf-8"))
    token = m1.hexdigest()
    return token


def common_translate(query: str, origin='auto', flow="zh-CHS"):
    '''
    普通文本翻译
    :param query: 需要翻译的文本
    :param origin: 需要翻译的语言 auto：自动
    :param flow: 翻译后的语言 zh-CHS：简体中文
    :return: None：翻译失败
    '''
    salt = str(int(time.time() * 10000))
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    data = {
        'i': query,
        'from': origin,
        'to': flow,
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': salt,
        'sign': MD5(['fanyideskweb' + query + str(salt) + "n%A-rKaT5fb[Gy?;N5@Tj"]),
        'ts': salt[:-1],
        'bv': '6ba427a653365049d202e4d218cbb811',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME'
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'OUTFOX_SEARCH_USER_ID=1944855340@221.219.225.40; OUTFOX_SEARCH_USER_ID_NCOO=1997242050.3906953; _ga=GA1.2.1551638093.1565616359; P_INFO=m18232003371_1@163.com|1566282170|0|other|00&99|null&null&null#bej&null#10#0#0|182371&1||18232003371@163.com; _ntes_nnid=377e77d2405afe0816cdd59ade547e7a,1567385119737; JSESSIONID=aaax0pdnMSVmHbJbYRB1w; ___rl__test__cookies=1569207897066',
        'Host': 'fanyi.youdao.com',
        'Origin': 'http://fanyi.youdao.com',
        'Referer': 'http://fanyi.youdao.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    try:
        res = requests.post(url=url, data=data, headers=headers)
        result = res.json()
        time.sleep(1)
    except Exception as e:
        logging.error('当前翻译请求异常:{}'.format(e))
    else:
        if result['errorCode'] == 0:
            return result['translateResult'][0][0]['tgt']
        else:
            logging.error('返回错误:{}'.format(result))


if __name__ == "__main__":
    a = common_translate('apple')
    print(a)
