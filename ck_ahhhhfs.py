# -*- coding: utf-8 -*-
"""
cron: 30 9 * * *
new Env('A姐分享签到');
"""

import requests

from notify_mtr import send
from utils import get_data


class AHHHHFS:
    def __init__(self, check_items):
        self.check_items = check_items
        self.s = requests.Session()
        self.s.headers.update({
            'authority': 'www.ahhhhfs.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'no-cache',
            'origin': 'https://www.ahhhhfs.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })

    def sign(self, cookie, nonce):
        url = "https://www.ahhhhfs.com/wp-admin/admin-ajax.php"
        self.s.headers.update({
            "cookie": cookie
        })
        payload = f"action=user_qiandao&nonce={nonce}"
        # {
        #     "status": "0",
        #     "msg": "今日已签到，请明日再来"
        # }
        r = self.s.post(url, data=payload).json()
        if r["status"] == "0":
            msg = "签到成功\n" + r["msg"]
        else:
            msg = "签到失败\n" + r["msg"]
        return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            try:
                sign_msg = self.sign(check_item["cookie"], check_item["nonce"])
                msg = f"签到信息: {sign_msg}"
                msg_all += msg + "\n\n"
            except Exception as e:
                msg = f"获取用户信息失败: {e}"
                print(msg)
                msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("AHHHHFS", [])
    res = AHHHHFS(check_items=_check_items).main()
    send("A姐分享", res)
