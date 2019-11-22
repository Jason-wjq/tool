# -*- coding: utf-8 -*-
'''
author: Jason
百度翻译自定义功能 需要在官网注册一个账号
'''
import requests
import time
import hashlib
import logging
import random

APP_ID = ''  # APP ID
PDK = ''  # 密钥
LANGUAGE = {'zh': '中文', 'en': '英语', 'yue': '粤语', 'wyw': '文言文', 'jp': '日语', 'kor': '韩语', 'fra': '法语', 'spa': '西班牙语',
            'th': '泰语', 'ara': '阿拉伯语', 'ru': '俄语', 'pt': '葡萄牙语', 'de': '德语', 'it': '意大利语', 'el': '希腊语', 'nl': '荷兰语',
            'pl': '波兰语', 'bul': '保加利亚语', 'est': '爱沙尼亚语', 'dan': '丹麦语', 'fin': '芬兰语', 'cs': '捷克语', 'rom': '罗马尼亚语',
            'slo': '斯洛文尼亚语', 'swe': '瑞典语', 'hu': '匈牙利语', 'cht': '繁体中文', 'vie': '越南语'}
STATUS_CODE = {
    '52000': '成功',
    '52001': '请求超时',
    '52002': '系统错误',
    '52003': '未授权用户',
    '54000': '必填参数为空',
    '54001': '签名错误',
    '54003': '访问频率受限',
    '54004': '账户余额不足',
    '54005': '长query请求频繁',
    '58000': '客户端IP非法',
    '58001': '译文语言方向不支持',
    '58002': '服务当前已关闭',
    '90107': '认证未通过或未生效'
}


def MD5(md5List: list):
    # 生成一个md5对象
    m1 = hashlib.md5()
    for value in md5List:
        if (value is not None) and (not isinstance(value, bool)):
            # 使用md5对象里的update方法md5转换
            m1.update(str(value).encode("utf-8"))
    token = m1.hexdigest()
    return token


def common_translate(query: str, origin='auto', flow="zh"):
    '''
    普通文本翻译
    :param query: 需要翻译的文本
    :param origin: 需要翻译的语言 auto：自动
    :param flow: 翻译后的语言 zh：简体中文
    :return: None：翻译失败
    '''
    params = {
        'q': query,
        'from': origin,
        'to': flow,
        'appid': APP_ID,
        'salt': random.randint(32768, 65536)
    }
    params['sign'] = MD5([APP_ID, query, params['salt'], PDK])
    try:
        res = requests.get(url='https://fanyi-api.baidu.com/api/trans/vip/translate', params=params)
        result = res.json()
    except Exception as e:
        logging.error('当前翻译请求异常: {}'.format(e))
    else:
        if result.get('error_code'):
            logging.error(STATUS_CODE[result['error_code']])
        else:
            time.sleep(1)
            return result['trans_result'][0]['dst']


if __name__ == '__main__':
    a = common_translate('apple')
    print(a)
