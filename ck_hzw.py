# -*- coding: utf-8 -*-
"""
cron: 30 10 * * *
new Env('亲宝宝签到');
"""

import requests

from notify_mtr import send
from utils import get_data


class HZW:
    def __init__(self, check_items):
        self.check_items = check_items
        self.s = requests.Session()
        self.s.headers.update({
            'User-Agent': 'HZWMALL/173/Android/14/Xiaomi/2201122C/Mozilla/5.0 (Linux; Android 14; 2201122C Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/123.0.6312.118 Mobile Safari/537.36',
            'sec-ch-ua-platform': 'Android',
            'Origin': 'https://w.cekid.com',
            'X-Requested-With': 'com.kidswant.ss',
            'Referer': 'https://w.cekid.com/',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        })

    def sign(self, uid):
        """
        签到
        :return:
        """
        url = f"https://marketingtools.cekid.com/sign-in/web/c/v1/sign/do?uid={uid}&rule_id=2"
        r = self.s.get(url).json()
        print(r)
        return r["msg"]

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            try:
                uid = check_item["uid"]
                cookie = check_item["cookie"]
                self.s.headers.update({
                    'Cookie': cookie
                })
                sign_msg = self.sign(uid)
                msg = f"uid: {uid}\n签到信息: {sign_msg}"
                msg_all += msg + "\n\n"
            except Exception as e:
                msg = f"签到失败: {e}"
                print(msg)
                msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("HZW", [])
    res = HZW(check_items=_check_items).main()
    send("孩子王", res)
