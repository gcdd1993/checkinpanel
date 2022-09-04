# -*- coding: utf-8 -*-
"""
cron: 40 8 * * *
new Env('哈弗智家签到');
"""

import requests
import time

from notify_mtr import send
from utils import get_data
from lxml import etree


# 13位时间戳
def get_ts():
    return str(int(time.time() * 1000))


class HAVAL:
    def __init__(self, check_items):
        self.check_items = check_items
        self.s = requests.Session()
        self.s.headers.update({
            'Host': 'bt-h5-gateway.beantechyun.com',
            'Referer': 'https://haval-restructure-h5.beantechyun.com/',
            'Cache-Control': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 /sa-sdk-ios fromappios haval',
            'bt-auth-appKey': '7849495624',
            'brand': '1',
            'Pragma': 'no-cache',
            'cVer': '4.4.400',
            'Origin': 'https://haval-restructure-h5.beantechyun.com',
            # 'accessToken': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NTk0NDg2NzQsImlhdCI6MTY1ODg0Mzg3NCwiaXNzIjoiZ3d0IFNlcnZlciIsImJlYW5JZCI6IjIwNjU4NzE3NDQ1OTQ5NjA3OTkiLCJyb2xlQ29kZSI6Imd1ZXN0IiwiY2hhbm5lbCI6IkFENDY2OEYzREM1RTQxQ0I4NTk1NTMwOUFGNjc2RjJFIn0.AtH_oSc5o5xDYfqh7dSslbo5pnufcWV3v1Dw90mrXl1xAFa20tH8ZIeBSWYvdZC8MWc-FXUCXVLDt7harn6fU7venA-e6TPL-w6c8ikSGcaI5ZJM3m1qwj_X2NpvJovwqLmhb2sfZeUzHbBhDTylVywOph0mcpoeDbHVGIt5kWrRpyXDMthgWaJbNWWU1p6NsWWyA4a2Ra0uIGpGYI3t7YCQtG0lpQd-3yjuuA5Hzc3Ef2VvmlFjR1HjE_mE1_uxjcNSV7tZAQ7CFOeBe5ffUhGQrc0xAtzAFDoXqAdJE2UcshVJnaGZeZu7tyHK05yW2YQCnKf4NuOp4zcH-6CJBBwbbnE1wC0',
            'os': 'IOS',
            'rs': '2',
            'terminal': 'GW_APP_Haval',
            'If-Modified-Since': '0',
            'tokenId': '45a7ce74225b4f9ea4f09f5e6ebaa7e6',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept': 'application/json, text/plain, */*',
            'enterpriseId': 'CC01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json;charset=utf-8'
        })

    def sign_info(self, appkey, access_token, token_id):
        """
        获取签到信息

        """
        url = "https://bt-h5-gateway.beantechyun.com/app-api/api/v1.0/point/queryPickupContinueSignInfo?queryNums=1"
        self.s.headers.update({
            'bt-auth-appKey': appkey,
            "accessToken": access_token,
            "tokenId": token_id
        })
        r = self.s.get(url).json()
        if r["description"] == "SUCCESS":
            data_ = r["data"]
            return f"签到成功，本次签到获得金币 {data_['currentPoint']}，连续签到 {data_['continueSignDays']}，账户金币余额 {data_['totalPoints']}"
        else:
            pass

    def sign(self, appkey, access_token, token_id):
        url = "https://bt-h5-gateway.beantechyun.com/app-api/api/v1.0/point/sign"
        self.s.headers.update({
            'bt-auth-appKey': appkey,
            "accessToken": access_token,
            "tokenId": token_id
        })
        data_ = {"port": "HJ0002"}
        r = self.s.post(url, json=data_).json()
        if r["description"] in ["不能重复签到", "SUCCESS"]:
            return self.sign_info(appkey, access_token, token_id)
        else:
            return f"签到失败 {r}"

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            try:
                sign_msg = self.sign(check_item["appkey"], check_item["access_token"], check_item["token_id"])
                msg = f"签到信息: {sign_msg}"
                msg_all += msg + "\n\n"
            except Exception as e:
                msg = f"签到失败: {e}"
                print(msg)
                msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("HAVAL", [])
    res = HAVAL(check_items=_check_items).main()
    send("哈弗智家", res)
