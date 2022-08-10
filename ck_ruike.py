# -*- coding: utf-8 -*-
"""
cron: 30 9 * * *
new Env('瑞客论坛签到');
"""

import requests

from notify_mtr import send
from utils import get_data
from lxml import etree


class RUIKE:
    def __init__(self, check_items):
        self.check_items = check_items
        self.s = requests.Session()
        self.s.headers.update({
            'authority': 'www.ruike1.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'dnt': '1',
            'referer': 'https://www.ruike1.com/',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47',
            'x-requested-with': 'XMLHttpRequest'
        })

    def sign(self, cookie):
        url = "https://www.ruike1.com/k_misign-sign.html?operation=qiandao&format=global_usernav_extra&formhash=06510fae&inajax=1&ajaxtarget=k_misign_topb"
        self.s.headers.update({
            "cookie": cookie
        })
        r = self.s.get(url)
        r.encoding = "gbk"
        res = r.text
        if "今日已签" in res:
            user_info = self.user_info(cookie)
            msg = f"签到成功，本次签到获得金币 {user_info['award']}，连续签到 {user_info['day_num']} 天，签到等级 {user_info['sign_level']}级，签到总天数 {user_info['total_sign']}"
        else:
            msg = "签到失败\n" + res
        return msg

    def user_info(self, cookie):
        """
        获取用户信息

        """
        url = "https://www.ruike1.com/k_misign-sign.html"
        self.s.headers.update({
            "cookie": cookie
        })
        text = self.s.get(url).text
        html = etree.HTML(text)
        return {
            "day_num": html.xpath('//*[@id="lxdays"]/@value')[0],  # 连续签到总天数
            "sign_level": html.xpath('//*[@id="lxlevel"]/@value')[0],  # 签到等级
            "award": html.xpath('//*[@id="lxreward"]/@value')[0],  # 积分奖励
            "total_sign": html.xpath('//*[@id="lxtdays"]/@value')[0]  # 签到总天数
        }

    def main(self):
        msg_all = ""
        for check_item in self.check_items:
            try:
                sign_msg = self.sign(check_item["cookie"])
                msg = f"签到信息: {sign_msg}"
                msg_all += msg + "\n\n"
            except Exception as e:
                msg = f"获取用户信息失败: {e}，Cookie不包含 open_mmid"
                print(msg)
                msg_all += msg + "\n\n"
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("RUIKE", [])
    res = RUIKE(check_items=_check_items).main()
    send("瑞客论坛", res)
