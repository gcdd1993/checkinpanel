# -*- coding: utf-8 -*-
"""
cron: 30 10 * * *
new Env('阿里云盘签到');
"""

import requests

from notify_mtr import send
from utils import get_data


class ALIYUNPAN:
    def __init__(self, check_items):
        self.check_items = check_items
        self.s = requests.Session()
        self.s.headers.update({
            'Content-Type': 'application/json'
        })

    def refresh_token(self, refresh_token):
        """
        使用 refresh_token 更新 access_token

        """
        body = {
            "grant_type": 'refresh_token',
            "refresh_token": refresh_token
        }
        r = self.s.post("https://auth.aliyundrive.com/v2/account/token", json=body).json()
        # print(r)
        return r["access_token"], r["user_name"]

    def checkin(self, refresh_token):
        """
        签到

        """
        (access_token, user_name) = self.refresh_token(refresh_token)
        # print(f"access_token : {access_token}")
        body = {
            "grant_type": 'refresh_token',
            "refresh_token": refresh_token
        }
        self.s.headers.update({
            "Authorization": 'Bearer ' + access_token
        })
        r = self.s.post("https://member.aliyundrive.com/v1/activity/sign_in_list", json=body).json()
        if r["success"]:
            result = r["result"]
            sign_in_count = result["signInCount"]
            msg = f"{user_name} 签到成功 本月累计签到 {sign_in_count} 天"
        else:
            msg = f"签到失败 {r['message']}"
        return msg

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            try:
                sign_msg = self.checkin(check_item["refresh_token"])
                msg = f"签到信息: {sign_msg}"
                msg_all += msg + "\n\n"
            except Exception as e:
                msg = f"获取用户信息失败: {e}"
                print(msg)
                msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    res = ALIYUNPAN(check_items=data.get("ALIYUNPAN", [])).main()
    send("阿里云盘", res)
