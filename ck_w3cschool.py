# -*- coding: utf-8 -*-
"""
cron: 30 9 * * *
new Env('编程狮签到');
"""

import time

import requests

from notify_mtr import send
from utils import get_data


# 13位时间戳
def get_ts():
    return str(int(time.time() * 1000))


class W3CSCHOOL:
    def __init__(self, check_items):
        self.check_items = check_items
        self.s = requests.Session()
        self.s.headers.update({
            'Host': 'appapi.w3cschool.cn',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Content-Length': '168',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
        })

    def sign(self, cookie, api_key, api_auth):
        url = "https://appapi.w3cschool.cn/api/myapp/checkin"
        self.s.headers.update({
            'Cookie': cookie
        })
        body = {
            "version": 1,
            "systemType": "ios",
            "appVersion": "3.10.86",
            "apikey": api_key,
            "apiauth": api_auth
        }
        r = self.s.post(url, data=body).json()
        if r["statusCode"] == 200:
            return f"签到成功，获得经验：{r['data']['exp']}"
        else:
            return f"签到失败，{r['message']}"

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            try:
                sign_msg = self.sign(check_item["cookie"], check_item["apikey"], check_item["apiauth"])
                msg = f"签到信息: {sign_msg}"
                msg_all += msg + "\n\n"
            except Exception as e:
                msg = f"获取用户信息失败: {e}"
                print(msg)
                msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("W3CSCHOOL", [])
    res = W3CSCHOOL(check_items=_check_items).main()
    send("编程狮", res)
