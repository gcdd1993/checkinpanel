# -*- coding: utf-8 -*-
"""
cron: 30 9 * * *
new Env('扫描全能王签到');
"""

import requests
import time

from notify_mtr import send
from utils import get_data
from lxml import etree


# 13位时间戳
def get_ts():
    return str(int(time.time() * 1000))


class CAMSCANNER:
    def __init__(self, check_items):
        self.check_items = check_items
        self.s = requests.Session()
        self.s.headers.update({
            'Host': 'v3.camscanner.com',
            'Origin': 'https://mo.camscanner.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 CamScanner_IP_FREE/6.19.1.2206212008',
            'Referer': 'https://mo.camscanner.com/',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded'
        })

    def sign(self, cs_ept_d, token):
        url = "https://v3.camscanner.com/app/rewardSignIn"
        data = {
            "api_domain": "https://api-cs.intsig.net/user/cs",
            "client_app": "CamScanner_IP_FREE@6.19.1.2206212008",
            "country": "cn",
            "cs_ept_d": cs_ept_d,
            "language": "zh-cn",
            "method": "done",
            "time_zone": 8,
            "timestamp": get_ts(),
            "token": token
        }
        r = self.s.post(url, data=data).json()
        return r

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            try:
                sign_msg = self.sign(check_item["cs_ept_d"], check_item["token"])
                msg = f"签到信息: {sign_msg}"
                msg_all += msg + "\n\n"
            except Exception as e:
                msg = f"获取用户信息失败: {e}"
                print(msg)
                msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("CAMSCANNER", [])
    res = CAMSCANNER(check_items=_check_items).main()
    send("扫描全能王", res)
