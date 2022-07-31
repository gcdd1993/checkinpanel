# -*- coding: utf-8 -*-
"""
cron: 30 9 * * *
new Env('灵锡签到');
"""

import requests

from notify_mtr import send
from utils import get_data


class LX:
    def __init__(self, check_items):
        self.check_items = check_items
        self.s = requests.Session()
        self.s.headers.update({
            'Host': 'api.internetofcity.cn',
            'guid': 'X226720955237376W',
            'province': '%E6%B1%9F%E8%8B%8F%E7%9C%81',
            'district': '%E6%83%A0%E5%B1%B1%E5%8C%BA',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/19G71 NebulaSDK/1.8.100112 Nebula  channel=lxapp WK PSDType(1) mPaaSClient/7',
            'real-version': '4.1.0',
            'Referer': 'https://cdn-prod.internetofcity.cn/',
            'Location': '120.280780,31.645720',
            'street': '%E6%B0%B4%E6%BE%84%E8%B7%AF',
            'channel': 'app',
            'phoneFactory': 'apple',
            'latitude': '31.645720',
            'Origin': 'https://cdn-prod.internetofcity.cn',
            'city': '%E6%97%A0%E9%94%A1%E5%B8%82',
            'resolution': '750x1334',
            'version': '4.1.0',
            'platformVersion': '15.6',
            'platform-type': 'ios',
            'Content-Length': '2',
            'number': '568-24%E5%8F%B7',
            'Connection': 'keep-alive',
            'longitude': '120.280780',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'ios-allow-track': 'denied',
            'os-type': '2',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json; charset=utf-8'
        })

    def sign(self, cookie, deviceid, bearer_token):
        url = "https://api.internetofcity.cn/api/resource/integral/sign"
        self.s.headers.update({
            "Cookie": cookie,
            "deviceid": deviceid,
            "Authorization": f"Bearer {bearer_token}"
        })
        r = self.s.post(url, json={}).json()
        return r

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            try:
                sign_msg = self.sign(check_item["cookie"], check_item["deviceid"], check_item["bearer_token"])
                msg = f"签到信息: {sign_msg}"
                msg_all += msg + "\n\n"
            except Exception as e:
                msg = f"获取用户信息失败: {e}"
                msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("LX", [])
    res = LX(check_items=_check_items).main()
    send("灵锡", res)
