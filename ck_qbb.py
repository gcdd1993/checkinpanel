# -*- coding: utf-8 -*-
"""
cron: 30 10 * * *
new Env('亲宝宝签到');
"""

import requests

from notify_mtr import send
from utils import get_data


class QBB:
    def __init__(self, check_items):
        self.check_items = check_items
        self.s = requests.Session()
        self.s.headers.update({
            'Host': 'webapi.qbb6.com',
            'Origin': 'https://stlib.qbb6.com',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Referer': 'https://stlib.qbb6.com/',
            'Accept-Encoding': 'gzip, deflate, br'
        })

    def sign(self, track_info, qbean_code, account_id):
        """
        获取登录用户信息

        """
        url = f"https://webapi.qbb6.com/h5/api/qbean/internal/user/sign/post?trackinfo={track_info}&qbeanCode={qbean_code}&accountId={account_id}"
        res = self.s.post(url).json()
        if res.get("rc") == 0:
            bean = res["userQBean"]
            serials = res["signSerials"][0]
            msg = f"签到成功，本次签到获得金币 {serials['score']}，连续签到 {serials['count']} 天\n账户金币余额 {bean['score']}"
        else:
            msg = "签到失败"
            print(res)
        return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            try:
                track_info = check_item["track_info"]
                qbean_code = check_item["qbean_code"]
                account_id = check_item["account_id"]
                sign_msg = self.sign(track_info, qbean_code, account_id)
                msg = f"帐号信息: {account_id}\n签到信息: {sign_msg}"
                msg_all += msg + "\n\n"
            except Exception as e:
                msg = f"获取用户信息失败: {e}"
                print(msg)
                msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("QBB", [])
    res = QBB(check_items=_check_items).main()
    send("QBB", res)
